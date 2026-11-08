---
title: "GUAC en OSINT: conectar metadatos de la cadena de suministro sin confundir el grafo con la verdad"
slug: /guac-grafo-cadena-suministro-osint
authors: [osint-writter]
tags: [osint, tooling, link-analysis, verification, data, investigation]
date: 2026-11-08
image: /img/blog/2026-11-08-guac-grafo-cadena-suministro.png
aiDisclosure: generated
humanReviewed: false
---

Un aviso atribuye una vulnerabilidad a una dependencia transitiva. El SBOM dice que el paquete existe, una atestación enlaza un binario con una compilación y una ficha VEX declara que el producto no está afectado. Cada documento parece razonable por separado, pero la decisión depende de cómo se relacionan **ese artefacto, esa versión, esa ruta de dependencia y esa afirmación**. Copiar datos entre hojas de cálculo puede ocultar justo el salto que hay que verificar. Un grafo ayuda a encontrarlo; no convierte el salto en un hecho.

![Analista examinando documentos de cadena de suministro conectados en un grafo de evidencia](/img/blog/2026-11-08-guac-grafo-cadena-suministro.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo presenta un uso responsable de **GUAC (Graph for Understanding Artifact Composition)** como apoyo a investigaciones OSINT y de debida diligencia sobre software público, propio o analizado con autorización. El ejemplo es ficticio. No requiere explotar vulnerabilidades, sondear sistemas ajenos ni recopilar datos personales de mantenedores.

## Qué es GUAC y para qué sirve

[GUAC](https://docs.guac.sh/guac/) agrega metadatos de seguridad de la cadena de suministro, normaliza entidades y representa relaciones entre paquetes, artefactos, repositorios, dependencias, vulnerabilidades, SBOM y procedencia. Su lugar no es el de otro escáner, sino el de una capa de **agregación y síntesis** sobre documentos y servicios que ya producen afirmaciones.

La documentación oficial enumera, entre otras, entradas en CycloneDX, SPDX, OSV, OpenSSF Scorecard, SLSA, in-toto, CSAF/VEX y OpenVEX. GUAC puede enriquecer el grafo mediante integraciones como `deps.dev` y exponerlo para consultas y visualización. Eso permite formular preguntas que cruzan varios documentos:

- ¿qué camino conecta un paquete usado por el producto con una vulnerabilidad conocida?;
- ¿qué artefacto procede de qué fuente o proceso de construcción?;
- ¿qué SBOM describe al sujeto consultado y cuándo se generó?;
- ¿qué afirmación VEX afecta a ese paquete o artefacto concreto?;
- ¿qué sabemos y qué sigue ausente sobre una versión determinada?

La [ontología de GUAC](https://docs.guac.sh/guac/guac-ontology/) separa objetos —paquetes, fuentes, artefactos, constructores o vulnerabilidades— de evidencias que los relacionan. Esta distinción es útil para investigar: una arista no debería leerse como una verdad desnuda, sino como una afirmación con origen, recolector, justificación y momento.

### Lo que un grafo no demuestra

Que dos nodos estén conectados no prueba automáticamente que:

- el SBOM corresponda al binario recibido;
- dos nombres parecidos designen el mismo paquete;
- una dependencia declarada esté presente o se cargue en ejecución;
- una vulnerabilidad sea explotable en la configuración analizada;
- una atestación sea auténtica, confiable o suficiente;
- una ausencia en el grafo equivalga a una ausencia en el producto.

El propio proyecto advierte que los identificadores no siempre están disponibles y que algunas vinculaciones requieren heurísticas, con posibles casos límite y errores de ingestión. Por eso, en OSINT, GUAC funciona mejor como **mapa interrogable de afirmaciones y procedencia** que como motor de veredictos.

## Caso de uso legítimo: reconstruir una ruta de riesgo

La entidad ficticia **Biblioteca del Estuario** evalúa una aplicación documental antes de desplegarla. Ha recibido, dentro de un proceso autorizado:

1. una imagen de contenedor fijada por digest;
2. un SBOM CycloneDX del proveedor;
3. una atestación de procedencia de compilación;
4. avisos públicos de vulnerabilidades;
5. una declaración VEX para una de ellas.

Un escáner señala que `visor-ejemplo@3.4.1` depende transitivamente de `parser-demo@1.8.0`, asociado a `CVE-20XX-12345`. Los nombres y el identificador son ficticios. La pregunta no es «¿hay una vulnerabilidad en el grafo?», sino:

> ¿Qué cadena de evidencias enlaza el artefacto recibido con la versión afectada, qué parte procede de cada fuente y qué incertidumbre impide todavía decidir?

Tras ingerir copias controladas de los documentos, el equipo obtiene una ruta candidata:

```text
artefacto por digest
  -> descrito por SBOM A
  -> contiene paquete visor-ejemplo@3.4.1
  -> depende de parser-demo@1.8.0
  -> asociado a CVE-20XX-12345
  -> sujeto de una declaración VEX "not_affected"
```

La ruta reduce el espacio de búsqueda, pero cada flecha necesita una lectura propia:

| Relación | Fuente | Pregunta de validación |
| --- | --- | --- |
| artefacto → SBOM | documento del proveedor | ¿el SBOM identifica este digest o una entrega distinta? |
| SBOM → paquete | inventario declarado | ¿el componente está realmente presente y cómo se identificó? |
| paquete → dependencia | SBOM o enriquecimiento externo | ¿la relación corresponde a esta versión, ecosistema y resolución? |
| paquete → vulnerabilidad | base de avisos | ¿el rango afectado y los alias coinciden sin ambigüedad? |
| sujeto → VEX | declaración del emisor | ¿el sujeto es el mismo artefacto y la justificación sigue vigente? |

El resultado puede ser una conclusión provisional: la ruta de dependencia está declarada y el aviso incluye esa versión, pero el VEX usa un identificador de producto que no enlaza inequívocamente con el digest recibido. El siguiente trabajo no es «buscar más nodos», sino pedir o producir evidencia que resuelva ese enlace.

## Flujo recomendado paso a paso

### 1. Escribe la decisión y fija el sujeto

Antes de desplegar una plataforma, define qué decisión debe apoyar. «Explorar la cadena de suministro» es demasiado amplio. Una pregunta mejor sería: «determinar si el artefacto con este digest requiere mitigación por estas vulnerabilidades antes de su aceptación».

Registra el sujeto con el identificador más estable disponible: digest del artefacto, PURL completo con versión, referencia de imagen o commit. Conserva también nombre original, origen, fecha y alcance. Un grafo rico construido sobre un sujeto ambiguo solo hace más convincente la ambigüedad.

### 2. Conserva los originales antes de ingerirlos

Guarda cada SBOM, aviso o atestación tal como se recibió y calcula su hash. Registra:

- URL o canal de origen;
- fecha de obtención y, si existe, fecha de emisión;
- tipo y versión del formato;
- identidad declarada del emisor;
- firma y resultado de verificación, si procede;
- condiciones de acceso y redistribución.

La ingestión normaliza información. Para poder auditar una arista, debes conservar el documento previo a esa transformación.

### 3. Empieza con un corpus pequeño y conocido

La documentación ofrece un arranque local y componentes para recoger, ingerir, consultar y visualizar datos. Para una primera evaluación, evita activar todos los enriquecimientos a la vez. Carga uno o dos artefactos y documentos cuyo contenido puedas revisar manualmente.

Comprueba entonces que:

- el número y tipo de sujetos son plausibles;
- las versiones no se han perdido durante la normalización;
- los identificadores pertenecen al ecosistema correcto;
- las relaciones decisivas conservan origen y justificación;
- una nueva ingestión no crea duplicados inesperados.

Solo después amplía el corpus. Esto permite distinguir un problema del documento, del recolector, de la normalización o de la consulta.

### 4. Separa evidencia aportada de enriquecimiento

Una relación extraída del SBOM del proveedor y otra recuperada de un servicio público pueden coincidir, pero no tienen la misma procedencia. Etiqueta al menos:

| Clase | Ejemplo | Lectura prudente |
| --- | --- | --- |
| evidencia primaria del caso | SBOM entregado con el artefacto | declaración del productor sobre su producto |
| observación independiente | SBOM generado sobre una copia autorizada | resultado de una herramienta y configuración concretas |
| enriquecimiento público | dependencias de `deps.dev` u OSV | contexto externo sujeto a cobertura y frescura |
| inferencia local | igualdad entre dos identificadores | hipótesis que exige justificación y revisión |

La integración oficial con [`deps.dev`](https://docs.guac.sh/guac/certifier-deps-dev/) puede mapear repositorios, resultados de Scorecard y árboles de dependencias de ecosistemas públicos. Sus límites también están documentados: necesita versiones explícitas en los PURL, depende de la cobertura del servicio y no resuelve paquetes privados o ecosistemas no indexados.

### 5. Consulta caminos, no solo coincidencias

La interfaz y las herramientas de GUAC permiten buscar vulnerabilidades a través de dependencias transitivas. Una coincidencia final es útil para priorizar, pero la investigación debe conservar el camino completo:

```text
sujeto inicial → relación 1 → nodo intermedio → relación 2 → hallazgo
```

Para cada tramo, exporta o registra:

- identificadores completos y versiones;
- tipo de relación;
- documento o servicio de origen;
- recolector y fecha;
- justificación disponible;
- estado de validación: confirmado, contradicho, inconcluso o caducado.

Evita construir automatizaciones duraderas sobre identificadores internos de nodo. La documentación de GraphQL indica que son opacos y específicos de cada instancia. Las consultas topológicas y algunas directivas también están marcadas como experimentales; revisa el esquema efectivo de tu despliegue antes de asumir estabilidad.

### 6. Valida la identidad en los pivotes decisivos

Los falsos positivos más costosos suelen nacer de unir entidades que solo parecen iguales. Antes de aceptar una ruta:

1. compara ecosistema, namespace, nombre, versión y calificadores del PURL;
2. contrasta digests cuando existan;
3. revisa alias de vulnerabilidad en fuentes primarias;
4. distingue paquete, artefacto, repositorio y producto comercial;
5. documenta cualquier equivalencia añadida manualmente;
6. busca evidencia que pueda refutar la unión, no solo confirmarla.

Una relación de igualdad puede ser evidencia en el grafo, pero debe seguir teniendo procedencia y justificación. «El nombre coincide» rara vez basta.

### 7. Corrobora fuera del grafo

GUAC organiza el trabajo; la conclusión sigue dependiendo de las fuentes. Para una ruta prioritaria:

- abre el aviso original y verifica rangos y fechas;
- comprueba el sujeto del SBOM y su vínculo con el artefacto;
- valida firmas o atestaciones con la política aplicable;
- compara la dependencia declarada con una observación autorizada;
- evalúa el VEX en contexto, incluida su justificación y caducidad;
- conserva discrepancias sin resolverlas por mayoría de fuentes.

Si el grafo dice que no existe un camino, formula la conclusión como «no se encontró con las fuentes, configuración y fecha indicadas». No como «el camino no existe».

### 8. Convierte la consulta en un producto reproducible

Entrega algo más útil que una captura del visualizador. El registro mínimo debería incluir:

- pregunta y alcance;
- sujeto inicial fijado por identificador;
- fuentes y hashes ingeridos;
- versión o referencia del despliegue y configuración relevante;
- consulta ejecutada;
- camino resultante con procedencia por arista;
- comprobaciones externas;
- incertidumbres, contradicciones y cobertura ausente;
- decisión, responsable y condición de reapertura.

Así, una actualización del SBOM o de una base de vulnerabilidades puede compararse con un estado anterior sin reescribir la historia.

## Limitaciones y falsos positivos

### Normalización equivocada

Mayúsculas, namespaces, calificadores, forks o convenciones de versión pueden separar entidades idénticas o unir entidades diferentes. Revisa manualmente los enlaces que cambian una decisión.

### Cobertura desigual

Un enriquecedor puede cubrir npm y PyPI con detalle y no conocer un ecosistema interno. La falta de aristas refleja la cobertura de las fuentes y del despliegue, no necesariamente la composición real.

### Frescura no uniforme

El SBOM, el aviso, Scorecard, la atestación y el VEX pueden representar momentos distintos. Una ruta correcta ayer puede quedar obsoleta tras una nueva compilación o un aviso revisado.

### Dependencia no equivale a ejecución

Una dependencia transitiva puede no empaquetarse, cargarse o alcanzar la ruta vulnerable. GUAC ayuda a localizar la relación declarada; demostrar presencia o explotabilidad exige evidencia adicional.

### Procedencia no equivale a confianza

Saber de dónde viene una afirmación permite evaluarla, pero no obliga a creerla. Dos aristas con el mismo origen tampoco son dos corroboraciones independientes.

### La visualización seduce

Los grafos densos parecen exhaustivos. Una ruta coloreada puede ocultar una equivalencia heurística, y un área vacía puede ser solo una fuente no configurada. Prioriza tablas de procedencia y estados de evidencia sobre la estética del diagrama.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con metadatos públicos, productos propios o material para el que exista autorización expresa.
- No conviertas la investigación de dependencias en escaneo activo de infraestructura de terceros.
- Despliega localmente cuando los SBOM, nombres de paquetes o repositorios internos sean sensibles.
- No envíes documentos privados a enriquecedores externos sin revisar autorización, retención y exposición de metadatos.
- Usa cuentas y credenciales de solo lectura; separa la plataforma de investigación de entornos de producción.
- Minimiza nombres, correos y otras identidades personales que no sean necesarias para evaluar el software.
- Protege GraphQL, REST, visualizadores y bases persistentes: el grafo puede revelar una cartografía valiosa de dependencias y debilidades.
- Registra qué conectores realizan llamadas salientes y aplica límites, caché y revisión de términos de uso.
- No atribuyas intención maliciosa a partir de una inconsistencia entre documentos.
- Coordina una divulgación responsable si el análisis descubre un riesgo no público que afecte a terceros.

## Checklist operativo

- [ ] La pregunta de decisión y el sujeto están definidos.
- [ ] El artefacto está fijado por digest, origen y fecha.
- [ ] Los documentos originales y sus hashes se conservan fuera del grafo.
- [ ] Cada fuente y enriquecedor tiene cobertura y límites documentados.
- [ ] Las versiones e identidades decisivas se han validado manualmente.
- [ ] Cada arista crítica conserva origen, recolector y justificación.
- [ ] El camino completo acompaña al hallazgo final.
- [ ] Las relaciones heurísticas están separadas de las confirmadas.
- [ ] Las ausencias se expresan como límites de observación.
- [ ] Las conclusiones se corroboran en fuentes primarias.
- [ ] El informe incluye incertidumbre, caducidad y eventos de reapertura.
- [ ] El despliegue protege metadatos internos, APIs y credenciales.

## Alternativas y siguientes pasos

GUAC resulta útil cuando varias clases de metadatos deben cruzarse de forma repetible. Para un caso pequeño, una tabla con identificadores, procedencia y relaciones puede ser más fácil de revisar. Para explorar solo dependencias públicas, `deps.dev` ofrece contexto directo; para vulnerabilidades de paquetes, OSV y sus herramientas pueden bastar; para inventariar un único artefacto, un generador de SBOM y una revisión manual reducen complejidad.

Ninguna alternativa elimina la pregunta central: **¿qué fuente sostiene cada enlace y qué observación podría refutarlo?** El valor de GUAC aparece cuando esa disciplina se conserva a escala.

El takeaway práctico es este: **usa el grafo para descubrir y explicar rutas de evidencia, no para fabricar certeza por conectividad**. Empieza con un artefacto conocido, ingiere pocas fuentes, audita cada unión decisiva y automatiza solo después de entender los errores posibles. Como siguiente tema, convendría estudiar pruebas de contrato para conectores de metadatos: cómo detectar que una fuente cambió de esquema o semántica antes de que el grafo produzca silencios convincentes.

## Fuentes oficiales consultadas

- [GUAC: documentación y casos de uso](https://docs.guac.sh/guac/)
- [GUAC: repositorio oficial, formatos soportados y límites de vinculación](https://github.com/guacsec/guac)
- [GUAC: ontología del grafo](https://docs.guac.sh/guac/guac-ontology/)
- [GUAC: definiciones GraphQL y estado experimental de consultas topológicas](https://docs.guac.sh/guac/graphql/)
- [GUAC: integración oficial con deps.dev](https://docs.guac.sh/guac/certifier-deps-dev/)

