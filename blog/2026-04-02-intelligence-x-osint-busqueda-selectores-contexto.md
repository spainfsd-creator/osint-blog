---
title: "Intelligence X en OSINT: buscar por selectores, filtrar contexto y no confundir indice con prueba"
slug: /intelligence-x-osint-busqueda-selectores-contexto
authors: [osint-writter]
tags: [osint, tools, investigation, methodology, search, privacy]
date: 2026-04-02
image: /img/blog/2026-04-02-intelligence-x-osint-busqueda-selectores-contexto.png
---

![Ilustracion editorial de un analista OSINT trabajando con indices, selectores y resultados historicos para contextualizar una investigacion sin sobreatribuir](/img/blog/2026-04-02-intelligence-x-osint-busqueda-selectores-contexto.png)

Cuando una investigacion arranca con un dominio, un correo, una URL o un telefono, el problema rara vez es "no tener datos". El problema real es **saber que buscar, donde cortar el ruido y como evitar que un resultado historico o ambiguo acabe convertido en una afirmacion demasiado fuerte**. Ahí es donde `Intelligence X` resulta util: no como oraculo, sino como indice amplio para orientar hipotesis y abrir comprobaciones posteriores.

La plataforma interesa a equipos de seguridad, periodistas, analistas de riesgo y perfiles de due diligence porque trabaja bien con selectores concretos y permite filtrar por categorias, fechas y tipos de dato. Pero conviene poner el freno a tiempo: un match en `Intelligence X` no es una atribucion cerrada ni una licencia para recolectar sin criterio. Sirve para contextualizar y priorizar verificacion manual.

<!-- truncate -->

## Que es y para que sirve

La documentacion oficial describe `Intelligence X` como la interfaz que usa su `Search API`, mientras que `identity.intelx.io` usa una `Leaks API` separada. Ese detalle importa porque aclara dos cosas: primero, que la experiencia web no es magia negra sino un cliente de su propia API; y segundo, que conviene distinguir entre busqueda general en `intelx.io` y capacidades de su portal de identidad.

La pagina oficial de selectores deja claro el tipo de entradas que la herramienta entiende bien: correos, dominios, URLs, IPs, CIDR, telefonos, direcciones de criptomonedas, MAC e incluso identificadores concretos como IPFS. Para un analista, eso significa una ventaja practica: **puedes empezar por una pieza pequena y dejar que el sistema busque variaciones razonables segun el selector**, en lugar de forzar consultas arbitrarias.

Hay un comportamiento especialmente util para investigaciones defensivas sobre infraestructura. Segun la ayuda oficial, al buscar un dominio la plataforma intenta encontrar ese dominio, subdominios, URLs y correos relacionados; en cambio, una URL con ruta se trata como busqueda exacta. Esa diferencia cambia por completo el enfoque: el dominio abre superficie; la URL exacta reduce ambiguedad.

Tambien hay novedades recientes que la hacen mas interesante para contexto tecnico. El blog oficial anuncio el 12 de enero de 2025 una nueva categoria `dns`, pensada para indexar registros DNS como TXT records. Para una investigacion legitima, esto puede aportar senales sobre verificacion de servicios, relaciones operativas o rastros de gestion de un dominio, siempre que luego se corroboren fuera de la herramienta.

## Caso de uso legitimo con ejemplo ficticio

Imagina una revision previa de terceros sobre la empresa ficticia `orbe-digital.example`. El objetivo no es "sacar todo lo posible", sino responder preguntas defensivas muy concretas:

- que huella publica existe alrededor del dominio principal;
- que subdominios o URLs merecen comprobacion adicional;
- y que resultados son historicos, redundantes o demasiado debiles para sostener una conclusion.

En un flujo asi, `Intelligence X` encaja bien como primera mesa de triage:

1. Empiezas por el dominio para obtener una vista amplia de dominios, subdominios, URLs y correos asociados.
2. Si aparece un subdominio sensible, cambias a una busqueda mas precisa por ese host concreto.
3. Si un resultado parece antiguo o parcial, lo mueves a la columna de "verificar" en lugar de tratarlo como evidencia cerrada.

Lo valioso no es el volumen de resultados, sino poder formular frases prudentes del tipo: "esta referencia historica sugiere una relacion que merece contraste" o "estos TXT records apuntan a una integracion de terceros que deberia validarse". Esa redaccion parece menos espectacular, pero es bastante mas profesional.

## Flujo recomendado

### 1. Empieza por el selector correcto

La documentacion de `Intelligence X` insiste en una idea simple: la plataforma trabaja por selectores. Si la pista inicial es un correo, busca el correo. Si es un dominio raiz, busca el dominio. Si es una URL especifica con ruta, usa esa URL exacta.

Ese detalle reduce ruido y ahorra malos pivotes. No es lo mismo investigar `empresa-ejemplo.com` que `https://empresa-ejemplo.com/login/`. El primer caso puede devolver ecos alrededor de toda la superficie; el segundo acota mucho mas.

### 2. Usa el dominio para abrir mapa; usa el subdominio para afinar

La ayuda oficial explica que un dominio cubre automaticamente subdominios, URLs y correos, pero un subdominio se trata como entidad mas concreta. Traducido a metodo OSINT: **abre ancho primero, afina despues**.

Una secuencia sensata suele ser:

- dominio principal para panorama general;
- subdominio concreto si aparece algo interesante;
- URL exacta cuando necesitas comprobar una ruta, recurso o panel especifico;
- y filtros de fecha o bucket cuando el ruido empieza a dominar.

### 3. Filtra por fecha, bucket y tipo antes de interpretar

La FAQ oficial advierte que no hay garantia de que una misma consulta devuelva siempre exactamente la misma ventana de resultados y que, cuando se llega al maximo por bucket, conviene apoyarse en filtros de fecha y categoria. Eso obliga a trabajar con mas disciplina de la que algunos esperan.

La conclusion practica es clara:

- una consulta amplia sirve para orientarte;
- una consulta filtrada sirve para leer mejor;
- y ninguna de las dos deberia acabar en informe sin corroboracion externa.

### 4. Trata el resultado como indice, no como prueba final

La misma documentacion tambien deja limites utiles sobre la mesa: no hay busqueda full-text, no hay operadores booleanos y parte del refinado se hace con filtros y tratamiento posterior del analista. Eso desmonta la fantasia de "meto una cadena y la plataforma razona por mi".

La herramienta funciona mejor cuando la usas para localizar piezas candidatas y luego confirmas con otras fuentes: archivos web, consultas DNS actuales, CT logs, hemeroteca, registros mercantiles, capturas propias o validacion tecnica directa.

## Limitaciones y falsos positivos

`Intelligence X` es potente, pero tiene limites muy concretos que merece la pena respetar.

Primero, los resultados pueden variar. La propia FAQ explica que influyen resultados nuevos, mantenimiento interno, timeouts y limites por bucket. Si una consulta cambia entre dos momentos, no siempre significa manipulacion ni error; a veces significa simplemente que estas viendo una ventana distinta sobre un corpus enorme.

Segundo, la plataforma no soporta full-text ni operadores booleanos clasicos. Eso empuja a pensar mejor los selectores, pero tambien limita ciertas estrategias de busqueda que algunos analistas intentan trasladar desde buscadores convencionales.

Tercero, la documentacion de limites deja claro que hay diferencias entre acceso gratuito y de pago. En la documentacion actual, `free.intelx.io` tiene un maximo de 200 resultados por bucket y timeout de 1 minuto, mientras que `2.intelx.io` para usuarios de pago sube a 1000 resultados y 2 minutos. Si comparas capturas o resultados con otro analista y no teneis el mismo tipo de acceso, es facil sacar conclusiones equivocadas.

Cuarto, el hecho de que exista una categoria o una referencia no te dice por si solo si un dato sigue vigente, si fue indexado desde una copia vieja o si describe una relacion operativa real. El indice ayuda a encontrar; el analista decide si esa pista merece pasar a evidencia.

## Buenas practicas de OPSEC, etica y privacidad

- Formula una pregunta concreta antes de buscar: entidad, periodo y motivo.
- Minimiza pivotes sobre personas fisicas salvo que exista base legitima y necesidad real.
- Separa siempre lo actual, lo historico y lo no corroborado.
- Conserva capturas o notas con fecha de consulta cuando un hallazgo vaya a usarse en un informe.
- No presentes coincidencias de correo, dominio o telefono como prueba de control o autoria sin contraste independiente.
- Si una pista apunta a datos sensibles o filtrados, documenta solo lo necesario para la finalidad legitima del caso.

Una buena regla de oficio es esta: si un hallazgo solo suena solido mientras dices "lo vi en la plataforma", todavia no esta listo para salir de tu libreta de trabajo.

## Alternativas y siguientes pasos

Si necesitas descubrir superficie expuesta en servicios y banners, `Shodan` o `Censys` suelen ser mas directos. Si tu prioridad es preservar paginas y reconstruir cambios, `Wayback Machine` o `Archive.today` encajan mejor. Si quieres vigilar DNS, historico web y artefactos de terceros con mas combinacion manual, puede ser mejor repartir el trabajo entre varias fuentes especializadas.

`Intelligence X`, en cambio, destaca cuando quieres empezar con un selector sencillo y obtener un mapa rapido de contexto alrededor de ese dato. No sustituye el criterio ni la verificacion. Pero bien usado, acelera justo la parte que mas tiempo roba a un analista: separar lo que merece seguimiento de lo que solo parece interesante durante diez minutos.

El takeaway practico es sencillo: la proxima vez que una investigacion arranque con un dominio, un correo o una URL, no preguntes primero "que mas puedo sacar". Pregunta "que selector describe mejor mi hipotesis inicial y que tendria que corroborar despues". Ese cambio de mentalidad vale mas que cualquier pantalla llena de resultados.

## Fuentes

- Intelligence X Help, `Selectors`: https://help.intelx.io/docs/get-started/selector/
- Intelligence X Help, `Search`: https://help.intelx.io/docs/faq/search/
- Intelligence X Help, `API`: https://help.intelx.io/api/
- Intelligence X Help, `Limits`: https://help.intelx.io/docs/api/limits/
- Intelligence X Blog, `New Category "DNS"` (12 de enero de 2025): https://blog.intelx.io/2025/01/12/new-category-dns/
- Intelligence X Blog, `New Search API Instances` (8 de marzo de 2025): https://blog.intelx.io/2025/03/08/new-search-api-instances/
- Intelligence X Blog, `Export Stealer Log` (8 de febrero de 2026): https://blog.intelx.io/2026/02/08/export-stealer-log/
