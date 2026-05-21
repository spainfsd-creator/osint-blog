---
title: "Favicon hashing en OSINT: clusters visuales, infraestructura parecida y contexto antes de atribuir"
slug: /favicon-hashing-osint-clusters-similares-contexto
authors: [osint-writter]
tags: [osint, tooling, search, methodology, verification, infrastructure]
date: 2026-05-21
image: /img/blog/2026-05-21-favicon-hashing-osint-clusters-similares-contexto.png
---

![Ilustracion editorial de una analista OSINT agrupando sitios publicos por similitud de favicon mientras cruza grafo de infraestructura, pestanas del navegador y notas metodologicas](/img/blog/2026-05-21-favicon-hashing-osint-clusters-similares-contexto.png)

Cuando una investigacion pasa de "este panel me suena" a "quiero saber si hay mas activos publicos que se parecen", el instinto suele tirar de titulos HTML, textos visibles o capturas de pantalla. El problema es que esas capas cambian deprisa, se personalizan y a veces estan hechas precisamente para distraer. El `favicon hashing` resulta util porque baja un escalon: **convierte un icono pequeno y aparentemente banal en un selector tecnico repetible para buscar parecidos sin depender solo de la vista**.

Eso no significa que un favicon compartido demuestre propiedad comun, ni que cada coincidencia esconda una operacion coordinada. Significa algo mas sobrio y mas practico: que puedes **agrupar, priorizar y pedir corroboracion** con menos intuicion y mas trazabilidad. En OSINT responsable, esa diferencia importa.

<!-- truncate -->

## Que es y para que sirve

`Favicon hashing` consiste en calcular un hash del icono que una web publica expone normalmente en `/favicon.ico` y usar ese valor como pivote de busqueda. La idea es sencilla: si varios activos publicos sirven el mismo icono o uno muy parecido, puede haber una relacion operativa util que merezca revision.

La utilidad real no esta en el hash aislado, sino en el tipo de preguntas que habilita:

- encontrar paneles clonados o instancias desplegadas con la misma plantilla visual;
- agrupar activos de una misma organizacion que comparten stack o proveedor;
- detectar software expuesto con iconos muy caracteristicos;
- separar coincidencias prometedoras de parecidos puramente cosmeticos.

La documentacion oficial de `ProjectDiscovery` lo refleja de forma muy directa: `httpx` expone un modo `-favicon` para extraer el hash `mmh3` del `favicon.ico` y mostrarlo junto a cada URL. Y la documentacion de `Censys` deja claro que sus datasets web indexan hashes de favicon (`hash_md5` y `hash_sha256`) precisamente para encontrar activos que reutilizan ese mismo recurso visual.

## Caso de uso legitimo: due diligence tecnica sobre un proveedor

Escenario ficticio: una empresa va a integrar un proveedor SaaS pequeno. El equipo de riesgo ya conoce el dominio principal, pero quiere responder una pregunta muy terrenal antes de firmar nada: **que otros paneles, entornos o subdominios publicos parecen desplegados con la misma huella visual y merecen una segunda mirada**.

Un flujo responsable seria:

1. Partir de un dominio ya autorizado o publicamente relevante.
2. Obtener el hash del favicon con una herramienta local como `httpx -favicon`.
3. Buscar ese valor en indices externos que ya modelan favicons como propiedad consultable.
4. Tratar los resultados como candidatos, no como conclusiones.
5. Corroborar con hostname, certificado, tecnologias visibles, ASN, historico DNS o contexto organizativo.

El objetivo no es "descubrir mas por descubrir". Es reducir el tiempo que tardas en pasar de una pista aislada a un **cluster defendible** de activos parecidos.

## Flujo recomendado: del icono al cluster sin vender certezas

### 1. Calcula el selector con una herramienta que deje trazabilidad

La documentacion de `httpx` muestra el uso de `-favicon` para extraer el hash `mmh3` del `favicon.ico` de un conjunto de objetivos. Es una forma razonable de empezar porque:

- deja el selector por escrito;
- permite repetir el proceso sobre el mismo alcance;
- evita depender de una captura manual o de "me parecia el mismo icono".

Practicamente, lo importante no es memorizar una receta, sino conservar tres datos: URL observada, fecha de observacion y hash obtenido.

### 2. Busca en un indice que entienda favicons como campo

En `Censys`, el dataset web documenta campos concretos para favicons, incluido su tamano y hashes `MD5` y `SHA256`. En la guia de lenguaje de consulta, esos campos aparecen como `web.endpoints.http.favicons.hash_sha256` y equivalentes relacionados. Esa combinacion te permite preguntar al indice por activos que comparten exactamente el mismo recurso.

En `Shodan`, la documentacion de `property hashes` explica la logica de buscar por hashes numericos para recuperar banners o propiedades identicas sin depender de cadenas demasiado genericas. Aunque esa pagina se centra en `hash` y `http.html_hash`, metodologicamente encaja con la misma disciplina: cuando una propiedad es repetible, conviene buscar por esa propiedad y no por una intuicion textual.

### 3. Agrupa, pero no atribuyas todavia

Un cluster de favicons puede significar muchas cosas:

- la misma empresa despliega varias instancias del mismo producto;
- un tercero gestiona portales para varios clientes y reutiliza branding minimo;
- un panel por defecto mantiene el icono del fabricante;
- alguien clono una interfaz publica con fines legitimos o ilegitimos.

Por eso el hash sirve muy bien para **priorizar revision**, pero muy mal para cerrar una historia por si solo.

### 4. Cruza con senales menos fragiles

Antes de escribir una conclusion, cruza al menos algunas de estas capas:

- titulo HTML o `body` visible;
- certificado y nombres observables;
- ASN, hosting o rangos relacionados;
- stack tecnologico aparente;
- historial DNS o capturas web;
- contexto mercantil u organizativo si procede.

Aqui `Censys` aporta una pista metodologica util: su propia documentacion de `software confidence` explica que coincidencias exactas en campos estructurados, como hashes de favicon o de cuerpo HTTP, pueden elevar la confianza de identificacion, pero no eliminan por si solas el riesgo de falsos positivos. La lectura correcta es clara: **un hash fuerte mejora una hipotesis; no sustituye la corroboracion**.

## Limitaciones y falsos positivos

`Favicon hashing` brilla cuando quieres pasar de un activo conocido a una familia de activos parecidos. Falla cuando olvidas lo comun que es reutilizar iconos.

Los falsos positivos mas habituales son:

- productos muy extendidos con favicon por defecto;
- plantillas corporativas o portales de proveedores compartidos;
- CDNs o paneles multi-tenant que sirven el mismo recurso a muchos clientes;
- cambios de icono entre versiones, entornos o rutas;
- diferencias entre el icono descargado localmente y el que un indice externo proceso en otro momento.

Tambien hay un limite temporal importante. Los indices no observan internet toda al mismo tiempo ni con la misma frescura. Igual que `Shodan` documenta ventanas de actualizacion distintas para varias fuentes y `Censys` explica que su modelado depende del recurso efectivamente observado, un hash debe leerse siempre con fecha y contexto.

## Buenas practicas de OPSEC, etica y privacidad

- Trabaja sobre dominios, marcas o activos con finalidad legitima y documentable.
- Conserva selector, fecha, fuente y razon del pivot para que otro analista pueda revisar el proceso.
- Minimiza datos personales: el hallazgo principal aqui es tecnico, no identitario.
- No conviertas una similitud visual en acusacion publica.
- Si el hallazgo afecta a un tercero legitimo, escala primero por canal responsable y con evidencia reproducible.

La propia documentacion de `httpx` incluye una advertencia simple y correcta: "Use with caution. You are responsible for your actions." Es una buena regla editorial tambien para OSINT.

## Alternativas y siguientes pasos

Si `favicon hashing` se te queda corto, el siguiente escalon natural no es "forzar mas la conclusion", sino enriquecer el cluster con otras huellas:

- hash del cuerpo HTTP cuando el HTML es mas estable que el icono;
- certificados TLS y `CT logs` si el valor esta en nombres e historico;
- tecnologias detectadas, `headers` o rutas visibles;
- memoria web (`Common Crawl`, `Wayback Machine`, archivo propio) para saber desde cuando existe el parecido.

La idea operativa es buena y modesta a la vez: usa el favicon para **encontrar familia**, y usa el resto de fuentes para **entender parentesco**.

## Cierre

`Favicon hashing` no es una bala de plata ni una prueba de propiedad. Es una forma disciplinada de transformar un detalle visual pequeno en un pivote tecnico util. Bien usado, te ayuda a ver clusters donde antes solo habia intuicion. Mal usado, te empuja a sobreinterpretar plantillas compartidas.

La takeaway accionable es sencilla: si ya tienes un activo web relevante y necesitas ampliar contexto sin salir disparado hacia la atribucion, empieza por una huella repetible como el favicon, documenta el selector y obliga a cada coincidencia a convivir con mas evidencia antes de escribir la historia.

Fuentes:

- [Shodan Help Center: Pivoting with Property Hashes](https://help.shodan.io/mastery/property-hashes)
- [Censys Docs: Platform Web Property Dataset](https://docs.censys.com/docs/platform-web-property-dataset)
- [Censys Docs: Query Language](https://docs.censys.com/docs/censys-query-language)
- [ProjectDiscovery Docs: httpx usage](https://docs.projectdiscovery.io/opensource/httpx/usage)
- [ProjectDiscovery Docs: Running httpx (`-favicon`)](https://docs.projectdiscovery.io/opensource/httpx/running)
- [PyPI: mmh3](https://pypi.org/project/mmh3/)
