---
title: "WhatsMyName en OSINT: usernames con criterio, cobertura y falsos positivos"
slug: /whatsmyname-osint-usernames-cobertura-falsos-positivos
authors: [osint-writter]
tags: [osint, tooling, socmint, verification, tradecraft, privacy]
date: 2026-03-18
image: /img/blog/2026-03-18-whatsmyname-osint-usernames-cobertura-falsos-positivos.png
---

![Ilustracion editorial de un analista OSINT contrastando reutilizacion de usernames en multiples plataformas publicas con marcadores de confianza y cuaderno de evidencias](/img/blog/2026-03-18-whatsmyname-osint-usernames-cobertura-falsos-positivos.png)

Cuando un alias aparece en varios sitios, la tentacion es saltar enseguida a la atribucion: mismo `username`, misma persona. Casi nunca es tan limpio. `WhatsMyName` sigue siendo valioso en 2026 precisamente porque empuja al analista a separar tres preguntas distintas: **donde existe un alias, con que calidad esta hecha la deteccion y que evidencia adicional hace falta para unir cuentas sin forzar la conclusion**.

Este contenido esta orientado a usos legitimos de periodismo, compliance, due diligence, investigacion academica y ciberinteligencia defensiva. No incluye tacticas para acoso, doxxing, intrusiones ni vigilancia abusiva.

<!-- truncate -->

## Que es y para que sirve

`WhatsMyName` no debe entenderse hoy como un "script magico" para encontrar a una persona. El propio repositorio oficial explica que en mayo de 2023 retiraron los checker scripts del proyecto y mantuvieron el nucleo realmente importante: `wmn-data.json`, el fichero de datos que describe como comprobar si un `username` existe en cientos de sitios.

Ese matiz importa mucho. La utilidad real de `WhatsMyName` no es prometer una atribucion automatica, sino ofrecer un corpus mantenido de detecciones para que otras herramientas o interfaces hagan comprobaciones repetibles. A fecha de esta publicacion, el fichero oficial incluye `731` sitios y categorias que van desde `social` o `coding` hasta `business`, `search`, `video` o `finance`.

La documentacion del proyecto tambien pone limites claros a lo que puede cubrir:

- el sitio debe ser accesible sin autenticacion;
- el `username` tiene que aparecer en la URL publica del perfil;
- y la plataforma no puede reescribir ese identificador hacia un ID interno que rompa la comprobacion.

Si una plataforma no cumple esas reglas, `WhatsMyName` no la "fuerza". Ese es precisamente uno de sus puntos fuertes: reduce fantasias y obliga a trabajar con superficies realmente observables.

## Caso de uso legitimo con ejemplo ficticio

Imagina una empresa que va a contratar a un ponente externo para un evento tecnico. El equipo de riesgos solo necesita contestar algo muy concreto sobre el alias publico `analista_norte`:

- si el alias parece tener una trayectoria consistente en espacios profesionales o tematicos;
- si hay reutilizacion del mismo nombre en sitios que merezcan una revision manual;
- y si los hallazgos justifican abrir una fase dos de verificacion documental.

En ese escenario, `WhatsMyName` sirve como capa de cribado:

- genera una lista inicial de coincidencias plausibles;
- deja ver en que categorias de sitios aparece el alias;
- y ayuda a decidir donde merece la pena invertir tiempo humano.

Lo que no hace por si solo es demostrar identidad. Que un alias exista en varios perfiles no significa que todos pertenezcan a la misma persona. La union correcta sigue dependiendo de bio, cronologia, foto, lenguaje, enlaces cruzados, contexto laboral y otras senales corroborables.

## Flujo recomendado

Un flujo prudente con `WhatsMyName` suele funcionar mejor si se parece mas a una auditoria de hipotesis que a una caza masiva:

1. Normaliza el alias exacto y anota variantes obvias antes de buscar.
2. Lanza una comprobacion inicial para ver presencia por categorias, no para cerrar identidad.
3. Separa resultados de alto valor de resultados triviales o ruidosos.
4. Revisa manualmente solo las coincidencias que aportan contexto verificable.
5. Documenta por que una cuenta suma, resta o queda en incertidumbre.

La propia arquitectura del proyecto favorece este enfoque. `WhatsMyName` alimenta varias implementaciones distintas, incluida la web `whatsmyname.app`, integraciones en `SpiderFoot`, transformadas de `Maltego` y clientes externos. Eso quiere decir que el valor esta menos en la interfaz concreta y mas en la calidad de las reglas de deteccion y en como las interpreta el analista.

## Limitaciones y falsos positivos

El principal riesgo con `WhatsMyName` no es tecnico, sino interpretativo. Un resultado positivo solo indica que un sitio devuelve senales compatibles con la existencia de ese `username`. No prueba titularidad comun ni relevancia analitica.

Los falsos positivos mas habituales suelen venir de aqui:

- aliases muy genericos o reciclados;
- perfiles vacios o semiautomaticos que no anclan identidad real;
- sitios que cambian su respuesta HTTP o su HTML y dejan vieja una regla;
- y plataformas con protecciones intermedias donde el checker ve menos de lo que el analista cree.

El archivo de datos ya contempla parte de ese problema. La contribucion oficial pide comparar una cuenta existente con otra inexistente, revisar codigos HTTP, escoger cadenas estables del HTML y marcar protecciones cuando proceda. En el dataset actual aparecen protecciones como `cloudflare`, `cloudfront`, `ddos-guard`, `anubis` o requisitos de `user-agent`, lo que recuerda que la cobertura nunca es uniforme.

Tambien hay una limitacion metodologica que conviene repetir: `WhatsMyName` trabaja bien con perfiles publicos cuyo `username` vive en la URL. Si la plataforma depende de login, IDs opacos o rutas dinamicas, hay que cambiar de enfoque y no exigirle lo que no esta disenado para resolver.

## Buenas practicas de OPSEC, etica y privacidad

- Empieza por una base legal o un interes legitimo claro antes de investigar personas.
- Trata cada coincidencia como una pista, no como una atribucion.
- Conserva capturas, URLs y notas de revision para poder explicar por que aceptaste o descartaste un resultado.
- Evita ampliar la busqueda a espacios irrelevantes o sensibles si no aportan valor real al caso.
- Si una conclusion puede afectar a terceros, exige corroboracion independiente antes de actuar.

Otra buena practica menos comentada: revisa el propio estado del proyecto antes de convertirlo en pieza central del flujo. Los metadatos publicos del repo oficial muestran actividad reciente, con `updated_at` el `17 de marzo de 2026` y `pushed_at` el `28 de enero de 2026`. Eso no sustituye la validacion de campo, pero si indica que no estas trabajando sobre un listado fosilizado.

## Alternativas y siguientes pasos

Si `WhatsMyName` se queda corto, la solucion no siempre es buscar una herramienta "mas agresiva". A menudo conviene cambiar de capa:

- `Sherlock` o `Maigret`, si necesitas otra logica de comprobacion y mas contexto por perfil;
- revision manual del perfil publico, si la atribucion depende de detalles cualitativos;
- y cruce con otras fuentes abiertas del caso, si el alias por si solo no basta.

La takeaway practica es sencilla: `WhatsMyName` funciona mejor como **mapa de cobertura y control de calidad** que como maquina de identificacion. Si te ayuda a decidir donde mirar, donde desconfiar y donde hace falta corroborar, ya esta haciendo el trabajo importante.

Siguiente tema sugerido para continuar la serie: `Toutatis`, pero con el mismo filtro metodologico de siempre: menos fetichismo de la extraccion y mas control de contexto, OPSEC y limites reales.

## Fuentes consultadas

- Repositorio oficial: https://github.com/WebBreacher/WhatsMyName
- README oficial del proyecto: https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/README.md
- Guia oficial de contribucion y formato del dataset: https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/CONTRIBUTING.md
- Dataset oficial `wmn-data.json`: https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json
- JSON de ejemplo para validar reglas: https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/sample.json
- Metadatos publicos del repositorio en GitHub API: https://api.github.com/repos/WebBreacher/WhatsMyName
