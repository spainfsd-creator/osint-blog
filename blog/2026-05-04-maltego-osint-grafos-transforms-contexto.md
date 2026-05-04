---
title: "Maltego en OSINT: grafos, transforms y contexto para investigar sin confundir conexiones con evidencia"
slug: /maltego-osint-grafos-transforms-contexto
authors: [osint-writter]
tags: [osint, tooling, investigation, link-analysis, methodology, opsec]
date: 2026-05-04
image: /img/blog/2026-05-04-maltego-osint-grafos-transforms-contexto.png
---

![Ilustracion editorial de una analista OSINT construyendo un grafo de relaciones con dominios, entidades, mapas y documentos publicos](/img/blog/2026-05-04-maltego-osint-grafos-transforms-contexto.png)

Hay investigaciones que no fallan por falta de datos, sino por falta de estructura. Un dominio lleva a una IP, la IP a un ASN, el ASN a una empresa, la empresa a otra web, la web a un tracking code y, cuando quieres darte cuenta, tienes veinte pestañas abiertas y una intuicion dificil de defender. `Maltego` sigue siendo util justo en ese punto: no porque "descubra la verdad" por ti, sino porque te obliga a **modelar relaciones, separar pivotes y visualizar que merece verificarse de nuevo**.

Ese matiz importa especialmente en 2026. La documentacion oficial deja claro que el ecosistema ha cambiado: `Maltego Graph` convive hoy con `Maltego Search`, `Cases`, `Admin`, `Data Pass` y conectores modernos, mientras que los `Standard Transforms` clasicos ya figuran como oferta heredada para usuarios legacy. Traducido a lenguaje de analista: el valor de `Maltego` ya no esta solo en "tirar transforms", sino en **combinar datos, metodo y criterio para no inflar una coincidencia tecnica hasta convertirla en una conclusion**.

<!-- truncate -->

## Que es y para que sirve

La pagina oficial de `Maltego Graph` lo presenta como una herramienta de analisis de enlaces para investigaciones complejas, pensada para descubrir conexiones en datasets grandes de forma visual e intuitiva. Su documentacion sobre `Transforms` añade la pieza importante: un transform es codigo que toma una entidad de entrada y devuelve entidades relacionadas. Parece una definicion pequena, pero condiciona toda la metodologia.

En la practica, `Maltego` sirve para preguntas como estas:

- que relaciones tecnicas aparecen alrededor de un dominio, persona, alias o empresa;
- que pivotes merecen repetirse con otra fuente antes de escribir nada;
- que partes de un caso son observacion directa y cuales son inferencia;
- y como documentar un mapa de relaciones sin depender de tu memoria ni de veinte pestañas sueltas.

No es lo mismo que un buscador especializado ni que una base de datos OSINT concreta. `Maltego` es, sobre todo, una **capa de orquestacion y visualizacion**. La gracia no esta en tener mas nodos, sino en tener un grafo que siga siendo legible cuando el caso se complica.

## Caso de uso legitimo con ejemplo ficticio

Imagina una `due diligence` tecnica sobre una empresa ficticia llamada `Norte Claro Energia`. El encargo no pide atribuir nada raro ni "hackear" nada; solo entender mejor su superficie publica y sus relaciones visibles antes de una compra.

El punto de partida podria ser un dominio corporativo y dos filiales conocidas. A partir de ahi, un flujo prudente en `Maltego` seria:

1. crear entidades separadas para dominio, organizacion y marcas relacionadas;
2. extraer DNS, MX y resoluciones visibles para no mezclar correo con hosting sin revisar;
3. anotar tracking codes, tecnologias web o certificados que merezcan contraste;
4. cruzar esos hallazgos con otra fuente externa antes de elevarlos a "relacion probable";
5. marcar en el propio grafo que es dato observado, que es hipotesis y que ha quedado descartado.

Lo importante no es que el grafo "quede bonito". Lo importante es que, si alguien te pregunta por que relacionaste dos webs o por que descartaste una tercera, puedas volver al nodo, a la fuente y al paso metodologico concreto.

## Flujo recomendado

### 1. Modela poco al principio

La propia definicion oficial de `Transform` insiste en devolver la pieza de informacion mas pequena posible para aprovechar el analisis de enlaces. Esa idea evita uno de los errores mas comunes: arrancar con entidades demasiado gordas, ambiguas o mezcladas.

En vez de meter una conclusion del tipo "infraestructura de la empresa X", conviene empezar con piezas mas defensables:

- un dominio;
- una direccion de correo;
- una IP;
- un alias;
- una organizacion nombrada de forma consistente.

Cuanto mejor sea la entidad de entrada, mejor sera el resto del grafo.

### 2. Usa transforms y conectores como capas, no como sentencia

La documentacion actual de `Maltego Graph` habla de mas de `120` proveedores de datos y mas de `12.000` metodos de busqueda. Eso no significa que todo deba consultarse siempre. Significa que el analista tiene mas superficie de enrichment y, por tanto, mas responsabilidad para no mezclar fuentes heterogeneas sin contexto.

Una disciplina sensata seria esta:

- primero, obtener relaciones basicas y visibles;
- despues, enriquecer con fuentes mas especializadas;
- luego, contrastar fuera de `Maltego` los pivotes sensibles;
- y finalmente, dejar notas claras sobre grado de confianza.

Si un tracking code aparece en dos webs, eso no prueba control comun por si solo. Si un correo sale vinculado a un dominio, tampoco demuestra rol actual. `Maltego` acelera el hallazgo del patron; tu trabajo sigue siendo validarlo.

### 3. Entiende la arquitectura cuando el caso es sensible

En investigaciones delicadas, la parte menos glamurosa importa mucho. La documentacion de `TDS/iTDS` explica que existe un `Public TDS`, alojado en infraestructura de Maltego, y un `iTDS` interno para organizaciones que no quieren que ciertos flujos pasen por internet o por la infraestructura del proveedor.

Operativamente, eso te obliga a pensar en tres cosas:

- que datos introduces en entidades y consultas;
- que transforms dependen de servicios de terceros;
- y cuando conviene usar infraestructura interna o compartimentada.

No es una cuestion puramente tecnica. Es `OPSEC` aplicada al tooling.

### 4. Separa el Maltego "clasico" del Maltego actual

Aqui hay una actualizacion importante. A `21 de enero de 2026`, la propia documentacion de `Standard Transforms` los marca como funcionalidad heredada para usuarios legacy y dice que ya no reciben soporte. Al mismo tiempo, la documentacion de `Data Pass and Connectors for Maltego Graph`, actualizada el `19 de enero de 2026`, explica que muchas capacidades viven ahora en modulos y conectores modernos, incluidos varios utilitarios que antes estaban en los `Standard Transforms`.

La lectura util para un analista no es nostalgica. Es practica:

- si lees guias antiguas, revisa si dependen de transforms legacy;
- si repites un flujo historico, comprueba si hoy vive en `Utilities`, `Data Pass` o un conector concreto;
- y si una investigacion depende de una integracion de pago o de creditos, planifica antes de lanzar consultas en masa.

## Limitaciones y falsos positivos

`Maltego` puede hacerte mas rapido, pero tambien te puede hacer mas convincente de la cuenta. Ese es su riesgo real.

Los falsos positivos suelen aparecer cuando:

- confundes proximidad visual en el grafo con relacion probada;
- tratas un enrich de tercero como si fuera observacion primaria;
- mezclas historico y presente sin marcar fechas;
- o arrastras demasiados nodos irrelevantes hasta que el grafo parece profundo solo por volumen.

Tambien hay limites practicos. La documentacion de `Maltego Graph Community Edition` indica limites como hasta `10.000` entidades por grafo, hasta `24` resultados por transform y una asignacion minima de `200` creditos al mes. Eso obliga a priorizar mejor en lugar de lanzar consultas sin criterio.

## Buenas practicas de OPSEC, etica y privacidad

La documentacion de Maltego sobre logging aclara que no registra el cuerpo HTTP con las entidades enviadas ni los resultados devueltos, pero si conserva metadatos de ejecucion como fecha, IP origen, URL del transform, nombre del transform, clave API derivada de la licencia, `user agent` y cabeceras de tamano. Esa distincion es importante: no es excusa para descuidar compartimentacion, minimizacion o higiene de consultas.

Buenas practicas razonables:

- no introduzcas mas datos personales de los necesarios para resolver la pregunta;
- usa workspaces, naming y notas coherentes para no mezclar casos;
- marca con claridad lo observado, lo inferido y lo pendiente de validar;
- revisa que proveedores y conectores participan en tu flujo antes de tocar casos sensibles;
- y evita convertir una capacidad tecnica en una invitacion a invadir la vida privada de nadie.

OSINT responsable no consiste en "ver hasta donde puedo llegar". Consiste en saber **cuando parar, que no afirmar y como dejar trazabilidad suficiente para que otra persona pueda revisar tu trabajo**.

## Alternativas y siguientes pasos

`Maltego` no reemplaza a herramientas concretas; las organiza. Segun el caso, puede encajar bien junto a:

- `SecurityTrails`, `urlscan.io` o `PeeringDB` para enriquecer infraestructura;
- `OpenSanctions` u `OpenCorporates` para contexto corporativo;
- `Hunchly` o captura propia para preservacion del recorrido;
- y `SQLite` o `Datasette` cuando necesitas explotar tablas, cronologias o exportaciones con mas control.

Si tu caso es pequeno y la pregunta es sencilla, puede que un cuaderno estructurado baste. Cuando la investigacion empieza a depender de relaciones cruzadas, historicos, enrichments y revision por terceros, ahi es donde `Maltego` suele justificar su coste cognitivo.

La takeaway accionable es esta: usa `Maltego` para **pensar mejor las relaciones**, no para adornarlas. Un buen grafo no es el que tiene mas nodos; es el que deja claro que viste, que dedujiste y que todavia no puedes sostener. Como siguiente puente editorial, tendria sentido aterrizar esto en un caso practico de infraestructura web con `Maltego`, `urlscan.io` y `CT logs`, mostrando donde acaba la correlacion util y donde empieza la fantasia.

## Fuentes

- [Maltego Graph](https://www.maltego.com/graph/)
- [What is a Transform?](https://support.maltego.com/en/support/solutions/articles/15000034010-what-is-a-transform-)
- [Introduction to Maltego Standard Transforms](https://docs.maltego.com/en/support/solutions/articles/15000041468-introduction-to-maltego-standard-transforms)
- [Data Pass and Connectors for Maltego Graph](https://docs.maltego.com/en/support/solutions/articles/15000058711-data-pass-and-connectors-for-maltego-graph)
- [What is a Transform Distribution Server (TDS/iTDS)?](https://support.maltego.com/en/support/solutions/articles/15000020198-what-is-a-transform-distribution-server-tds-itds-)
- [Maltego Products and Plans](https://support.maltego.com/en/support/solutions/articles/15000036759-maltego-products-and-plans)
- [What is Maltego Graph Community Edition (CE)?](https://docs.maltego.com/en/support/solutions/articles/15000018947-what-is-maltego-graph-community-edition-ce-)
- [What is logged when I run a Transform?](https://docs.maltego.com/en/support/solutions/articles/15000011924-what-is-logged-when-i-run-a-transform-)
