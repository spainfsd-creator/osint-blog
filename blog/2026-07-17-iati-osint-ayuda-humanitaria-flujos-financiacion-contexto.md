---
title: "IATI en OSINT: ayuda humanitaria, flujos de financiacion y contexto antes de concluir"
slug: /iati-osint-ayuda-humanitaria-flujos-financiacion-contexto
authors: [osint-writter]
tags: [osint, data, verification, due-diligence, privacy, methodology]
date: 2026-07-17
image: /img/blog/2026-07-17-iati-osint-ayuda-humanitaria-flujos-financiacion-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando datos abiertos de ayuda humanitaria, flujos de financiacion, tablas CSV, mapas y notas de verificacion](/img/blog/2026-07-17-iati-osint-ayuda-humanitaria-flujos-financiacion-contexto.png)

Una cifra de ayuda internacional puede viajar muy rapido: un titular, una promesa de financiacion, una tabla de proyecto y una captura de mapa. El problema es que en cooperacion y accion humanitaria **dinero anunciado, comprometido, desembolsado y gastado no significan lo mismo**. `IATI` ayuda a poner orden en ese terreno, siempre que el analista trate sus datos como una pista estructurada y no como una sentencia automatica sobre impacto, fraude o responsabilidad.

Revisando la documentacion oficial el **17 de julio de 2026**, la `International Aid Transparency Initiative` se presenta como una iniciativa global para mejorar la transparencia de los recursos de desarrollo y humanitarios. Su pagina principal mostraba `1.038.446` actividades publicadas y `1.846` publicadores. La plataforma permite explorar datos mediante `d-portal`, `Country Development Finance Data`, `Datastore Search` y `Datastore API v3`, con salidas en `XML`, `JSON` y `CSV` para analisis posterior.

Este articulo esta escrito para periodistas de datos, analistas OSINT, equipos de rendicion de cuentas, investigadores civicos y organizaciones que necesitan seguir fondos publicos o humanitarios con prudencia. No es una guia para acosar cooperantes, exponer beneficiarios, senalar comunidades vulnerables ni convertir datos incompletos en acusaciones.

<!-- truncate -->

## Que es IATI y para que sirve

[`IATI`](https://iatistandard.org/) es una iniciativa y un estandar abierto para publicar informacion sobre actividades de desarrollo y ayuda humanitaria. Su objetivo practico es que gobiernos, organismos multilaterales, ONG, fundaciones y otros actores puedan publicar datos de proyectos, presupuestos, transacciones, resultados, sectores, ubicaciones y organizaciones participantes con una estructura comun.

Para OSINT, su valor no esta en "seguir cada euro hasta el ultimo recibo". Esta en convertir preguntas amplias en rutas verificables:

- que organizaciones publican actividades en un pais o sector;
- que proyectos aparecen vinculados a una emergencia, region o tema;
- que diferencia hay entre presupuesto, compromiso, desembolso, gasto y resultados;
- que fechas, codigos de sector, paises receptores y organizaciones participantes acompanan una actividad;
- que documentos publicos se enlazan desde una ficha;
- que parte del dato procede del publicador y que parte requiere contraste externo.

La propia pagina de uso de datos recuerda una idea importante: existen herramientas para perfiles tecnicos y no tecnicos. `d-portal` permite explorar y visualizar actividades; `Country Development Finance Data` resume compromisos, desembolsos, gastos y presupuestos por pais o region; y `Datastore Query Builder` permite construir consultas sobre elementos del estandar sin empezar por codigo.

## Caso de uso legitimo con ejemplo ficticio

Imagina que una redaccion investiga si la ayuda anunciada tras unas inundaciones en el pais ficticio `Ribera del Sur` se corresponde con proyectos publicados, sectores declarados y entregas documentadas. El objetivo no es buscar culpables a ciegas, sino entender la trazabilidad publica de la respuesta.

Un flujo responsable podria empezar asi:

1. Buscar en `d-portal` por pais receptor, periodo y palabras como `flood`, `emergency response`, `shelter` o `water`.
2. Revisar las actividades relevantes y anotar `iati-identifier`, organizacion publicadora, organizaciones participantes, estado, fechas y sectores.
3. Descargar resultados desde `Datastore Search` en `CSV` para separar actividades, transacciones y presupuestos.
4. Distinguir importes comprometidos, desembolsados y gastados antes de sumar nada.
5. Abrir documentos enlazados, paginas del donante, informes de situacion, comunicados locales y registros presupuestarios del pais.
6. Marcar como hipotesis, no como conclusion, cualquier hueco entre anuncio publico, dato IATI y evidencia de ejecucion.

La diferencia metodologica es clave: una actividad publicada en IATI puede demostrar que una organizacion declaro cierto proyecto bajo cierto estandar. No demuestra por si sola que la ayuda llegara, que no llegara, que se ejecutara bien o que existiera mala fe.

## Flujo recomendado

### 1. Empezar por la pregunta, no por el dataset

Antes de tocar la API, define una pregunta que pueda responderse con datos publicos:

- "Que proyectos de agua y saneamiento se declararon en esta region entre dos fechas?"
- "Que organizaciones aparecen como financiadoras o implementadoras?"
- "Hay transacciones publicadas o solo presupuestos?"
- "Que documentos primarios respaldan esta actividad?"

Si la pregunta exige identificar beneficiarios individuales, domicilios, personal local o rutas sensibles, probablemente no deberia resolverse con una busqueda abierta. En contextos humanitarios, la minimizacion importa mas que la curiosidad.

### 2. Elegir la herramienta segun el nivel tecnico

Para exploracion rapida, [`d-portal`](https://d-portal.org/) suele ser suficiente. La documentacion de IATI lo recomienda para usuarios nuevos porque permite buscar actividades en el navegador y ver mapas, graficos y fichas.

Para descargar y filtrar, [`IATI Datastore`](https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/) es mas adecuado. La version 3 procesa datos publicados por organizaciones segun el estandar, los actualiza dinamicamente desde el registro y busca procesarlos en las 24 horas siguientes a su disponibilidad. Tambien permite consultar elementos y atributos del estandar y exportar datos como una actividad, transaccion o presupuesto por fila.

Para analisis reproducible, la [`Datastore API`](https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/how-to-use-the-datastore-api/) permite construir consultas con filtros. La guia oficial muestra endpoints para `activity`, `transaction` y `budget`, y ejemplos de busqueda por codigos, pais receptor, sector, narrativas, fechas y rangos financieros. Requiere cuenta gratuita y clave de suscripcion.

### 3. Trabajar con unidades correctas

El error clasico consiste en sumar campos incompatibles. En IATI hay actividades, transacciones, presupuestos, resultados, sectores y documentos. Una tabla de actividad no equivale a contabilidad completa, y una tabla de transacciones no explica por si sola contexto, elegibilidad o entrega final.

Una disciplina util:

- conserva el `iati-identifier` como clave estable de cada actividad;
- separa `budget`, `commitment`, `disbursement` y `expenditure`;
- guarda moneda, fecha de valor y tipo de transaccion;
- documenta si estas leyendo una fila de actividad, presupuesto o transaccion;
- evita mezclar publicadores sin revisar duplicados, cadenas de financiacion o actividades relacionadas.

### 4. Contrastar fuera de IATI

Un buen uso de IATI termina saliendo de IATI. Si una actividad parece relevante, busca:

- documentos enlazados desde la ficha;
- paginas del donante o implementador;
- registros presupuestarios nacionales;
- informes de evaluacion, auditoria o contratacion;
- comunicados humanitarios, datos de OCHA, bases sectoriales o informacion local;
- cobertura periodistica y contexto de terreno.

El objetivo es formar una cadena de evidencia: dato declarado, fuente primaria, fecha, limite y corroboracion independiente.

## Limitaciones y falsos positivos

IATI mejora la transparencia, pero no elimina los problemas de calidad de datos. Algunas organizaciones publican con mas detalle que otras; unas actualizan antes, otras despues; y no todos los campos disponibles en el estandar aparecen completos en cada actividad.

Conviene vigilar especialmente:

- **Cobertura desigual**: que una organizacion o actividad no aparezca no prueba que no exista.
- **Retrasos**: el Datastore puede procesar datos despues de que esten disponibles en el registro, y cada publicador tiene su propio ritmo.
- **Doble conteo**: un flujo puede pasar por donante, intermediario e implementador; sumar todas las declaraciones puede inflar el total.
- **Campos narrativos**: buscar texto libre por `title` o `description` puede perder sinonimos, traducciones o abreviaturas.
- **Ubicaciones sensibles**: una localizacion declarada puede ser aproximada, agregada o deliberadamente prudente.
- **Resultados e impacto**: que exista una actividad o transaccion no equivale a impacto verificado sobre el terreno.

En investigaciones publicables, la frase "segun datos IATI publicados por..." suele ser mas honesta que "se gasto..." si no has contrastado contabilidad, ejecucion y evidencia local.

## Buenas practicas de OPSEC, etica y privacidad

La ayuda humanitaria trabaja con poblaciones vulnerables. Eso cambia el umbral de publicacion. Una investigacion responsable debe evitar que una visualizacion bonita exponga campamentos, beneficiarios, rutas logisticas, personal local o comunidades en riesgo.

Buenas reglas:

- no publiques coordenadas sensibles si no aportan valor publico claro;
- agrega resultados cuando el detalle pueda poner a alguien en riesgo;
- evita inferir fraude por huecos de datos sin pedir contexto;
- conserva capturas, fechas de consulta y consultas usadas;
- separa hechos observados, inferencias y preguntas pendientes;
- contacta a las organizaciones afectadas antes de publicar acusaciones relevantes;
- revisa licencias, atribucion y condiciones de uso de cada dataset complementario.

La prudencia no debilita el analisis. Lo hace defendible.

## Alternativas y siguientes pasos

IATI encaja bien cuando la pregunta gira alrededor de financiacion, proyectos, organizaciones, sectores y resultados declarados. Segun el caso, puede complementarse con:

- `OCHA` y portales humanitarios para contexto operativo;
- registros de contratacion publica cuando la pregunta baja a proveedores;
- presupuestos nacionales y sistemas `AIMS` si el pais receptor integra datos de ayuda;
- `OpenRefine` para limpiar nombres de organizaciones y sectores;
- `OpenSanctions` y registros mercantiles solo si hay una pregunta legitima de riesgo o debida diligencia;
- `Datasette` o `SQLite` para conservar consultas reproducibles.

El takeaway practico es sencillo: usa `IATI` para **ordenar preguntas sobre ayuda y desarrollo con datos declarados, descargables y trazables**, no para saltar directamente a una conclusion moral o penal. Si una actividad parece importante, el siguiente paso sano es comprobar que publicador, fecha, tipo de importe, documento y contexto local cuentan realmente la misma historia.

## Fuentes consultadas

- [International Aid Transparency Initiative](https://iatistandard.org/)
- [How do I use IATI data?](https://iatistandard.org/en/using-data/how-to-use-iati-data/)
- [IATI Datastore](https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/)
- [How to use the Datastore API](https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/how-to-use-the-datastore-api/)
- [Activity Standard 2.03](https://iatistandard.org/en/iati-standard/203/activity-standard/)
- [Organisation Standard 2.03](https://iatistandard.org/en/iati-standard/203/organisation-standard/)
