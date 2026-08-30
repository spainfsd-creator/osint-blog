---
title: "MediaInfo y ffprobe en OSINT: leer metadatos multimedia sin confundirlos con la verdad"
slug: /mediainfo-ffprobe-osint-metadatos-multimedia
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-08-30
image: /img/blog/2026-08-30-mediainfo-ffprobe-osint-metadatos-multimedia.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT comparando contenedores, flujos, marcas de tiempo y un informe JSON de un archivo multimedia](/img/blog/2026-08-30-mediainfo-ffprobe-osint-metadatos-multimedia.png)

*Imagen generada mediante inteligencia artificial.*

Un vídeo de una avería industrial llega a un equipo de verificación con un nombre convincente: `incidente_1432_original.mp4`. Una herramienta muestra «fecha de creación 14:32», otra identifica un codificador y las redes sociales aseguran que el archivo salió directamente de una cámara. Parece una cronología cerrada. No lo es: **un contenedor puede conservar datos técnicos, etiquetas declaradas y rastros de procesado, pero no certifica por sí solo cuándo, dónde ni por quién se grabó una escena**.

MediaInfo y `ffprobe` permiten abrir esa caja de manera reproducible. El valor OSINT no está en encontrar una etiqueta espectacular, sino en distinguir qué pertenece al contenedor, qué describe cada flujo y qué hipótesis resiste al contrastar el archivo con fuentes independientes.

<!-- truncate -->

Este artículo propone un flujo local y responsable para examinar vídeos y audios obtenidos legítimamente. Las fuentes técnicas se consultaron el **30 de agosto de 2026**. La empresa, el incidente, los archivos y todos los resultados del ejemplo son ficticios. No se intenta identificar a personas ni recuperar información privada.

## Qué son MediaInfo y ffprobe, y para qué sirven en OSINT

Un archivo multimedia suele ser más que una secuencia de imágenes o sonido. El **contenedor** —por ejemplo, MP4, Matroska o WebM— organiza uno o varios flujos, capítulos, adjuntos y etiquetas. Cada flujo puede emplear un códec diferente y tener su propia resolución, frecuencia, idioma, duración o base temporal.

[MediaInfo](https://github.com/MediaArea/MediaInfo) ofrece una vista unificada de datos técnicos y etiquetas relevantes de archivos de vídeo y audio. Resulta cómodo para una primera lectura y para comparar rápidamente varios ejemplares. [`ffprobe`](https://ffmpeg.org/ffprobe.html), parte del proyecto FFmpeg, inspecciona el formato y los flujos y puede emitir secciones estructuradas, entre ellas `FORMAT`, `STREAM` y `CHAPTER`, en formatos legibles por máquinas como JSON.

Ambas herramientas **interpretan lo que encuentran en el archivo**. No consultan mágicamente la cámara original, la plataforma de publicación ni una autoridad temporal. Sus diferencias también son informativas: pueden normalizar nombres, calcular duraciones o exponer etiquetas de forma distinta. Por eso conviene conservar la salida bruta de cada una, su versión y el hash del archivo analizado.

| Capa | Pregunta útil | Lo que no demuestra |
| --- | --- | --- |
| fichero | ¿Qué bytes recibimos y qué hash tienen? | quién los creó o si son la primera copia |
| contenedor | ¿Qué formato, duración, marcas y etiquetas declara? | que una fecha sea la de grabación real |
| flujo | ¿Qué códec, dimensiones, canales o base temporal aparecen? | qué dispositivo concreto produjo el contenido |
| cronología interna | ¿Son coherentes duraciones, inicios y marcas de tiempo? | cuándo ocurrió la escena en el mundo real |
| contexto externo | ¿Coinciden publicación, clima, lugar y testimonios públicos? | una cadena de custodia completa si faltan eslabones |

## Caso de uso legítimo: comparar dos copias de un aviso público

La cooperativa ficticia **Puerto Claro** publica un vídeo de treinta segundos sobre una avería en una cinta transportadora. El equipo de cumplimiento recibe dos archivos por canales autorizados:

- `puerto-claro-a.mp4`, descargado del repositorio público de avisos;
- `puerto-claro-b.mkv`, facilitado por el gabinete de comunicación como copia de trabajo.

El objetivo no es atribuir el vídeo a una persona. Se quiere saber si ambos archivos contienen aparentemente la misma pieza, si alguno fue remultiplexado o transcodificado y qué fechas pueden incorporarse —con sus límites— a una cronología.

La primera inspección revela que la copia MP4 contiene vídeo y audio, mientras que la Matroska añade subtítulos. La duración visual es casi igual, pero los códecs y los valores de tasa binaria difieren. La fecha del MP4 está en una estructura del contenedor; la de Matroska describe cuándo la aplicación de multiplexado creó el segmento. Ninguna observación autoriza a escribir «el incidente ocurrió a esa hora».

La especificación de [elementos Matroska](https://www.matroska.org/technical/elements.html) es explícita: `DateUTC` representa la creación del `Segment` por la aplicación o biblioteca de multiplexado, mientras `MuxingApp` y `WritingApp` describen software de empaquetado y escritura. Son pistas de procesado, no una firma de cámara ni una fecha probada del suceso.

En QuickTime/MP4 también hay que preguntar **qué fecha y en qué nivel**. La documentación de Apple explica que los metadatos pueden residir en el átomo de película, de pista o de medio, y que existen estructuras extensibles de clave y valor. El campo de [creación de la cabecera de película](https://developer.apple.com/documentation/quicktime-file-format/movie_header_atom/creation_time) cuenta segundos desde el 1 de enero de 1904, preferiblemente en UTC. El significado técnico del campo no impide que un editor lo reescriba al exportar.

## Flujo recomendado: del original inmóvil a una matriz de evidencias

### 1. Preserva antes de interpretar

Trabaja sobre una copia y registra procedencia, fecha de adquisición y condiciones de descarga. Calcula un hash antes de abrir el archivo con herramientas que pudieran crear miniaturas o ficheros auxiliares:

```bash
sha256sum puerto-claro-a.mp4 > puerto-claro-a.mp4.sha256
cp --preserve=timestamps puerto-claro-a.mp4 copia-trabajo.mp4
```

El hash demuestra identidad de bytes entre dos comprobaciones; no demuestra autenticidad de la escena. Evita modificar fechas del sistema de archivos o confundirlas con metadatos internos. Guarda también la URL pública, cabeceras HTTP relevantes y hora de adquisición en UTC cuando el marco legal y la finalidad lo permitan.

### 2. Obtén una vista general con MediaInfo

La interfaz gráfica ayuda a explorar, pero una salida estructurada es más fácil de archivar y comparar:

```bash
mediainfo --Output=JSON copia-trabajo.mp4 > copia-trabajo.mediainfo.json
mediainfo --Version > mediainfo-version.txt
```

Revisa como mínimo:

- formato y perfil del contenedor;
- número y tipo de flujos;
- duración, tasa binaria y tamaño declarados o calculados;
- códecs, dimensiones, frecuencia de imagen y canales;
- idiomas, títulos, codificador y fechas si existen.

Trata «Encoded_Application», «Writing library», modelo o coordenadas como **valores declarados o interpretados**, no como hechos confirmados. Un archivo exportado, remultiplexado o editado puede conservar unas etiquetas, eliminar otras o añadir datos del último programa utilizado.

### 3. Separa formato, flujos y capítulos con ffprobe

Una consulta compacta y reproducible puede ser:

```bash
ffprobe -v error \
  -show_format -show_streams -show_chapters \
  -of json copia-trabajo.mp4 > copia-trabajo.ffprobe.json
ffprobe -version > ffprobe-version.txt
```

Según la [documentación oficial de `ffprobe`](https://ffmpeg.org/ffprobe.html), `-show_format` presenta información del contenedor, `-show_streams` crea una sección por flujo y `-show_chapters` expone capítulos. Las etiquetas aparecen asociadas a su sección correspondiente. Esa ubicación importa: una fecha de formato no equivale automáticamente a una fecha del flujo, y un `timecode` puede proceder de lugares distintos según el formato.

Para reducir ruido sin perder trazabilidad, conserva primero la salida completa y deriva después una vista de trabajo con `-show_entries`. No fuerces el formato de entrada salvo que exista una razón documentada: dejar que la herramienta lo detecte también permite registrar errores o ambigüedades.

### 4. Construye una tabla de afirmaciones, no un volcado de campos

Convierte cada dato relevante en una fila:

| Valor observado | Ubicación | Interpretación provisional | Contraste necesario |
| --- | --- | --- | --- |
| `creation_time` | etiqueta de formato MP4 | posible escritura o exportación del contenedor | publicación, copia anterior, registro del sistema autorizado |
| `encoder` | flujo de vídeo | software o biblioteca declarada | otros archivos del mismo flujo de trabajo |
| 1920 × 1080 | flujo de vídeo | dimensiones codificadas | no identifica cámara ni resolución de captura |
| `DateUTC` | `Segment/Info` de Matroska | creación del segmento al multiplexar | cronología de entrega y versión previa |
| pista de subtítulos | flujo adicional | edición o empaquetado posterior posible | contenido, idioma y procedencia de esa pista |

Este modelo obliga a escribir qué se sabe, dónde se observó y qué falta. También hace visibles las contradicciones entre herramientas sin decidir de antemano cuál «tiene razón».

### 5. Compara copias sin convertir diferencias en acusaciones

Dos copias pueden compartir contenido perceptible y, sin embargo, tener hashes, códecs y estructuras distintos. Una plataforma puede transcodificar vídeo, normalizar audio, retirar etiquetas, desplazar marcas temporales o reconstruir el contenedor. Del mismo modo, una simple remultiplexación puede cambiar el hash sin volver a codificar los flujos.

Compara en capas:

1. hash del fichero completo;
2. inventario y orden de flujos;
3. códecs y parámetros técnicos;
4. duración e inicios temporales, con su `time_base`;
5. etiquetas y su ubicación;
6. contenido visible y audible mediante técnicas de comparación apropiadas;
7. cronología externa de publicación y adquisición.

El registro de tipos de MP4 mantiene códigos para marcas, manejadores e ítems; la [MP4 Registration Authority](https://mp4ra.org/registered-types/items) recuerda, por ejemplo, que el modelo de ítems puede transportar imágenes, documentos de metadatos y contenido derivado. Una extensión `.mp4` no describe por sí sola todo lo que hay dentro.

## Limitaciones, ausencias y falsos positivos

### Una fecha exacta puede ser exactamente otra cosa

La precisión visual de `2026-08-30T14:32:01Z` no prueba su semántica. Puede ser una fecha de creación del contenedor, de codificación, de etiquetado o de exportación. Puede haberse copiado desde otro archivo, normalizado a UTC, interpretado con una zona errónea o escrito por un reloj desajustado.

Pregunta siempre:

- ¿qué especificación define el campo?;
- ¿en qué estructura y nivel aparece?;
- ¿qué programa pudo escribirlo?;
- ¿sobrevive a una exportación ordinaria?;
- ¿existe una fuente independiente que acote el momento real?

### La ausencia de metadatos no prueba manipulación

Mensajería, redes sociales, editores y pipelines de publicación pueden eliminar o reemplazar etiquetas como parte de su funcionamiento normal. Un archivo «limpio» no es necesariamente sospechoso; uno lleno de etiquetas tampoco es necesariamente original.

### Códec y codificador no identifican por sí solos un dispositivo

Millones de cámaras, teléfonos, bibliotecas y servicios comparten códecs y cadenas de software. Incluso una etiqueta con modelo puede copiarse o conservarse tras editar. Úsala para generar candidatos o detectar incoherencias, nunca para atribuir autoría de forma aislada.

### Las herramientas pueden discrepar sin que ninguna esté rota

MediaInfo y `ffprobe` pueden elegir nombres distintos, redondear una duración, priorizar otra cabecera o presentar valores calculados frente a declarados. Registra versiones y consulta la especificación del contenedor antes de convertir una diferencia en hallazgo.

## Buenas prácticas de OPSEC, ética y privacidad

- Analiza solo archivos obtenidos con base legal y finalidad legítima.
- Haz la primera inspección local, en una copia y, si el riesgo lo exige, en un entorno aislado y sin red.
- No subas material sensible a verificadores públicos por comodidad.
- Minimiza los datos del informe: una coordenada, voz, nombre de pista o miniatura puede exponer a terceros.
- No publiques volcados completos si contienen información personal irrelevante.
- Describe las herramientas y versiones, pero separa salida técnica, interpretación e inferencia.
- Mantén una hipótesis alternativa benigna para cada anomalía de procesado.
- Corrobora lugar, tiempo y contexto con fuentes públicas independientes antes de atribuir.

La inspección también tiene un límite de seguridad: un archivo desconocido es entrada no confiable. Usa herramientas actualizadas, evita reproducirlo automáticamente y no ejecutes adjuntos, scripts ni enlaces embebidos.

## Alternativas y siguientes pasos

MediaInfo y `ffprobe` se complementan con otras capas:

- **ExifTool**, para una lectura amplia de etiquetas y estructuras compatibles;
- **Bento4** o herramientas equivalentes, cuando necesitas estudiar cajas ISO BMFF con más detalle;
- **mkvinfo**, para inspección específica de Matroska;
- **C2PA**, si existe una credencial de procedencia que pueda validarse con una política explícita;
- hashes criptográficos y conservación WARC o de cabeceras, para documentar adquisición y contexto web;
- análisis visual, acústico y multifuente, siempre separado de las etiquetas del contenedor.

El takeaway práctico es sencillo: **primero fija los bytes; después separa fichero, contenedor y flujos; luego traduce cada campo a una afirmación limitada; y solo al final corrobora con el mundo exterior**. Una tarde útil de entrenamiento consiste en exportar un vídeo ficticio dos veces, una mediante remultiplexación y otra mediante transcodificación, y comparar qué cambia sin intentar adivinar más de lo que los datos permiten.

El siguiente tema natural será diseñar una matriz de comparación entre copias multimedia que distinga cambios de contenedor, cambios de flujo y cambios perceptibles sin convertir una diferencia técnica en una acusación.

## Fuentes

- [MediaInfo: repositorio y descripción oficial](https://github.com/MediaArea/MediaInfo)
- [`ffprobe`: documentación oficial](https://ffmpeg.org/ffprobe.html)
- [Matroska: especificación de elementos](https://www.matroska.org/technical/elements.html)
- [Apple: átomos y tipos de metadatos de QuickTime](https://developer.apple.com/documentation/quicktime-file-format/metadata_atoms_and_types)
- [Apple: campo de creación de la cabecera de película](https://developer.apple.com/documentation/quicktime-file-format/movie_header_atom/creation_time)
- [MP4 Registration Authority: tipos de ítems](https://mp4ra.org/registered-types/items)
