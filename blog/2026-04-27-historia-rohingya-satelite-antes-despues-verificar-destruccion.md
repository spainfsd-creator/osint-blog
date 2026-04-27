---
title: "Historia OSINT: Rohingya, satelite antes/despues y el metodo para verificar destruccion a distancia"
slug: /historia-rohingya-satelite-antes-despues-verificar-destruccion
authors: [osint-writter]
tags: [osint, geoint, verification, investigation, methodology]
date: 2026-04-27
image: /img/blog/2026-04-27-historia-rohingya-satelite-antes-despues-verificar-destruccion.png
---

![Ilustracion editorial de una analista OSINT comparando imagenes satelitales antes y despues para verificar la destruccion de aldeas Rohingya con metodologia responsable](/img/blog/2026-04-27-historia-rohingya-satelite-antes-despues-verificar-destruccion.png)

Hay historias en las que el dato mas importante no aparece en un tuit, ni en un video viral, ni en una rueda de prensa. Aparece cuando alternas dos imagenes tomadas desde cientos de kilometros de altura y descubres que donde antes habia casas, arboles, caminos y parcelas, despues solo queda una cicatriz gris y negra.

La crisis Rohingya de 2017 es una de esas lecciones duras. Cuando el acceso al terreno era limitado, las negaciones oficiales competian con testimonios de huida masiva y aldeas arrasadas. El trabajo OSINT util no consistia en ganar una discusion en internet. Consistia en **verificar destruccion de forma reproducible, acotar fechas, cruzar fuentes y documentar que parte del relato estaba sostenida por evidencia abierta**.

<!-- truncate -->

## Contexto minimo: humo, huida y una pregunta dificil

El `25 de agosto de 2017`, la violencia en el norte del estado de Rakhine se disparo tras ataques de `ARSA` contra puestos de seguridad y la posterior respuesta militar. Segun `UNHCR`, mas de `750.000` Rohingya huyeron a Bangladesh a partir de aquella ofensiva, sumandose a desplazamientos previos y creando una de las mayores crisis de refugio de la region.

En ese contexto, una parte central del problema era epistemica. Habia testimonios directos, fotos, videos, versiones oficiales contradictorias y enormes restricciones de acceso. La pregunta OSINT no era "quien tiene la historia mas impactante", sino otra mucho mas sobria:

- que aldeas muestran destruccion visible;
- en que ventana temporal puede detectarse;
- si el patron es aislado o sistematico;
- y que grado de confianza permite unir satelite, testimonios y material audiovisual.

`Human Rights Watch`, `Amnesty International` y mecanismos de la `ONU` fueron empujando esa respuesta capa a capa. Lo importante para un analista no es memorizar cada informe, sino entender el metodo comun que aparece detras.

## El metodo OSINT: cuando el acceso fisico falla, la comparativa temporal manda

### 1. Empezar por una comparacion antes/despues, no por una conclusion

La imagen satelital no sustituye al terreno, pero obliga a ordenar la conversacion. `Human Rights Watch` publico el `19 de septiembre de 2017` un analisis que hablaba de `214` aldeas casi totalmente destruidas y de mas del `90 %` de las estructuras afectadas en cada una de ellas. Ese tipo de comparativa vale porque baja la ambiguedad: ya no discutes impresiones sueltas, discutes cambios visibles entre una fecha y otra.

La disciplina clave aqui es sencilla de formular y facil de olvidar:

- fijar un "antes" util;
- fijar un "despues" util;
- comprobar nubosidad, resolucion y cobertura;
- y describir el cambio observado antes de interpretar su causa o su autoria.

Parece elemental, pero evita uno de los errores mas comunes en `GEOINT`: enamorarte de una imagen impactante sin contexto temporal suficiente.

### 2. Acotar ventanas de deteccion, no fingir una precision que no tienes

La hoja de imagenes satelitales publicada por `OHCHR` para la Mision Internacional Independiente sobre Myanmar explica muy bien este limite. Su mapa de danos en el norte de Rakhine se basa en imagenes recogidas entre el `25 de agosto de 2017` y el `18 de marzo de 2018`, y deja claro que la fecha asociada es una **ventana de deteccion del dano**, no necesariamente el instante exacto en que ocurrio.

Esa precision honesta es una gran leccion metodologica. En OSINT serio, "no se exactamente en que minuto ocurrio" no es una debilidad vergonzosa. Es un limite documentado. Y un limite documentado siempre vale mas que una exactitud inventada.

### 3. Cruzar patron espacial con testimonios y videos

El satelite por si solo muestra cambio fisico. Para interpretar mejor ese cambio necesitas otras capas. `Amnesty International` publico el `22 de septiembre de 2017` nuevas evidencias en video y satelite que, segun su analisis, mostraban incendios activos semanas despues de que las autoridades afirmaran que las operaciones habian terminado el `5 de septiembre`. `Human Rights Watch` fue en la misma linea un mes despues: al menos `66` aldeas habrian ardido despues de esa fecha oficial.

Aqui aparece un patron muy util para cualquier investigacion:

- el satelite detecta destruccion o humo;
- los testimonios describen secuencia, huida y contexto humano;
- los videos ayudan a fijar continuidad o actividad en fechas concretas;
- y la comparacion entre zonas quemadas e intactas reduce la idea de que todo puede explicarse por azar, clima o error de lectura.

En varias aldeas mixtas, `Human Rights Watch` describio ademas un detalle especialmente importante: zonas Rohingya arrasadas junto a areas Rakhine cercanas que permanecian intactas. Ese contraste espacial no cierra por si solo una atribucion penal, pero si refuerza la lectura de un patron selectivo y no meramente accidental.

### 4. Pasar del hallazgo visual al patron sistematico

Una sola aldea destruida puede tener multiples explicaciones y exige mucha prudencia. Decenas o cientos de casos comparables ya plantean otra cosa: un patron. En octubre de 2017, `Human Rights Watch` elevo su recuento a `288` aldeas parcial o totalmente destruidas desde el `25 de agosto`. El valor OSINT no estaba solo en el numero, sino en demostrar que el dano no era anecdota ni rumor repetido, sino una huella espacial repetida en numerosos puntos del mapa.

Ese salto de "caso llamativo" a "patron verificable" es uno de los mayores aportes del OSINT cuando el acceso sobre el terreno es incompleto. No reemplaza una investigacion judicial, pero ayuda a fijar donde mirar, que negar resulta menos sostenible y que narrativas empiezan a quedarse sin base.

## El giro: a veces la prueba mas fuerte no es un frame heroico, sino la persistencia del vacio

En historias de guerra o limpieza etnica, internet suele imaginar que la pieza decisiva sera el video perfecto. En el caso Rohingya, una parte enorme de la fuerza probatoria vino de algo menos cinematografico y mas demoledor: **el vacio repetido en el tiempo**.

Casas que ya no estan. Vegetacion quemada. Trazas de aldeas visibles en mayo y ausentes o arrasadas en septiembre. Nuevas alteraciones del terreno meses despues. La historia se vuelve incontestable no porque una sola imagen lo diga todo, sino porque muchas observaciones independientes empiezan a decir lo mismo.

Es una leccion que conviene recordar. En OSINT, la evidencia fuerte a menudo no grita. Acumula.

## Evidencia y limites: que se podia afirmar y que no

Con fuentes abiertas de calidad se podia sostener bastante:

- que existia destruccion visible a gran escala en numerosas aldeas;
- que esa destruccion podia observarse mediante comparativas satelitales antes/despues;
- que algunos incendios o danos seguian detectandose despues de fechas oficiales presentadas como fin de operaciones;
- y que el patron espacial era consistente con testimonios y otros materiales reunidos por organizaciones independientes.

Pero seguian existiendo limites importantes:

- una imagen satelital no identifica por si sola a cada autor material;
- la teledeteccion puede mostrar dano, humo o alteracion del terreno, pero no siempre establece mecanismo exacto sin apoyo adicional;
- la ausencia de acceso seguro al terreno deja huecos inevitables;
- y la atribucion juridica final requiere mucho mas que una buena lectura geoespacial.

El valor del metodo esta justo ahi: **decir con claridad donde termina el hecho observable y donde empieza la inferencia**.

## Toolkit metodologico que deja esta historia

- `Google Earth` y visores satelitales para fijar ubicaciones y cambios basicos.
- Comparativas temporales con control de fecha, nubosidad y resolucion.
- Archivo disciplinado de capturas, URLs y fecha de consulta.
- Cruce con informes de `HRW`, `Amnesty`, `OHCHR` y `UNHCR` para no leer una imagen en vacio.
- Videos y fotografias de contexto solo cuando aporten continuidad temporal o espacial real.
- Una libreta metodologica donde separemos observacion, hipotesis e interpretacion.

## Takeaways para cualquier investigacion de destruccion remota

- Si no puedes entrar al terreno, compensa con mas disciplina temporal y espacial.
- Un "antes/despues" bien elegido suele aportar mas que diez imagenes impactantes sin contexto.
- Las ventanas de deteccion importan: no inventes una fecha exacta si tus fuentes no la permiten.
- El patron espacial puede ser tan relevante como el evento individual.
- El satelite rara vez cierra un caso solo; su fuerza real aparece al cruzarlo con otras capas abiertas.
- La prudencia metodologica no enfria la historia: la vuelve util para terceros.

## Fuentes recomendadas

- `UNHCR`, *Rohingya emergency* (consulta actualizada en 2026): https://www.unhcr.org/emergencies/rohingya-emergency
- `Human Rights Watch`, *Burma: Satellite Imagery Shows Mass Destruction* (`19 de septiembre de 2017`): https://www.hrw.org/news/2017/09/19/burma-satellite-imagery-shows-mass-destruction
- `Human Rights Watch`, *Burma: New Satellite Images Confirm Mass Destruction* (`17 de octubre de 2017`): https://www.hrw.org/news/2017/10/17/burma-new-satellite-images-confirm-mass-destruction
- `Amnesty International`, *Myanmar: Video and satellite evidence shows new fires still torching Rohingya villages* (`22 de septiembre de 2017`): https://www.amnesty.org/en/latest/news/2017/09/myanmar-video-and-satellite-evidence-shows-new-fires-still-torching-rohingya-villages/
- `OHCHR`, *Imagery of Rakhine State* (anexo de la Fact-Finding Mission): https://www.ohchr.org/sites/default/files/Documents/HRBodies/HRCouncil/FFM-Myanmar/ImageryofRakhineState.pdf

Takeaway final: la historia Rohingya ensena que el OSINT no siempre ilumina un hecho con una gran revelacion puntual. A veces hace algo mas importante: convierte un paisaje negado en un patron verificable. Si quieres seguir por esta linea, el siguiente puente natural seria un post practico sobre `Sentinel Hub EO Browser` para aprender a montar comparativas temporales sin vender mas certeza de la que realmente tienes.
