---
title: "Lampyre en OSINT: grafos, entidades y macros para investigar con mas contexto"
slug: /lampyre-osint-grafos-entidades-macros-contexto
authors: [osint-writter]
tags: [osint, tooling, link-analysis, methodology, geoint, investigation]
date: 2026-05-13
image: /img/blog/2026-05-13-lampyre-osint-grafos-entidades-macros-contexto.png
---

![Ilustracion editorial de una analista OSINT construyendo un grafo con entidades, mapas y tablas a partir de fuentes publicas](/img/blog/2026-05-13-lampyre-osint-grafos-entidades-macros-contexto.png)

Hay investigaciones que se rompen por un motivo poco espectacular: cada hallazgo vive en un sitio distinto. Una tabla con dominios por un lado, capturas de mapa por otro, relaciones dibujadas deprisa en una libreta y notas dispersas sobre que pivote salio de donde. `Lampyre` resulta util justo en ese punto, porque propone algo mas disciplinado que "abrir mas pestañas": **convertir datos en entidades, mapearlos a grafos y lanzar tareas repetibles sin perder el contexto del caso**.

La documentacion oficial ayuda a colocar bien la herramienta. `Lampyre` usa la plataforma `Lighthouse` para ejecutar peticiones analiticas y su propia API en Python permite extender el sistema con tareas personalizadas. Ademas, esa misma documentacion subraya un detalle importante para OPSEC: esas tareas pueden ejecutarse en tu propia maquina y no dependen de la infraestructura de red de `Lampyre`. Traducido a trabajo serio: sirve para **ordenar y enriquecer una investigacion**, no para saltarte la necesidad de definir alcance, contrastar fuentes y separar observacion de inferencia.

<!-- truncate -->

## Que es y para que sirve

`Lampyre` es una plataforma orientada a modelar investigaciones como tablas, entidades, enlaces, mapas y grafos en un mismo flujo. La capa `Lighthouse` describe las peticiones analiticas como `Tasks`, escritas en Python, con sus parametros de entrada, sus tablas de salida y sus esquemas de visualizacion.

Eso lo vuelve interesante para preguntas como estas:

- como paso de una tabla de resultados a un grafo legible sin rehacer el trabajo a mano;
- como reutilizo entidades del sistema para dominios, IPs, ubicaciones o perfiles;
- como lanzo una tarea desde un objeto ya presente en el caso;
- y como mantengo una investigacion local, reproducible y menos dependiente de servicios externos.

La pieza metodologica importante no es "ver muchos nodos". Es mantener una cadena de transformacion defendible: dato de entrada, tarea ejecutada, tabla generada, esquema aplicado y pivote posterior.

## Caso de uso legitimo con ejemplo ficticio

Imagina una investigacion defensiva sobre una empresa ficticia llamada `Puerto Azul Media`. El equipo quiere revisar su huella publica antes de una `due diligence` tecnica y ya tiene varios materiales legitimos:

- una lista de dominios y subdominios conocidos;
- algunas IPs observadas en historicos internos;
- resultados previos de una busqueda cartografica o de infraestructura;
- y la necesidad de explicarle a otra persona por que ciertos nodos quedaron conectados.

En un flujo asi, `Lampyre` no es valioso por "automatizarlo todo". Aporta valor porque puedes:

- importar o generar una tabla estructurada;
- mapear campos a objetos y enlaces concretos;
- desplegar ese resultado en grafo, tabla, mapa o cronologia;
- y relanzar tareas o macros desde el propio workspace cuando aparece un nuevo pivote.

Eso reduce uno de los errores mas comunes en OSINT tecnico: tener intuiciones correctas, pero no una narrativa reproducible de como llegaste a ellas.

## Flujo recomendado

### 1. Empieza por la pregunta, no por el grafo

`Lampyre` puede resultar vistoso, pero conviene entrar con una hipotesis humilde. Antes de crear entidades o cargar resultados, define que quieres comprobar: relacion entre dominios e IPs, contexto geografico de un hallazgo, o expansion de una tabla hacia enlaces mas legibles. Si no haces eso, la plataforma solo te ayudara a dibujar ruido con mejor aspecto.

### 2. Modela bien la tabla de salida

La documentacion de `Lighthouse` insiste en que la tabla es la pieza central de cualquier tarea. Ese detalle importa mucho: si los encabezados, tipos y fechas estan mal pensados, el grafo posterior tambien lo estara. Un analista prudente define primero:

- que columnas representan hechos observados;
- cuales son atributos identificadores;
- y que valores deben conservar fecha, coordenadas o procedencia.

### 3. Usa esquemas para no duplicar razonamiento

La documentacion de `Task schemas` explica que un esquema describe como convertir columnas de una tabla en objetos y enlaces de un grafo. Tambien deja una idea muy util: el mismo mapeo puede aprovecharse a la vez en grafo, mapa, cronologia y tabla. Eso ayuda a trabajar mejor cuando un caso necesita varias vistas del mismo dato en lugar de exportaciones manuales y contradictorias.

En la practica, esto te permite pasar de "tengo filas" a "tengo relaciones" sin reetiquetar todo cada vez que cambias de vista.

### 4. Reutiliza la ontologia del sistema cuando tenga sentido

La documentacion de `Ontology` explica que `Lampyre` ya trae entidades y enlaces del sistema, incluyendo objetos como `IP`, `Domain` y otros tipos comunes. Eso evita reinventar tipos basicos y te permite mantener consistencia entre tareas distintas.

La recomendacion practica es sencilla:

- usa objetos del sistema para lo comun;
- crea tipos propios solo cuando el caso lo pida;
- y documenta que atributo identifica de verdad a cada entidad para no fusionar nodos distintos por error.

### 5. Reserva las macros para pivotes repetibles

La documentacion de `Macros` las presenta como una forma de lanzar tareas desde el menu contextual de entidades en grafo o mapa, enriqueciendo el workspace con el resultado. Bien usadas, son una ayuda fuerte para repetibilidad; mal usadas, son una maquina de inflar el caso con consultas reflejas.

Una buena regla operativa es esta: crea o usa macros solo para pivotes que ya hayas validado como utiles y legitimos dentro del alcance del caso.

## Limitaciones y falsos positivos

`Lampyre` no elimina los problemas clasicos del OSINT. Solo los vuelve mas visibles si trabajas con disciplina.

Los errores tipicos suelen aparecer cuando:

- unificas entidades distintas porque comparten un atributo pobre;
- conviertes un mapa o un grafo bonito en una conclusion cerrada;
- mezclas datos de momentos diferentes sin etiquetar temporalidad;
- o lanzas tareas encadenadas sin revisar si el pivote sigue teniendo sentido.

Tambien conviene recordar que la documentacion oficial distingue claramente entre la ejecucion de la tarea y la construccion del grafo. La tarea rellena tablas; luego `Lampyre` crea visualizaciones a partir de ese resultado. Metodologicamente eso es bueno, porque te obliga a pensar primero en la calidad del dato y despues en su representacion.

## Buenas practicas de OPSEC, etica y privacidad

El detalle mas util de la documentacion oficial para un analista prudente es que las tareas de `Lighthouse` pueden ejecutarse en modo local y no usan la infraestructura de red de `Lampyre`. Eso no resuelve por si solo todos los riesgos, pero si ayuda a plantear mejor ciertos casos sensibles.

Buenas practicas razonables:

- trabaja solo con objetivos propios, autorizados o legitimamente investigables;
- minimiza datos personales cuando no sean necesarios para responder la pregunta;
- conserva procedencia y fecha en cada tabla o exportacion;
- marca que es dato observado, que es inferencia y que sigue pendiente de validar;
- y no conviertas una capacidad de automatizacion en licencia para ampliar alcance sin justificacion.

OSINT responsable no consiste en ver cuantas entidades puedes dibujar. Consiste en dejar un rastro metodologico que otra persona pueda auditar.

## Alternativas y siguientes pasos

Si tu prioridad es solo buscar infraestructura publica, herramientas como `Censys`, `Netlas`, `ZoomEye` o `FOFA` pueden darte respuestas mas directas. Si lo que necesitas es mas bien una capa de analisis visual y enlace sobre datasets heterogeneos, `Maltego` sigue siendo una referencia. Y si el problema principal es preservar navegacion o evidencia web, conviene mirar antes a `Hunchly`, `ArchiveBox` o flujos WARC.

Donde `Lampyre` encaja mejor es en este punto intermedio: cuando quieres **convertir consultas, tablas y APIs en un workspace analitico coherente**, con vistas multiples y posibilidad de extender la herramienta con tareas propias.

La takeaway accionable es simple: usa `Lampyre` para mejorar la trazabilidad del caso, no para adornar relaciones debiles. Si una entidad, un enlace o un mapa no te ayudan a explicar mejor el origen del hallazgo, sobran aunque queden bien en pantalla.

Como siguiente puente editorial del blog, tendria sentido bajar a un tutorial mas acotado: por ejemplo, una comparativa entre `Lampyre`, `Maltego` y `Datasette` segun tipo de caso, o un flujo practico de infraestructura web cruzando grafo, tabla y cronologia.

## Fuentes

- [Lighthouse: What is Lighthouse](https://lampyre.io/python-api-doc/lighthouse_intro/what_is_lighthouse_and_request.html)
- [Lighthouse: Your first task](https://lampyre.io/python-api-doc/lighthouse_intro/hello_task.html)
- [Lighthouse: Task execution process](https://lampyre.io/python-api-doc/api_explained/execution_process.html)
- [Lighthouse: Task schemas](https://lampyre.io/python-api-doc/api_explained/schemas.html)
- [Lighthouse: Ontology](https://lampyre.io/python-api-doc/api_explained/ontology.html)
- [Lighthouse: Macros](https://lampyre.io/python-api-doc/task_tutorial_advanced/macros.html)
- [Lighthouse: WiGLE task example](https://lampyre.io/python-api-doc/task_tutorial/wigle_task.html)
