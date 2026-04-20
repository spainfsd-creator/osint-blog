---
title: "RDAP y WHOIS en OSINT: registro, fechas y contexto sin sobreatribuir"
slug: /rdap-whois-osint-registro-contexto-fechas
authors: [osint-writter]
tags: [osint, recon, verification, investigation, tradecraft, privacy]
date: 2026-04-20
image: /img/blog/2026-04-20-rdap-whois-osint-registro-contexto-fechas.png
---

![Ilustracion editorial de una analista OSINT contrastando respuestas RDAP y WHOIS sobre dominios, IPs y ASNs en un tablero de investigacion](/img/blog/2026-04-20-rdap-whois-osint-registro-contexto-fechas.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/rdap-whois-osint-registro-contexto-fechas.m4a)


Cuando una investigacion tecnica toca un dominio, una IP o un `ASN`, mucha gente sigue haciendo la misma pregunta de hace quince anos: "que dice el WHOIS". El problema es que en 2026 esa pregunta, por si sola, ya llega tarde. En el espacio de `gTLD`, `ICANN` dejo claro que desde el **28 de enero de 2025** el `RDAP` es la fuente definitiva para entregar datos de registro, mientras que `WHOIS` ha quedado como tecnologia heredada o paralela segun el caso. Para un analista OSINT, esto cambia menos el objetivo que el metodo: **ya no basta con leer un bloque de texto; hay que entender de que registro procede, que parte es actual, que parte esta redactada o limitada, y que inferencias no debes hacer**.

Este contenido esta orientado a usos legitimos: inventario externo, due diligence, respuesta a incidentes, proteccion de marca, analisis de terceros y verificacion tecnica. No incluye tacticas para acoso, doxxing ni intrusiones.

<!-- truncate -->

## Que es y para que sirve

`WHOIS` fue durante anos la forma clasica de consultar datos de registro de dominios y recursos numericos. Sigue existiendo en muchos sitios, pero su formato libre, sus diferencias entre operadores y sus limites de seguridad y estandarizacion lo convierten en una base incomoda para analisis serio.

`RDAP` (`Registration Data Access Protocol`) nace precisamente para ordenar ese terreno. La documentacion de `ICANN` y la base de conocimiento de `Maltego` lo resumen bien: aporta acceso estructurado, soporte para internacionalizacion, mecanismos de acceso diferenciados, descubrimiento autoritativo del servicio y respuestas mas faciles de procesar de forma automatizada.

Traducido a trabajo real de OSINT, esto sirve para cinco cosas muy concretas:

- pasar de una consulta manual dispersa a respuestas estructuradas y comparables;
- distinguir mejor entre registrador, registro, titular aparente y contactos operativos;
- descubrir a que servicio autoritativo debes preguntar antes de interpretar el dato;
- documentar fechas, estados y relaciones sin depender de un parser improvisado;
- y reducir errores cuando cruzas dominios, `IP`, `ASN`, redes y entidades asociadas.

La utilidad practica no es "saber de quien es todo". La utilidad es **formular preguntas mas precisas**:

1. que objeto estoy consultando exactamente;
2. que servicio me responde y con que autoridad;
3. que campos son visibles de forma publica y cuales ya no lo son;
4. y que parte del relato que estoy construyendo es dato registral frente a inferencia analitica.

## Caso de uso legitimo con ejemplo ficticio

Imagina a la empresa ficticia `Boreal Logistica`, que detecta un dominio parecido a su marca circulando en una campana de phishing. El equipo no necesita una "atribucion total" en diez minutos. Necesita responder cuatro preguntas sobrias:

1. cuando se registro el dominio y con que estado aparece;
2. que registrador o registro interviene;
3. si hay infraestructura, contactos o identificadores que merezcan correlacion con otros activos;
4. y que datos faltan o estan ocultos, para no rellenar huecos con fantasia.

Un flujo responsable seria este:

- consultar el dominio en una fuente `RDAP` autoritativa o descubierta por bootstrap;
- guardar la respuesta completa, incluyendo `status`, `events`, `nameservers`, entidades y `remarks`;
- comprobar si la fecha observada es de creacion, actualizacion o expiracion, y no mezclarlas;
- contrastar el dominio con `DNS`, `CT logs`, capturas web, historico y telemetria propia;
- y dejar por escrito que un registrador comun, un proveedor comun o una privacidad comun no prueban por si solos control comun.

Ese ultimo punto importa mucho. En OSINT de infraestructura, la trampa habitual no es la ausencia de datos, sino la tentacion de convertir una coincidencia administrativa en una conclusion operativa.

## Flujo recomendado

### 1. Empieza por la pregunta, no por la herramienta

Si tu pregunta es sobre un dominio `gTLD`, la referencia actual de `ICANN` importa mucho: desde el **28 de enero de 2025** `RDAP` es la fuente definitiva para entregar informacion de registro en ese espacio. Si tu pregunta es sobre recursos numericos, debes mirar el `RIR` correspondiente (`ARIN`, `RIPE NCC`, `APNIC`, `LACNIC`, `AFRINIC`) o el operador que toque.

La consecuencia metodologica es simple: no hagas una consulta "donde sea" y luego intentes arreglar la trazabilidad despues. Decide primero **que namespace investigas**.

### 2. Localiza el servicio autoritativo

El bootstrap de `IANA` existe para esto: decirte a que base `RDAP` debes ir para un `TLD`, un registrador o un recurso numerico concreto. En investigaciones con varias jurisdicciones o muchos dominios, este paso evita leer datos de un intermediario cuando puedes consultar la fuente mas cercana al registro.

Para un analista, este detalle no es burocracia. Es control de calidad.

### 3. Lee bien los campos que si importan

En una respuesta `RDAP`, suele merecer mas la pena fijarse en:

- `events` y sus fechas;
- `status` del dominio o del objeto;
- `nameservers`;
- entidades relacionadas y sus roles;
- `remarks` o notas del registro;
- y enlaces autocontenidos (`self`) o referencias relacionadas.

En cambio, conviene ser prudente con campos incompletos, datos parcialmente anonimizados o contactos que solo reflejan una capa administrativa.

### 4. Cruza con otras fuentes antes de concluir

Ni `RDAP` ni `WHOIS` viven solos. Si el objetivo es un dominio sospechoso, la lectura mejora al combinarla con:

- `DNS` actual para ver resoluciones y servicios activos;
- `CT logs` para descubrir certificados y nombres relacionados;
- historico web para reconstruir cambios o activacion del sitio;
- datos de registrador o hosting solo como contexto, no como prueba final;
- y evidencia interna o defensiva si trabajas con autorizacion.

### 5. Conserva la respuesta completa

Guardar el `JSON` completo de `RDAP` ayuda mucho mas que copiar tres lineas a mano en una nota. Te deja volver a revisar el objeto, justificar una fecha concreta y comparar estados si mas adelante el activo cambia.

## Limitaciones y falsos positivos

La principal limitacion es conceptual: **registro no equivale a operacion**. Que un objeto aparezca ligado a una organizacion, un registrador o una entidad concreta no significa que esa parte controle el activo de la forma que te imaginas.

Errores comunes:

- confundir el registro del dominio con el operador real del contenido;
- leer una fecha de actualizacion como si fuera la de creacion;
- asumir que la privacidad o redaccion de datos es sospechosa por si misma;
- mezclar datos de `WHOIS` antiguo con `RDAP` actual sin documentar la fuente;
- y extrapolar relacion entre activos solo porque comparten proveedor, `nameserver` o patron administrativo.

Ademas, `WHOIS` no ha desaparecido de forma uniforme en todo Internet. El cambio de `ICANN` del **28 de enero de 2025** afecta al suministro de datos registrales de `gTLD`, pero en la practica todavia veras servicios heredados, pasarelas web, politicas regionales distintas y registros con grados muy diferentes de detalle publico. Esa heterogeneidad obliga a escribir siempre **que servicio consultaste y cuando**.

## Buenas practicas de OPSEC, etica y privacidad

- Consulta solo datos necesarios para la pregunta investigativa.
- No conviertas datos registrales en perfiles personales si no existe una base legitima para ello.
- Documenta redacciones, campos ausentes y limites del servicio como parte del hallazgo.
- Separa claramente "dato observado" de "hipotesis analitica".
- Si manejas informacion potencialmente sensible, comparte resumenes minimizados en lugar de volcar respuestas completas sin contexto.

La regla operativa util es esta: `RDAP` y `WHOIS` son capas de **contexto registral**, no licencias para especular sobre personas.

## Alternativas y siguientes pasos

Si lo que necesitas es descubrir historial de subdominios o certificados, `CT logs` y fuentes de historico DNS te daran mas recorrido. Si tu prioridad es correlacion visual entre entidades ya verificadas, una herramienta de grafo puede ayudarte a ordenar relaciones. Si lo importante es preservar estados y cambios visibles de una web, el historico web y las capturas propias siguen siendo imprescindibles.

Como siguiente paso natural para el blog, una continuacion potente seria bajar un nivel y cubrir `BGP` y rutas publicas para entender por que un `ASN` o un prefijo no cuentan toda la historia por si solos.

## Fuentes

- [ICANN Update: Launching RDAP; Sunsetting WHOIS](https://www.icann.org/en/announcements/details/icann-update-launching-rdap-sunsetting-whois-27-01-2025-en)
- [ICANN: Proposed Amendments to the Base gTLD RA and RAA to Add RDAP Contract Obligations](https://www.icann.org/en/public-comment/proceeding/proposed-amendments-to-the-base-gtld-ra-and-raa-to-add-rdap-contract-obligations-06-09-2022)
- [IANA: Bootstrap Service Registry for Domain Name Space](https://www.iana.org/assignments/rdap-dns/rdap-dns.xhtml)
- [ARIN: Whois/Registration Data Access Protocol (RDAP)](https://www.arin.net/resources/registry/whois/rdap/)
- [RIPE NCC: RIPE Database](https://www.ripe.net/manage-ips-and-asns/db)
- [RIPE Database docs: RIPE Database](https://docs.db.ripe.net/Available-Databases/RIPE-Database)
