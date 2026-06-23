---
title: "crt.sh en OSINT: Certificate Transparency para descubrir nombres sin confundirlos con activos"
slug: /crtsh-certificate-transparency-osint-contexto
authors: [osint-writter]
tags: [osint, investigation, verification, tls, infrastructure, methodology]
date: 2026-06-23
image: /img/blog/2026-06-23-crtsh-certificate-transparency-osint-contexto.png
---

![Ilustración editorial de un analista OSINT revisando certificados TLS, una cronología y relaciones entre dominios con criterio defensivo](/img/blog/2026-06-23-crtsh-certificate-transparency-osint-contexto.png)

Una empresa asegura que ya ha retirado un entorno antiguo, pero en su inventario aparece un nombre que nadie reconoce: `proveedores.empresa-ejemplo.test`. No figura en la web pública, no está en la documentación reciente y buscarlo a ciegas solo añade ruido. En un caso así, `crt.sh` puede abrir una pista útil al consultar registros públicos de **Certificate Transparency** (`CT`): qué nombres aparecieron en certificados o precertificados, cuándo se observaron y qué autoridad certificadora intervino.

La clave está en no pedirle más de lo que sabe. Un registro `CT` demuestra que un nombre quedó incluido en material de certificado; **no demuestra por sí solo que el host siga activo, que resuelva hoy, que pertenezca todavía a la misma organización ni que esté expuesto de forma insegura**. Este artículo propone un flujo para inventario defensivo, `due diligence` técnica y verificación responsable, no para intrusión, acoso ni ampliación abusiva de objetivos.

<!-- truncate -->

## Qué es Certificate Transparency y dónde encaja crt.sh

Certificate Transparency es un sistema de registros públicos y auditables para certificados TLS. El [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html), publicado en diciembre de 2021, describe `CT v2` como un protocolo para registrar públicamente certificados de servidor TLS conforme se emiten u observan. Su objetivo es que la actividad de las autoridades certificadoras pueda auditarse y que resulte posible detectar emisiones sospechosas.

Los logs funcionan como árboles de Merkle **append-only**: se pueden añadir entradas, pero su diseño permite comprobar criptográficamente que el historial no se ha reescrito en silencio. Una autoridad certificadora, el titular o un tercero puede presentar un certificado; el log devuelve un `Signed Certificate Timestamp` (`SCT`) como compromiso de incorporarlo dentro de su plazo máximo de integración.

En ese ecosistema hay tres piezas distintas:

- los **logs** reciben certificados y precertificados y mantienen el historial auditable;
- los **monitores** revisan esos logs en busca de emisiones relevantes o sospechosas;
- herramientas de búsqueda como **crt.sh** hacen que ese corpus sea consultable para un analista.

`crt.sh` no es “el log” ni una prueba de disponibilidad. Es una interfaz de búsqueda sobre datos de certificados. Su organización pública mantiene, entre otros componentes, un monitor de logs, el esquema de la base de datos y utilidades de procesamiento de certificados.

## Caso de uso legítimo: reconciliar el inventario de una empresa ficticia

Imagina que el equipo de seguridad de `Northbridge Foods`, una compañía ficticia, prepara una auditoría de su superficie externa. El inventario aprobado contiene `www`, `clientes` y `correo`, pero una consulta por el dominio corporativo devuelve también estos nombres históricos:

| Nombre observado | Primera pregunta | Evidencia adicional necesaria |
| --- | --- | --- |
| `clientes.northbridge.example` | ¿Es un portal vigente? | DNS actual, inventario y responsable interno |
| `vpn-antigua.northbridge.example` | ¿Se retiró realmente? | DNS histórico, ticket de baja y comprobación autorizada |
| `*.laboratorio.northbridge.example` | ¿Qué cubría el comodín? | Emisión del certificado y alcance documentado; no enumera cada host |

El objetivo no es “encontrar algo vulnerable”. Es comparar tres listas: **lo documentado, lo observado históricamente y lo que sigue validado hoy**. Esa diferencia puede revelar deuda de inventario, nombres olvidados, proveedores que ya no deberían emitir certificados o simplemente residuos históricos sin relevancia operativa.

## Flujo recomendado paso a paso

### 1. Define alcance y pregunta

Empieza por un dominio que la organización controla o que está expresamente dentro de una revisión autorizada. Anota antes de buscar:

- quién ha solicitado la comprobación;
- qué dominio o unidad de negocio entra en alcance;
- qué periodo interesa;
- y qué decisión dependerá del resultado.

Una pregunta útil sería: “¿Qué nombres incluidos en certificados durante los últimos doce meses no aparecen en el inventario aprobado?”. “Descubrir todo lo posible” no es una pregunta: es una receta para acumular datos sin criterio.

### 2. Consulta crt.sh y conserva la búsqueda

En la interfaz web, busca el dominio y revisa los nombres incluidos en el `Common Name` y en los `Subject Alternative Names` (`SAN`). Para una revisión reproducible, conserva:

- la consulta exacta;
- la fecha y zona horaria;
- el identificador de la entrada o certificado;
- el emisor;
- las fechas `Not Before` y `Not After`;
- y los nombres observados.

Si usas una salida estructurada para un volumen moderado, documenta igualmente el origen y limita la automatización. Un ejemplo con un dominio reservado para documentación sería:

```bash
curl --fail --silent --show-error \
  'https://crt.sh/?q=%25.example.com&output=json' \
  -o crtsh-example-com.json
```

El comodín codificado `%25` amplía la búsqueda a nombres que terminan en el dominio. Eso puede generar duplicados: un mismo certificado puede aparecer en más de una entrada y `name_value` puede contener varios nombres separados por saltos de línea. Deduplicar ayuda a ordenar; **no convierte los resultados en activos confirmados**.

### 3. Normaliza sin borrar el tiempo

Crea una tabla de trabajo con, al menos:

```text
nombre_observado | primera_observacion | not_before | not_after | emisor | id_fuente | estado_validacion
```

Normaliza mayúsculas, elimina el prefijo `*.` solo en una columna derivada y conserva siempre el valor original. Un comodín como `*.laboratorio.example` no enumera automáticamente todos los subdominios posibles: solo indica el alcance nominal que cubre ese certificado.

Tampoco mezcles “fecha del certificado” y “momento en que tu equipo lo consultó”. La primera ayuda a reconstruir una cronología; la segunda asegura trazabilidad de tu informe.

### 4. Valida cada nombre con otra capa

Antes de elevar una pista a hallazgo, contrástala con fuentes que respondan preguntas diferentes:

1. **DNS actual:** ¿el nombre resuelve ahora? Guarda tipo de registro, respuesta y hora.
2. **DNS histórico o archivo web:** ¿resolvía o mostraba contenido durante el periodo relevante?
3. **Inventario autorizado:** ¿hay propietario, proveedor, servicio y fecha de retirada?
4. **Certificado servido actualmente:** ¿coincide con el registro histórico o se ha sustituido?
5. **Contexto documental:** ¿un ticket, contrato o cambio de infraestructura explica la relación?

Que un nombre no resuelva hoy no invalida el registro histórico. Que resuelva tampoco prueba control organizativo: puede apuntar a alojamiento compartido, un servicio gestionado o infraestructura reutilizada.

### 5. Clasifica la certeza, no solo el resultado

Una escala sencilla evita conclusiones infladas:

- **Observado:** el nombre figura en un certificado o precertificado registrado.
- **Corroborado:** otra fuente independiente sitúa el nombre en una fecha o contexto compatible.
- **Activo validado:** el equipo confirma que forma parte del inventario vigente.
- **Pendiente:** hay una pista, pero falta información suficiente.
- **Descartado con motivo:** duplicado, comodín mal interpretado, nombre de tercero o residuo explicado.

El informe debe poder mostrar cómo pasó cada fila de una categoría a otra.

## Qué puede salir mal: limitaciones y falsos positivos

### Un certificado no equivale a un servidor vivo

Los certificados pueden caducar, renovarse, reemplazarse o emitirse antes de que un servicio llegue a producción. Los precertificados también forman parte del sistema. Por eso, una coincidencia es evidencia sobre **emisión u observación**, no una sonda de disponibilidad.

### Los nombres pueden revelar más contexto del previsto

El propio RFC dedica una consideración de seguridad a la posible filtración de información DNS. Nombres internos trasladados por error a certificados públicamente confiables, etiquetas de proyecto o referencias a proveedores pueden quedar visibles. Esa visibilidad justifica revisar las prácticas de nomenclatura y emisión; no autoriza a explotar el hallazgo.

### Los comodines crean una falsa sensación de cobertura

`*.example.com` indica que un certificado puede cubrir determinados nombres bajo ese nivel, pero no lista cuáles existen. Tratar el comodín como un inventario de hosts produce conclusiones ficticias.

### La cronología tiene varios relojes

Conviene separar al menos:

- timestamp de entrada o precertificado;
- `Not Before` y `Not After`;
- momento de primera observación por tu equipo;
- y fecha de cualquier comprobación DNS o web.

Ordenar mal esos relojes puede convertir una migración normal en una supuesta anomalía.

### crt.sh y cualquier agregador tienen límites operativos

Una interfaz de búsqueda puede responder lentamente, aplicar límites o devolver resultados repetidos. Para monitorización continua de activos propios, no dependas de una única consulta ocasional: combina alertas de emisión, inventario y revisión periódica.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con activos propios, encargos documentados o preguntas de interés público legítimo y proporcional.
- Evita incluir nombres personales, correos o etiquetas sensibles en capturas compartidas si no son necesarios.
- No abras hosts desconocidos desde el navegador de trabajo; valida primero DNS, alcance y procedimiento interno.
- Limita frecuencia y volumen de consultas. Conserva resultados suficientes para reproducir el análisis, no un volcado indiscriminado.
- Separa datos brutos, notas analíticas y conclusiones. Una cadena de custodia ligera —URL, timestamp, hash del fichero y capturas— mejora la auditabilidad.
- Informa de un certificado inesperado al propietario o al equipo de seguridad por un canal responsable; no lo presentes públicamente como brecha sin corroboración.

## Checklist para una revisión defendible

- [ ] El dominio está autorizado y la pregunta está escrita.
- [ ] La consulta, la fecha y el identificador de cada entrada se han conservado.
- [ ] Los nombres originales y normalizados están en columnas distintas.
- [ ] Los comodines no se han tratado como hosts enumerados.
- [ ] Cada nombre relevante tiene al menos una validación independiente.
- [ ] “Observado”, “corroborado” y “activo” no se usan como sinónimos.
- [ ] Las fechas del certificado, del log y de la comprobación están separadas.
- [ ] Los datos personales o etiquetas sensibles se han minimizado en el informe.
- [ ] Las conclusiones incluyen límites y una acción concreta para el propietario.

## Alternativas y siguientes pasos

`crt.sh` es una entrada cómoda, pero no cubre todas las preguntas:

- los monitores de `Certificate Transparency` encajan mejor cuando necesitas alertas continuas sobre dominios propios;
- `Censys` permite relacionar certificados con servicios observados, con sus propios tiempos y límites de cobertura;
- `RDAP/WHOIS` aporta contexto registral, no prueba de operación;
- DNS histórico ayuda a reconstruir resoluciones pasadas;
- `urlscan.io` y el archivo web aportan comportamiento o contenido observado, siempre con cuidado de no enviar URLs sensibles a servicios públicos.

El takeaway práctico es este: usa `crt.sh` para **generar una lista de nombres y momentos que merecen validación**, no para declarar activos, propietarios o incidentes. La calidad del análisis aparece cuando el registro del certificado se cruza con DNS, inventario y contexto temporal, y cuando cada conclusión conserva el grado de certeza que realmente soportan las fuentes.

Como siguiente tema, tendría sentido comparar monitorización continua de `CT` con revisiones puntuales de DNS histórico: qué detecta antes cada capa, qué omite y cómo evitar alertas sin contexto.

## Fuentes consultadas

- [Certificate Transparency: How CT Works](https://certificate.transparency.dev/howctworks/)
- [Certificate Transparency: Logs](https://certificate.transparency.dev/logs)
- [Certificate Transparency: Monitors](https://certificate.transparency.dev/monitors)
- [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162.html)
- [Organización oficial de crt.sh en GitHub](https://github.com/crtsh)
- [Chrome Certificate Transparency Policy](https://googlechrome.github.io/CertificateTransparency/ct_policy.html)
