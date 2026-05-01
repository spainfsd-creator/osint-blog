---
title: "SunCalc en OSINT: sombras, cronolocalizacion y contexto antes de concluir"
slug: /suncalc-osint-sombras-cronolocalizacion-contexto
authors: [osint-writter]
tags: [osint, verification, tooling, geoint, methodology, investigation]
date: 2026-05-01
image: /img/blog/2026-05-01-suncalc-osint-sombras-cronolocalizacion-contexto.png
---

![Ilustracion editorial de una analista OSINT midiendo sombras y trayectorias solares sobre un mapa y una fotografia urbana para acotar lugar y hora](/img/blog/2026-05-01-suncalc-osint-sombras-cronolocalizacion-contexto.png)

Hay fotos y videos que parecen contar una historia completa hasta que miras la sombra. Un poste demasiado largo para esa hora. Una fachada iluminada desde un angulo raro. Un amanecer que no encaja con la orientacion de la calle. En esos casos, el dato mas util no siempre esta en un metadato ni en una declaracion: a veces esta en **como cae la luz**.

`SunCalc` es una de esas herramientas que no impresionan por apariencia, pero si por disciplina. Sirve para modelar la posicion del sol, la longitud de las sombras y las fases de luz para una fecha y un lugar concretos. En OSINT responsable, eso no significa "adivinar la hora exacta". Significa algo mas serio: **acotar escenarios plausibles y descartar los que no encajan**.

<!-- truncate -->

## Que es y para que sirve

La web `suncalc.org` se presenta de forma bastante directa: muestra el movimiento del sol y las fases de luz para un dia y un lugar determinados, incluyendo datos como amanecer, altitud, azimut y longitud de sombra. El proyecto original de `Vladimir Agafonkin` tambien tiene una libreria JavaScript publica cuyo README explica que calcula posicion solar y momentos de luz como amanecer, atardecer y crepusculos para una ubicacion y tiempo dados.

Traducido a lenguaje de analista, `SunCalc` sirve sobre todo para:

- comprobar si una hora declarada encaja con la direccion de la luz;
- estimar si una sombra es compatible con una latitud o una estacion concretas;
- comparar varios momentos plausibles de una misma escena;
- y documentar por que una afirmacion temporal o geografica parece coherente, incoherente o indeterminada.

No es un oraculo. Es una calculadora de contexto.

## Caso de uso legitimo: una foto viral con hora dudosa

Imagina una imagen difundida como "tomada hoy a las 08:15" en una ciudad concreta. En la foto hay una sombra nítida de farola, una fachada iluminada lateralmente y una calle cuyo eje puedes estimar con mapa. Antes de publicar o incorporar esa pieza a una investigacion, quieres saber si la luz encaja con lo que se afirma.

Eso es un uso muy razonable de `SunCalc`:

- no para identificar personas;
- no para perseguir a nadie;
- sino para verificar si la escena soporta la etiqueta temporal que la acompana.

## Flujo recomendado

### 1. Fijar orientacion y punto de observacion antes de tocar la hora

El mayor error al usar herramientas solares es empezar por la hora. Primero necesitas una hipotesis espacial decente:

- orientacion aproximada de la camara;
- direccion de la calle o del muro principal;
- y un punto geografico plausible o, al menos, una zona candidata.

Sin ese paso, cualquier calculo solar parece preciso pero flota en el aire. `SunCalc` mejora mucho cuando ya llegas con una geografia minimamente acotada.

### 2. Trabajar con azimut y altitud, no solo con intuicion visual

El README de la libreria `SunCalc` define dos variables clave para OSINT:

- `altitude`: la altura del sol sobre el horizonte;
- `azimuth`: la direccion del sol a lo largo del horizonte.

Esa pareja es lo importante. La longitud y orientacion de una sombra dependen de ahi. Si en la escena una sombra cae hacia cierto lado, pero el azimut solar esperado para la hora declarada apunta en otro sentido, ya tienes una incompatibilidad util. Si la sombra resulta demasiado corta o demasiado larga para la altitud solar prevista, la hora o incluso la fecha pueden necesitar revision.

### 3. Acotar ventanas plausibles, no vender un minuto exacto

La propia logica astronomica obliga a la prudencia. Herramientas como `SunCalc` o las ecuaciones solares publicadas por `NOAA` son utiles para modelar posicion del sol, pero la escena real introduce ruido:

- inclinacion del terreno;
- altura real del objeto que proyecta sombra;
- lente y perspectiva;
- pequenos errores al estimar la orientacion;
- y posibles oclusiones parciales por edificios o arbolado.

Por eso lo serio no suele ser decir "esto fue a las 08:13". Lo serio suele ser decir algo como:

- entre las `08:00` y las `08:30` la luz encaja razonablemente;
- antes de esa ventana, el azimut no cuadra;
- y a partir de cierto momento la sombra deberia ser claramente mas corta.

En OSINT, una buena ventana temporal suele valer mas que una falsa exactitud.

### 4. Cruzar calculo solar con detalles de escena

`SunCalc` no trabaja solo. Gana valor cuando lo cruzas con observables muy concretos:

- sombras de postes, farolas o personas;
- brillo relativo de fachadas opuestas;
- zonas de sombra proyectada por edificios altos;
- orientacion de tejados, carriles o mobiliario urbano;
- y condiciones meteorologicas coherentes con ese tipo de iluminacion.

La regla practica es sencilla: si varias senales visuales independientes cuentan la misma historia solar, tu confianza sube. Si unas dicen una cosa y otras otra, frena.

### 5. Documentar supuestos y margenes

Una buena nota metodologica con `SunCalc` deberia dejar por escrito:

- coordenadas o area candidata usadas;
- fecha y franja horaria probadas;
- orientacion estimada de la escena;
- objeto o sombra usados como referencia;
- y que parte es medicion frente a interpretacion.

Eso permite que otra persona repita el analisis y vea rapidamente donde podria estar el error.

## Limitaciones y falsos positivos

`SunCalc` es muy util, pero tambien muy facil de sobreactuar:

- una sombra puede no pertenecer al objeto que crees;
- una fotografia puede estar girada, recortada o espejada;
- la hora declarada puede venir de publicacion y no de captura;
- la perspectiva puede deformar percepciones de longitud;
- y una calle con edificios altos puede alterar la lectura intuitiva de la luz disponible.

Tambien hay un limite conceptual importante: compatibilidad no equivale a prueba unica. Que una escena sea solarmente posible no demuestra por si sola que la ubicacion o la fecha sean correctas. Solo elimina o conserva hipotesis.

## Buenas practicas de OPSEC, etica y privacidad

- Usa analisis solar para verificar contexto, no para facilitar acoso o localizacion invasiva de personas.
- Evita publicar coordenadas exactas si el caso no las necesita.
- Separa siempre hecho observable de inferencia: "la luz es compatible" no es lo mismo que "la escena ocurrio ahi".
- Si una conclusion depende de una sola sombra dudosa, no escales.
- Guarda captura de parametros y resultados para poder auditar tu propio analisis despues.

## Alternativas y siguientes pasos

La propia web `suncalc.org` es suficiente para muchas comprobaciones rapidas. La libreria original tambien puede integrarse en flujos propios si necesitas automatizar comparaciones. Y si quieres una segunda opinion matematica, las ecuaciones solares publicadas por `NOAA` son una buena referencia para entender de donde sale este tipo de calculo.

Un flujo muy razonable seria:

- geolocalizar o acotar la escena con mapa;
- usar `SunCalc` para probar varias horas plausibles;
- contrastar con sombras visibles y orientacion;
- y cerrar con una conclusion graduada: compatible, incompatible o no concluyente.

## Fuentes recomendadas

- `SunCalc.org`, web oficial con altitud, azimut y longitud de sombra: https://www.suncalc.org/
- `mourner/suncalc`, README oficial del proyecto: https://github.com/mourner/suncalc/blob/master/README.md
- `NOAA`, ecuaciones generales de posicion solar: https://gml.noaa.gov/grad/solcalc/solareqns.PDF

Takeaway final: `SunCalc` no sirve para adivinar. Sirve para disciplinar. Convierte una intuicion sobre la luz en una hipotesis verificable, repetible y discutible. Si quieres seguir por esta linea, el siguiente puente natural seria un post practico sobre `Overpass Turbo` para pasar de una geolocalizacion probable a una lista controlada de objetos y referencias sobre el mapa.
