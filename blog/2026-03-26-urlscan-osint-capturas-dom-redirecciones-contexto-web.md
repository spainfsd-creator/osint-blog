---
title: "urlscan.io en OSINT: capturas, DOM y redirecciones para investigar webs con contexto"
slug: /urlscan-osint-capturas-dom-redirecciones-contexto-web
authors: [osint-writter]
tags: [osint, tools, tradecraft, verification, infrastructure, recon]
date: 2026-03-26
image: /img/blog/2026-03-26-urlscan-osint-capturas-dom-redirecciones-contexto-web.png
---

![Ilustracion editorial de un analista OSINT investigando una web con urlscan.io, cadena de redirecciones, artefactos DOM y evidencias visuales](/img/blog/2026-03-26-urlscan-osint-capturas-dom-redirecciones-contexto-web.png)

**Descargar el podcast!**: <a href="/podcasts/urlscan-osint-capturas-dom-redirecciones-contexto-web.m4a">Descargar el podcast</a>


Cuando una URL sospechosa aparece en un correo, en una alerta o en una conversacion interna, el problema rara vez es solo "abrirla". El problema real es **entender que hizo, con quien hablo, a donde redirigio y que artefactos dejo** sin convertir el analisis en una improvisacion peligrosa. `urlscan.io` destaca precisamente ahi: te deja observar una pagina como si un navegador la visitara y te devuelve contexto util para investigar con mas rigor.

Este contenido esta orientado a defensa, respuesta a incidentes, periodismo, due diligence y verificacion responsable. No incluye tacticas de intrusiones, acoso ni operativa ofensiva.

<!-- truncate -->

## Que es y para que sirve

La documentacion oficial define `urlscan.io` como un servicio gratuito para escanear y analizar sitios web. Cuando se envia una URL, un proceso automatizado navega hacia ella como un usuario normal y registra la actividad que esa navegacion genera: dominios e IPs contactados, recursos cargados y datos adicionales sobre la propia pagina. Ademas, el servicio puede guardar captura de pantalla, contenido DOM, variables globales de JavaScript y cookies observadas durante la carga.

Eso lo convierte en una pieza muy practica para OSINT web y triage defensivo, porque permite responder preguntas como estas:

- que URL final se cargo realmente tras las redirecciones;
- que infraestructura o terceros participaron en la carga;
- si la pagina mostraba una marca, un login o un formulario concreto;
- que recursos, hashes o ficheros descargados quedaron asociados al escaneo;
- y si existe historial publico parecido para ese dominio, esa IP o esa ruta.

No es una "bola de cristal" ni un veredicto magico. Es una capa de observacion de la navegacion web que gana valor cuando separas bien evidencia, contexto e inferencia.

## Caso de uso legitimo con ejemplo ficticio

Imagina que el equipo de seguridad de la empresa ficticia `Norte Atlas Logistics` recibe un aviso sobre la URL `https://portal-norteatlas-secure.example/login`. Nadie quiere abrirla directamente en un equipo corporativo y tampoco basta con mirar el dominio a ojo.

Con `urlscan.io`, el analista puede perseguir un objetivo mas prudente:

- ver si la URL redirige a otra distinta;
- capturar la apariencia general de la pagina;
- revisar que dominios secundarios y ficheros se solicitaron;
- y comprobar si ese dominio o patrones parecidos ya aparecieron en escaneos historicos.

El resultado ideal no es una conclusion precipitada del tipo "esto es phishing seguro", sino una libreta mejor estructurada:

- la URL inicial;
- la URL final;
- la marca o senales visuales observadas;
- la cadena de infraestructura;
- y las hipotesis que merecen corroboracion con otras fuentes.

## Flujo recomendado

### 1. Decide primero la visibilidad correcta

Este paso importa mucho mas de lo que parece. La documentacion de `urlscan.io` insiste en que los escaneos tienen tres niveles de visibilidad:

- `Public`: visible en portada, resultados publicos e info pages;
- `Unlisted`: no aparece en la busqueda publica, pero si para investigadores y empresas de seguridad validadas en `urlscan Pro`;
- `Private`: solo visible para ti o para quien tenga el ID del escaneo.

La propia guia de buenas practicas recomienda retirar `PII` de las URLs o enviarlas como `Unlisted` cuando puedan contener datos sensibles. En trabajo real, ese consejo evita un error muy comun: publicar sin querer tokens, correos, rutas internas o identificadores de victimas.

### 2. Usa el escaneo para observar, no para sentenciar

La fuerza de `urlscan.io` esta en el conjunto de artefactos. Segun la guia rapida oficial, tras enviar una URL puedes recuperar:

- el resultado JSON;
- la captura PNG;
- y el `DOM snapshot` del escaneo.

Eso te da tres planos complementarios:

- visual: que vio el navegador;
- estructural: que habia en el DOM;
- y tecnico: que recursos, IPs, ASN, cabeceras o hashes quedaron registrados.

En una investigacion defensiva, este triple enfoque es mas util que una sola captura aislada, porque te deja cruzar narrativa y evidencia tecnica.

### 3. Lee la cadena de redirecciones con calma

La referencia oficial del `Search API` deja claro que puedes buscar por campos como `task.url`, `page.url`, `page.redirected`, `page.domain`, `page.ip`, `page.server` o `page.tlsIssuer`. Para el analista, eso significa que no estas limitado a "buscar una web"; puedes preguntar por comportamientos y atributos de la carga final.

En el ejemplo ficticio, si la URL original apunta a un subdominio aparentemente corporativo pero la pagina final aterriza en otro dominio, con otro `ASN` y otro emisor TLS, ya tienes una historia tecnica que merece atencion. Aun asi, la historia correcta no es "culpable sin mas", sino "hay una discrepancia observable entre origen aparente y destino final".

### 4. Separa dataset de escaneos y dataset de hostnames

Aqui hay una trampa frecuente. La documentacion de las fuentes de datos dice expresamente que el dataset de `Website Scans` sirve para encontrar escaneos historicos de un dominio, IP, URL u otros atributos, pero **no** es el dataset correcto para descubrir hostnames nuevos. Para ese caso, `urlscan.io` remite a su dataset de `Hostnames`.

Esa distincion mejora mucho el metodo:

- si buscas "que se escaneo sobre este dominio o URL", usa `Website Scans`;
- si buscas "que hostnames historicos se han observado alrededor de este dominio", usa `Hostnames`.

La referencia del `Hostname API` anade ademas que el dataset combina varias fuentes, entre ellas `Certificate Transparency`, `Passive DNS`, `Website Scans`, `Zonefiles`, sujetos de certificados TLS y enlaces encontrados en paginas escaneadas. Es decir, `urlscan.io` no solo te sirve para una pagina concreta, sino tambien para abrir pivotes historicos bien delimitados.

### 5. Trata la fotografia temporal como eso: una fotografia

El FAQ oficial es muy claro: `urlscan.io` ofrece capturas puntuales del contenido de un sitio y no re-crawlea automaticamente escaneos ya existentes para decidir si la amenaza sigue activa. Tambien recuerda que el veredicto `malicious` no deberia usarse como senal de bloqueo desatendida porque puede haber falsos positivos.

Traducido a OSINT responsable:

- una captura valida lo que se vio en ese momento, no para siempre;
- una clasificacion automatica es una pista util, no una sentencia;
- y todo hallazgo serio necesita contexto adicional.

## Limitaciones y falsos positivos

### Un escaneo no reemplaza la corroboracion

El propio servicio explica que usa `Google Chrome` en modo `headless` y anota despues el resultado con fuentes adicionales. Eso es potentisimo, pero sigue siendo una observacion mediada por una plataforma concreta, con sus tiempos, geografia, configuracion y restricciones.

### La retencion y la disponibilidad no son eternas

El FAQ advierte que no garantizan retencion para escaneos publicos y recomienda descargar los resultados si los necesitas. Si tu investigacion depende de un artefacto concreto, guardarlo con su contexto y fecha forma parte del trabajo analitico, no un detalle logistico menor.

### El campo correcto importa

La referencia de busqueda ofrece decenas de campos. Usarlos mal suele producir ruido. Mezclar `task.url` con `page.url`, o interpretar cualquier `page.redirected` como prueba de mala fe, genera errores metodologicos mas rapido de lo que parece.

## Buenas practicas de OPSEC, etica y privacidad

- no subas como `Public` una URL que lleve identificadores personales, tokens o rutas sensibles;
- documenta que es observable en la captura, que es observable en el DOM y que es inferencia tuya;
- descarga y conserva artefactos clave si el caso va a requerir revision posterior;
- usa el veredicto automatizado como ayuda para priorizar, no como sustituto del analista;
- y si el caso afecta a terceros legitimos, valora si `Unlisted` o `Private` es mas apropiado que `Public`.

## Alternativas y siguientes pasos

Si trabajas mucho con la plataforma, la documentacion oficial del `urlscan-cli` destaca tres ventajas practicas: soporte amplio de API, envios en bloque e iteracion automatica de busquedas grandes. Para equipos que ya operan en terminal o que quieren integrarlo con `jq`, es un paso natural.

Tambien conviene combinar `urlscan.io` con otras capas:

- reputacion y contexto DNS;
- historico de certificados;
- archivo web;
- sandboxing adicional si el caso lo exige;
- y notas internas que separen evidencia de interpretacion.

El takeaway accionable es sencillo: usa `urlscan.io` para convertir una URL dudosa en una observacion mas completa, pero no confundas una buena observacion con una conclusion cerrada. Si la herramienta te da captura, DOM, redirecciones y contexto de busqueda, tu trabajo es ordenar esas piezas sin vender mas certeza de la que realmente existe.

Como siguiente tema natural del blog, el puente logico seria profundizar en `VirusTotal` o en `GreyNoise` desde una perspectiva metodologica: como cruzar contexto de infraestructura sin caer en automatismos.

## Fuentes oficiales

- urlscan.io, About: https://docs.urlscan.io/about
- urlscan.io, Quickstart Guide: https://docs.urlscan.io/guides/quickstart
- urlscan.io, Website Scans Search Reference: https://docs.urlscan.io/pages/search-api-reference
- urlscan.io, Website Scans: https://docs.urlscan.io/pages/source-scans
- urlscan.io, Hostname API: https://docs.urlscan.io/pages/hostname-search
- urlscan.io, Scan Visibility Levels: https://docs.urlscan.io/pages/visibility
- urlscan.io, FAQ: https://urlscan.io/docs/faq/
- urlscan.io, API Use Best Practices: https://docs.urlscan.io/pages/api-best-practices
- urlscan.io, CLI - Introduction: https://docs.urlscan.io/pages/cli-intro
