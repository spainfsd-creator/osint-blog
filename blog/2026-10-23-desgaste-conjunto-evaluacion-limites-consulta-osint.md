---
title: "Desgaste del conjunto de evaluación en OSINT: límites de consulta sin enseñar el examen"
slug: /desgaste-conjunto-evaluacion-limites-consulta-osint
authors: [osint-writter]
tags: [osint, methodology, verification, automation, privacy]
date: 2026-10-23
image: /img/blog/2026-10-23-desgaste-conjunto-evaluacion-limites-consulta-osint.png
aiDisclosure: generated
humanReviewed: false
---

El equipo no ha abierto ni una sola fila del corpus reservado. Solo ha preguntado veinte veces si su extractor mejora y ha recibido veinte porcentajes. En la iteración veintiuna, el resultado es magnífico. **El conjunto sigue cerrado, pero ya ha enseñado parte del examen a través de sus respuestas.**

![Archivo de evaluación sellado que entrega respuestas limitadas a varios equipos mediante un punto de control](/img/blog/2026-10-23-desgaste-conjunto-evaluacion-limites-consulta-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Un conjunto de evaluación se desgasta cuando sus resultados influyen repetidamente en qué reglas, prompts, umbrales o pipelines se prueban después. No hace falta copiar los documentos: la secuencia «consultar, observar, ajustar» crea una dependencia entre el sistema y la muestra que debía representar datos nuevos.

En OSINT, este problema aparece cuando varios equipos comparten un corpus de resoluciones públicas, capturas web o documentos anonimizados. Una puntuación agregada puede parecer inocua, pero también comunica qué cambio funcionó sobre esos casos concretos. Con suficientes rondas, el equipo puede acabar optimizando peculiaridades del corpus en vez de mejorar el proceso que se encontrará fuera de él.

Todos los nombres, documentos, dominios, cifras y resultados del ejemplo son ficticios. El flujo descrito se limita a datos sintéticos, fuentes públicas o sistemas propios y autorizados. Una buena evaluación no convierte una inferencia sobre personas en un hecho ni autoriza vigilancia, atribuciones o decisiones perjudiciales.

## Qué es el desgaste (y para qué sirve reconocerlo)

Google explica que los conjuntos de validación y prueba pueden «desgastarse» con el uso repetido: si sus resultados guían cambios, el sistema se ajusta indirectamente a ellos y pierde fuerza como medida de comportamiento futuro. La causa no es que el fichero se deteriore, sino que deja de ser independiente del proceso que evalúa.

Dwork y colaboradores formalizaron un problema más general: el análisis adaptativo. Una nueva pregunta se elige a la luz de respuestas anteriores sobre los mismos datos. Su trabajo sobre el *reusable holdout* muestra que existen mecanismos formales para contestar muchas consultas bajo garantías concretas, mediante técnicas de estabilidad y privacidad diferencial. Esto no significa que cualquier API con ruido vuelva reutilizable un corpus ni que exista un contador universal de consultas seguras.

Conviene distinguir cuatro fenómenos:

- **reutilización:** evaluar varias veces sobre la misma muestra;
- **adaptación:** dejar que una respuesta influya en el siguiente candidato;
- **contaminación:** incorporar casos, soluciones o artefactos de evaluación al desarrollo;
- **deriva:** cambiar la población real mientras el corpus permanece fijo.

Pueden coexistir, pero requieren respuestas distintas. Renovar datos no arregla una fuga en los logs; limitar consultas no corrige una muestra que nunca representó documentos escaneados; sellar etiquetas no impide que un desglose demasiado preciso revele dónde falla cada candidato.

Reconocer el desgaste sirve para interpretar correctamente una mejora, decidir cuándo una evaluación ya es exploratoria y reservar evidencia verdaderamente independiente para la promoción final.

## Caso legítimo: seis equipos y un corpus compartido

Imaginemos una organización ficticia, **Archivo Claro**, que extrae fechas y referencias cruzadas de boletines públicos. Mantiene un corpus autorizado de 1.200 documentos con etiquetas verificadas. Seis equipos trabajan sobre OCR, detección de tablas, normalización y deduplicación.

El servicio de evaluación devuelve exactitud global, cinco métricas por tipo documental y una lista de los veinte errores más frecuentes. Cada equipo puede consultar cuando quiera. En ocho semanas se registran 146 ejecuciones. Nadie descarga las etiquetas, pero las reglas empiezan a incluir excepciones que solo mejoran determinados boletines. El panel sube del 86 % al 96 %; una evaluación prospectiva sobre documentos posteriores obtiene un 88 %.

No hace falta acusar a nadie de manipulación. El sistema de incentivos convirtió el corpus reservado en una interfaz de desarrollo. Las respuestas detalladas, compartidas entre equipos y sin historial común, permitieron aprender sus singularidades.

El objetivo no es castigar la iteración, sino asignarle un lugar honesto:

1. un conjunto de desarrollo visible para diagnosticar;
2. una evaluación interna con feedback limitado para seleccionar;
3. un conjunto final sellado para confirmar una versión congelada;
4. una prueba prospectiva en sombra cuando el tiempo o la fuente formen parte del problema.

## Flujo recomendado: gobernar consultas y evidencia

### 1. Define la unidad protegida y el propósito

Antes de contar consultas, documenta qué debe permanecer independiente: documento, expediente, dominio, organismo, incidente o ventana temporal. Agrupa versiones relacionadas y evita repartir páginas del mismo PDF entre desarrollo y evaluación.

Registra también el propósito. Un corpus para encontrar fallos puede reutilizarse como material exploratorio, pero no debe conservar indefinidamente la etiqueta de «confirmación». Un conjunto final existe para responder una pregunta previamente acordada sobre un candidato congelado.

NIST recomienda documentar conjuntos, métricas, herramientas y procesos de prueba. En forense digital, Lyle y Horsman advierten además que un dataset mal construido o mal documentado debilita la fiabilidad de cualquier resultado posterior.

### 2. Crea un ledger de consultas compartido

El presupuesto pertenece al corpus, no a cada equipo por separado. Una hoja local por proyecto oculta la adaptación colectiva. Un registro mínimo puede contener:

```yaml
evaluation_set: public-docs-confirmation-v3
query_id: ev-2026-10-23-014
candidate_digest: sha256:ejemplo-ficticio
requested_by: extraction-team
purpose: confirmar umbral preregistrado
metrics: [field_recall, provenance_completeness]
segments: [scanned_pdf, born_digital]
result_precision: 0.01
result_released_to: [evaluation-owner, extraction-lead]
decision: no-promote
changes_triggered: [review-ocr-routing]
```

Guarda el digest del candidato, configuración, métricas solicitadas, granularidad devuelta, destinatarios y decisiones provocadas. Cuenta también las consultas fallidas, los desgloses extraordinarios y las inspecciones manuales. El feedback humano sobre ejemplos concretos puede revelar mucho más que una métrica.

### 3. Devuelve la mínima información útil

Blum y Hardt estudiaron el sobreajuste adaptativo en clasificaciones de competiciones. Su mecanismo *Ladder* limita el feedback y solo refleja mejoras suficientemente relevantes bajo un diseño formal. La lección operativa no es copiar ese algoritmo sin revisar supuestos, sino entender que **la forma de responder importa tanto como el número de consultas**.

Aplica una escalera de divulgación:

- durante desarrollo, devuelve errores detallados sobre datos destinados a desarrollo;
- durante selección, devuelve pocas métricas preregistradas y con precisión justificada;
- no entregues automáticamente filas fallidas, etiquetas ni cortes diminutos;
- agrupa resultados cuando un segmento pueda revelar un caso único;
- reserva el resultado confirmatorio completo para una decisión formal;
- separa quién desarrolla de quién custodia y ejecuta la evaluación final.

Reducir decimales o imponer una espera puede disminuir feedback, pero son heurísticas, no garantías universales. Una señal binaria repetida también puede filtrar información. Si hacen falta garantías cuantitativas para consultas adaptativas, se necesita un mecanismo analizado para ese tipo de consulta, muestra y composición, con apoyo estadístico especializado.

### 4. Define estados, no un número mágico

No escribas «50 consultas son seguras» sin un modelo que lo demuestre. Define estados operativos observables:

- **sellado:** ninguna respuesta ha influido en desarrollo;
- **confirmatorio:** una única familia de consultas preregistradas para un candidato congelado;
- **adaptativo controlado:** se permiten iteraciones mediante un mecanismo y presupuesto explícitos;
- **exploratorio:** los resultados ya han guiado cambios y solo sirven para diagnosticar;
- **retirado:** el corpus no sustenta nuevas afirmaciones de generalización.

La transición puede activarse por cualquier cambio motivado por el resultado, una ampliación no prevista de métricas, acceso a errores individuales, demasiados equipos consumidores, indicios de fuga o un cambio material en la población. El ledger explica por qué cambió el estado.

### 5. Renueva sin borrar la historia

Renovar no consiste en sustituir silenciosamente los casos difíciles. Conserva versión, manifiesto, procedencia, reglas de inclusión, periodo de captura y motivo del cambio. Mantén métricas comparables sobre una parte estable cuando sea legítimo y añade un bloque fresco para medir el presente.

Separa tres acciones:

1. **ampliar**, cuando falta cobertura pero la definición sigue vigente;
2. **refrescar**, cuando la fuente o población ha cambiado;
3. **retirar**, cuando la exposición o adaptación impide usar el corpus como confirmación.

El programa AITE de NIST usa datos ciegos en un entorno separado para mitigar la contaminación entre entrenamiento y prueba. Ese modelo de custodia por un tercero neutral es una opción para evaluaciones de alto impacto; un equipo pequeño puede aproximarlo con permisos separados, ejecución automatizada y resultados entregados por una persona que no desarrolla el candidato.

### 6. Confirma con una salida que pueda decir «no sabemos»

La puerta final debe admitir cuatro resultados: promover, no promover, detener por barrera de seguridad o declarar evidencia insuficiente. Informa numeradores, denominadores, incertidumbre, exclusiones y estado del corpus. Revisa divergencias críticas de forma ciega antes de convertir un promedio en decisión.

Si el candidato cambia tras ver la confirmación, esa ronda pasa a ser información de desarrollo. La siguiente afirmación confirmatoria requiere datos nuevos o un procedimiento formal que cubra la adaptación. Cambiar el nombre del conjunto no restaura su independencia.

## Limitaciones y falsos positivos

Una caída fuera del corpus no prueba por sí sola sobreajuste adaptativo. Puede deberse a deriva temporal, distinta mezcla de formatos, errores de etiquetado, dependencia entre unidades o una incidencia del pipeline. El ledger permite reconstruir qué decisiones dependieron de qué respuestas, pero no identifica automáticamente la causa.

Tampoco todo uso repetido invalida cualquier comparación. Ejecutar dos veces el mismo binario para comprobar reproducibilidad no equivale a crear un candidato nuevo a partir del resultado. El riesgo crece cuando el feedback modifica hipótesis, código, datos, prompts, reglas o selección de resultados.

Evita estos atajos:

- repartir el límite por equipo y olvidar el consumo total del corpus;
- contar ejecuciones, pero no desgloses, revisiones o mensajes informales;
- ocultar etiquetas mientras se devuelven errores fila a fila;
- declarar una cifra fija de consultas «seguras» sin supuestos;
- añadir ruido casero y llamarlo privacidad diferencial;
- renovar solo los casos que bajan la puntuación;
- mezclar contaminación con deriva y aplicar una única solución;
- publicar un porcentaje sin versión ni estado del conjunto;
- convertir rendimiento técnico en veracidad de una conclusión OSINT;
- promocionar automáticamente porque el panel ha mejorado.

## Buenas prácticas de OPSEC, ética y privacidad

- Minimiza datos reales y usa casos sintéticos para el diagnóstico detallado.
- Separa credenciales, almacenamiento y logs de desarrollo y evaluación.
- No expongas URLs privadas, consultas sensibles ni documentos con datos personales en paneles.
- Aplica control de acceso al corpus, a sus etiquetas y también a los resultados segmentados.
- Conserva logs suficientes para auditar sin duplicar contenido sensible.
- Define retención, borrado y respuesta ante contaminación antes de evaluar.
- No recolectes más información sobre personas solo para refrescar una métrica.
- Revisa licencias, términos de servicio, finalidad y base legal de cada fuente.
- Documenta quién puede abrir casos individuales y bajo qué criterio.
- Mantén revisión humana para publicación, atribución y cualquier efecto externo.

## Alternativas y siguientes pasos

Si el corpus es pequeño, puede ser mejor usarlo como banco exploratorio y realizar confirmación prospectiva sobre una ventana futura. Si varios equipos necesitan iterar, crea un conjunto de validación compartido y reserva una evaluación final bajo custodia independiente. Si solo importan fallos críticos, una revisión ciega caso a caso puede aportar más que una puntuación global.

Los mecanismos formales de análisis adaptativo —incluidos los basados en estabilidad, privacidad diferencial o feedback limitado— son alternativas reales, pero sus garantías dependen del diseño. No los sustituyas por ruido arbitrario, redondeo o límites copiados de otro proyecto.

El takeaway accionable es sencillo: abre el historial del corpus que hoy llamas «reservado» y registra **cada respuesta que cambió una decisión**. Asigna después uno de los cinco estados propuestos. Si ya sirvió para ajustar el sistema, conserva su valor diagnóstico, cambia su etiqueta a exploratorio y prepara una confirmación que el candidato todavía no haya podido aprender.

Como siguiente tema convendría estudiar la **renovación prospectiva de benchmarks OSINT**: cómo incorporar datos futuros con reglas de procedencia, congelación y comparación que distingan mejora real de deriva de las fuentes.

## Fuentes consultadas

- [Dwork et al.: The reusable holdout — Preserving validity in adaptive data analysis](https://pubmed.ncbi.nlm.nih.gov/26250683/)
- [Dwork et al.: Generalization in Adaptive Data Analysis and Holdout Reuse](https://papers.nips.cc/paper_files/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html)
- [Blum y Hardt: The Ladder — A Reliable Leaderboard for Machine Learning Competitions](https://proceedings.mlr.press/v37/blum15.html)
- [Google for Developers: dividir los datos de entrenamiento, validación y prueba](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)
- [NIST: Artificial Intelligence Technology Evaluation (AITE)](https://pages.nist.gov/ai-technology-evaluation/)
- [NIST AI RMF Playbook: Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)
- [Lyle y Horsman: Dataset construction challenges for digital forensics](https://www.nist.gov/publications/dataset-construction-challenges-digital-forensics)
