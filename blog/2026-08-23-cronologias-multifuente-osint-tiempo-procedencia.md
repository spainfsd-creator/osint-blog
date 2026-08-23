---
title: "Cronologías multifuente en OSINT: ordenar el tiempo sin inventar causalidades"
slug: /cronologias-multifuente-osint-tiempo-procedencia
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, data, privacy]
date: 2026-08-23
image: /img/blog/2026-08-23-cronologias-multifuente-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT alineando archivos web, documentos públicos, metadatos y relojes con distintas zonas horarias](/img/blog/2026-08-23-cronologias-multifuente-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un aviso municipal, una noticia y una fotografía parecen contar la misma historia. Sus horas también parecen encajar: `09:18`, `09:30` y `09:36`. El problema es que una marca procede de EXIF sin zona horaria, otra anuncia cuándo debía empezar un cierre y la tercera indica cuándo un medio publicó su página. **Ordenar esos tres números como si midieran el mismo acontecimiento puede fabricar una causalidad que ninguna fuente demuestra.** Una cronología OSINT útil no es una lista de horas: es un modelo de qué reloj observamos, quién lo proporcionó y cuánta incertidumbre conserva.

<!-- truncate -->

Este artículo propone un flujo responsable para alinear documentos, archivos web, metadatos multimedia y publicaciones abiertas sin borrar sus diferencias. Las fuentes técnicas se consultaron el **23 de agosto de 2026**. Todos los nombres, lugares, URLs, horas, archivos y organizaciones del caso práctico son ficticios.

## Qué es una cronología multifuente y para qué sirve

Una cronología multifuente relaciona observaciones procedentes de sistemas distintos alrededor de una pregunta temporal. Puede ayudar en *due diligence*, verificación periodística, respuesta a incidentes, análisis de políticas públicas o reconstrucción de una incidencia técnica. Su valor no está en llenar una línea de tiempo, sino en distinguir al menos cinco relojes:

| Reloj | Qué representa | Error habitual |
| --- | --- | --- |
| tiempo del acontecimiento | cuándo se afirma que ocurrió algo en el mundo | tratar una declaración como observación independiente |
| tiempo de publicación | cuándo una plataforma dice que hizo visible un contenido | asumir que coincide con su creación o primera disponibilidad |
| tiempo de modificación | cuándo se actualizó una página, registro o fichero | sustituir silenciosamente la fecha original |
| tiempo de captura | cuándo el analista o un archivo obtuvo una copia | confundir observación posterior con publicación |
| tiempo de metadatos | valor guardado dentro de un fichero o por su sistema contenedor | asumir zona, reloj correcto o autenticidad |

El [RFC 3339](https://www.rfc-editor.org/info/rfc3339/) define un formato interoperable para representar instantes en Internet con año de cuatro cifras y un desplazamiento numérico respecto de UTC. Un valor como `2026-08-19T09:30:00+02:00` representa el mismo instante que `2026-08-19T07:30:00Z`. Eso permite comparar valores, pero no demuestra que el reloj del productor estuviera bien configurado ni que la etiqueta describa el hecho que nos interesa.

El [RFC 9557](https://www.rfc-editor.org/info/rfc9557/) amplía el formato para transportar información adicional, como el nombre de una zona horaria. La diferencia importa: un desplazamiento `+02:00` describe una relación con UTC en ese instante; una zona como `Europe/Madrid` contiene reglas históricas y futuras. En una investigación conviene conservar tanto el valor original como la normalización utilizada.

## Caso de uso legítimo: el cierre del puente de Villa Serena

El ayuntamiento ficticio de **Villa Serena** investiga si la comunicación pública sobre el cierre preventivo del puente `Alba` fue coherente. La pregunta no es quién pasó por allí ni qué hicieron personas concretas. Es más acotada: **¿qué podía conocerse públicamente y en qué orden observable?**

El analista recibe cuatro piezas:

1. un aviso municipal que dice «cierre desde las 09:30» y cuya página muestra publicación a las `09:12 +02:00`;
2. una fotografía del acceso cerrado con `DateTimeOriginal: 2026:08:19 09:18:04`, sin zona horaria;
3. una noticia marcada como publicada a las `09:36 +02:00` y actualizada a las `11:05 +02:00`;
4. una captura de la página municipal indexada por un archivo web a las `07:52Z`.

La tabla de trabajo separa observación de interpretación:

| ID | Fuente | Valor literal | Tipo de reloj | UTC normalizado | Incertidumbre | Lectura prudente |
| --- | --- | --- | --- | --- | --- | --- |
| `E01` | página municipal | `09:12 +02:00` | publicación declarada | `07:12Z` | plataforma y reloj no auditados | la página declara esa hora de publicación |
| `E02` | texto del aviso | `desde las 09:30` | tiempo afirmado del cierre | `07:30Z` si se confirma la zona | falta la zona en el texto aislado | el documento anuncia esa hora; no prueba ejecución exacta |
| `E03` | fotografía | `2026:08:19 09:18:04` | metadato del fichero | no normalizar | zona ausente y reloj desconocido | el fichero contiene el valor; no basta para ordenar la toma |
| `E04` | noticia | `09:36 +02:00` | publicación declarada | `07:36Z` | posible programación o corrección | el medio declara publicación a esa hora |
| `E05` | archivo web | `07:52Z` | captura | `07:52Z` | captura posterior a disponibilidad | a esa hora el archivo pudo recuperar esa representación |

La conclusión defendible es limitada: la página municipal declara una publicación anterior al inicio anunciado y el archivo obtuvo una copia después. La foto no puede colocarse con precisión en UTC porque su marca carece de desplazamiento. Tampoco la captura de archivo demuestra que la página no existiera antes de `07:52Z`.

## Flujo recomendado: de cinco relojes a una secuencia auditable

### 1. Formula una pregunta temporal que pueda fallar

Evita «reconstruir todo». Define sujeto, ventana y criterio de cierre. Por ejemplo: «¿qué avisos públicos sobre el puente eran observables entre las 07:00Z y las 09:00Z?». Anota también qué queda fuera: identidades privadas, desplazamientos individuales y cualquier dato no necesario.

### 2. Preserva la fuente antes de interpretarla

Guarda la URL completa, fecha de consulta, respuesta o captura permitida, hash del fichero y método de obtención. Mantén una copia original de solo lectura y trabaja sobre otra. Para una página dinámica, conserva además el HTML o un formato de archivo web cuando sea legal y técnicamente posible; una captura de pantalla por sí sola puede perder enlaces, cabeceras y contexto.

La documentación del [servidor CDX de Internet Archive](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md) expone campos como `timestamp`, URL original, tipo MIME, código de estado, digest y longitud. Son útiles para localizar y comparar capturas. El `timestamp` pertenece a la captura del archivo: no debe renombrarse como fecha de publicación.

### 3. Extrae todos los tiempos y conserva su forma literal

No elijas todavía «la fecha buena». Registra cada valor con su ubicación:

```text
source_id: E03
field: EXIF:ExifIFD:DateTimeOriginal
raw_value: 2026:08:19 09:18:04
offset: unknown
extraction_time: 2026-08-23T05:40:12Z
method: exiftool -time:all -a -G1 -s foto.jpg
```

La [FAQ oficial de ExifTool](https://exiftool.org/faq.html) distingue las fechas internas del fichero de las fechas del sistema de archivos y recomienda mostrar grupos y duplicados al inspeccionar metadatos. También señala que el formato EXIF habitual no incorpora por sí solo subsegundos y zona horaria, aunque otros formatos sí pueden hacerlo. Por eso `DateTimeOriginal` no debe convertirse automáticamente a UTC usando la zona del ordenador del analista.

### 4. Clasifica la semántica antes de normalizar

Añade a cada valor un tipo explícito: `ocurrido`, `afirmado`, `publicado`, `modificado`, `capturado`, `extraído` o `desconocido`. Una misma fuente puede contener varios. Conserva además quién hace la afirmación y de qué entidad habla.

El modelo [W3C PROV-O](https://www.w3.org/TR/prov-o/) ofrece un vocabulario útil: una `Entity` es la página o el fichero; una `Activity`, la publicación, captura o transformación; un `Agent`, el sistema u organización responsable. No hace falta desplegar RDF para aprovechar la idea. Basta con impedir que «el documento», «la actividad que lo generó» y «quien lo publica» se fundan en una sola columna ambigua.

### 5. Normaliza solo lo justificable

Convierte a UTC únicamente cuando exista un desplazamiento explícito o una base documentada para resolverlo. Guarda siempre:

- valor literal;
- zona o desplazamiento declarado;
- regla de conversión;
- valor UTC calculado;
- precisión original;
- nivel y motivo de incertidumbre.

No rellenes una zona ausente con la de tu navegador. Si una fuente solo dice «por la mañana», represéntala como intervalo. Si una plataforma redondea a minutos, no inventes segundos `:00` como si fueran precisión observada.

### 6. Modela intervalos, no solo puntos

Dos columnas, `earliest` y `latest`, suelen ser más honestas que una hora única. Una página capturada a las `07:52Z` y ya enlazada desde otra captura de las `07:40Z` pudo estar disponible como tarde a las `07:40Z`; el límite inferior seguirá abierto hasta hallar otra observación. Expresa estos límites como *no antes de*, *no después de* o intervalo probable, indicando la evidencia que los sostiene.

### 7. Comprueba restricciones antes de ordenar

Construye relaciones que sí puedas defender:

```text
E01 observado-antes-de E05
E02 afirma-inicio E06
E03 tiempo-interno-incomparable-con E01
E04 modificado-despues-de publicado
```

Busca contradicciones: una actualización anterior a su publicación, un archivo creado después de haber sido enviado o dos marcas que solo encajan si se supone una zona no declarada. La contradicción es una señal para revisar procedencia, no una licencia para corregir el dato en silencio.

### 8. Separa hecho, inferencia e hipótesis

Usa tres columnas o etiquetas:

- **observación:** «la página muestra `09:12 +02:00`»;
- **inferencia:** «si el reloj y la etiqueta son correctos, equivale a `07:12Z`»;
- **hipótesis:** «el aviso estaba disponible antes del cierre anunciado».

Exige una fuente independiente para elevar una hipótesis. La proximidad temporal puede justificar una pregunta; no demuestra coordinación, conocimiento previo ni causalidad.

## Limitaciones y falsos positivos

Una cronología limpia puede seguir siendo equivocada. Los fallos más comunes son:

- **hora legal y horario estacional:** una zona cambia reglas; el desplazamiento aislado no identifica siempre la zona;
- **relojes desviados:** cámaras, servidores y dispositivos pueden adelantar o atrasar;
- **metadatos editables:** un campo interno es una afirmación técnica, no un sello inviolable;
- **procesado de plataformas:** una red social o gestor de contenidos puede recomprimir, reexportar o sustituir metadatos;
- **publicaciones programadas:** la hora visible puede pertenecer al calendario editorial, no a la primera entrega HTTP;
- **cachés y réplicas:** usuarios distintos pueden observar versiones diferentes durante una transición;
- **actualizaciones silenciosas:** una página conserva URL y cambia contenido, título o fecha;
- **latencia de archivo:** la primera captura conocida solo fija un límite, no el nacimiento de la página;
- **precisión falsa:** transformar «09:18» en `09:18:00.000Z` añade exactitud inexistente;
- **ausencia de evidencia:** no encontrar una captura no demuestra que el contenido no existiera.

Documenta las alternativas. Si dos secuencias siguen siendo compatibles con los datos, publica ambas o declara que el orden no puede resolverse.

## Buenas prácticas de OPSEC, ética y privacidad

- trabaja sobre acontecimientos y fuentes de interés legítimo, no sobre rutinas de personas privadas;
- minimiza nombres, ubicaciones precisas y metadatos personales que no respondan a la pregunta;
- separa el almacén de evidencias del material que vas a publicar;
- usa identificadores ficticios o seudónimos en tablas de método;
- registra accesos y transformaciones sin modificar el original;
- no contactes a terceros ni fuerces autenticación para completar una hora ausente;
- somete acusaciones, decisiones de alto impacto y datos sensibles a revisión humana y asesoramiento adecuado.

La procedencia sirve también para reconocer límites. El [W3C PROV Overview](https://www.w3.org/TR/prov-overview/) define la procedencia como información sobre entidades, actividades y personas implicadas en producir datos, útil para evaluar calidad, fiabilidad o confianza. No garantiza por sí sola que una afirmación sea verdadera.

## Alternativas y siguientes pasos

Una hoja de cálculo con validación de columnas basta para un caso pequeño. SQLite o Datasette ayudan a consultar cientos de eventos; un grafo resulta útil cuando varias fuentes derivan unas de otras. El formato importa menos que conservar identificadores estables, valores literales, procedencia, conversiones y contradicciones.

Combina la cronología con:

- archivos web para fijar límites de observabilidad;
- hashes y copias originales para controlar transformaciones;
- registros institucionales para confirmar horas anunciadas;
- meteorología, imágenes o sensores públicos cuando sean pertinentes y proporcionales;
- una segunda fuente independiente para cualquier inferencia causal.

El takeaway accionable es este: **no ordenes una fecha hasta poder nombrar su reloj**. Para cada fila, conserva el valor original, su semántica, zona, precisión, fuente, método y rango de incertidumbre. Solo entonces normaliza, compara y escribe una conclusión que no diga más que la evidencia.

Como siguiente tema, merece la pena estudiar cómo gestionar versiones y correcciones de una fuente viva sin perder el historial de qué vio cada analista.

## Fuentes consultadas

- [RFC 3339: Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/info/rfc3339/)
- [RFC 9557: Date and Time on the Internet: Timestamps with Additional Information](https://www.rfc-editor.org/info/rfc9557/)
- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/)
- [Internet Archive Wayback CDX Server API](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md)
- [ExifTool FAQ](https://exiftool.org/faq.html)
