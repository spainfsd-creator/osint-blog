---
title: "Historia OSINT: MH17 (2014-2022) y el oficio de convertir pistas en prueba verificable"
slug: /historia-mh17-osint-cronologia-verificacion
authors: [osint-writter]
tags: [osint, investigation, history, verification, tradecraft, privacy]
date: 2026-02-15
image: /img/blog/2026-02-15-mh17-osint-cronologia-verificacion.png
---

![Ilustracion editorial sobre OSINT: cronologia, geolocalizacion y verificacion de evidencias (caso MH17)](/img/blog/2026-02-15-mh17-osint-cronologia-verificacion.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/historia-mh17-osint-cronologia-verificacion.m4a)


Hay investigaciones donde el reto no es encontrar una pieza, sino **demostrar que un conjunto de piezas encaja** sin forzar la historia. En el derribo del vuelo **MH17** (17 de julio de 2014), el mundo vio un alud de imagenes, declaraciones, trazas tecnicas, rumores y "evidencias" parciales. El trabajo OSINT responsable no consiste en ganar un debate en redes: consiste en **convertir informacion publica en una cronologia auditable**, con margenes de incertidumbre claros y con una disciplina feroz frente a los sesgos.

Este post no es un "caso para imitar" en lo tactico, ni un tutorial de atribucion ofensiva. Es una leccion de oficio: **como estructurar una investigacion abierta** para que sea verificable, reproducible y util para periodismo, analisis y documentacion.

<!-- truncate -->

## Que paso (resumen de contexto)

El 17 de julio de 2014, el vuelo MH17 de Malaysia Airlines se estrello en el este de Ucrania, causando la muerte de sus 298 ocupantes. Con el paso de los anos, el caso produjo informes tecnicos, investigaciones penales y un volumen enorme de material abierto (fotos, videos, comunicaciones, mapas, publicaciones en redes, etc.).

Para un analista OSINT, este tipo de casos son una escuela acelerada: te obligan a separar "lo posible" de "lo demostrable".

## Leccion 1: el problema real no es el dato, es la *trazabilidad*

En OSINT, la pregunta rara vez es "hay una foto". Es:

- Quien la subio primero (y cuando).
- En que condiciones se obtuvo.
- Si el archivo fue reescalado, recomprimido o reeditado.
- Si hay corroboracion independiente (otra camara, otro angulo, otro testigo, un registro tecnico).
- Si el hallazgo encaja en una cronologia que **no rompe** con otras evidencias.

Una practica simple que mejora todo: tratar cada pieza como **un item de evidencia** con ficha.

### Plantilla corta de ficha de evidencia (practica y segura)

Usa algo asi (en un cuaderno local, una hoja de calculo o un repo privado):

- ID: `EV-001`
- Tipo: foto / video / documento / registro / testimonio
- URL(s) de origen: (una o mas)
- Primera observacion: fecha/hora (con zona horaria)
- Copia local: hash del archivo (si procede)
- Hipotesis que soporta: una frase
- Corroboraciones: enlaces a EV-00x
- Riesgos/privacidad: que PII contiene (si la contiene)
- Estado: pendiente / verificado parcialmente / verificado / descartado

Esto no es burocracia: es lo que te permite rectificar sin romper el caso.

## Leccion 2: cronologia primero, conclusiones despues

La trampa mas comun en investigaciones publicas es la "cronologia inversa": empiezas por la conclusion y luego buscas piezas que la apoyen.

El antiveneno es construir una **linea temporal** con eventos y evidencias asociadas:

1. Define un reloj: UTC (o especifica siempre la zona).
2. Para cada evento: anota "que paso" y "con que evidencia".
3. Marca la incertidumbre: "entre X e Y" cuando no sea exacto.
4. Reevalua cuando aparezca nueva informacion.

En casos complejos, una buena cronologia suele ser mas valiosa que un hilo viral.

## Leccion 3: geolocalizacion es un metodo, no un truco

La geolocalizacion (cuando aplica) funciona por acumulacion:

- Elementos fijos: carreteras, lineas electricas, rios, edificios, relieve.
- Elementos variables: vegetacion estacional, obras, sombras (con cuidado), meteorologia.
- Corroboracion cruzada: imagen satelital, fotos de otros dias, mapas, metadatos, archivos web.

Regla de oro: si no puedes explicar por que un detalle es diagnostico (y no una coincidencia), todavia no tienes geolocalizacion: tienes una intuicion.

## Leccion 4: la verificacion es un pipeline (no una accion)

Cuando el volumen de material abierto es enorme, necesitas un flujo repetible. Uno razonable (para casos publicos, sin tocar nada intrusivo) es:

1. Ingesta: recopilar enlaces con etiquetas (tema, fecha, fuente).
2. Preservacion: capturas y copias con hashes cuando proceda.
3. Normalizacion: extraer texto, fotogramas clave, metadatos disponibles.
4. Analisis: cronologia, geolocalizacion, comparativas, grafos (si hace falta).
5. Corroboracion: buscar independencia de fuentes y consistencia temporal.
6. Redaccion: que afirmas, con que evidencia, y que NO sabes.

La clave es que el pipeline se pueda **auditar**: otro analista deberia poder llegar a lo mismo o explicar por que no.

## Caso de uso (ficticio): verificar un video antes de publicarlo

Imagina que recibes un video supuestamente grabado "hoy" que muestra un evento grave. En lugar de lanzarte a compartirlo:

- Verifica el origen: quien lo sube, historial, reuploads.
- Comprueba coherencia: clima, luz, idioma/acentos, rotulos, objetos.
- Busca corroboracion: otras grabaciones, fotos, comunicados oficiales, testigos independientes.
- Anota incertidumbre: "no confirmado" es un estado valido.

El objetivo es evitar dos danos: difundir desinformacion o exponer a personas innecesariamente.

## Limitaciones y falsos positivos (y como vivir con ellos)

- **Reuploads**: el "primer" enlace que encuentras rara vez es el primero real.
- **Manipulacion editorial**: recortes, subtitulos y montajes cambian el sentido.
- **Errores honestos**: testigos se equivocan con lugares y horas.
- **Atribucion apresurada**: que algo sea "probable" no lo hace "probado".

En OSINT serio, los estados intermedios importan: "probable", "posible", "sin evidencia suficiente".

## Buenas practicas (OPSEC, etica y privacidad)

- Minimiza PII: si no aporta a la verificacion, no la recolectes ni la publiques.
- Evita "cazar identidades": enfoca en hechos, no en personas, salvo necesidad legitima y alta confianza.
- Documenta tus dudas: las notas de incertidumbre son parte del resultado.
- Separa investigacion de activismo: el primero requiere controles de calidad, el segundo tiende a recortar esquinas.

## Herramientas que ayudan (sin convertirlas en el centro)

Segun el tipo de evidencia, suelen ser utiles:

- Gestores de notas y trazabilidad (cualquier sistema que permita IDs y enlaces cruzados).
- Herramientas de metadatos (para leer lo disponible, no para "forzar" conclusiones).
- Busqueda inversa y archivo web (para ver si algo ya existia).
- Mapas e imagen satelital (para corroborar contexto, con cautela).
- Visualizacion (grafos/timelines) cuando el caso lo exige.

Recuerda: la herramienta amplifica tu metodo. Si el metodo es malo, la herramienta solo lo hace mas rapido.

## Siguiente paso: un checklist minimo para tu proxima investigacion abierta

Si quieres practicar el "oficio" sin meterte en un caso sensible:

1. Elige un tema de interes publico y baja sensibilidad (por ejemplo, una nota de prensa corporativa con fotos).
2. Construye una cronologia de 5-10 eventos con evidencias citadas.
3. Haz una tabla de evidencias con estados (pendiente/verificado/descartado).
4. Publica un resumen que incluya incertidumbre y limites.

El objetivo no es impresionar: es **ser verificable**.

## Fuentes y lecturas (para profundizar, desde lo publico y verificable)

- Fiscalia neerlandesa (vision general y recursos del caso MH17): https://www.prosecutionservice.nl/topics/mh17-plane-crash
- Resumen del veredicto (17 de noviembre de 2022) en la web del tribunal del caso: https://www.courtmh17.com/en/news/2022/summary-of-the-day-in-court-17-november-2022---judgment.html
- Consejo Neerlandes de Seguridad (pagina sobre el accidente MH17, informes y material tecnico): https://www.onderzoeksraad.nl/en/page/3546/mh17-crash-17-juli-2014
- Archivo de investigaciones abiertas sobre MH17 (coleccion de articulos): https://www.bellingcat.com/tag/mh17/
