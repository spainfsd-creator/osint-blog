---
title: "Censys y SecurityTrails en OSINT: cartografiar infraestructura, DNS e historial sin perder el contexto"
slug: /censys-securitytrails-osint-infraestructura-dns-historial
authors: [osint-writter]
tags: [osint, tooling, dns, infrastructure, verification, recon]
date: 2026-03-15
image: /img/blog/2026-03-15-censys-securitytrails-osint-infraestructura-dns-historial.png
---

![Ilustracion editorial de un analista OSINT correlacionando infraestructura expuesta, certificados TLS e historial DNS en paneles tipo grafo](/img/blog/2026-03-15-censys-securitytrails-osint-infraestructura-dns-historial.png)

Cuando una investigacion defensiva ya conoce un dominio o una IP, el siguiente cuello de botella no suele ser "encontrar mas ruido", sino **entender como se relacionan activos, nombres, certificados y cambios en el tiempo**. Ahi es donde Censys y SecurityTrails destacan: no como sustitutos del criterio analitico, sino como dos capas complementarias para ver infraestructura publica con mas contexto y menos intuicion improvisada.

Este contenido esta orientado a usos legitimos de ciberinteligencia defensiva, due diligence tecnica, respuesta a incidentes, periodismo y verificacion. No incluye tacticas para intrusiones, doxxing, stalking ni vigilancia abusiva.

<!-- truncate -->

## Que son y para que sirven

`Censys` trabaja sobre un mapa de Internet construido a partir de escaneos continuos y organiza los datos en hosts, web properties y certificados. Eso lo hace especialmente util cuando necesitas responder preguntas como:

- que servicios expone un activo de cara a Internet;
- que certificados, puertos o banners ayudan a pivotar;
- y que ha cambiado en una ventana temporal relevante.

`SecurityTrails`, por su parte, se centra en enriquecimiento DNS, WHOIS y relaciones de dominio. Su valor practico suele aparecer cuando el analista necesita:

- listar subdominios asociados a un hostname;
- revisar historial DNS por tipo de registro;
- encontrar dominios relacionados o contexto SSL para una atribucion prudente.

La combinacion funciona bien porque cada plataforma ilumina una parte distinta del problema:

- Censys te ayuda a observar infraestructura y servicios visibles;
- SecurityTrails te ayuda a reconstruir contexto de nombres, resoluciones e historial;
- y el analista une ambas capas con fuentes propias o autorizadas antes de concluir nada.

## Caso de uso legitimo

Imagina una empresa con varias filiales y marcas secundarias que prepara una auditoria externa tras un incidente menor de exposicion accidental. El equipo ya tiene un dominio principal, dos netblocks autorizados y varios nombres historicos de proyectos.

El objetivo legitimo no es "mapear media Internet", sino responder a tres preguntas operativas:

1. que activos publicos parecen realmente vinculados a la organizacion;
2. que subdominios o certificados sugieren servicios heredados, pruebas o despliegues olvidados;
3. que cambios recientes merecen validacion interna antes de elevar una alerta.

En ese escenario, Censys sirve para observar servicios, certificados y relacion entre activos; SecurityTrails sirve para revisar subdominios, historial DNS y dominios asociados; y la conclusion final solo se da por buena cuando encaja con inventario interno, tickets de cambio o responsables tecnicos.

## Flujo recomendado

### 1. Empieza por un alcance concreto

Antes de abrir ninguna plataforma, deja por escrito que dominios, ASN, IPs o marcas estan dentro del analisis. Sin alcance, una investigacion de infraestructura se vuelve rapidamente un catalogo de curiosidades.

Checklist minima:

- dominio principal y secundarios autorizados;
- netblocks o ASN conocidos;
- marcas, CN/SAN de certificados y nombres historicos;
- hipotesis concreta a validar.

### 2. Usa Censys para ver activos y puntos de pivote

La query language de Censys permite combinar busquedas full-text con pares campo-valor sobre hosts, web properties y certificados. En la practica, eso facilita una primera pasada para localizar:

- hosts que resuelven o presentan un nombre concreto;
- certificados que contienen una marca o subdominio;
- servicios visibles en puertos no estandar que merecen contraste.

Ejemplos defensivos con datos ficticios:

```text
"empresa-ejemplo.es"
host.ip="198.51.100.24"
cert.names: "vpn.empresa-ejemplo.es"
web.endpoints.http.response.headers.server: "nginx"
```

La regla sana es no saltar del hallazgo a la conclusion. Un certificado visto por Censys puede ser historico, compartido o pertenecer a una plataforma de terceros. Lo util es tratarlo como pivote.

### 3. Cruza con SecurityTrails para nombres e historial

Cuando ya tienes un dominio o conjunto pequeno de indicadores, SecurityTrails ayuda a responder preguntas diferentes:

- que subdominios ha observado para ese hostname;
- que cambios hubo en registros DNS concretos;
- que otros dominios aparecen asociados en su contexto.

En una revision responsable, eso sirve para distinguir entre:

- activos aun vigentes;
- residuos historicos que siguen apareciendo en datasets pasivos;
- y cambios de resolucion que requieren confirmacion con el equipo de red o sistemas.

### 4. Introduce la variable tiempo

Una de las mayores trampas del OSINT de infraestructura es olvidar que casi todo tiene tiempo de observacion. Censys ofrece historico de servicios y certificados; SecurityTrails expone historial DNS por tipo de registro. Eso no equivale a "verdad en tiempo real", pero si ayuda a formular mejores preguntas:

- cuando aparecio este servicio por primera vez;
- cuando cambio la resolucion de este nombre;
- el certificado actual y el historico apuntan a la misma propiedad o a proveedores distintos.

La diferencia entre una pista util y un falso positivo suele estar ahi: en la cronologia.

### 5. Documenta observacion, inferencia y validacion por separado

Para que el trabajo sea reutilizable, separa siempre tres capas:

- observacion: lo que la plataforma devuelve;
- inferencia: lo que crees que sugiere esa observacion;
- validacion: la comprobacion con otra fuente autorizada.

Ese separador evita una deriva muy comun: convertir una relacion tecnica posible en una atribucion rotunda antes de tiempo.

## Limitaciones y falsos positivos

- ni Censys ni SecurityTrails representan por si solos el estado exacto e instantaneo de un activo;
- certificados, IPs o DNS pueden pertenecer a CDN, proveedores o infra compartida;
- un subdominio historico no demuestra que siga operativo ni bajo control actual;
- un banner o una tecnologia detectada no equivale automaticamente a vulnerabilidad explotable;
- una relacion entre dominios puede ser operativa, historica o accidental.

En resumen: sirven para priorizar y contextualizar, no para cerrar un caso en solitario.

## Buenas practicas de OPSEC, etica y privacidad

- trabaja solo con activos propios, autorizados o claramente dentro del marco legal del encargo;
- minimiza la recoleccion: busca lo necesario para responder tu hipotesis;
- guarda fecha, consulta y razon de cada pivot relevante;
- evita difundir listados de infraestructura sensible mas alla del equipo que debe actuar;
- trata datos pasivos y graficos bonitos como apoyo analitico, no como licencia para sobreatribuir.

## Alternativas y siguientes pasos

Si tu necesidad principal es inventario de exposicion pura, una plataforma tipo Shodan puede complementar bien la primera fase. Si lo que necesitas es reconstruir nombres, cambios DNS y propiedad historica, fuentes como CT logs, WHOIS y archivos web siguen siendo igual de importantes.

El takeaway practico es sencillo: usa Censys para ver superficie y relaciones tecnicas visibles; usa SecurityTrails para entender nombres e historial; y reserva las conclusiones fuertes para el momento en que varias fuentes distintas empiecen a contar la misma historia.

Siguiente tema sugerido para continuar la serie: `PhoneInfoga` o `WhatsMyName`, pero con el mismo filtro metodologico de siempre: menos fetichismo de herramienta y mas control de falsos positivos.

## Fuentes consultadas

- Censys Docs, Censys Query Language: https://docs.censys.com/docs/censys-query-language
- Censys Docs, Platform Datasets: https://docs.censys.com/docs/platform-datasets
- Censys Docs, Platform Historical Data: https://docs.censys.com/docs/platform-historical-data
- Censys Docs, Certificates: https://docs.censys.com/docs/ls-certificates
- SecurityTrails Docs, Overview: https://docs.securitytrails.com/docs/overview
- SecurityTrails API Reference, List Subdomains: https://docs.securitytrails.com/reference/list-subdomains-old-1
- SecurityTrails API Reference, DNS history by record type: https://docs.securitytrails.com/reference/dns-history-by-record-type-old-1
- SecurityTrails API Reference, Find associated domains: https://docs.securitytrails.com/reference/find-associated-domains-old-1
