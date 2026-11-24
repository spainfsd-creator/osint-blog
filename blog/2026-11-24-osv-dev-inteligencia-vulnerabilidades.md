---
title: "OSV.dev en OSINT: investigar vulnerabilidades sin confundir coincidencia con impacto"
slug: /osv-dev-osint-inteligencia-vulnerabilidades
authors: [osint-writter]
tags: [osint, tooling, vulnerability-management, verification, data, privacy]
date: 2026-11-24
image: /img/blog/2026-11-24-osv-dev-inteligencia-vulnerabilidades.png
aiDisclosure: generated
humanReviewed: false
---

Un proveedor asegura que su aplicación no está afectada por una vulnerabilidad crítica. El inventario menciona una biblioteca con el mismo nombre que aparece en un aviso y el escáner enciende una alerta roja. Parece una contradicción concluyente, hasta que descubrimos que nadie ha fijado el ecosistema, la versión instalada, el artefacto desplegado ni la ruta de ejecución. **En inteligencia de vulnerabilidades, una coincidencia abre una investigación; no demuestra por sí sola impacto, exposición ni explotación.**

![Analista contrastando un inventario de dependencias con registros estructurados de vulnerabilidades](/img/blog/2026-11-24-osv-dev-inteligencia-vulnerabilidades.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/osv-dev-osint-inteligencia-vulnerabilidades.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [OSV.dev](https://osv.dev/) para verificar afirmaciones sobre dependencias de código abierto. El producto, el proveedor, los paquetes y los datos del caso son ficticios. El objetivo es trabajar con inventarios propios, software autorizado y fuentes públicas; no buscar sistemas vulnerables de terceros ni convertir datos defensivos en una guía de explotación.

## Qué es OSV.dev y para qué sirve en OSINT

OSV.dev es un servicio abierto que agrega registros de vulnerabilidades expresados en el formato OSV de OpenSSF. A diferencia de una búsqueda puramente textual por CVE, su modelo intenta describir el **paquete**, el **ecosistema** y los **intervalos de versiones o commits afectados**. Su API permite consultar un paquete y una versión, un commit o un identificador de aviso, y también agrupar consultas por lotes.

Para una investigación legítima resulta útil cuando necesitamos:

- comprobar si una dependencia concreta coincide con avisos conocidos;
- distinguir el nombre de un paquete de su identidad dentro de un ecosistema;
- seguir alias entre identificadores sin contarlos como hallazgos independientes;
- localizar versiones corregidas y referencias al aviso original;
- conservar datos estructurados y fechados para repetir la consulta;
- comparar una declaración del proveedor con un SBOM, un lockfile o un artefacto autorizado;
- separar vulnerabilidad conocida, presencia del componente, alcanzabilidad e impacto real.

OSV.dev no observa nuestro despliegue. Tampoco certifica que el inventario sea completo, que una función vulnerable se ejecute, que exista una vía de ataque o que haya explotación activa. Solo puede devolver lo que sus fuentes conocen y lo que nuestra consulta identifica correctamente.

### Seis objetos que no conviene mezclar

| Objeto | Pregunta | Evidencia adecuada | Error frecuente |
| --- | --- | --- | --- |
| aviso | ¿qué vulnerabilidad se describe? | registro OSV y fuente del aviso | tratar alias como fallos distintos |
| paquete | ¿qué componente es? | ecosistema, nombre canónico y PURL | unir paquetes homónimos |
| versión | ¿qué revisión está presente? | lockfile, SBOM y artefacto | usar la versión declarada sin verificar |
| afectación | ¿cae en el rango publicado? | eventos `introduced`, `fixed` o versiones afectadas | leer solo la puntuación |
| alcanzabilidad | ¿el producto puede ejecutar el código vulnerable? | análisis técnico y configuración | inferirla por mera presencia |
| exposición | ¿puede activarse en el entorno real? | arquitectura, controles y pruebas autorizadas | confundir posibilidad teórica con riesgo actual |

La conclusión debe conservar esas capas. «OSV devuelve un aviso para la versión declarada» es una observación reproducible. «El servicio es explotable desde Internet» es otra afirmación, mucho más exigente, que necesita pruebas diferentes.

## Caso de uso legítimo: revisar una declaración de seguridad

La cooperativa ficticia **Archivo del Río** contrata una plataforma para publicar documentos municipales. Tras conocer un aviso de seguridad en una biblioteca de plantillas, pide al proveedor una evaluación. La respuesta dice: «No nos afecta porque actualizamos el trimestre pasado».

El equipo recibe, con autorización, tres artefactos:

1. un SBOM generado durante la compilación;
2. el lockfile del mismo release;
3. el digest de la imagen desplegada.

La investigación no empieza buscando servidores en Internet. Empieza formulando una afirmación comprobable:

> El artefacto con digest `sha256:ejemplo-ficticio` desplegado el 20 de noviembre no contiene una versión afectada conocida del paquete `plantillas-rio` según los registros consultados el 24 de noviembre.

El nombre y el digest son ficticios y no deben usarse como indicadores reales. La frase fija objeto, fecha y alcance. Si el proveedor entrega el SBOM de otra compilación o un inventario sin vínculo con el digest, todavía no podemos evaluar la declaración.

## Flujo recomendado, paso a paso

### 1. Fija el objeto antes de consultar

Registra producto, release, digest, plataforma, origen del inventario y momento de observación. Conserva el archivo original y calcula su huella. Un SBOM correcto pero perteneciente a otro artefacto puede producir una respuesta técnicamente impecable y metodológicamente inútil.

Mantén también una tabla de procedencia:

| Campo | Ejemplo ficticio |
| --- | --- |
| artefacto | `registry.example/archivo-rio@sha256:...` |
| inventario | `sbom-release-47.cdx.json` |
| generado por | pipeline de compilación autorizado |
| observado | `2026-11-24T09:30:00+01:00` |
| consulta | paquete, ecosistema y versión exactos |
| fuente OSV | URL del registro y JSON conservado |
| estado | coincide / no coincide / sin resolver |

### 2. Normaliza sin borrar el original

El nombre aislado no basta. Un paquete debe ir acompañado por su ecosistema y, cuando sea posible, por un Package URL. La documentación de la consulta de OSV advierte de que los nombres se comparan exactamente salvo las reglas de normalización propias de algunos ecosistemas.

Conserva dos columnas: `identificador_observado` e `identificador_normalizado`. Si el SBOM dice `Plantillas_Rio` y una regla lo transforma, la decisión debe poder auditarse. No fuerces una equivalencia cuando falte el namespace, el ecosistema o la versión: usa `sin_resolver`.

### 3. Consulta de forma reproducible

La API acepta una petición `POST` con paquete, ecosistema y versión. Este ejemplo usa datos deliberadamente ficticios:

```bash
curl -sS https://api.osv.dev/v1/query \
  -H 'Content-Type: application/json' \
  -d '{
    "package": {
      "name": "plantillas-rio",
      "ecosystem": "PyPI"
    },
    "version": "4.7.2"
  }' > consulta-osv.json
```

Guarda la petición, la respuesta completa, la fecha y una huella del JSON. Para una lista grande, usa el endpoint por lotes o una copia fechada de los volcados oficiales; no conviertas cientos de llamadas sueltas en un conjunto imposible de reconstruir.

Una respuesta vacía significa **«no se devolvieron coincidencias para esta consulta en este momento»**. No significa «el paquete es seguro». La identidad puede ser incorrecta, la versión puede faltar, la fuente puede no cubrir ese ecosistema o la vulnerabilidad puede no ser pública todavía.

### 4. Lee el registro, no solo el color

En cada resultado revisa al menos:

- `id`, `published`, `modified` y, si existe, `withdrawn`;
- paquete y ecosistema dentro de `affected`;
- rangos y eventos `introduced`, `fixed`, `last_affected` o `limit`;
- versiones enumeradas cuando las haya;
- `aliases`, `upstream` y `related`, que expresan relaciones distintas;
- referencias al aviso, al cambio corrector y al repositorio;
- procedencia de la severidad cuando esté indicada;
- campos específicos de la base o del ecosistema.

El esquema OSV reserva `aliases` para identificadores de la misma vulnerabilidad. `upstream` representa una relación direccional con un aviso ascendente y `related` agrupa registros cercanos que no cumplen la equivalencia estricta. Por tanto, cinco identificadores enlazados no son necesariamente cinco vulnerabilidades independientes.

Comprueba también `withdrawn`. Un registro retirado no debe alimentar una conclusión actual como si siguiera vigente, aunque puede ser relevante para explicar una alerta histórica.

### 5. Vuelve al artefacto y a la fuente primaria

Contrasta el resultado con el aviso del proyecto, el repositorio, la corrección y la documentación del proveedor. Verifica que la versión del inventario corresponde al artefacto desplegado. Si existe vendorización, backport o parche local, la cadena de versiones puede no expresar toda la realidad.

Formula preguntas discriminantes:

- ¿el componente está realmente incluido o era solo una dependencia de desarrollo?
- ¿la versión empaquetada conserva un parche retroportado?
- ¿la funcionalidad vulnerable está compilada y habilitada?
- ¿la entrada controlada por un atacante puede alcanzar esa función?
- ¿los controles del entorno cambian la exposición?
- ¿la declaración del proveedor se refiere al mismo digest y fecha?

OSV-Scanner puede extraer paquetes de distintos objetivos y cotejarlos con bases conocidas, pero su propio modelo separa extracción y matching. Esa separación es una buena disciplina investigadora: primero demuestra qué componente observaste; después evalúa qué avisos coinciden.

### 6. Clasifica la conclusión y programa revisión

Evita un único campo `vulnerable: sí/no`. Una clasificación más honesta podría ser:

- `coincidencia_confirmada`: identidad y versión caen en el rango;
- `presente_no_alcanzable`: el componente aparece, pero un análisis autorizado sustenta que la ruta no se ejecuta;
- `mitigado`: el impacto está contenido por una medida documentada y con caducidad;
- `no_afectado_corregido`: el artefacto enlazado contiene una versión o parche verificado;
- `sin_resolver`: faltan identidad, versión, procedencia o evidencia suficiente;
- `registro_retirado`: la fuente retiró el aviso;
- `no_hay_coincidencias_conocidas`: resultado negativo limitado a la consulta y fecha.

Registra quién decidió, qué evidencia utilizó y cuándo debe revisarse. Los registros cambian: `modified` existe precisamente porque el conocimiento sobre una vulnerabilidad evoluciona.

## Limitaciones y falsos positivos

### Un inventario puede mentir sin querer

Los SBOM y lockfiles son observaciones de una fase concreta. Pueden omitir componentes añadidos después, incluir dependencias que nunca llegan al artefacto o describir otro release. Vincula inventario y binario mediante el pipeline, el digest y controles independientes.

### Los rangos dependen del ecosistema

No compares versiones como cadenas genéricas. Cada ecosistema puede tener reglas propias y un mismo nombre puede significar paquetes diferentes. Los commits de un fork tampoco equivalen automáticamente a los del repositorio original.

### La ausencia no es una garantía

OSV.dev agrega vulnerabilidades conocidas procedentes de múltiples fuentes. Ninguna base contiene fallos desconocidos, avisos aún no publicados ni todos los problemas de configuración. Documenta cobertura y fecha antes de escribir «no afectado».

### La severidad no sustituye al contexto

Una puntuación resume propiedades bajo supuestos concretos; no demuestra alcance funcional, valor del activo ni exposición. Tampoco una severidad baja autoriza a ignorar un componente crítico para el caso. Conserva el vector y su fuente, no solo el número.

### La automatización multiplica errores de identidad

Si una normalización incorrecta asigna el mismo paquete a mil artefactos, mil alertas no son mil corroboraciones. Son la repetición de una decisión defectuosa. Revisa una muestra, conserva controles negativos y mide falsos positivos y falsos negativos.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con repositorios, inventarios y artefactos propios o expresamente autorizados.
- No publiques rutas internas, nombres de clientes, tokens, registros privados ni versiones explotables innecesarias.
- Usa ejemplos sintéticos al enseñar el método.
- Trata lockfiles y SBOM como datos potencialmente sensibles: revelan arquitectura, proveedores y deuda técnica.
- No conviertas el análisis en búsqueda activa de objetivos vulnerables.
- Separa el informe técnico del material de explotación; para validar impacto, utiliza un entorno controlado y autorización escrita.
- Protege las respuestas, exportaciones y excepciones con acceso mínimo y retención definida.
- Comunica primero al responsable del sistema y evita amplificar una exposición antes de su corrección.
- Expresa incertidumbre y corrige públicamente el informe si cambia el aviso o el inventario.

## Checklist antes de publicar una conclusión

- [ ] La pregunta identifica producto, release, digest, entorno y fecha.
- [ ] El inventario está vinculado al artefacto observado.
- [ ] Paquete, ecosistema y versión se conservaron antes y después de normalizar.
- [ ] La petición y la respuesta de OSV son reproducibles.
- [ ] Se revisaron rangos, correcciones, retirada y fecha de modificación.
- [ ] Alias, relaciones ascendentes y avisos relacionados no se contaron dos veces.
- [ ] La coincidencia se contrastó con el aviso y el repositorio originales.
- [ ] Presencia, alcanzabilidad, exposición e impacto permanecen separados.
- [ ] Los resultados negativos describen cobertura y fecha, no seguridad absoluta.
- [ ] Las excepciones tienen evidencia, responsable y caducidad.
- [ ] Los datos internos y personales se han minimizado.
- [ ] La conclusión permite `sin resolver` cuando la evidencia no basta.

## Alternativas y siguientes pasos

GitHub Advisory Database, las bases de avisos de cada lenguaje y los boletines del proveedor pueden aportar la fuente original; NVD y los registros CVE ayudan a seguir identificadores y descripciones; `pip-audit`, `govulncheck`, Trivy y otras herramientas aplican modelos distintos a ecosistemas o artefactos concretos; VEX permite expresar, con justificación y alcance, si una vulnerabilidad conocida afecta a un producto. Ninguna alternativa elimina la necesidad de identificar el artefacto y verificar la cadena de procedencia.

OSV.dev es especialmente valioso como **índice estructurado y reproducible** entre inventario y avisos. Su fortaleza no está en pronunciar un veredicto final, sino en reducir la ambigüedad de paquetes y versiones para que el análisis posterior empiece en el lugar correcto.

El takeaway práctico es este: **guarda la consulta como evidencia, trata la coincidencia como hipótesis y no cierres el caso hasta enlazar aviso, paquete, versión y artefacto real**. Como ejercicio, crea un SBOM sintético con una dependencia afectada, otra corregida y un homónimo de otro ecosistema; comprueba si tu proceso distingue los tres casos sin recurrir a una etiqueta binaria. El siguiente paso natural sería diseñar un protocolo para reconciliar cambios entre dos capturas fechadas de OSV sin reabrir automáticamente todas las decisiones históricas.

## Fuentes y documentación

- [OSV.dev: introducción y modelo de agregación](https://google.github.io/osv.dev/)
- [OSV.dev: referencia oficial de la API](https://google.github.io/osv.dev/api/)
- [OSV.dev: consulta de paquete y versión](https://google.github.io/osv.dev/post-v1-query/)
- [OSV.dev: fuentes y volcados de datos](https://google.github.io/osv.dev/data/)
- [OpenSSF: esquema oficial OSV](https://ossf.github.io/osv-schema/)
- [OSV.dev: propiedades de un registro de calidad](https://google.github.io/osv.dev/data_quality.html)
- [OSV-Scanner: uso y separación entre extracción y matching](https://google.github.io/osv-scanner/usage/)
