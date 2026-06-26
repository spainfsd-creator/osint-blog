---
title: "NASA FIRMS en OSINT: anomalías térmicas, incendios y contexto antes de atribuir causas"
slug: /nasa-firms-osint-anomalias-termicas-contexto
authors: [osint-writter]
tags: [osint, geoint, verification, data, methodology, investigation]
date: 2026-06-26
image: /img/blog/2026-06-26-nasa-firms-osint-anomalias-termicas-contexto.png
---

![Ilustración editorial de una analista OSINT revisando un mapa satelital con anomalías térmicas, línea temporal y notas de verificación](/img/blog/2026-06-26-nasa-firms-osint-anomalias-termicas-contexto.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/nasa-firms-osint-anomalias-termicas-contexto.m4a)


Una columna de humo aparece en redes, una cuenta local habla de una explosión y un mapa satelital muestra varios puntos rojos cerca de la zona. El salto tentador es convertir esos puntos en una causa: ataque, sabotaje, incendio industrial, accidente. El salto correcto es más lento: **una anomalía térmica indica calor observado por un sensor, no explica por sí sola qué ocurrió ni quién lo provocó**.

`NASA FIRMS` es útil precisamente cuando se usa con esa disciplina. Revisando la documentación oficial el **26 de junio de 2026**, FIRMS distribuye datos de incendios activos y anomalías térmicas en tiempo casi real a partir de observaciones `MODIS` y `VIIRS`, con visualización en mapas, alertas, descargas y servicios web. Para OSINT responsable, su valor no está en señalar culpables, sino en ayudar a construir una cronología verificable y a decidir qué evidencia falta.

Este artículo está pensado para verificación, periodismo, análisis humanitario, gestión de crisis y contexto defensivo. No sirve para acosar personas, dirigir acciones sobre objetivos ni presentar una lectura técnica como prueba cerrada sin corroboración.

<!-- truncate -->

## Qué es NASA FIRMS y para qué sirve

[`FIRMS`](https://firms.modaps.eosdis.nasa.gov/) significa `Fire Information for Resource Management System`. Es un sistema de NASA/LANCE orientado a distribuir datos de incendios activos y anomalías térmicas observadas desde satélites. La página oficial resume el núcleo operativo: datos `NRT` de `MODIS` a bordo de los satélites `Aqua` y `Terra`, y de `VIIRS` a bordo de `S-NPP`, `NOAA-20` y `NOAA-21`.

La diferencia práctica para un analista es sencilla:

- `MODIS` ofrece continuidad histórica y una lectura amplia del fenómeno;
- `VIIRS` aporta detecciones con mejor detalle espacial para muchos usos operativos;
- el mapa permite explorar puntos, capas y ventanas temporales;
- las descargas (`SHP`, `KML`, `TXT`) y los servicios web facilitan reproducir el análisis;
- las alertas sirven para monitorizar un área cuando hay interés legítimo y proporcional.

NASA indica que los datos globales están disponibles normalmente dentro de unas `3` horas desde la observación satelital, mientras que para Estados Unidos y Canadá algunas detecciones se ofrecen en tiempo real. Esa frase debe leerse con cuidado: "casi en tiempo real" no significa "instantáneo", "completo" ni "sin incertidumbre".

## Caso de uso legítimo con ejemplo ficticio

Imagina que una ONG ambiental investiga un incendio en una planta de reciclaje ficticia cerca de `Puerto Claro`. Hay tres piezas abiertas:

| Evidencia inicial | Qué aporta | Qué no demuestra |
| --- | --- | --- |
| Vídeos locales con humo | Existencia visual de un evento y posible dirección de la columna | Causa, hora exacta o foco inicial |
| Detecciones en FIRMS | Señales térmicas con coordenadas, hora de observación, sensor y confianza | Que el punto sea el origen del incendio o que haya una acción deliberada |
| Comunicados oficiales | Cronología declarada y respuesta institucional | Independencia, precisión completa o ausencia de omisiones |

El equipo no empieza preguntando "quién lo hizo". Empieza con preguntas observables:

1. ¿Qué detecciones aparecen en un radio razonable alrededor de la planta?
2. ¿Qué sensor las observó y a qué hora UTC?
3. ¿La señal aparece antes, durante o después de los primeros vídeos públicos?
4. ¿Hay fuentes alternativas que corroboren humo, actividad de bomberos, cortes de carretera o imágenes satelitales posteriores?
5. ¿El punto cae sobre la planta, sobre vegetación cercana, sobre una chimenea, sobre una zona industrial caliente o sobre otro elemento plausible?

Ese flujo evita dos errores habituales: convertir el mapa en sentencia y tratar una publicación viral como reloj fiable.

## Flujo recomendado

### 1. Define área, ventana y pregunta

Antes de abrir el mapa, escribe la hipótesis mínima: "verificar si hubo actividad térmica compatible con un incendio cerca de `X` entre `T1` y `T2`". Si la pregunta es demasiado grande, FIRMS devuelve ruido; si es demasiado estrecha, puedes descartar señales útiles por una geolocalización inicial imprecisa.

Trabaja siempre con hora `UTC` y conserva la zona horaria local por separado. Muchas confusiones nacen de mezclar hora de publicación, hora local del testigo, hora de adquisición satelital y hora de descarga del dato.

### 2. Consulta el mapa y descarga los datos

El [`FIRMS Fire Map`](https://firms.modaps.eosdis.nasa.gov/map/) es suficiente para una primera lectura visual, pero una investigación revisable necesita exportar datos o documentar la consulta. La [`API de FIRMS`](https://firms.modaps.eosdis.nasa.gov/api/) expone servicios por área, país, disponibilidad de datos, huellas `KML` y configuración de `MAP_KEY`.

Para una nota de caso, conserva como mínimo:

- URL o parámetros de consulta;
- fecha y hora de descarga;
- sensor (`MODIS`, `VIIRS` u otro producto disponible);
- coordenadas;
- hora de observación;
- valor de confianza o clasificación que muestre el producto;
- captura o exportación usada en el análisis;
- explicación de por qué el área de búsqueda es proporcional.

### 3. Separa observación, inferencia y conclusión

Una buena tabla de análisis distingue tres capas:

| Capa | Ejemplo prudente | Ejemplo problemático |
| --- | --- | --- |
| Observación | "VIIRS muestra una anomalía térmica cerca de la zona a las 19:24 UTC" | "VIIRS prueba que explotó la planta" |
| Inferencia | "La señal es compatible con calor intenso en la ventana analizada" | "La señal confirma un ataque" |
| Conclusión | "Debe corroborarse con vídeo, respuesta local e imagen posterior" | "Caso cerrado" |

La palabra clave es **compatible**. En OSINT serio, muchas piezas son compatibles con una hipótesis sin demostrarla por completo.

### 4. Corrobora con fuentes independientes

FIRMS encaja bien con:

- imágenes satelitales ópticas posteriores para evaluar cambio visible;
- `Sentinel Hub EO Browser`, `NASA Worldview` o servicios equivalentes para contexto visual;
- vídeos y fotografías geolocalizadas;
- comunicados de bomberos, protección civil o autoridades locales;
- sensores de calidad del aire, si la pregunta es ambiental;
- tráfico marítimo, aéreo o terrestre cuando el evento afecta logística;
- archivo web y medios locales para reconstruir la cronología pública.

La guía de [Bellingcat sobre NASA FIRMS en zonas de guerra](https://www.bellingcat.com/resources/2022/10/04/scorched-earth-using-nasa-fire-data-to-monitor-war-zones/) es útil como recordatorio metodológico: las firmas térmicas pueden aportar pistas en contextos complejos, pero deben tratarse con cautela porque no toda fuente de calor tiene el mismo significado.

## Limitaciones y falsos positivos

El error más peligroso es olvidar que FIRMS detecta **anomalías térmicas**. Un hotspot puede corresponder a un incendio forestal, una quema agrícola, una antorcha industrial, actividad volcánica, un incendio urbano, una explosión, calor persistente de una instalación o un artefacto de observación. Sin contexto, el punto es una pista.

Hay límites técnicos y metodológicos que conviene escribir en el informe:

- **Resolución espacial**: la coordenada no siempre equivale al foco exacto del evento; representa una detección asociada a un píxel o producto.
- **Revisita temporal**: el satélite observa cuando pasa; puede perder eventos breves o ver solo una fase.
- **Nubes, humo y ángulo de observación**: las condiciones atmosféricas y geométricas afectan la lectura.
- **Saturación y brillo**: una señal intensa no ordena por sí sola causas ni daños.
- **Confianza**: los campos de confianza ayudan a priorizar, pero no sustituyen la corroboración.
- **Cambios de producto**: compara sensores y versiones con cuidado, especialmente si mezclas histórico y tiempo casi real.

La propia [FAQ de NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms/faq) explica conceptos como `FRP` (`Fire Radiative Power`) y recuerda que factores como resolución del sensor, temperatura de saturación, ángulo de visión y hora de observación influyen en la interpretación. Es material que merece leerse antes de convertir una captura de mapa en afirmación fuerte.

## Buenas prácticas de OPSEC, ética y privacidad

FIRMS suele tratar fenómenos físicos, pero las investigaciones alrededor de incendios, ataques o accidentes pueden afectar a personas concretas. La ética no desaparece porque la fuente sea satelital.

Aplica estas reglas:

- no publiques coordenadas sensibles si pueden exponer víctimas, equipos de emergencia o infraestructuras críticas;
- no atribuyas intención a partir de calor observado;
- no mezcles rumores de redes con datos satelitales como si tuvieran el mismo peso;
- conserva capturas, exportaciones y notas de consulta para que otra persona pueda revisar el razonamiento;
- minimiza datos personales en vídeos, testimonios y capturas;
- marca incertidumbre de forma explícita: "compatible con", "no descarta", "no permite concluir".

El estándar sano es que una persona externa pueda reconstruir por qué miraste esa zona, qué viste, qué descartaste y qué queda sin probar.

## Alternativas y siguientes pasos

FIRMS no vive solo. Según la pregunta, puede tener más sentido empezar por otra capa:

- `NASA Worldview`, si necesitas revisar imagen satelital contextual y no solo puntos de calor;
- `Sentinel Hub EO Browser`, si buscas comparativas visuales antes/después con sensores concretos;
- sistemas nacionales o regionales de incendios, si la prioridad es respuesta local;
- `EFFIS`, para contexto europeo de incendios forestales;
- `GDELT` o medios locales, si el objetivo es rastrear narrativa pública;
- `Datasette` o `SQLite`, si quieres conservar una cronología consultable de detecciones, fuentes y decisiones.

El siguiente paso práctico es crear una plantilla de caso con cuatro bloques: `consulta FIRMS`, `corroboración visual`, `cronología pública` y `conclusiones con incertidumbre`. Si una anomalía térmica no puede pasar por esos cuatro filtros, probablemente todavía no es una conclusión: es una pista que merece más trabajo.

## Fuentes consultadas

- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- [NASA Earthdata: FIRMS](https://www.earthdata.nasa.gov/data/tools/firms)
- [NASA Earthdata: FIRMS FAQ](https://www.earthdata.nasa.gov/data/tools/firms/faq)
- [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/)
- [Bellingcat: Scorched Earth, Using NASA Fire Data to Monitor War Zones](https://www.bellingcat.com/resources/2022/10/04/scorched-earth-using-nasa-fire-data-to-monitor-war-zones/)
