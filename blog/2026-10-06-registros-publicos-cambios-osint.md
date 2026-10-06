---
title: "Registros públicos de cambios en OSINT: versiones, avisos y trazabilidad sin exponer de más"
slug: /registros-publicos-cambios-osint
authors: [osint-writter]
tags: [osint, methodology, verification, tradecraft, automation, privacy]
date: 2026-10-06
image: /img/blog/2026-10-06-registros-publicos-cambios-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando un registro cronológico de versiones y correcciones OSINT](/img/blog/2026-10-06-registros-publicos-cambios-osint.png)

*Imagen generada mediante inteligencia artificial.*

Una organización corrige un informe, sustituye el CSV y regenera dos gráficos. La página ya muestra la versión buena, pero una periodista conserva el fichero anterior, un socio recibió el PDF por correo y el buscador aún enseña una descripción desactualizada. El equipo sabe qué cambió porque puede leer Git; la audiencia, no. **Sin un registro público de cambios, la versión vigente existe, pero descubrirla depende de llegar por el camino correcto.**

Un registro de cambios para OSINT conecta cada modificación relevante con el artefacto afectado, su alcance y la acción que debe tomar quien lo reutilizó. No necesita revelar el dato equivocado ni publicar deliberaciones internas. Necesita ofrecer una señal estable, proporcionada y verificable que también pueda consumir una máquina.

<!-- truncate -->

Este artículo propone un formato mínimo y un flujo responsable. Todas las entidades, URLs, fechas operativas, identificadores y hashes del caso práctico son ficticios. Un hash permite comprobar bytes; un historial permite reconstruir cambios; **ninguno demuestra que una conclusión sea verdadera**.

## Qué es un registro público de cambios

Es una secuencia ordenada de eventos que describe cambios con impacto externo sobre una investigación o sus derivados. Puede publicarse como HTML para personas y como JSON o feed para automatización. Su unidad no es el `commit`, sino un **evento editorial comprensible**.

Conviene separar tres capas:

1. **La obra estable:** la investigación, identificada por una URL o ID que no cambia.
2. **Las versiones:** estados concretos del informe, dataset, gráfico o anexo.
3. **Los eventos:** publicación, corrección, sustitución, retirada o restauración que relacionan esos estados.

[PROV-O](https://www.w3.org/TR/prov-o/) permite expresar que una entidad fue derivada de otra o es su revisión. [DataCite](https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/) define relaciones como `IsNewVersionOf` y `IsPreviousVersionOf`. No hace falta implantar ambos estándares para empezar, pero sus conceptos evitan confundir identidad, versión y procedencia.

### Lo que no es

- No es el historial de Git expuesto sin contexto.
- No es una lista de fechas de modificación sin explicación.
- No es una copia pública del ticket interno.
- No es una garantía criptográfica de veracidad.
- No es una excusa para conservar datos personales que ya deben retirarse.
- No sustituye una [nota de corrección visible](/comunicacion-publica-correcciones-osint) cuando el error afecta a la audiencia.

El registro funciona como índice. La nota explica una rectificación importante; el evento permite encontrarla, relacionarla con versiones y automatizar avisos.

## Caso ficticio: el informe de Puerto Claro

El observatorio ficticio **Puerto Claro** publica un informe sobre ayudas municipales con tres salidas:

- una página HTML;
- un CSV descargable;
- un gráfico PNG incluido en un boletín.

El 6 de octubre detecta que una fila corresponde al ejercicio anterior. La cifra agregada cambia un 1,8 %, pero la conclusión principal se mantiene. El equipo genera la versión `2026.10.06-2` y necesita que una persona que solo conserve el CSV antiguo pueda saber:

- que existe una revisión;
- qué artefactos quedaron sustituidos;
- si las conclusiones cambiaron;
- dónde obtener la versión vigente;
- y cómo verificar que descargó el fichero previsto.

No necesita publicar el nombre contenido en la fila, el mensaje de quien avisó ni un `diff` que vuelva a exponer información inexacta.

## El esquema mínimo

Un evento útil puede caber en pocos campos, siempre que sus significados estén documentados.

| Campo | Pregunta que responde | Regla práctica |
|---|---|---|
| `event_id` | ¿Qué evento es? | ID estable y único; no reutilizarlo |
| `published_at` | ¿Cuándo se anunció? | Fecha y hora con zona; preferiblemente UTC |
| `type` | ¿Qué ocurrió? | Vocabulario corto y documentado |
| `work_id` | ¿Qué investigación identifica? | URL o ID canónico estable |
| `from_version` / `to_version` | ¿Qué estados conecta? | No sobrescribir una versión ya publicada |
| `summary` | ¿Qué cambió? | Lenguaje claro, sin reproducir daño |
| `impact` | ¿Qué conclusiones afecta? | Distinguir datos, visuales y conclusiones |
| `artifacts` | ¿Qué salidas cambian? | Enlaces, estado y tipo de cada artefacto |
| `supersedes` | ¿Qué deja de ser vigente? | Referencia explícita a la versión anterior |
| `action` | ¿Qué debe hacer quien la usó? | Descargar, volver a calcular, dejar de citar, etc. |
| `notice_url` | ¿Dónde está la explicación humana? | Obligatoria para cambios materiales |
| `integrity` | ¿Cómo compruebo los bytes? | Algoritmo, digest y artefacto exacto |

La [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) ofrece un formato interoperable para fechas y horas de Internet. Un valor como `2026-10-06T10:42:00Z` evita que «10:42» dependa de una zona implícita. La hora de publicación del aviso no debe reemplazar la hora de adquisición de la fuente ni la de generación del artefacto: son hechos diferentes.

### Tipos de evento

Empieza con un vocabulario pequeño:

- `published`: primera publicación pública;
- `corrected`: se corrige un error factual o de transformación;
- `updated`: se añade o refresca contenido sin corregir un error;
- `superseded`: otra versión pasa a ser la vigente;
- `withdrawn`: el artefacto deja de recomendarse o de estar disponible;
- `restored`: vuelve a estar disponible tras una revisión.

Evita nombres ambiguos como `changed`. [ActivityStreams 2.0](https://www.w3.org/TR/activitystreams-vocabulary/) distingue actividades como `Create`, `Update` y `Delete`, pero advierte de que `Update` no describe por sí solo el conjunto real de modificaciones. La lección práctica es clara: un tipo normalizado ayuda a filtrar; el resumen y el impacto siguen siendo imprescindibles.

## Ejemplo legible por máquinas

El caso ficticio podría publicar un evento como este:

```json
{
  "schema_version": "1.0",
  "event_id": "chg_01J9B7M4Y8P2",
  "published_at": "2026-10-06T10:42:00Z",
  "type": "corrected",
  "work_id": "https://ejemplo.invalid/informes/ayudas-puerto-claro",
  "from_version": "2026.10.06-1",
  "to_version": "2026.10.06-2",
  "summary": "Se excluyó una fila fuera del periodo declarado y se regeneraron los agregados.",
  "impact": {
    "data": "La suma publicada disminuye un 1,8 %.",
    "conclusions": "La conclusión principal no cambia."
  },
  "artifacts": [
    {
      "url": "https://ejemplo.invalid/descargas/ayudas-2026.10.06-2.csv",
      "media_type": "text/csv",
      "status": "current",
      "integrity": {
        "algorithm": "sha-256",
        "value": "DIGEST_FICTICIO_NO_UTILIZABLE"
      }
    }
  ],
  "supersedes": "https://ejemplo.invalid/versiones/2026.10.06-1",
  "action": "Sustituir el CSV anterior y recalcular cualquier cifra derivada.",
  "notice_url": "https://ejemplo.invalid/correcciones/2026-10-06"
}
```

El digest está marcado como ficticio para impedir que parezca una comprobación real. Si sirves artefactos por HTTP, la [RFC 9530](https://www.rfc-editor.org/rfc/rfc9530.html) define `Content-Digest` para comunicar resúmenes calculados sobre el contenido del mensaje. También puedes publicar un manifiesto separado. En ambos casos registra el algoritmo y el objeto exacto: el mismo CSV comprimido y sin comprimir produce bytes distintos.

## Flujo recomendado

### 1. Inventariar las salidas antes de corregir

Enumera HTML, CSV, JSON, PDF, imágenes, API, boletines, repositorios y copias entregadas. Dibuja sus dependencias. Si no sabes qué se generó a partir del dato, consulta el linaje antes de declarar cerrado el cambio.

### 2. Clasificar significado e impacto

Decide si es mantenimiento, actualización, corrección o retirada. Registra por separado:

- qué artefacto cambió;
- qué dato o proceso motivó el cambio;
- qué conclusiones cambian;
- qué conclusiones permanecen;
- y qué debe hacer quien reutilizó la versión anterior.

No conviertas «el número cambió poco» en «el impacto es bajo». Una variación mínima puede alterar una identidad, una ubicación o una atribución sensible.

### 3. Crear una versión nueva e inmutable

Conserva un ID estable para la investigación y otro para cada estado. La nueva versión debe apuntar a la anterior; la anterior debe indicar que fue sustituida cuando sea seguro mantenerla accesible. La propiedad `wasRevisionOf` de PROV-O y las relaciones de versión de DataCite ofrecen modelos reutilizables.

Si la versión antigua contiene datos que no deben seguir públicos, publícala como **metadato de estado**, no como contenido recuperable: ID, fecha, motivo general de retirada y enlace a la versión vigente pueden bastar.

### 4. Escribir primero para personas

Redacta una frase que alguien pueda entender sin abrir el repositorio. Incluye alcance y acción. Después serializa esos mismos conceptos en JSON. Si el texto y los campos estructurados cuentan historias distintas, detén la publicación.

[Schema.org](https://schema.org/correction) permite asociar una corrección a una `CreativeWork`, mientras que las directrices de [IPTC sobre confianza y credibilidad](https://www.iptc.org/std/guidelines/trust-and-credibility/) contemplan enlaces entre la obra incorrecta y la que la corrige. Añadir metadatos semánticos puede facilitar el descubrimiento, pero no sustituye la nota visible en la página.

### 5. Fijar tiempo e integridad

Genera hashes después de producir los artefactos finales, no antes de comprimirlos o trasladarlos. Guarda la hora de generación y la de publicación como campos distintos. Verifica el fichero desde la URL pública y en una sesión limpia.

### 6. Publicar el evento de forma atómica

La secuencia ideal es:

1. subir la versión nueva;
2. comprobar enlaces, tamaño, formato y digest;
3. marcar la anterior como sustituida o retirada;
4. publicar la nota y el evento;
5. actualizar el índice o feed;
6. emitir avisos a suscriptores y destinatarios conocidos.

Si no puedes hacer el cambio de forma atómica, publica primero una advertencia temporal. Una ventana en la que el registro anuncia una versión que devuelve `404` también es un fallo observable.

### 7. Probar desde el punto de vista de quien reutiliza

Empieza con una copia de la versión anterior y solo el registro público. Comprueba si puedes localizar la vigente, saber qué reemplazar y entender si tu análisis queda afectado. Esta prueba detecta enlaces que funcionan para el equipo pero no para la audiencia.

## Automatización responsable

La automatización debe comprobar coherencia, no decidir la verdad. Un pipeline puede validar que:

- `event_id` no está repetido;
- `published_at` incluye zona horaria;
- `to_version` existe y es distinta de `from_version`;
- cada URL vigente responde y entrega el tipo esperado;
- cada digest coincide con el artefacto descargado;
- el evento enlaza una nota cuando el impacto es material;
- no hay dos versiones marcadas simultáneamente como vigentes;
- y el feed mantiene un orden determinista.

También puede generar Atom, RSS o notificaciones desde la fuente canónica. No debería redactar automáticamente el impacto, decidir que una atribución sigue siendo válida ni publicar un `diff` sin revisar su sensibilidad.

Usa fixtures sintéticos en las pruebas. Copiar una dirección, un correo o una acusación real a los logs de CI multiplica el problema que pretendías corregir.

## Limitaciones y falsos positivos

### Un cambio técnico no siempre es editorial

Una regeneración puede alterar orden de claves, compresión, miniaturas o metadatos sin cambiar el significado. No emitas una corrección factual por cada diferencia binaria. Define qué cambios son materiales y conserva el detalle técnico internamente.

### Un digest diferente no explica la diferencia

Solo demuestra que los bytes no coinciden. Puede deberse a una corrección, a una marca temporal incrustada o a otra codificación. Necesitas versión, resumen e impacto.

### Un digest coincidente no valida la fuente

Confirma que dos partes comparan el mismo objeto bajo el mismo algoritmo. No prueba que la adquisición fuera completa, que la entidad estuviera bien resuelta ni que la interpretación sea correcta.

### La ausencia de evento no prueba ausencia de cambio

El publicador puede tener cobertura incompleta, un fallo de despliegue o una política distinta. Monitoriza también la página y los artefactos, pero trata cualquier discrepancia como señal para revisar, no como prueba de ocultación.

### La cronología pública puede ser incompleta por diseño

Privacidad, seguridad o una orden legítima pueden impedir conservar una versión. La transparencia responsable permite explicar la retirada sin mantener disponible el contenido dañino.

## Buenas prácticas de OPSEC, ética y privacidad

- Publica el efecto del cambio; no reproduzcas el dato sensible equivocado.
- Usa roles o equipos en vez de nombres personales cuando la autoría individual no sea necesaria.
- Separa el registro público del ticket, el canal de chat y la evidencia restringida.
- No expongas rutas internas, tokens, consultas privadas ni identificadores de víctimas.
- Mantén IDs opacos; no codifiques correos, alias o acusaciones en ellos.
- Conserva versiones retiradas solo con base, acceso y plazo definidos.
- Evita `diffs` públicos cuando puedan reidentificar a una persona.
- Firma o sella el registro solo si puedes operar y custodiar las claves correctamente.
- Documenta la cobertura: qué tipos de cambio aparecen y desde qué fecha.
- Ofrece un canal seguro para comunicar otra inexactitud.
- No atribuyas intención a partir de una edición, una retirada o un silencio.
- Revisa cachés, feeds y derivados para no seguir distribuyendo el artefacto sustituido.

## Alternativas y siguientes pasos

Si necesitas preservar estados completos con inventarios, estudia [OCFL](/ocfl-osint-preservacion-versionada). Para empaquetar un conjunto con contexto semántico, revisa [RO-Crate](/ro-crate-osint-paquete-evidencia); para transferirlo y validar que llegó íntegro, [BagIt](/bagit-osint-transferencia-evidencia). Si el problema es descubrir qué salidas dependen de un dato, empieza por [OpenLineage](/openlineage-linaje-datos-osint).

Una tabla Markdown puede bastar para un proyecto pequeño. JSON Lines resulta práctico para eventos anexables; JSON-LD facilita reutilizar vocabularios de procedencia; ActivityStreams puede encajar si ya distribuyes actividades. Elige el formato que tu audiencia pueda consultar y exportar. La sofisticación que nadie encuentra es peor que una página estable y clara.

## Checklist de publicación

- [ ] La investigación tiene un ID canónico y cada versión, uno distinto.
- [ ] El evento explica tipo, fecha, alcance, impacto y acción.
- [ ] La versión nueva enlaza la anterior y viceversa cuando procede.
- [ ] La nota humana y el registro estructurado son coherentes.
- [ ] Todos los artefactos derivados están inventariados.
- [ ] Los hashes se calcularon sobre los ficheros finales y se verificaron de nuevo.
- [ ] La versión vigente puede descargarse sin sesión.
- [ ] La versión sustituida está marcada o retirada según el riesgo.
- [ ] El evento no filtra datos personales ni deliberaciones internas.
- [ ] Una prueba desde la versión antigua conduce a la vigente.
- [ ] Suscriptores y destinatarios conocidos reciben un aviso proporcional.
- [ ] El registro declara su cobertura y sus limitaciones.

El takeaway accionable es sencillo: elige el último informe que modificaste y trata de responder, desde fuera del equipo, **qué cambió, qué versión está vigente, qué derivados quedaron afectados y qué debe hacer quien conserva una copia anterior**. Si una de esas respuestas depende de leer Git o preguntar por privado, todavía no tienes un registro público de cambios.

Como próximo tema, merece la pena estudiar **feeds de correcciones y retiradas en OSINT**: cómo distribuir eventos con Atom o ActivityStreams, controlar reintentos y evitar que una notificación duplicada parezca una nueva corrección.

## Fuentes consultadas

- [W3C: PROV-O, The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [W3C: Activity Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
- [RFC 3339: Date and Time on the Internet](https://www.rfc-editor.org/rfc/rfc3339)
- [RFC 9530: Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)
- [DataCite Metadata Schema: relationType](https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/)
- [Schema.org: correction](https://schema.org/correction)
- [IPTC: Expressing Trust and Credibility Information](https://www.iptc.org/std/guidelines/trust-and-credibility/)
