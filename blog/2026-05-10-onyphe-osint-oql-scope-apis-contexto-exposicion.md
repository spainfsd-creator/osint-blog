---
title: "ONYPHE en OSINT: OQL, scope APIs y contexto para mapear exposicion sin sobreatribuir"
slug: /onyphe-osint-oql-scope-apis-contexto-exposicion
authors: [osint-writter]
tags: [osint, tooling, data, methodology, investigation]
date: 2026-05-10
image: /img/blog/2026-05-10-onyphe-osint-oql-scope-apis-contexto-exposicion.png
---

![Ilustracion editorial de una analista OSINT cruzando datos de infraestructura, consultas OQL y contexto tecnico en una mesa de investigacion](/img/blog/2026-05-10-onyphe-osint-oql-scope-apis-contexto-exposicion.png)

Cuando una investigacion sobre infraestructura publica se vuelve ruidosa, el problema no suele ser la falta de banners, puertos o dominios. El problema serio es **confundir observacion tecnica con atribucion**, o mezclar datos recientes, historicos y on-demand como si contaran exactamente la misma historia. `ONYPHE` resulta util justo en ese borde: no como veredicto, sino como una forma de **buscar, filtrar y contextualizar exposicion publica con mas estructura que intuicion**.

Su documentacion oficial deja varias pistas que conviene tomarse en serio desde el principio. La `Search API` usa `OQL`, por defecto consulta `datascan` y, salvo que pidas historico, busca sobre los ultimos 30 dias. Ademas, la documentacion separa muy claramente busqueda general, `Summary`, `Alert`, `Export` y `Scope APIs` on-demand. Traducido a trabajo real: `ONYPHE` no es solo una caja de resultados, sino un ecosistema de vistas distintas sobre la misma pregunta tecnica.

<!-- truncate -->

## Que es y para que sirve

`ONYPHE` se presenta como un motor de busqueda y base de datos orientados a `Attack Surface Discovery`, `Attack Surface Management` y `Cyber Threat Intelligence`. En clave OSINT responsable, eso se convierte en varias utilidades concretas:

- buscar huella publica de dominios, `hostnames`, IPs, puertos y artefactos de servicios;
- usar `OQL` para reducir ruido con filtros reproducibles;
- separar barridos recientes de consultas historicas;
- lanzar consultas `scope` on-demand cuando la pregunta ya esta bien acotada;
- y recibir alertas sobre activos propios o legitimamente monitorizados.

La parte importante es metodologica. `ONYPHE` puede ayudarte a encontrar **donde mirar mejor**; no puede decidir por ti si un activo observado pertenece de verdad a una organizacion, si una exposicion sigue vigente o si un hallazgo tecnico es relevante para la hipotesis del caso.

## Caso de uso legitimo con ejemplo ficticio

Imagina una revision externa autorizada sobre la empresa ficticia `Puerto Boreal Energia`. El equipo tiene tres preguntas prudentes:

- que servicios visibles aparecen asociados a un dominio o ASN relacionado;
- que parte de esa exposicion parece reciente y que parte podria ser historica;
- y que activos merecen corroboracion con otras fuentes antes de escalar.

En un flujo sano, `ONYPHE` encaja asi:

1. arrancas con una consulta simple por dominio o `hostname`;
2. conviertes esa primera busqueda en una expresion `OQL` mas precisa;
3. revisas si los resultados pertenecen a `datascan`, `vulnscan` u otra categoria relevante;
4. y solo cuando la pregunta ya es especifica pasas a una `Scope API` on-demand para enriquecer un objetivo concreto.

Ese orden protege bastante de una trampa comun: ver una IP, un certificado o un banner y saltar demasiado pronto a una narrativa de propiedad, compromiso o relacion operativa.

## Flujo recomendado

### 1. Empezar por una consulta corta y observable

La guia de `Getting Started` explica que la `Search API` intenta detectar patrones comunes de forma automatica, como dominios, `hostnames` o puertos. Eso es util para una primera pasada, pero no deberia ser el final del trabajo. Empieza simple y anota exactamente que selector lanzaste.

### 2. Reescribir la pregunta en `OQL`

La documentacion de `ONYPHE Query Language` deja claro que `OQL` trabaja con categorias, filtros y funciones. Esa capa es la que vuelve reproducible una consulta y evita depender de una busqueda difusa de una sola vez.

En practica, conviene fijar:

- categoria de datos;
- selector principal;
- restricciones por protocolo, ASN, puerto o dominio;
- y si necesitas historico o solo una ventana reciente.

### 3. No mezclar reciente e historico sin decirlo

La `Search API` documenta que, si no pides historico, consulta por defecto los ultimos 30 dias. Ese detalle cambia bastante la interpretacion del resultado. Si ves algo en `ONYPHE`, la primera pregunta no deberia ser "es mio o no"; deberia ser "de que ventana temporal me esta hablando exactamente?".

### 4. Usar `Scope APIs` solo cuando el objetivo ya esta acotado

Las `Scope APIs v3` existen para preguntas mas concretas sobre IPs, puertos, dominios o `hostnames`. Son potentes precisamente porque ya no estas explorando a ciegas. Si todavia no sabes que activo quieres validar, probablemente todavia estas en fase de busqueda, no de `scope`.

### 5. Reservar `Export` y `Alert` para flujos maduros

La propia estructura de la documentacion muestra que `Search`, `Export` y `Alert` son piezas distintas. Eso ayuda a pensar mejor el caso:

- `Search` para explorar;
- `Summary` para resumir contexto;
- `Export` para volumen y tratamiento posterior;
- `Alert` para vigilancia legitima de activos que ya controlas o supervisas.

## Lo que hace diferente a ONYPHE

Muchas plataformas de infraestructura te devuelven resultados. `ONYPHE` destaca sobre todo por la separacion de capas:

- `OQL` como lenguaje comun;
- categorias distintas de dataset;
- APIs generales frente a APIs on-demand;
- documentacion especifica sobre historico y refresco de datos;
- y una `CLI` oficial para integrar el flujo fuera de la interfaz web.

Esa distincion importa mucho en OSINT serio. Obliga a dejar claro si estas viendo una observacion barrida, un enriquecimiento puntual, un dato historico o una consulta solicitada al momento. Sin esa disciplina, la investigacion de infraestructura se llena de falsas certezas muy rapido.

## Limitaciones y falsos positivos

`ONYPHE` aporta estructura, pero no elimina los riesgos clasicos del analisis tecnico abierto.

Limites habituales:

- un resultado puede describir observacion publica sin demostrar control operativo actual;
- el dataset reciente no equivale a foto instantanea del presente;
- el historico abre contexto, pero tambien puede arrastrar relaciones ya caducadas;
- una consulta demasiado amplia genera mucho ruido aunque la herramienta sea buena;
- y el limite documentado de resultados en `Search API` obliga a pensar mejor la estrategia cuando el universo crece.

La propia documentacion del `Search API` indica un maximo de `10,000` resultados recuperables y separa esa necesidad del `Export API`. Eso ya te da una leccion metodologica: cuando la pregunta se hace demasiado grande para una busqueda normal, el problema no es "pedir mas", sino refinar mejor el alcance.

## Buenas practicas de OPSEC, etica y privacidad

- Usa `ONYPHE` para activos propios, autorizados o de interes legitimo bien documentado.
- Conserva siempre la consulta exacta, fecha y ventana temporal usada.
- No trates una coincidencia de infraestructura como prueba suficiente de titularidad.
- Si pasas a `Alert` o `Scope APIs`, deja claro por que ese activo entra dentro del alcance.
- Cruza los hallazgos relevantes con `RDAP`, `CT logs`, historico web, DNS y notas humanas antes de concluir.

## Alternativas y siguientes pasos

Si la pregunta principal gira alrededor de servicios expuestos y lenguaje de consulta, `Netlas`, `Censys`, `Shodan` o `LeakIX` pueden complementar bien el flujo. Si necesitas mas cronologia de nombres y ownership, `SecurityTrails`, `CT logs` y `RDAP/WHOIS` suelen aportar mejor contexto. Y si el objetivo es vigilancia operativa de activos propios, conviene combinar busqueda puntual con alertado y un registro claro de cambios.

La takeaway practica es esta: **usa `ONYPHE` para formular consultas mejores, separar tiempo de observacion y priorizar corroboracion; no para convertir un indice tecnico en una atribucion cerrada antes de tiempo**.

## Fuentes

- [ONYPHE Documentation](https://search.onyphe.io/docs)
- [ONYPHE Getting Started](https://search.onyphe.io/docs/getting-started)
- [ONYPHE Search API](https://search.onyphe.io/docs/general-apis/search)
- [ONYPHE Query Language](https://search.onyphe.io/docs/onyphe-query-language)
- [ONYPHE Ondemand APIs](https://search.onyphe.io/docs/ondemand-apis)
- [ONYPHE Scope Port API](https://search.onyphe.io/docs/ondemand-apis/scope-port)
