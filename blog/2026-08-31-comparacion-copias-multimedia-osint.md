---
title: "Comparar copias multimedia en OSINT: bytes, flujos y percepción sin convertir diferencias en acusaciones"
slug: /comparacion-copias-multimedia-osint
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-08-31
image: /img/blog/2026-08-31-comparacion-copias-multimedia-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista comparando dos copias multimedia por capas visuales, acústicas y técnicas](/img/blog/2026-08-31-comparacion-copias-multimedia-osint.png)

*Imagen generada mediante inteligencia artificial.*

Dos vídeos muestran aparentemente la misma escena, pero sus hashes no coinciden. Uno dura 40 milisegundos más, pesa la mitad y declara otra fecha. La conclusión tentadora es que alguien lo manipuló. La conclusión profesional es más modesta: **todavía no sabemos qué capa cambió, por qué cambió ni si la diferencia afecta al contenido que importa**.

Comparar copias multimedia en OSINT no consiste en buscar un número mágico de «similitud». Consiste en formular una pregunta verificable, conservar los originales, alinear aquello que sea comparable y documentar por separado bytes, contenedores, flujos, tiempo y percepción. Esa separación convierte una sospecha vaga en un análisis reproducible sin acusar a nadie por una transcodificación rutinaria.

<!-- truncate -->

## Qué significa que dos copias sean «la misma»

La palabra *misma* puede describir relaciones diferentes:

| Capa | Pregunta comprobable | Lo que no demuestra por sí sola |
| --- | --- | --- |
| fichero | ¿Los bytes completos coinciden? | que una copia distinta muestre otra escena |
| contenedor | ¿Coinciden formato, pistas, etiquetas y orden? | que el contenido audiovisual haya sido alterado |
| flujo codificado | ¿Coinciden los paquetes o bitstreams seleccionados? | identidad del archivo completo |
| muestras decodificadas | ¿Producen los mismos fotogramas o muestras de audio bajo condiciones registradas? | autenticidad del suceso representado |
| percepción | ¿La imagen o el sonido son suficientemente parecidos para una hipótesis concreta? | igualdad matemática, intención o autoría |
| contexto | ¿Encajan publicación, procedencia y cronología externas? | una cadena de custodia completa si faltan eslabones |

Un remultiplexado puede cambiar el fichero y el contenedor sin recodificar los flujos. Una transcodificación puede conservar la escena a costa de introducir pérdidas. Un recorte puede mantener la mayor parte del contenido, pero eliminar precisamente el instante relevante. Incluso dos archivos con muestras visuales equivalentes pueden diferir en audio, subtítulos o miniaturas.

Por eso, antes de abrir una herramienta, escribe la hipótesis: «¿La copia B contiene la misma secuencia audiovisual pública que la copia A, salvo empaquetado y compresión?». Esa pregunta no es igual que «¿B es el original?» ni que «¿B fue manipulada con intención de engañar?».

## Caso de uso legítimo: dos copias de un aviso público

La empresa ficticia **Puerto Claro** publica un vídeo sobre una interrupción de servicio. El equipo de cumplimiento obtiene, por canales autorizados:

- `aviso-web.mp4`, descargado de la página pública a las 10:15 UTC;
- `aviso-prensa.mkv`, recibido del gabinete de comunicación a las 10:42 UTC.

Ambos parecen mostrar los mismos 27 segundos, pero el segundo incluye subtítulos y conserva más calidad. El objetivo es determinar qué diferencias se observan y si el fragmento visual central es consistente. No se intenta identificar a las personas que aparecen ni atribuir intenciones al editor.

El equipo crea una ficha por copia con URL o canal de origen, hora de adquisición, cabeceras relevantes, tamaño y hash. También registra qué pregunta motivó la comparación y qué tratamiento de datos está autorizado. El resultado esperado no es un veredicto binario, sino una matriz que distinga coincidencias, diferencias explicables y cuestiones abiertas.

## Flujo recomendado por capas

### 1. Conserva antes de comparar

Trabaja con copias y fija primero la identidad de los bytes:

```bash
sha256sum aviso-web.mp4 aviso-prensa.mkv > hashes-adquisicion.sha256
cp --preserve=timestamps aviso-web.mp4 trabajo-web.mp4
cp --preserve=timestamps aviso-prensa.mkv trabajo-prensa.mkv
```

El SHA-256 responde a una pregunta estrecha: si coincide, los ficheros comparados tienen los mismos bytes con una confianza criptográfica adecuada al flujo; si difiere, solo sabemos que **algún byte** es distinto. No localiza el cambio, no mide parecido y no prueba manipulación maliciosa.

Guarda también la versión de cada herramienta. Un análisis reproducible necesita saber con qué decodificador, opciones y entorno se obtuvo cada salida.

### 2. Haz inventarios estructurados sin reproducir automáticamente

Obtén una vista separada de formato y flujos:

```bash
ffprobe -v error -show_format -show_streams \
  -of json trabajo-web.mp4 > trabajo-web.ffprobe.json

ffprobe -v error -show_format -show_streams \
  -of json trabajo-prensa.mkv > trabajo-prensa.ffprobe.json
```

Compara, como mínimo:

- número, tipo y orden de flujos;
- códecs, perfiles, dimensiones, frecuencia de imagen y formato de píxel;
- canales, frecuencia de muestreo e idioma del audio;
- duración, `start_time`, `time_base` y marcas temporales;
- subtítulos, capítulos, imágenes adjuntas y etiquetas;
- software de escritura declarado y nivel del contenedor donde aparece.

No compares el JSON completo como si cada diferencia tuviera igual significado. Una etiqueta de título, un identificador interno y una pista de vídeo requieren interpretaciones distintas. Conserva la salida original y construye después una tabla normalizada con los campos relevantes.

### 3. Distingue remultiplexación de recodificación

Una remultiplexación reorganiza flujos en otro contenedor sin tener que volver a codificarlos. Puede cambiar extensión, tamaño, índices, marcas temporales, etiquetas y hash global. Una transcodificación decodifica y vuelve a codificar al menos un flujo; puede alterar muestras, tasa, resolución, color o audio aunque el resultado parezca igual.

Busca una explicación técnica por capas:

1. si cambia solo el contenedor y los flujos seleccionados son equivalentes, anota «compatible con remultiplexación»;
2. si cambian códec, resolución o parámetros de compresión, anota «existe recodificación o transformación de flujo»;
3. si cambia la duración, localiza dónde aparece el desfase antes de hablar de recorte;
4. si hay pistas nuevas, determina si añaden información o modifican la presentación principal.

«Compatible con» es deliberado. El patrón técnico rara vez demuestra quién ejecutó la transformación o con qué intención.

### 4. Compara muestras decodificadas cuando la pregunta lo exige

FFmpeg documenta `framehash` para calcular hashes de paquetes de audio y vídeo convertidos a formatos crudos. Puede producir un registro SHA-256 por unidad decodificada:

```bash
ffmpeg -v error -i trabajo-web.mp4 \
  -map 0:v:0 -f framehash -hash sha256 web-video.framehash

ffmpeg -v error -i trabajo-prensa.mkv \
  -map 0:v:0 -f framehash -hash sha256 prensa-video.framehash
```

Esto es más informativo que el hash del fichero, pero no elimina los problemas de alineación. Diferencias en formato de píxel, rango de color, resolución, frecuencia de imagen, orden temporal o decodificación pueden cambiar la salida. Registra la compilación de FFmpeg y las opciones; no mezcles resultados generados bajo normalizaciones distintas.

Si las secuencias están alineadas y comparten geometría y formato, los filtros `ssim` o `psnr` pueden describir diferencias numéricas. La propia documentación de FFmpeg exige dos vídeos con la misma resolución y formato de píxel para SSIM. Antes de calcular nada, decide explícitamente:

- qué copia actúa como referencia solo a efectos de la métrica;
- cómo se alinean los inicios y los fotogramas;
- si se recorta, escala, cambia el formato de píxel o ignora audio;
- qué segmentos quedan fuera y por qué.

Una posible ejecución, **solo después de justificar esa alineación**, es:

```bash
ffmpeg -i trabajo-web.mp4 -i trabajo-prensa.mkv \
  -filter_complex \
  "[0:v]settb=AVTB,setpts=PTS-STARTPTS,scale=1280:720,format=yuv420p[a]; \
   [1:v]settb=AVTB,setpts=PTS-STARTPTS,scale=1280:720,format=yuv420p[b]; \
   [a][b]ssim=stats_file=ssim.log" \
  -f null -
```

El escalado y la conversión introducen su propia transformación. Guarda el comando completo y no presentes el valor final como «porcentaje de autenticidad». SSIM o PSNR cuantifican una relación bajo unas condiciones; no explican la causa ni valoran el significado de una diferencia localizada.

### 5. Trata el audio como una capa propia

Dos vídeos visualmente equivalentes pueden tener narraciones, silencios, mezclas o desfases distintos. Compara primero inventario, duración, canales y tasa de muestreo. Después escucha o inspecciona únicamente lo necesario y autorizado, teniendo en cuenta voces y otros datos personales.

Chromaprint y su utilidad `fpcalc` pueden ayudar a detectar audio casi idéntico:

```bash
fpcalc audio-web.wav > audio-web.fingerprint.txt
fpcalc audio-prensa.wav > audio-prensa.fingerprint.txt
```

El proyecto define Chromaprint para identificación de audio casi idéntico, duplicados y monitorización de flujos largos; advierte que no es una solución general de huella acústica. Una coincidencia es una pista de contenido relacionado. Una no coincidencia puede deberse a recorte, mezcla, velocidad, ruido o codificación, y no prueba que las escenas visuales sean diferentes.

### 6. Localiza las diferencias relevantes

Una media global puede ocultar un cambio breve. Crea puntos de control reproducibles:

- inicio, final y transiciones detectadas;
- fotogramas anteriores y posteriores al segmento investigado;
- forma de onda o espectrograma de intervalos autorizados;
- subtítulos y texto sobreimpreso;
- cambios de relación de aspecto, barras, recortes o interpolación;
- silencios, desplazamientos y canales añadidos o eliminados.

Extraer imágenes de control no demuestra por sí solo continuidad. Conserva el tiempo de presentación, el comando de extracción y el vínculo con la copia de origen. Si la alineación es incierta, usa intervalos («entre 12,4 y 12,6 segundos») en vez de fingir precisión de fotograma.

### 7. Construye una matriz de evidencias, no un semáforo

La tabla final puede adoptar esta forma:

| Observación | Capa | Interpretación limitada | Alternativa benigna | Contraste pendiente |
| --- | --- | --- | --- | --- |
| SHA-256 global distinto | fichero | los bytes no son idénticos | contenedor o etiqueta diferente | inventario de flujos |
| vídeo H.264 frente a H.265 | flujo | existe recodificación o fuente derivada | exportación para reducir tamaño | comparar contenido alineado |
| subtítulos solo en MKV | presentación | B incorpora una pista adicional | copia accesible para prensa | revisar procedencia de la pista |
| desfase de 80 ms | tiempo | los inicios no están alineados | `start_time` o edición técnica | localizar primer evento común |
| SSIM alto salvo 0,5 s | percepción | tramo localizado diferente tras normalización | rótulo, fundido o fotograma perdido | inspección manual y contexto |

Cada fila separa **dato observado**, **inferencia** y **prueba que falta**. Esa disciplina evita que una diferencia técnica se transforme por inercia en una acusación editorial.

## Limitaciones y falsos positivos

### Una métrica alta puede ocultar justo lo importante

Un vídeo largo puede obtener una similitud media elevada aunque cambie un rótulo decisivo durante un segundo. También puede puntuar peor por una recompresión visible que no altera el significado. Revisa distribuciones e intervalos, no solo promedios.

### Alinear también es transformar

Recortar, reescalar, resincronizar y convertir color hacen comparables dos entradas, pero modifican aquello que se mide. Conserva originales, salidas intermedias y parámetros. Si hay varias alineaciones plausibles, informa del rango de resultados.

### Decodificadores y versiones importan

La salida cruda puede depender de biblioteca, aceleración, gestión de color y tratamiento de errores. No combines hashes por fotograma generados con pipelines desconocidos. Una discrepancia reproducida por dos herramientas independientes tiene más peso, pero sigue necesitando interpretación.

### Parecido no equivale a procedencia

Dos copias casi idénticas pueden proceder de fuentes distintas. Dos copias diferentes pueden derivar legítimamente de un mismo original. La relación técnica debe cruzarse con URLs, horas de adquisición, cabeceras, historial de publicación y, cuando exista, información verificable de procedencia.

## OPSEC, ética y privacidad

- Compara únicamente material adquirido legalmente y con una finalidad definida.
- Evita subir archivos sensibles a servicios externos; empieza con herramientas locales y copias de trabajo.
- Trata voz, rostros, ubicaciones y subtítulos como datos potencialmente personales.
- No publiques fotogramas irrelevantes que expongan a terceros.
- Aísla archivos no confiables y desactiva reproducción automática, enlaces y adjuntos embebidos.
- Registra transformaciones y versiones para que otra persona pueda reproducir el análisis.
- Mantén separadas observación, inferencia, confianza y explicación alternativa.
- No atribuyas autoría o intención a partir de un códec, una fecha o una métrica de similitud.

## Alternativas y siguientes pasos

MediaInfo y `ffprobe` sirven para inventariar; Bento4 o `mkvinfo` permiten profundizar en contenedores concretos; `framehash` ayuda a comparar salidas decodificadas; SSIM y PSNR cuantifican diferencias bajo alineación explícita; Chromaprint aporta una pista especializada para audio casi idéntico. Ninguna sustituye el contexto ni convierte una copia en «original» por decreto.

El takeaway práctico es una secuencia de seis verbos: **preserva, inventaría, separa, alinea, compara y corrobora**. Si el informe puede señalar en qué capa aparece cada diferencia, qué transformación aplicaste y qué explicación alternativa sigue abierta, ya ofrece mucho más valor que un porcentaje de parecido sin método.

Como ejercicio seguro, crea en un entorno propio tres derivados de un vídeo sintético: una remultiplexación, una transcodificación y un recorte breve. Construye la matriz sin mirar los comandos de creación y comprueba después qué observaciones permitían distinguir cada caso. El siguiente paso natural será profundizar en sincronización audiovisual y deriva temporal sin confundir desfase técnico con edición engañosa.

## Fuentes

- [FFmpeg: documentación de formatos (`framehash` y `framemd5`)](https://ffmpeg.org/ffmpeg-formats.html#framehash-1)
- [FFmpeg: documentación de filtros (`ssim`, `psnr` y métricas relacionadas)](https://ffmpeg.org/ffmpeg-filters.html)
- [`ffprobe`: documentación oficial](https://ffmpeg.org/ffprobe.html)
- [Chromaprint: repositorio y alcance declarado del proyecto](https://github.com/acoustid/chromaprint)
- [MediaInfo: repositorio y descripción oficial](https://github.com/MediaArea/MediaInfo)
