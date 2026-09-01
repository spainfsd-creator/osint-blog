---
title: "Sincronización audiovisual en OSINT: medir desfase y deriva temporal sin inventar una manipulación"
slug: /sincronizacion-audiovisual-deriva-osint
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-09-01
image: /img/blog/2026-09-01-sincronizacion-audiovisual-deriva-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT comparando una línea de vídeo y una forma de onda cuyos marcadores se separan con el tiempo](/img/blog/2026-09-01-sincronizacion-audiovisual-deriva-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/sincronizacion-audiovisual-deriva-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Una portavoz golpea la mesa y el sonido llega 180 milisegundos después. Diez minutos más tarde, el retraso parece acercarse al medio segundo. Es tentador concluir que alguien movió el audio para ocultar un corte. Pero dos observaciones visuales todavía no distinguen entre **un desfase fijo, una deriva acumulada, una transcodificación defectuosa, latencia de reproducción o una edición real**.

En OSINT, sincronizar no significa hacer que un vídeo «parezca bien». Significa medir eventos comunes en varios puntos, conservar los originales y separar lo que declara la línea temporal de lo que realmente contiene la señal. Solo entonces puede construirse una explicación limitada y reproducible.

<!-- truncate -->

Este artículo propone un flujo local para material obtenido legítimamente en verificación periodística, respuesta a incidentes o análisis de comunicaciones públicas. Las fuentes técnicas se consultaron el **1 de septiembre de 2026**. La entidad, los archivos, los eventos y las mediciones del caso son ficticios. No se pretende identificar voces ni personas.

## Qué son el desfase y la deriva

Audio y vídeo son flujos con muestras o fotogramas que el reproductor presenta siguiendo marcas temporales. En FFmpeg, el **PTS** es la marca de tiempo de presentación; debe interpretarse con la base temporal del flujo. El **DTS** indica orden de decodificación y puede diferir cuando la compresión reordena imágenes. Confundir ambos puede crear un problema que solo existe en la tabla del analista.

Conviene distinguir cuatro situaciones:

| Situación | Patrón observable | Hipótesis prudente |
| --- | --- | --- |
| desfase constante | audio y vídeo mantienen casi la misma separación en varios puntos | un flujo empezó antes, se añadió silencio o cambió su origen temporal |
| deriva aproximadamente lineal | la separación crece o disminuye con el tiempo | relojes, tasas efectivas o conversiones temporales no coincidentes |
| salto localizado | la relación cambia de golpe en un intervalo | pérdida, inserción, discontinuidad, corte o error de captura |
| percepción variable | distintos eventos producen medidas incompatibles | marcador ambiguo, eco, movimiento anticipatorio o reproducción inestable |

La [documentación oficial de `ffprobe`](https://ffmpeg.org/ffprobe.html) permite extraer flujos, paquetes, fotogramas y campos temporales en formatos estructurados. La [documentación de filtros de FFmpeg](https://ffmpeg.org/ffmpeg-filters.html) explica que `setpts` y `asetpts` cambian PTS, mientras que `aresample` puede estirar o comprimir audio, o insertar y retirar muestras, para ajustarlo a marcas temporales. Son capacidades de transformación, no detectores de engaño.

## Caso de uso legítimo: una comparecencia pública

La cooperativa ficticia **Puerto Claro** publica una comparecencia de doce minutos. El equipo de verificación descarga dos copias por canales autorizados:

- `rueda-prensa-web.mp4`, desde la página institucional;
- `rueda-prensa-sala.mkv`, entregada por el gabinete de comunicación.

Ambas muestran la misma intervención. En la copia web, tres golpes de mesa parecen retrasados respecto al sonido. El objetivo no es decidir quién editó qué, sino responder preguntas estrechas:

1. ¿Qué marcas temporales conserva cada flujo?
2. ¿La diferencia entre un evento visual y su sonido es constante?
3. ¿Cambia gradualmente o mediante saltos?
4. ¿La anomalía está en una copia, en ambas o en el entorno de reproducción?

Antes de observar el contenido, el equipo registra URL o canal, hora de adquisición, tamaño, hash SHA-256, versión de las herramientas y finalidad del tratamiento. Trabaja sobre copias y conserva intactos los archivos recibidos.

## Flujo recomendado paso a paso

### 1. Fija identidad y alcance

```bash
sha256sum rueda-prensa-web.mp4 rueda-prensa-sala.mkv \
  > hashes-adquisicion.sha256

ffmpeg -version > version-ffmpeg.txt
ffprobe -version > version-ffprobe.txt
```

El hash identifica los bytes examinados; no certifica que una copia sea original, auténtica o completa. Define también qué pista de audio analizarás si existen idiomas, comentarios o mezclas diferentes.

### 2. Inventaría flujos y líneas temporales

Empieza por una salida compacta:

```bash
ffprobe -v error \
  -show_entries \
  "stream=index,codec_type,time_base,start_time,duration,sample_rate,r_frame_rate:format=start_time,duration" \
  -of json rueda-prensa-web.mp4 > inventario-tiempo.json
```

`start_time` y `duration` ayudan a formular hipótesis, pero una diferencia declarada no equivale todavía a un desfase perceptible. Para revisar paquetes en intervalos pequeños:

```bash
ffprobe -v error -read_intervals "0%+8,00:09:55%+8" \
  -show_packets \
  -show_entries \
  "packet=stream_index,pts_time,dts_time,duration_time,flags:stream=index,codec_type,time_base" \
  -of json rueda-prensa-web.mp4 > paquetes-muestras.json
```

La propia documentación advierte que el inicio real tras una búsqueda puede diferir del solicitado. No conviertas `-read_intervals` en una promesa de corte exacto.

### 3. Elige eventos comunes y medibles

Busca marcadores breves presentes en imagen y sonido, por ejemplo:

- contacto visible de una mano con una mesa y su impacto;
- cierre de una puerta y golpe acústico;
- encendido visible de una señal acompañado por un tono;
- claqueta o patrón de prueba, si el material lo incluye.

El habla es peor marcador de lo que parece: la forma de la boca, el inicio fonético y la llegada del sonido no siempre ofrecen un instante único. El eco y la distancia entre fuente y micrófono también importan. La [recomendación EBU R37-2007](https://tech.ebu.ch/docs/r/r037.pdf) usa marcadores concurrentes de destello y tono para mediciones técnicas y trata por separado tolerancias de producción y de salida; esos límites de radiodifusión no son un umbral forense universal.

### 4. Mide en varios puntos, no solo al principio

Registra al menos un evento cerca del inicio, otro en la zona central y otro cerca del final. Para cada uno anota:

| Campo | Ejemplo ficticio |
| --- | --- |
| evento | golpe de carpeta 3 |
| tiempo visual | 00:10:02.440 |
| tiempo acústico | 00:10:02.781 |
| diferencia audio menos vídeo | +341 ms |
| incertidumbre | ±20 ms |
| método | inspección fotograma a fotograma y forma de onda |

Si llamamos `d(t)` a la diferencia entre el evento acústico y el visual, una estimación sencilla de deriva entre dos puntos es:

```text
deriva = d(t2) - d(t1)
tasa aproximada en ppm = deriva / (t2 - t1) × 1 000 000
```

En el ejemplo, pasar de `+180 ms` a `+420 ms` en 600 segundos supone `+240 ms` de deriva, unas 400 ppm. Esa cifra describe la pendiente observada bajo el método elegido; no identifica la causa ni atribuye intención.

### 5. Genera ayudas visuales sin alterar los originales

Una forma de onda permite localizar transitorios. Créala desde una copia de trabajo:

```bash
ffmpeg -i rueda-prensa-web.mp4 \
  -filter_complex "[0:a:0]showwavespic=s=1600x320:split_channels=1" \
  -frames:v 1 onda-web.png
```

Para un tramo corto, extrae audio sin subirlo a servicios externos:

```bash
ffmpeg -ss 00:09:55 -i rueda-prensa-web.mp4 -t 15 \
  -map 0:a:0 -c:a pcm_s24le tramo-analisis.wav
```

Anota el comando completo. `-ss`, la decodificación y la conversión de audio pueden introducir decisiones de búsqueda, redondeo o remuestreo. La visualización ayuda a medir; no reemplaza la señal ni el contexto.

### 6. Separa metadatos, señal y reproducción

Repite una muestra en otro reproductor o decodificador y comprueba si el problema persiste en la salida decodificada. La guía de Apple sobre [sincronización y temporización en QuickTime](https://developer.apple.com/documentation/quicktime-file-format/the_timing_and_synchronization_problem) documenta, por ejemplo, que no compensar muestras iniciales de ciertos audios codificados puede producir desincronización. Una reproducción defectuosa no demuestra que el fichero contenga una edición engañosa.

Clasifica cada observación por capa:

- **contenedor:** tiempos de inicio, duración, orden y edición declarada;
- **paquetes y fotogramas:** PTS, DTS, duraciones y discontinuidades;
- **señal:** posición del transitorio acústico y del evento visual;
- **reproducción:** comportamiento del decodificador, dispositivo o navegador;
- **procedencia:** cómo se obtuvo, publicó o transformó cada copia.

### 7. Corrige solo una copia de análisis y declara cómo

Para probar una hipótesis de desfase constante, puedes retrasar 240 ms el audio de una **copia derivada**:

```bash
ffmpeg -i rueda-prensa-web.mp4 \
  -filter_complex "[0:a:0]adelay=240:all=1[a]" \
  -map 0:v:0 -map "[a]" -c:v copy -c:a pcm_s16le \
  prueba-desfase-240ms.mkv
```

El filtro `adelay` rellena con silencio los canales retrasados. Esta salida sirve para comprobar si un modelo constante explica varios eventos; no debe sustituir al original ni circular sin una etiqueta clara.

Una deriva exige otro modelo. `asetpts` cambia marcas, pero no repara por sí solo el contenido temporal de las muestras. `aresample=async=1000` puede estirar o comprimir el audio para ajustarlo a timestamps con un límite de compensación, según la documentación oficial. No lo apliques a ciegas: primero demuestra que los timestamps son una referencia adecuada y conserva los parámetros. Si una corrección mejora el inicio y empeora el final, el modelo elegido es incorrecto.

### 8. Redacta una conclusión por hipótesis

Una matriz evita el salto de anomalía a acusación:

| Observación | Interpretación limitada | Alternativa plausible | Contraste pendiente |
| --- | --- | --- | --- |
| audio `+185 ms` en tres eventos iniciales | existe un desfase inicial consistente | latencia de codificación o inicio distinto | comparar copia de sala |
| audio `+420 ms` cerca del final | la separación aumentó | reloj o tasa efectiva diferente | estimar pendiente con más eventos |
| PTS sin saltos visibles | no se observa discontinuidad en esos campos | la señal pudo transformarse manteniendo timestamps regulares | inspeccionar contenido decodificado |
| otro reproductor reproduce igual | baja la probabilidad de un fallo exclusivo del primer reproductor | ambos comparten biblioteca o interpretación | probar decodificador independiente |

Una conclusión responsable podría ser: «En seis eventos, la diferencia audio-vídeo crece de `+180 ±20 ms` a `+420 ±25 ms`. El patrón es compatible con deriva aproximadamente lineal en esta copia. No permite determinar si se originó durante captura, codificación, distribución o edición».

## Limitaciones y falsos positivos

### Un evento visible no siempre coincide físicamente con el sonido

La luz llega antes que el sonido y un micrófono distante recibe el impacto más tarde. En una sala grande, reflejos y mezclas pueden desplazar el pico aparente. Usa eventos próximos al micrófono o incorpora la geometría a la incertidumbre.

### La frecuencia nominal no garantiza la tasa efectiva

Que un flujo declare 48 kHz o una cadencia concreta no demuestra que los relojes de captura permanecieran perfectamente sincronizados. Tampoco una duración distinta prueba que se hayan eliminado escenas.

### El códec puede añadir retardo o muestras de cebado

Algunos pipelines compensan estas muestras mediante metadatos; otros las interpretan de forma diferente. Compara señal decodificada y comportamiento de reproducción antes de atribuir el problema al contenido editorial.

### Una pendiente no siempre es lineal

Pérdidas, duplicados, cambios de reloj o concatenaciones pueden producir tramos con pendientes distintas. Ajustar una recta a todo el vídeo puede esconder saltos relevantes. Conserva puntos individuales y residuos, no solo el promedio.

### Sin un marcador compartido no hay medida fuerte

Correlacionar aplausos, música o ruido continuo puede ofrecer máximos engañosos. El filtro `axcorrelate` de FFmpeg calcula correlación cruzada normalizada entre dos audios, pero una correlación alta en una ventana indica parecido de señal, no identidad de fuente, sincronía audiovisual ni autenticidad.

## OPSEC, ética y privacidad

- Analiza solo material adquirido legalmente y con una finalidad definida.
- Evita servicios externos para voces, reuniones internas o grabaciones sensibles.
- Minimiza fragmentos y elimina copias de trabajo cuando termine el periodo autorizado.
- No uses voz, acento o sincronía labial para identificar personas sin una base legítima y evidencia independiente.
- Aísla ficheros no confiables y desactiva reproducción automática o elementos embebidos.
- Conserva originales, hashes, comandos, versiones, zona horaria y estimaciones de incertidumbre.
- Etiqueta toda salida corregida como derivada y nunca la presentes como el archivo recibido.
- Separa observación, modelo, explicación alternativa y nivel de confianza.

## Checklist reproducible

- [ ] Originales preservados y hashes registrados.
- [ ] Pistas de audio y vídeo identificadas sin asumir que las primeras son las relevantes.
- [ ] PTS, DTS, bases temporales e inicios exportados.
- [ ] Tres o más eventos compartidos medidos a lo largo del contenido.
- [ ] Incertidumbre anotada para cada evento.
- [ ] Desfase fijo, deriva y saltos evaluados como modelos distintos.
- [ ] Reproducción contrastada con una ruta independiente.
- [ ] Copias corregidas etiquetadas y separadas de los originales.
- [ ] Causa e intención no inferidas únicamente de la sincronía.

## Alternativas y siguientes pasos

`ffprobe` sirve para inspeccionar líneas temporales; `showwavespic` y `showspectrumpic` ayudan a visualizar audio; `adelay` permite ensayar un desfase fijo; `setpts`, `asetpts` y `aresample` permiten construir copias de prueba bajo supuestos explícitos. Editores como Audacity o herramientas de vídeo con lectura fotograma a fotograma pueden complementar el análisis, siempre que registres versión, ajustes y exportaciones.

El takeaway es sencillo: **mide varios eventos, modela por separado offset, deriva y salto, y trata cada corrección como una transformación declarada**. Si tus notas permiten reconstruir qué observaste antes de corregir nada, el análisis seguirá siendo útil incluso cuando la causa permanezca abierta.

Como ejercicio seguro, genera un vídeo sintético con un destello y un tono periódicos. Crea una copia con 200 ms de desfase fijo y otra con deriva gradual; mezcla los nombres y aplica el checklist sin mirar los comandos de creación. El siguiente paso natural será estudiar discontinuidades y concatenaciones de líneas temporales sin confundir un salto técnico con un corte editorial deliberado.

## Fuentes

- [`ffprobe`: documentación oficial](https://ffmpeg.org/ffprobe.html)
- [FFmpeg: documentación oficial de filtros](https://ffmpeg.org/ffmpeg-filters.html)
- [FFmpeg: documentación oficial del remuestreador](https://ffmpeg.org/ffmpeg-resampler.html)
- [FFmpeg: referencia de `AVPacket` y PTS](https://ffmpeg.org/doxygen/trunk/structAVPacket.html)
- [EBU R37-2007: temporización relativa de sonido e imagen](https://tech.ebu.ch/docs/r/r037.pdf)
- [Apple: el problema de temporización y sincronización en QuickTime](https://developer.apple.com/documentation/quicktime-file-format/the_timing_and_synchronization_problem)
