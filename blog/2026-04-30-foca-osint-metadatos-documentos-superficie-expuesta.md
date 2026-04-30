---
title: "FOCA en OSINT: metadatos, documentos y superficie expuesta sin sobreatribuir"
slug: /foca-osint-metadatos-documentos-superficie-expuesta
authors: [osint-writter]
tags: [osint, metadata, recon, tooling, due-diligence, verification]
date: 2026-04-30
image: /img/blog/2026-04-30-foca-osint-metadatos-documentos-superficie-expuesta.png
---

![Ilustracion editorial de una analista OSINT cruzando metadatos de documentos publicos, relaciones de dominio y notas de due diligence sobre una mesa de investigacion](/img/blog/2026-04-30-foca-osint-metadatos-documentos-superficie-expuesta.png)

Cuando una investigacion parte de una empresa, una administracion o un proveedor, la tentacion habitual es mirar solo la web visible. Pero muchas veces el rastro util esta en otro sitio: **PDFs, DOCX, presentaciones y hojas de calculo que una organizacion publica sin pensar demasiado en la huella que dejan detras**. `FOCA` sigue siendo interesante justo por eso: convierte una carpeta dispersa de documentos abiertos en una lectura mas estructurada de metadatos, nombres internos, rutas, tecnologias y senales de exposicion.

Eso no la convierte en una maquina de atribucion. Un autor en un PDF, un nombre de equipo o una ruta de red no prueban por si solos propiedad, actualidad ni intencion. Lo que si aportan es contexto verificable para una due diligence, una investigacion defensiva o una auditoria de exposicion documental. En OSINT responsable, ese matiz lo es todo.

<!-- truncate -->

## Que es y para que sirve

`FOCA` significa `Fingerprinting Organizations with Collected Archives`. Segun su repositorio oficial, se centra en **encontrar metadatos e informacion oculta en documentos** localizados en paginas web, descargarlos y analizarlos. Trabaja sobre tipos habituales como `Microsoft Office`, `OpenOffice`, `PDF`, `Adobe InDesign` o `SVG`, y tambien puede extraer `EXIF` de ficheros graficos locales.

La utilidad OSINT no esta solo en abrir un PDF y leer su autor. La gracia aparece cuando ordenas muchos documentos juntos y preguntas:

- que nombres de usuario, equipos o rutas se repiten;
- que dominios, subdominios o hostnames asoman en la documentacion publica;
- si hay software, impresoras, generadores PDF o flujos internos que se repiten;
- y que parte de esa huella merece una segunda verificacion con otras fuentes abiertas.

El propio `README` oficial tambien recuerda un punto importante para situarla hoy: `FOCA` sigue pensada para `Windows` de 64 bits, requiere `.NET Framework 4.7.1` y necesita una instancia de `SQL Server` para funcionar. Su wiki oficial explica incluso el alta paso a paso de `SQL Server Express`. Dicho de otra forma: es una herramienta potente, pero no ligera ni particularmente moderna en dependencias.

## Caso de uso legitimo: due diligence documental sobre un proveedor ficticio

Imagina que tu equipo evalua a `proveedor-ejemplo.test` antes de compartirle pliegos, credenciales limitadas o documentacion sensible. No quieres “hackear” nada ni tocar sistemas internos. Solo necesitas responder una pregunta sobria: **que revela la documentacion publica de esa organizacion sobre su higiene operativa y su superficie visible**.

Un flujo prudente con `FOCA` seria este:

1. localizar documentos publicos del dominio principal y de sus subdominios visibles;
2. descargar `PDF`, `DOCX`, `XLSX` o presentaciones publicas relevantes;
3. extraer metadatos para ver autores, software, rutas, fechas y referencias internas;
4. agrupar coincidencias repetidas en lugar de fijarte en un hallazgo aislado;
5. contrastar solo lo prometedor con otras fuentes abiertas como `DNS`, `CT logs`, archivo web o tecnografia.

El valor practico es claro. Si varios documentos distintos repiten un mismo patron de nombres internos, una convencion de equipos o referencias a subdominios no obvios, ya tienes pistas para mejorar el mapa publico de la organizacion. Si, en cambio, solo aparece un autor desactualizado de hace ocho anos en un PDF heredado, lo correcto es no inflarlo como si fuera una fotografia actual del entorno.

## Flujo recomendado

### 1. Empezar por los documentos, no por la fantasia

La disciplina buena consiste en tratar cada fichero como una pieza de contexto, no como una revelacion. `FOCA` ayuda a localizar documentos desde buscadores y a analizarlos en lote, pero el analista sigue teniendo que decidir que documentos son relevantes, que fecha tienen y que peso merece cada metadato.

Lo util suele salir de los patrones:

- un mismo nombre de autor en varias areas del sitio;
- rutas internas repetidas en documentos de equipos distintos;
- generadores PDF o suites ofimaticas coherentes con cierto flujo corporativo;
- y referencias tecnicas que encajan con otros hallazgos abiertos.

### 2. Separar metadato heredado de senal viva

Una de las trampas mas comunes con `FOCA` es asumir que todo metadato refleja el presente. No siempre es asi. Un `username` puede pertenecer a un antiguo empleado, una ruta de red puede venir de una plantilla reciclada y una fecha puede corresponder a la exportacion del documento, no a su ultima edicion sustantiva.

Por eso conviene etiquetar cada hallazgo con tres preguntas:

- es reciente o historico;
- aparece una vez o se repite en varios documentos;
- y encaja con otras fuentes abiertas independientes.

Si la respuesta a la tercera pregunta es “no lo se todavia”, aun no tienes una conclusion. Solo tienes una pista.

### 3. Usar la huella documental para abrir pivotes defensivos

La huella documental sirve sobre todo para formular mejores pivotes:

- un subdominio citado en un documento puede justificar una comprobacion posterior en `SecurityTrails`, `RDAP` o `CT logs`;
- un nombre interno de departamento puede ayudarte a leer mejor organigramas, ofertas de empleo o notas de prensa;
- un software repetido en varios metadatos puede aportar contexto sobre flujos editoriales o madurez operativa;
- y una convencion de nombres puede ayudarte a agrupar documentos relacionados sin tocar nada privado.

El principio es simple: **documento primero, pivote despues, conclusion al final**.

### 4. Recordar el estado real de la herramienta

`FOCA` sigue teniendo comunidad y su repositorio publico muestra una ultima `release` visible `v3.4.7.1`, publicada el `27 de agosto de 2021`, con correcciones sobre `Bing`, `DNS search common names` y `DNSDumpster query`. Eso sugiere dos cosas a la vez:

- sigue siendo util para ciertos flujos de metadatos y reconocimiento documental;
- pero no conviene tratarla como una navaja suiza recien salida del horno ni como herramienta universal para cualquier stack actual.

En la practica, ese contexto te obliga a validar mas: algunos buscadores cambian, algunos formatos evolucionan y algunas rutas de integracion envejecen mal.

## Limitaciones y falsos positivos

`FOCA` aporta mucho contexto, pero tambien puede empujarte a errores si la usas con ansiedad:

- metadato no equivale a evidencia actual;
- una ruta interna no demuestra que ese recurso siga existiendo;
- un autor en un documento no certifica responsabilidad operativa hoy;
- un subdominio mencionado puede estar caido, ser historico o pertenecer a otra etapa;
- y una herramienta con dependencias pesadas puede no encajar bien en todos los entornos de trabajo.

Tambien hay un limite mas estructural: si una organizacion ha limpiado metadatos, centralizado sus exportaciones o apenas publica documentos ricos, el rendimiento investigativo baja mucho. En esos casos `FOCA` no “falla”; simplemente no es la palanca adecuada para ese objetivo.

## Buenas practicas: OPSEC, etica y privacidad

El uso responsable de `FOCA` exige frenar dos impulsos: coleccionar demasiado y contar demasiado pronto.

- Trabaja solo con documentos publicamente accesibles y dentro de un alcance legitimo.
- Anonimiza ejemplos sensibles cuando escribas informes o docencia.
- Conserva notas de procedencia: URL, fecha, hash y por que ese documento importaba.
- No publiques nombres personales o rutas internas si no son necesarios para explicar el metodo.
- Separa siempre “dato observado” de “inferencia analitica”.

En otras palabras: `FOCA` es muy buena sacando huella residual de documentos. Tu trabajo consiste en no convertir esa huella residual en una historia mas grande de lo que permite la evidencia.

## Alternativas y siguientes pasos

`FOCA` no tiene por que trabajar sola. Suele encajar mejor cuando la combinas con herramientas mas ligeras o mas especializadas:

- `ExifTool`, si tu prioridad es inspeccionar metadatos de ficheros concretos con control fino;
- `theHarvester`, si quieres ampliar reconocimiento sobre dominios, correos y fuentes publicas;
- `CT logs`, `RDAP` o `SecurityTrails`, si un hallazgo documental te abre pivotes de infraestructura;
- `Hunchly` o flujos de archivo/hash, si necesitas conservar trazabilidad del proceso.

La takeaway accionable es esta: `FOCA` sigue mereciendo sitio en el cinturón de un analista cuando el caso tiene **muchos documentos publicos y preguntas de contexto organizativo**. No porque resuelva sola una investigacion, sino porque te obliga a mirar donde a menudo nadie mira: la letra pequena incrustada en los archivos que una organizacion deja a plena vista.

## Fuentes y documentacion recomendada

- `ElevenPaths/FOCA` en GitHub (README oficial y requisitos): https://github.com/ElevenPaths/FOCA
- `ElevenPaths/FOCA` releases en GitHub (`v3.4.7.1`, `27 de agosto de 2021`): https://github.com/ElevenPaths/FOCA/releases/tag/v3.4.7.1
- Wiki oficial de `FOCA`, configuracion de `SQL Server`: https://github.com/ElevenPaths/FOCA/wiki/How-to-set-up-a-SQL-database-connection
