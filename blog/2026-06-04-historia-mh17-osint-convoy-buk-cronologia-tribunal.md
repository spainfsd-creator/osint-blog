---
title: "Historia OSINT: MH17, el convoy Buk y la cronologia abierta que acabo en un tribunal"
slug: /historia-mh17-osint-convoy-buk-cronologia-tribunal
authors: [osint-writter]
tags: [osint, history, geoint, verification, investigation, methodology]
date: 2026-06-04
image: /img/blog/2026-06-04-historia-mh17-osint-convoy-buk-cronologia-tribunal.png
---

![Ilustracion editorial de una investigacion OSINT sobre MH17 con mapa de ruta, fotos geolocalizadas de un convoy Buk, notas cronologicas y analistas cruzando evidencias publicas](/img/blog/2026-06-04-historia-mh17-osint-convoy-buk-cronologia-tribunal.png)

Hay historias OSINT que parecen imposibles precisamente porque son demasiado grandes. Un avion comercial cae, mueren `298` personas, el espacio informativo se llena de versiones enfrentadas y cada bando intenta usar la niebla del conflicto como si fuera una coartada. En un caso asi, el peligro no es solo no saber suficiente. El peligro real es **dejar que el volumen de ruido haga pasar por inevitable la confusion**.

El caso `MH17` importa porque ensena lo contrario. No fue una sola foto, ni un solo mapa, ni un solo analista con una intuicion brillante. Fue una cadena de trabajo bastante mas sobria: recoger material publico, fijar lugares, ordenar horas, comparar detalles tecnicos, cruzar testimonios, revisar satelite y obligar a que cada pieza conviviera con las demas. Lo interesante para el oficio no es el dramatismo del caso. Es comprobar como una cronologia abierta, bien trabajada, puede reducir el espacio de negacion hasta volverse util incluso en sede judicial.

<!-- truncate -->

## Contexto minimo: un desastre, muchas versiones y una pregunta central

El `17 de julio de 2014`, el vuelo `MH17` de `Malaysia Airlines`, que cubria la ruta entre Amsterdam y Kuala Lumpur, fue derribado sobre el este de Ucrania. El saldo fue total: `283` pasajeros y `15` tripulantes muertos. Desde el principio, la escena publica quedo contaminada por dos problemas clasicos de investigacion en guerra:

- abundancia de material parcial;
- propagacion de narrativas incompatibles;
- y un incentivo politico evidente para sembrar duda sobre origen, autoria y contexto.

En este tipo de entorno, OSINT no sirve para "ganar una discusion en internet". Sirve para responder preguntas mas secas y mas dificiles:

- que se vio exactamente y donde;
- en que secuencia aparecieron ciertos activos;
- que partes de la cronologia pueden comprobarse con datos publicos;
- y que hipotesis dejan de sostenerse cuando todas esas capas se miran juntas.

El `Joint Investigation Team` (`JIT`) presento sus primeros resultados el `28 de septiembre de 2016`. Ahi ya afirmaba que el vuelo fue alcanzado por un misil `Buk` lanzado desde un campo cerca de `Pervomaiskyi`, en una zona entonces controlada por separatistas. El `17 de noviembre de 2022`, el tribunal de La Haya condeno a `Kharchenko`, `Dubinskiy` y `Girkin` a cadena perpetua y absolvio a `Pulatov`. Y el `8 de febrero de 2023`, el `JIT` publico un informe adicional sobre la cadena de mando y explico que habia indicios fuertes sobre el suministro del sistema `Buk`, aunque no evidencia bastante para nuevas acusaciones individuales en ese momento.

Eso ya marca una leccion importante: **OSINT no sustituyo la investigacion penal, pero ayudo a fijar una columna vertebral publica que luego pudo contrastarse, tensionarse y reutilizarse**.

## El metodo OSINT: cuando la cronologia obliga a que todo encaje

Lo mas didactico del caso `MH17` no es el titular final. Es el flujo de trabajo.

### 1. No empezar por "quien fue", sino por "que ruta puede demostrarse"

Buena parte de la investigacion abierta se concentro primero en un objeto concreto: un lanzador `Buk-TELAR` visto en imagenes y videos compartidos publicamente el mismo `17 de julio de 2014`. La pregunta util no era "de quien era" en abstracto. La pregunta correcta era mas humilde: **puedo demostrar que el mismo sistema aparece en distintos puntos, en una secuencia temporal coherente y con marcas identificables**.

Segun el dossier de `Bellingcat` de `8 de octubre de 2015`, tras el derribo aparecieron fotos y videos que supuestamente mostraban el movimiento del `Buk` por territorio controlado por separatistas. El trabajo no consistio en aceptar esas publicaciones por fe. Consistio en geolocalizarlas una por una, fijar su orden aproximado y compararlas con otros detalles visibles del vehiculo y del entorno.

### 2. Convertir fotos sueltas en un recorrido verificable

Ese paso cambia el juego. Una foto aislada puede discutirse durante horas. Una cadena de fotos geolocalizadas en `Donetsk`, `Zuhres`, `Torez` y `Snizhne`, con referencias visibles y ventanas horarias aproximadas, empieza a comportarse como una ruta.

El valor metodologico no esta en la estetica del hallazgo, sino en su disciplina:

- comprobar donde se tomo cada imagen;
- revisar sombras, orientacion y contexto urbano;
- buscar coincidencias del mismo remolque o del mismo vehiculo;
- y descartar material que no aguanta la comprobacion.

`Bellingcat` describio precisamente ese enfoque: localizar con precision donde se habia grabado cada imagen y usar ese conjunto para reconstruir el desplazamiento del `Buk` durante el `17 de julio de 2014`. Tambien explico que el mismo analisis se apoyo en material compartido por civiles a lo largo de la ruta del convoy en Rusia unas semanas antes, lo que permitio enlazar visualmente el sistema con un origen mas concreto.

### 3. Tratar las huellas visuales como identificadores tecnicos

Uno de los detalles mas potentes del caso fue metodologicamente pequeno: **no bastaba con decir "es un Buk"**. Habia que preguntarse si era ese mismo `Buk`.

La investigacion abierta comparo marcas parciales, pintura, desperfectos y rasgos de las faldillas laterales del vehiculo. Ese nivel de lectura importa mucho en OSINT serio. El analista responsable no trabaja con categorias generales si puede trabajar con rasgos distintivos. La pregunta deja de ser "se parece" y pasa a ser "cuantos elementos independientes apuntan al mismo objeto".

Segun `Bellingcat`, la revision de imagenes en Ucrania y Rusia llevo a vincular el lanzador visto el `17 de julio` con un `Buk` fotografiado en Rusia a finales de junio, apodado `3x2`. La conclusion no descansaba en una sola mancha de pintura, sino en una suma de rasgos visibles y en el hecho de que otras comparaciones no encajaban igual de bien.

### 4. Corroborar la posible zona de lanzamiento con capas distintas

El siguiente error que conviene evitar en cualquier caso OSINT es pensar que una ruta basta. No basta. Hace falta otra capa.

En `MH17`, la zona de lanzamiento propuesta cerca de `Pervomaiskyi` se fue apoyando en varios tipos de material:

- foto del rastro de humo;
- geolocalizacion de ese material;
- imagenes satelitales;
- marcas observables sobre el terreno;
- conversaciones interceptadas incorporadas por la investigacion oficial;
- y testimonios o publicaciones locales sobre el lanzamiento.

El tribunal de La Haya resumio despues un punto clave: no basaba su certeza en un unico tipo de evidencia, sino en un conjunto que incluia fotos del rastro, imagenes satelitales, llamadas interceptadas, datos de telefonia, fotos y videos del `Buk-TELAR` y examen forense de fragmentos hallados en cuerpos y restos del avion. Esa acumulacion disciplinada es exactamente el tipo de convergencia que un analista deberia buscar antes de subir el tono de una conclusion.

## El giro: cuando internet deja de ser escaparate y se convierte en archivo de movimientos

Hay una version simplista del caso `MH17` que dice: "las redes sociales resolvieron el misterio". Es una mala lectura. Las redes, por si solas, no resuelven nada. Lo que resuelve es el metodo aplicado sobre material publico.

El giro real del caso fue otro: **internet dejo de ser solo el lugar donde circulaba el ruido y paso a ser tambien el lugar donde quedaban rastros involuntarios del movimiento de un sistema concreto**. Fotos casuales, videos de paso, referencias urbanas, comentarios locales y material satelital no formaban una narrativa cerrada por separado. Pero juntos reducian mucho el espacio para escenarios alternativos.

Por eso el caso sigue siendo tan didactico. Ensena que la fuerza del OSINT no siempre esta en descubrir una pieza secreta, sino en obligar a que cientos de piezas publicas dejen de comportarse como anecdotas sueltas.

## Evidencia y limites: que puede afirmarse con solidez y que no

Con fuentes publicas e institucionales, hay varias afirmaciones fuertes que hoy se sostienen bien:

- el `17 de julio de 2014` el vuelo `MH17` fue derribado en el este de Ucrania y murieron `298` personas;
- el `JIT` comunico el `28 de septiembre de 2016` que el misil `Buk` se habia lanzado desde un campo cerca de `Pervomaiskyi`;
- el tribunal de La Haya establecio el `17 de noviembre de 2022` que `MH17` fue alcanzado por un misil `Buk` disparado desde esa zona y condeno a tres acusados a cadena perpetua;
- el `JIT` mantuvo la investigacion abierta hasta publicar su informe adicional el `8 de febrero de 2023`, con indicios fuertes sobre la cadena de suministro del sistema pero sin base suficiente para nuevas imputaciones individuales.

Tambien conviene mantener limites claros:

- OSINT no reemplaza por si solo la cadena completa de custodia penal.
- Una geolocalizacion fuerte no explica automaticamente toda la cadena de mando.
- Material compartido en redes necesita autenticacion y contraste, no entusiasmo.
- En conflictos armados siempre existe riesgo de manipular contexto, tiempos o procedencia.

El punto responsable no es vender invulnerabilidad metodologica. Es reconocer que un buen caso OSINT se vuelve valioso cuando diferentes capas independientes cuentan una historia compatible y, ademas, sobreviven al escrutinio judicial o institucional.

## Toolkit metodologico para aprender de MH17 sin romantizar el caso

Lo replicable de `MH17` no es el dramatismo del expediente. Es el oficio:

- construir una cronologia unica antes de discutir atribucion;
- trabajar con objetos identificables, no con categorias vagas;
- conservar enlaces, capturas, fechas y contexto de cada hallazgo;
- exigir corroboracion geografica y temporal a todo material visual;
- y separar siempre hecho, inferencia y hueco pendiente.

Herramientas y practicas que este caso vuelve especialmente valiosas:

- geolocalizacion sobre mapas y referencia urbana;
- analisis de sombras y secuencia temporal;
- archivo sistematico de publicaciones y multimedia;
- tablas de comparacion para rasgos tecnicos de vehiculos u objetos;
- satelite comercial o historico para confirmar cambios sobre el terreno;
- y notas de investigacion que expliquen por que una pieza entra o sale del caso.

## Takeaways

- En una guerra informativa, la cronologia es una forma de higiene intelectual.
- Una foto no vale por lo que impresiona, sino por lo que puede ubicarse y compararse.
- El OSINT mas util suele ser el que convierte material disperso en una secuencia refutable.
- Las conclusiones fuertes aparecen cuando varias capas independientes convergen.
- El objetivo no es sonar seguro antes de tiempo, sino dejar cada afirmacion mejor atada que el ruido que la rodea.

Como puente natural para el siguiente tema del blog, tendria sentido bajar de esta historia a una tecnica concreta de trabajo: **como geolocalizar y cronolocalizar material visual sin forzar coincidencias**.

## Fuentes y lecturas recomendadas

- `Public Prosecution Service`, "JIT presentation of first results of the MH17 criminal investigation", `28 de septiembre de 2016`: https://www.prosecutionservice.nl/topics/m/mh17-plane-crash/criminal-investigation-jit-mh17/jit-presentation-first-results-mh17-criminal-investigation-28-9-2016
- `Rechtspraak`, "Levenslange gevangenisstraffen..." sobre el veredicto de `MH17`, `17 de noviembre de 2022`: https://www.rechtspraak.nl/organisatie-en-contact/organisatie/rechtbanken/rechtbank-den-haag/nieuws/mh17
- `Public Prosecution Service`, "Report MH17", `8 de febrero de 2023`: https://www.prosecutionservice.nl/topics/mh17-plane-crash/documents/publications/mh17/map/2023/report-mh17
- `Public Prosecution Service`, "JIT MH17: strong indications that Russian president decided on supplying Buk", `8 de febrero de 2023`: https://www.prosecutionservice.nl/latest/news/2023/02/08/jit-mh17-strong-indications-that-russian-president-decided-on-supplying-buk
- `Eurojust`, "Eurojust support to joint investigation team MH17: three suspects sentenced to life imprisonment", `17 de noviembre de 2022`: https://www.eurojust.europa.eu/news/eurojust-support-joint-investigation-team-mh17-three-suspects-sentenced-life-imprisonment
- `Bellingcat`, "MH17 - The Open Source Evidence", `8 de octubre de 2015`: https://www.bellingcat.com/news/europe/2015/10/08/mh17-the-open-source-evidence/
