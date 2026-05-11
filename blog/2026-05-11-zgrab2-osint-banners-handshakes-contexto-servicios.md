---
title: "ZGrab2 en OSINT: banners, handshakes y contexto para enriquecer servicios sin sobreatribuir"
slug: /zgrab2-osint-banners-handshakes-contexto-servicios
authors: [osint-writter]
tags: [osint, tooling, data, verification, tradecraft]
date: 2026-05-11
image: /img/blog/2026-05-11-zgrab2-osint-banners-handshakes-contexto-servicios.png
---

![Ilustracion editorial de una analista OSINT revisando banners, handshakes TLS y contexto de servicios publicos con telemetria estructurada](/img/blog/2026-05-11-zgrab2-osint-banners-handshakes-contexto-servicios.png)

Cuando un activo ya ha aparecido en una fase previa de investigacion, el siguiente error tipico es tratarlo como una simple IP con un puerto abierto. A partir de ahi llegan conclusiones pobres: "parece web", "probablemente es tal producto", "esto seguro pertenece al mismo bloque". `ZGrab2` resulta util justo antes de caer en ese salto mental, porque permite **hacer handshakes de capa de aplicacion y recoger banners o respuestas estructuradas para describir mejor un servicio visible**.

La advertencia importante va primero: esto no es una herramienta para curiosear sistemas ajenos "porque total solo responde". El propio proyecto `ZMap` recuerda que el escaneo a escala de Internet tiene implicaciones eticas y operativas serias, y `ZGrab2` deja claro que su filosofia se limita a informacion accesible para un cliente estandar sin autenticacion. En OSINT responsable, eso traduce a una norma sencilla: usarlo en patrimonio propio, entornos autorizados o investigaciones defensivas con alcance bien definido; y tratar cada respuesta como **contexto tecnico**, no como prueba final de propiedad, criticidad o intencion.

<!-- truncate -->

## Que es y para que sirve

`ZGrab2` es el escaner de capa de aplicacion del ecosistema `ZMap`. El `README` oficial lo describe como un escaner rapido y modular pensado para encuestas de Internet a gran escala, trabajando en tandem con `ZMap`: primero identificas hosts con respuesta de capa 4 y despues haces handshakes mas ricos en capa 7.

La diferencia practica importa mucho. Una IP con `443/tcp` abierto no te dice demasiado por si sola. Un `handshake` `TLS`, una respuesta `HTTP`, un banner `SMTP` o una negociacion `SSH` te dan:

- protocolo observado con mas precision;
- metadatos de configuracion visibles para cualquier cliente;
- material estructurado para analisis offline;
- y una forma reproducible de repetir la misma pregunta tecnica sobre varios activos.

El proyecto soporta muchos modulos, entre ellos `HTTP`, `TLS`, `SSH`, `FTP`, `SMTP`, `POP3`, `IMAP`, `Redis`, `MongoDB`, `MySQL`, `Telnet` o `SOCKS5`. Eso lo vuelve util no para "saberlo todo", sino para enriquecer un inventario tecnico ya acotado con preguntas concretas.

## Caso de uso legitimo con ejemplo ficticio

Imagina una revision autorizada sobre `Puerto Boreal Energia`, una empresa ficticia que mantiene varios dominios publicos, un rango pequeno de IPs propias y proveedores externos para distintas aplicaciones. Tras una fase inicial con DNS, historico web y telemetria pasiva, el equipo ya tiene una lista razonable de endpoints visibles. El problema ya no es descubrir mas cosas, sino **entender mejor que responde realmente en cada punto sin perder trazabilidad**.

En ese escenario, `ZGrab2` puede encajar como paso intermedio:

1. `ZMap` o una fuente previa te deja un conjunto limitado de hosts y puertos dentro de alcance autorizado.
2. `ZGrab2` ejecuta un `handshake` concreto por protocolo y devuelve salida JSON.
3. El analista revisa banners, certificados, cabeceras, redirecciones o detalles de negociacion.
4. Solo despues correlaciona eso con `RDAP`, `WHOIS`, `CT logs`, capturas web o inventario interno.

El valor no esta en que el banner "revele la verdad", sino en que reduce ambiguedad. Tal vez dos IPs que parecian equivalentes responden con certificados distintos. Tal vez un `HTTP 200` en un puerto raro no es una app corporativa, sino una consola por defecto o un proxy. Tal vez un host responde en `443`, pero el `SNI` y el certificado dejan claro que estas viendo infraestructura compartida y no una propiedad directa del objetivo.

## Flujo recomendado

### 1. Delimita alcance antes de tocar la red

Si `ZGrab2` va a abrir conexiones y completar handshakes, ya no estas en una capa puramente pasiva. Define por escrito:

- que activos entran en alcance;
- con que base legitima;
- que modulos necesitas realmente;
- y que ritmo o profundidad son proporcionales al caso.

La documentacion de `ZMap` insiste en buenas practicas de ciudadania en Internet: escanear a la menor velocidad necesaria, mas despacio si el espacio objetivo es pequeno, y ofrecer mecanismos de exclusion cuando el trabajo lo requiera. Ese principio es incluso mas importante cuando subes de `L4` a `L7`.

### 2. Prepara entradas limpias

El formato de entrada que documenta `ZGrab2` admite hasta cuatro campos CSV: `IP, DOMAIN, TAG, PORT`. Ese detalle es muy util porque permite separar varios escenarios:

- conectar a una `IP` concreta;
- usar `DOMAIN` para cabecera `Host` o `SNI`;
- etiquetar lotes con `TAG`;
- y sobrescribir el puerto por linea cuando hace falta.

En investigaciones serias, esa estructura ayuda mucho a no mezclar preguntas distintas dentro del mismo lote.

### 3. Usa modulos concretos, no una ambicion difusa

El modo de uso mas simple es lanzar un solo modulo, por ejemplo `http`, `tls` o `ssh`, y revisar la salida JSON. Pero la pieza mas potente para equipos es el modo `multiple`, que usa un archivo `.ini` para declarar varios modulos con nombre, puerto y `trigger`.

Eso tiene una ventaja metodologica clara: puedes dejar la pregunta tecnica escrita como configuracion reproducible. En vez de "hicimos varias pruebas", dejas algo mas auditable:

- `http80` para raiz web en `80`;
- `http8080` para un puerto alternativo;
- `tls443` para recoger negociacion y certificado;
- `ssh22` solo para activos etiquetados con otro `TAG`.

### 4. Analiza la salida como observacion, no como sentencia

La propia razon de ser de `ZGrab2` es producir transcripciones y resultados detallados para analisis offline. Aprovechalo:

- guarda la salida cruda;
- anota fecha y alcance;
- separa hechos observables de inferencias;
- y registra tambien incertidumbre.

Si un banner apunta a un producto concreto, todavia falta validar si es actual, si esta delante de un `proxy`, si se trata de una firma generica o si el servicio realmente pertenece al objetivo investigado.

## Limitaciones y falsos positivos

`ZGrab2` es muy util, pero conviene vigilar varias trampas comunes:

- un `banner` puede estar desactualizado o deliberadamente maquillado;
- una respuesta `HTTP` puede venir de infraestructura compartida;
- el certificado `TLS` puede describir varios nombres que no significan propiedad exclusiva;
- las redirecciones pueden arrastrarte a otro host o servicio;
- y un `handshake` correcto no demuestra por si solo relevancia analitica.

Ademas, que una herramienta sea modular y potente no significa que sea inocua en cualquier contexto. Algunas preguntas pueden responderse mejor con fuentes pasivas o historicas antes de abrir una conexion nueva. Otras merecen hacerlo al reves: primero corroborar con `RDAP`, `CT logs` o historico DNS y despues usar `ZGrab2` para comprobar una hipotesis ya razonable.

## Buenas practicas de OPSEC, etica y privacidad

- No escales de un hallazgo pasivo a un `handshake` activo sin revisar alcance y necesidad.
- No confundas "visible para un cliente estandar" con "vale todo en cualquier objetivo".
- No publiques banners sensibles, rutas internas o metadatos innecesarios si no aportan valor pedagogico.
- No mezcles evidencia de captura con atribucion organizativa sin una segunda capa de corroboracion.
- No uses una sola respuesta tecnica para perfilar personas o sacar conclusiones desproporcionadas.

Una disciplina sencilla ayuda mucho: pregunta tecnica pequena, salida guardada, contraste con otras fuentes y conclusion humilde.

## Alternativas y siguientes pasos

Si necesitas **descubrimiento** a gran escala de puertos o respuesta inicial de red, `ZMap` cubre mejor esa capa. Si lo que buscas es una vista mas consolidada y navegable de resultados activos y pasivos, herramientas como `IVRE`, `Netlas` o `Censys` pueden encajar mejor. Si tu prioridad es resolver DNS rapido y con control, el propio ecosistema `ZMap` ofrece `ZDNS`.

`ZGrab2` aporta otra cosa: el tramo entre "este host responde" y "ya entiendo mejor que servicio me esta hablando". Usado con cuidado, ese tramo evita bastantes historias inventadas por exceso de intuicion tecnica.

El takeaway accionable es este: usa `ZGrab2` para **enriquecer servicios visibles con preguntas pequenas y reproducibles**, no para inflar una investigacion con mas ruido del necesario. Como siguiente puente editorial del blog, tendria sentido bajar aun mas a tierra con un flujo comparado entre `ZGrab2`, `ZDNS` y `IVRE` para mostrar como cambia una hipotesis cuando separas descubrimiento, enriquecimiento y consolidacion.

## Fuentes

- [zmap/zgrab2 en GitHub (README oficial)](https://github.com/zmap/zgrab2)
- [zmap/zmap en GitHub (README oficial)](https://github.com/zmap/zmap)
- [The ZMap Project](https://zmap.io/)
- [About the ZMap Project](https://zmap.io/about)
- [ZMap: Fast Internet-Wide Scanning and its Security Applications (USENIX Security 2013)](https://zmap.io/paper.pdf)
