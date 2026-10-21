---
title: "Guardas para múltiples métricas y candidatos en OSINT: elegir sin premiar al azar"
slug: /guardas-multiples-metricas-candidatos-osint
authors: [osint-writter]
tags: [osint, methodology, experimentation, verification, automation, privacy]
date: 2026-10-21
image: /img/blog/2026-10-21-guardas-multiples-metricas-candidatos-osint.png
aiDisclosure: generated
humanReviewed: false
---

Tres extractores compiten sobre el mismo lote de documentos públicos. El equipo observa cinco métricas, prueba varios cortes y conserva la combinación que ofrece el gráfico más convincente. Todo parece medido; sin embargo, **la libertad de elegir candidato, métrica y momento después de mirar ha convertido el ruido en ganador**.

![Analista OSINT comparando varios candidatos y métricas antes de una puerta de decisión humana](/img/blog/2026-10-21-guardas-multiples-metricas-candidatos-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/guardas-multiples-metricas-candidatos-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Un experimento puede respetar su regla de parada y aun producir una conclusión frágil si abre demasiadas rutas hacia el éxito. Cada candidato adicional, cada métrica rebautizada como principal y cada subgrupo examinado después amplían el conjunto de oportunidades para encontrar una diferencia favorable por casualidad.

En un flujo OSINT, la solución no consiste en aplicar una corrección estadística al final y continuar como si nada. Hace falta definir de antemano qué decisiones forman una familia, separar métricas de éxito y barreras de seguridad, conservar los resultados desfavorables y mantener la promoción bajo revisión humana.

Todos los nombres, dominios, documentos, cifras y resultados del ejemplo son ficticios. Este artículo se refiere a datos sintéticos, fuentes públicas o sistemas propios y autorizados. No propone experimentar sobre personas, ampliar la recogida ni automatizar acusaciones, atribuciones o decisiones perjudiciales.

## Qué es la multiplicidad (y por qué importa)

Una prueba aislada tiene una tasa de falso positivo asociada a su diseño. Si repetimos muchas pruebas y tratamos cada una como si fuera la única, aumenta la probabilidad de que al menos una parezca favorable aun cuando ningún candidato mejore realmente el proceso. El [manual estadístico de NIST](https://www.itl.nist.gov/div898/handbook/prc/section4/prc47.htm) advierte precisamente que repetir comparaciones por pares no mantiene, en general, el nivel global especificado para una sola comparación.

La multiplicidad puede entrar por varias puertas:

- tres candidatos frente a un control;
- una métrica primaria, cuatro secundarias y seis segmentos;
- varias transformaciones o ventanas temporales;
- exclusiones decididas tras ver qué casos estropean el resultado;
- sucesivas versiones del candidato alimentadas por el mismo conjunto de evaluación;
- lecturas intermedias combinadas con cualquiera de las anteriores.

No todas las observaciones necesitan convertirse en una hipótesis formal. Un panel diagnóstico puede mostrar muchas señales para entender un fallo. El problema aparece cuando cualquiera de ellas puede autorizar la misma afirmación —«el candidato es mejor»— sin que esa ruta formase parte del contrato.

### FWER y FDR responden a preguntas distintas

El **error familiar** o *family-wise error rate* (FWER) controla la probabilidad de cometer al menos un falso rechazo dentro de una familia. Es una opción natural cuando una sola falsa promoción puede publicar datos incorrectos, perder una corrección o romper la procedencia.

Bonferroni reparte un presupuesto de error entre un conjunto finito de comparaciones preseleccionadas. Es sencillo y general, aunque puede perder potencia. El procedimiento escalonado de [Holm](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf) también controla el FWER y suele ser menos conservador que aplicar el mismo corte de Bonferroni a todas las pruebas.

La **tasa de falsos descubrimientos** o FDR controla otra cantidad: la proporción esperada de falsos positivos entre los resultados declarados positivos. El trabajo de [Benjamini y Hochberg](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) planteó este criterio como una alternativa con mayor potencia para colecciones de descubrimientos. Puede encajar en exploración a gran escala, pero no significa que cada hallazgo individual sea fiable ni que sea apropiado usarlo para una única decisión de alto impacto.

Elegir entre FWER y FDR no es un ajuste cosmético. Depende de qué daño produce un falso positivo, qué afirmación se hará y qué unidad considera el equipo una familia. Esa decisión debe quedar escrita antes de conocer los resultados y, cuando el análisis lo requiera, contar con apoyo estadístico competente.

## Caso legítimo: cuatro extractores y demasiadas formas de ganar

El observatorio ficticio **Faro Documental** archiva boletines públicos. Su extractor estable conserva URL, momento de observación, digest, texto y relaciones entre versiones. El equipo quiere evaluar tres candidatos: uno cambia el OCR, otro la detección de tablas y un tercero combina ambos cambios.

El corpus versionado contiene documentos digitales, escaneos, anexos tabulares y correcciones. Al principio, el equipo define «porcentaje de páginas con texto» como objetivo. Al ver que gana el candidato de OCR, alguien descubre que pierde varias tablas. El candidato combinado gana en tablas, pero fusiona dos correcciones con sus originales. Entonces aparece una tercera métrica —tiempo medio— que favorece al candidato restante.

Cada observación es útil para diagnosticar. Ninguna autoriza por sí sola a coronar al candidato que salga mejor parado. Si el equipo permite que cualquier candidato gane por cualquier métrica, el experimento ya no responde a una pregunta concreta.

Faro Documental reinicia la evaluación con un contrato. Designa una métrica primaria, fija tres barreras sin tolerancia, declara qué comparaciones pertenecen a la familia de promoción y reserva las métricas restantes para diagnóstico. Conserva también una salida válida: **ninguno promociona**.

## Flujo recomendado

### 1. Formula una única decisión operativa

Empieza por el verbo que cambiará el sistema: promocionar, detener, continuar o declarar el resultado inconcluso. Después identifica qué comparación puede autorizarlo.

«Explorar qué funciona» y «autorizar el reemplazo del extractor» son objetivos distintos. La exploración puede generar hipótesis para otro corpus. La promoción necesita criterios previos y evidencia que no haya servido simultáneamente para diseñar el candidato y certificarlo.

### 2. Define la familia antes de mirar

Una familia no es necesariamente todo lo calculado en un proyecto. Es el conjunto de afirmaciones que compiten por sostener una misma decisión. Si cualquiera de tres candidatos puede reemplazar al control por superar la misma métrica, esas tres comparaciones pertenecen normalmente a la familia de promoción.

Escribe también qué queda fuera y por qué. Dividir una familia después de ver los valores favorables no reduce el problema; solo lo oculta. NIST señala que Bonferroni resulta apropiado para un conjunto finito de contrastes escogidos de antemano y ofrece cobertura simultánea al repartir el nivel global entre ellos.

### 3. Da a cada métrica un trabajo concreto

Clasifica las métricas antes del ensayo:

- **primaria:** responde a la pregunta que podría justificar la promoción;
- **barreras:** detienen por daño, privacidad, pérdida de procedencia o efectos externos;
- **secundarias:** ayudan a caracterizar el resultado, con reglas explícitas si afectarán a la decisión;
- **diagnósticas:** sirven para investigar divergencias, no para rescatar una promoción fallida.

Una barrera no tiene que esperar a ser «estadísticamente significativa» para detener una acción prohibida. Si el contrato dice que no puede perderse ninguna corrección conocida, observar una pérdida confirmada basta para parar y examinar el sistema. Tampoco conviene interpretar «no significativo» como «seguro»: puede significar que la muestra no permite excluir un daño relevante.

### 4. Predeclara comparaciones, cortes y excepciones

Un contrato conceptual podría ser:

```yaml
experiment_id: extractores-boletines-m4
control: extractor-estable
candidates: [ocr-b, tablas-c, combinado-d]
population: corpus-sintetico-versionado-v6
primary_metric: valid_document_rate
promotion_family:
  comparisons: [ocr-b_vs_control, tablas-c_vs_control, combinado-d_vs_control]
  error_target: family_wise
  procedure: chosen_with_statistical_review
guardrails:
  lost_known_corrections: 0
  missing_provenance: 0
  unauthorized_requests: 0
diagnostic_only: [latency, pages_with_text, table_cell_recall]
decision_states: [promote_one, continue, stop, inconclusive]
promotion_requires: independent_human_review
```

El ejemplo no prescribe un test ni un umbral universal. Obliga a que el equipo revele cuántas rutas pueden producir la decisión, qué señales solo explican y qué daños no son compensables.

### 5. Trata conjuntamente tiempo y multiplicidad

Corregir por tres candidatos no soluciona las miradas repetidas; usar inferencia secuencial no soluciona por sí solo las veinte métricas. Son dimensiones distintas del diseño.

[Johari, Pekelis y Walsh](https://arxiv.org/abs/1512.04922) describen inferencia válida en cualquier momento y su combinación con control de hipótesis múltiples en contexto secuencial. Las [secuencias de confianza de Howard y colaboradores](https://doi.org/10.1214/20-AOS1991) ofrecen garantías uniformes a lo largo del tiempo bajo sus supuestos. Llevar estas ideas a una promoción real requiere especificar familia, dependencias, política de observación y método como un conjunto; no basta con pegar una etiqueta *anytime-valid* a valores calculados de forma incompatible.

Si el equipo no dispone de esa capacidad, una alternativa honesta es simplificar: un candidato, una métrica primaria, un horizonte fijo y barreras deterministas sobre un corpus versionado.

### 6. Separa selección y confirmación

Usar el mismo corpus para inventar una regla, escoger el candidato y estimar su rendimiento favorece el sobreajuste. Divide el trabajo:

1. una fase exploratoria genera hipótesis y detecta clases difíciles;
2. el candidato y el contrato quedan congelados;
3. una evaluación confirmatoria usa datos reservados o una nueva muestra autorizada;
4. las divergencias se revisan caso por caso antes de promover.

Si se modifica el candidato después de ver la evaluación confirmatoria, registra el cambio y decide si hace falta una nueva confirmación. No borres los intentos fallidos: forman parte de cuántas oportunidades tuvo el sistema para parecer ganador.

### 7. Conserva un registro de decisiones, no solo un gráfico

El expediente debería enlazar corpus, versiones, candidatos, familia, métricas, exclusiones, lecturas, resultados completos y decisión. Registra también análisis no planificados como exploratorios. Una tabla incómoda no desaparece porque no llegue a la presentación.

La revisión humana debe comprobar al menos:

- que ningún candidato o subgrupo fue añadido o retirado silenciosamente;
- que la métrica primaria y las barreras conservan su definición;
- que el procedimiento corresponde a la familia y a la política de observación;
- que datos ausentes, fallos y exclusiones están contabilizados;
- que una mejora técnica no se presenta como prueba de verdad factual;
- que existe base para no promover a nadie.

## Limitaciones y falsos positivos

Una corrección de multiplicidad no arregla un corpus sesgado, una unidad de análisis equivocada, una dependencia ignorada ni una métrica que no representa el daño real. Tampoco compensa haber cambiado hipótesis, exclusiones o transformaciones tras mirar sin declararlo.

Los métodos tienen supuestos y objetivos distintos. Bonferroni puede ser conservador; Holm mejora el uso del presupuesto bajo control FWER, pero no convierte una familia improvisada en preespecificada. FDR resulta útil para conjuntos de descubrimientos, aunque puede ser una garantía inadecuada cuando cualquier falso positivo individual desencadena una publicación delicada. Las comparaciones entre muchos candidatos comparten a menudo datos y errores, por lo que la dependencia no debe darse por inocua.

Además, seleccionar al ganador introduce optimismo: su estimación suele parecer mejor precisamente porque fue el máximo observado. Antes de desplegar, conviene confirmar el efecto, examinar intervalos y casos concretos, y preguntar si la diferencia es operativamente útil, no solo compatible con un corte estadístico.

## Buenas prácticas de OPSEC, ética y privacidad

- Empieza con fixtures sintéticos y un corpus público o autorizado mínimo.
- No multipliques consultas a terceros para alimentar más candidatos o segmentos.
- Mantén todos los candidatos en sombra y sin efectos externos durante la comparación.
- Separa credenciales, almacenamiento, destinos y logs de cada ejecución.
- Redacta tokens, URLs firmadas, consultas sensibles e identificadores personales.
- No uses personas, acusaciones o grupos vulnerables como unidades experimentales.
- Predefine barreras de privacidad, procedencia y publicación.
- Conserva resultados negativos sin retener contenido personal innecesario.
- Revisa términos de servicio, licencias y límites de acceso.
- Exige una persona responsable que pueda detener y otra que autorice la promoción.

## Alternativas y siguientes pasos

Si el volumen es pequeño, una revisión ciega de divergencias sobre un corpus reservado puede ser más informativa que una batería de pruebas. Si solo hay una regresión conocida, conviértela en un test determinista. Si existen muchos candidatos inmaduros, filtra primero con datos sintéticos y confirma únicamente uno en una evaluación separada. Si la pregunta es exploratoria, etiqueta los resultados como hipótesis y no los uses para publicar una conclusión.

El takeaway accionable es concreto: abre hoy el contrato de tu próximo canary y dibuja una matriz con candidatos en filas y métricas en columnas. Marca cada celda que podría justificar una promoción. Si aparecen varias rutas, define la familia, el objetivo de error y la fase confirmatoria antes de ejecutar. Si no puedes explicar por qué una celda pertenece o no a la decisión, todavía estás explorando.

Como siguiente tema convendría estudiar la **selección del ganador y la estimación posterior**: cómo evitar que el candidato elegido conserve una ventaja inflada y cómo confirmar su efecto sin reutilizar indefinidamente el mismo corpus.

## Fuentes consultadas

- [NIST/SEMATECH: procedimientos para comparaciones múltiples](https://www.itl.nist.gov/div898/handbook/prc/section4/prc47.htm)
- [NIST/SEMATECH: método de Bonferroni e intervalos simultáneos](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm)
- [Holm: A Simple Sequentially Rejective Multiple Test Procedure](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf)
- [Benjamini y Hochberg: Controlling the False Discovery Rate](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)
- [Johari, Pekelis y Walsh: Always Valid Inference](https://arxiv.org/abs/1512.04922)
- [Howard et al.: Time-uniform, nonparametric, nonasymptotic confidence sequences](https://doi.org/10.1214/20-AOS1991)
- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)
