---
title: "BBOT en OSINT: recursion, presets y scope para automatizar sin perder el control"
slug: /bbot-osint-recursion-presets-scope
authors: [osint-writter]
tags: [osint, tools, investigation, tradecraft, privacy]
date: 2026-04-04
image: /img/blog/2026-04-04-bbot-osint-recursion-presets-scope.png
---

![Ilustracion editorial de un analista OSINT trabajando con BBOT, presets modulares, grafo de eventos y limites de alcance bien definidos](/img/blog/2026-04-04-bbot-osint-recursion-presets-scope.png)

Hay herramientas que prometen "sacar todo" de un dominio, una URL o una organizacion. El problema no es que se queden cortas. El problema real es que **mezclan hallazgos heterogeneos, empujan al analista a correr demasiadas cosas a la vez y hacen dificil explicar despues que se descubrio, con que alcance y con que nivel de confianza**. `BBOT` resulta interesante porque intenta resolver justo eso: automatizar la expansion de una investigacion sin convertirla en un escaneo impulsivo.

En un flujo defensivo u OSINT responsable, eso importa mucho. No se trata de lanzar modulos agresivos "por si acaso", sino de elegir un preset, dejar claro el scope y tratar cada nuevo dato como un evento que merece contexto. `BBOT` puede servir para inventario de activos, due diligence tecnica, mapeo inicial de infraestructura y apoyo a investigaciones periodisticas o corporativas. No debe usarse para acosar, doxxear ni hostigar personas, y tampoco para ejecutar pruebas activas sobre sistemas ajenos sin autorizacion.

<!-- truncate -->

## Que es y para que sirve

El repositorio oficial describe `BBOT` como un escaner multiproposito inspirado por `SpiderFoot`, pensado para automatizar tareas de `recon`, bug bounty y ASM. Esa definicion conviene traducirla a lenguaje operativo: **no es solo una lista de modulos**, sino una forma de encadenar objetivos, descubrimientos y enriquecimientos sin tener que rehacer el flujo en cada caso.

Una de sus ideas mas utiles para OSINT tecnico es que acepta varios tipos de target desde el principio. Segun la documentacion oficial, puedes partir de un dominio, una IP, un rango, una URL, un correo, una organizacion, un username e incluso ciertos artefactos mas especificos. Eso cambia la conversacion metodologica: en vez de pensar "que herramienta toca ahora", puedes pensar "que entidad inicial tengo y que caminos de expansion tienen sentido".

Tambien ayuda su enfoque basado en `presets`. La documentacion de `BBOT` explica que un preset en YAML puede reunir targets, modulos, salidas y opciones de configuracion en una sola pieza reutilizable. Para un analista responsable, esto vale oro: te obliga a declarar de antemano el tipo de recogida que quieres hacer, en vez de improvisar veinte banderas en caliente.

## Caso de uso legitimo con ejemplo ficticio

Imagina una revision defensiva sobre la empresa ficticia `orbita-civica.example`. El objetivo no es "exprimir internet", sino responder preguntas concretas:

- que subdominios publicos merecen inventario;
- que correos aparecen expuestos en fuentes abiertas;
- y que rutas de descubrimiento deberian quedarse en modo pasivo antes de plantear comprobaciones adicionales.

Con esa premisa, un arranque prudente podria ser tan simple como este:

```bash
bbot -t orbita-civica.example -p subdomain-enum -rf passive
```

Ese detalle, `-rf passive`, importa porque reduce el impulso de mezclar recoleccion pasiva con pruebas mas intrusivas. En OSINT serio, el orden importa: primero orientas superficie y contexto; despues decides si hace falta algo mas. Saltarte ese orden suele generar ruido y, peor aun, hallazgos dificiles de defender ante un tercero.

## Flujo recomendado

### 1. Arranca por la entidad, no por el modulo mas espectacular

Si tu selector inicial es un dominio, el preset `subdomain-enum` suele tener mas sentido que un preset de web mas pesado. Si partes de una URL concreta, conviene pensar antes si necesitas expansion alrededor del host o solo documentar esa ruta. La clave es que `BBOT` te deja adaptar el arranque al tipo de target en vez de forzarte a un unico recorrido.

### 2. Declara el preset como una hipotesis metodologica

La documentacion oficial insiste en que los presets pueden agrupar configuracion, modulos y salidas. Leido desde una perspectiva investigadora, un preset no es solo comodidad: es una **declaracion previa de intencion**. Si usas uno ligero, tu expectativa debe ser descubrimiento inicial. Si activas presets mas amplios o cadenas de modulos, el nivel de riesgo, ruido y validacion posterior sube.

Un ejemplo prudente para trabajo repetible seria mantener un preset propio con:

- solo fuentes pasivas;
- salida a `JSON` o `SQLite`;
- y notas claras sobre que modulos quedan explicitamente fuera.

La propia documentacion recomienda revisar la configuracion final con `--current-preset`. Ese paso es mas importante de lo que parece: evita creer que estas ejecutando una version "light" cuando en realidad una inclusion o sobreescritura ha metido mas cosas de las previstas.

### 3. Trata la salida como material de trabajo, no como veredicto

El `README` y la documentacion de `output` muestran que `BBOT` puede enviar resultados a formatos y destinos como `JSON`, `CSV`, `SQLite`, `Neo4j`, `Splunk` o `Elasticsearch`. Eso es potente, pero tambien peligroso si no pones disciplina. Exportar mas bonito no convierte una observacion en evidencia firme.

La practica sana es separar tres niveles:

- descubrimiento: una senal encontrada por un modulo;
- corroboracion: una pieza validada con una fuente externa o una segunda via independiente;
- conclusion: una afirmacion que ya puede entrar en informe.

### 4. Reserva lo agresivo para contexto autorizado

El propio proyecto documenta presets mucho mas intensos, incluido `kitchen-sink` con `--allow-deadly`. Eso no deberia verse como una invitacion a "probarlo todo", sino como una advertencia metodologica: si una receta necesita una bandera que reconoce explicitamente riesgo o agresividad, tu pregunta deberia ser por que la necesitas y si tienes autorizacion para ello.

En un blog OSINT responsable, la respuesta suele ser clara: para investigacion abierta y defensiva general, primero usa expansion limitada, salidas trazables y corroboracion manual. Lo demas pertenece a contextos muy concretos, con permisos y objetivos bien definidos.

## Limitaciones y falsos positivos

`BBOT` ahorra tiempo, pero no sustituye criterio. Hay varias trampas comunes:

- un subdominio historico puede seguir apareciendo aunque ya no represente un activo vivo;
- un correo descubierto en una pagina antigua puede no describir la exposicion actual;
- una relacion entre entidades puede ser solo tecnica o circunstancial, no una vinculacion fuerte;
- y un grafo bonito puede hacer que un resultado parezca mas solido de lo que realmente es.

Ademas, cuanto mas modular y recursivo es el flujo, mas facil resulta olvidar que cada modulo hereda supuestos, sesgos y limitaciones de sus fuentes. Si una API esta desactualizada, si una busqueda web devolvio basura o si el preset estaba sobredimensionado, el problema no desaparece por agregacion: se multiplica.

## Buenas practicas de OPSEC, etica y privacidad

- Define por escrito que entidades entran en scope y cuales no.
- Prioriza presets y modulos pasivos cuando el objetivo sea OSINT o inventario defensivo.
- Conserva salida estructurada para poder reconstruir de donde salio cada pista.
- No mezcles descubrimiento tecnico con atribucion personal sin una segunda y tercera corroboracion.
- Si el caso toca personas fisicas, minimiza datos y evita publicar detalles innecesarios.
- Si una comprobacion pasa de observacion publica a interaccion activa, detente y revisa permisos.

## Alternativas y siguientes pasos

Si buscas una experiencia mas visual de grafo desde el arranque, `Maltego` sigue siendo una referencia. Si prefieres una herramienta muy centrada en automatizacion OSINT clasica, `SpiderFoot` sigue siendo util para ciertos flujos. Y si lo que necesitas es una disciplina fuerte de workspace, entidades y modulos con sabor mas "framework", `sn0int` encaja muy bien.

La aportacion particular de `BBOT` esta en otra parte: **pensar una investigacion como una cadena de eventos expandible, con presets reutilizables y salidas preparadas para analisis posterior**. Si lo usas asi, puede ser una pieza valiosa. Si lo usas como boton de "hazme todo", solo conseguiras ruido a gran velocidad.

La leccion accionable es simple: el siguiente salto de calidad en OSINT tecnico no suele venir de activar mas modulos, sino de declarar mejor el alcance, reducir el ruido y documentar por que cada pivote merecia existir.

## Fuentes oficiales y recomendadas

- [BBOT en GitHub (README oficial)](https://github.com/blacklanternsecurity/bbot)
- [BBOT Docs: Getting Started](https://www.blacklanternsecurity.com/bbot/Stable/)
- [BBOT Docs: Presets](https://www.blacklanternsecurity.com/bbot/Dev/scanning/presets/)
- [BBOT Docs: Output](https://www.blacklanternsecurity.com/bbot/Dev/scanning/output/)
