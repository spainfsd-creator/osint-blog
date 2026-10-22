---
title: "Selección del ganador en OSINT: estimar sin inflar su ventaja"
slug: /seleccion-ganador-estimacion-postseleccion-osint
authors: [osint-writter]
tags: [osint, methodology, experimentation, verification, automation, privacy]
date: 2026-10-22
image: /img/blog/2026-10-22-seleccion-ganador-estimacion-postseleccion-osint.png
aiDisclosure: generated
humanReviewed: false
---

Tres pipelines procesan el mismo lote de documentos públicos. El primero acierta el 91 %, el segundo el 93 % y el tercero el 95 %. El equipo elige el tercero y anuncia una mejora de cuatro puntos. Parece una comparación limpia, pero falta una pregunta incómoda: **¿el 95 % describe al pipeline ganador o describe, en parte, la suerte que hizo que lo eligiéramos?**

![Analista comparando varios flujos antes de una validación independiente y una revisión humana](/img/blog/2026-10-22-seleccion-ganador-estimacion-postseleccion-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Cuando se escoge el máximo entre varias estimaciones ruidosas, el ganador suele reunir dos cosas: capacidad real y una fluctuación favorable. Usar después ese mismo resultado como estimación final convierte la selección en una fuente de optimismo. En estadística y evaluación de sistemas, este problema aparece bajo nombres como **sesgo de selección**, **inferencia postselección** o *winner's curse*.

En OSINT no es una curiosidad académica. Puede llevarnos a desplegar el extractor que casualmente recibió los PDF más fáciles, a preferir la regla que encajó mejor con un corpus ya muy conocido o a comunicar una mejora que desaparece con documentos nuevos. La respuesta práctica no es desconfiar de toda métrica, sino dar trabajos distintos a los datos de selección y a los de confirmación.

Todos los nombres, documentos, dominios, cifras y resultados del ejemplo son ficticios. El flujo se limita a datos sintéticos, fuentes públicas o sistemas propios y autorizados. Evaluar mejor un pipeline no convierte automáticamente sus salidas en hechos ni autoriza decisiones sobre personas.

## Qué es la estimación postselección (y para qué sirve)

Supongamos que cada candidato tiene un rendimiento real que no podemos observar directamente. Lo estimamos sobre una muestra finita. Esa estimación contiene variabilidad: otra muestra, otra semana o una mezcla distinta de documentos producirían otro valor.

Si probamos un único candidato predefinido, su error puede ser positivo o negativo. Si probamos muchos y elegimos el valor más alto, favorecemos precisamente a los candidatos cuyo error fue positivo. El ganador no tiene por qué ser malo; lo que deja de ser neutral es la cifra con la que ganó.

Andrews, Kitagawa y McCloskey describen esta lógica en su trabajo sobre inferencia de ganadores: cuando la elección se basa en estimaciones inciertas, es más probable seleccionar una opción justo cuando su efectividad ha sido sobreestimada. Cawley y Talbot muestran un problema estrechamente relacionado en selección de modelos: optimizar un criterio de evaluación con varianza puede sobreajustar ese criterio, y las diferencias observadas entre algoritmos pueden ser del mismo orden que el propio sesgo de selección.

Conviene separar tres tareas:

1. **Selección:** elegir qué candidato merece pasar de fase.
2. **Estimación:** medir cuánto aporta el candidato ya elegido sobre datos que no lo eligieron.
3. **Decisión:** valorar utilidad, daños, procedencia, coste y casos concretos antes de promoverlo.

Un único porcentaje reutilizado para las tres tareas parece eficiente, pero oculta el proceso que lo hizo ganador. La estimación postselección intenta medir al candidato teniendo en cuenta que fue seleccionado. En la práctica cotidiana, la defensa más clara suele ser una evaluación independiente, reservada de antemano y acompañada de incertidumbre y revisión de divergencias.

## Caso legítimo: el extractor que ganó dos veces sobre el mismo examen

El observatorio ficticio **Archivo Abierto** recopila resoluciones públicas de varios organismos. Su pipeline estable conserva URL, fecha de observación, digest, versión y texto extraído. El equipo prepara cuatro candidatos: dos motores OCR, una regla nueva para anexos y una combinación de ambos cambios.

Construye un corpus con documentos digitales, escaneos, tablas, anexos y correcciones. Lo utiliza para ajustar umbrales, corregir fallos y comparar candidatos. Después de varias iteraciones, la combinación obtiene la mejor puntuación. Para demostrar su superioridad, el equipo vuelve a ejecutar los cuatro candidatos sobre el mismo corpus y presenta el máximo como rendimiento esperado.

El corpus ya ha influido en qué reglas sobrevivieron, qué excepciones se añadieron y qué candidato llegó al final. Aunque nadie haya cambiado una etiqueta de mala fe, el examen se ha convertido en material de estudio. Además, la puntuación media oculta que el ganador fusiona algunas correcciones con la resolución original.

Archivo Abierto reinicia la fase de evaluación, no el desarrollo. Congela el candidato, registra su versión y abre una partición de confirmación que no participó en la búsqueda. Esa partición mantiene proporciones acordadas de cada tipo documental, separa versiones de una misma familia y respeta el tiempo: los documentos posteriores no se filtran hacia el pasado.

El candidato conserva una mejora más modesta que la anunciada inicialmente. El intervalo de incertidumbre incluye efectos pequeños y dos anexos requieren revisión. El equipo comunica ambos resultados: puntuación de selección y estimación confirmatoria. No promociona todavía; corrige los anexos y reserva una nueva evaluación para la siguiente versión. Ha perdido una cifra espectacular y ha ganado una decisión explicable.

## Flujo recomendado

### 1. Define la unidad y la familia antes de dividir

Un fichero no siempre es una observación independiente. Una resolución y su corrección, diez páginas del mismo PDF o varias capturas del mismo sitio comparten origen y errores. Si sus fragmentos caen en selección y confirmación, la segunda fase puede reconocer patrones que ya influyeron en la primera.

Decide qué debe permanecer agrupado: expediente, dominio, organismo, plantilla, incidente o ventana temporal. Para flujos que operarán sobre el futuro, una división temporal suele representar mejor el uso real que mezclar al azar documentos cercanos. La documentación de scikit-learn advierte que barajar noticias ordenadas en el tiempo puede producir una validación artificialmente parecida al entrenamiento e inflar el resultado.

### 2. Asigna un trabajo a cada conjunto

Una separación mínima puede expresarse así:

```yaml
evaluation_contract: extractor-public-docs-v6
development:
  purpose: ajustar reglas y diagnosticar
selection:
  purpose: elegir un candidato
  candidates: [ocr-a, ocr-b, tables-a, combined-a]
confirmation:
  purpose: estimar al ganador congelado
  access: sealed-until-selection
  grouped_by: document_family
  ordered_by_time: true
promotion:
  requires:
    - provenance_complete
    - no_known_correction_lost
    - uncertainty_reported
    - human_divergence_review
```

El tamaño y la composición dependen del caso; no existe un reparto universal. Lo esencial es que la confirmación no guíe la elección que después pretende evaluar. Si los datos son escasos, una validación cruzada anidada puede separar la búsqueda interior de la estimación exterior. El ejemplo oficial de scikit-learn explica que la validación no anidada usa los mismos datos para ajustar y evaluar, mientras que la anidada estima el proceso completo de selección en un bucle exterior.

### 3. Congela al ganador antes de abrir la confirmación

Registra código, dependencias, configuración, prompt si lo hubiera, semillas relevantes y manifiesto de entrada. Calcula digests de los artefactos. El candidato confirmado debe ser el candidato seleccionado, no una versión retocada después de mirar dónde falla.

Si la confirmación revela un defecto y se modifica el pipeline, esa información ya forma parte del desarrollo. La siguiente medición honesta necesita otra partición no consultada, un diseño de remuestreo adecuado o una etiqueta explícita de resultado exploratorio. Cambiar dos líneas y volver a llamar «independiente» al mismo conjunto no restaura su independencia.

### 4. Informa la caída, no la escondas

Conserva al menos:

- puntuación de selección del candidato elegido;
- resultado de confirmación con numerador, denominador e incertidumbre;
- diferencia frente al control sobre las mismas unidades;
- distribución por tipos críticos, no solo promedio global;
- candidatos, métricas y exclusiones examinados;
- fallos, datos ausentes y decisiones humanas.

Que la ventaja disminuya en confirmación es información sobre el proceso, no una razón para borrar la primera medición. Tampoco toda caída demuestra una *maldición del ganador*: puede haber deriva temporal, una partición mal equilibrada o un fallo de instrumentación. Investiga la causa sin convertir cada explicación posible en una excusa para conservar el titular inicial.

### 5. Revisa divergencias, no solo agregados

Toma una muestra ciega de desacuerdos entre control y candidato. Clasifica falsos duplicados, omisiones, texto inventado por OCR, fechas ambiguas y procedencia incompleta. Una mejora media puede ser inaceptable si pierde una corrección oficial o si funciona peor justo en el formato de mayor impacto.

La revisión debe poder concluir **ninguno promociona**. El candidato con mejor cifra no adquiere por ello derecho a producción. Las barreras de privacidad, trazabilidad y efectos externos siguen siendo condiciones separadas.

### 6. Protege la confirmación del desgaste

Dwork y colaboradores estudian el problema general de los análisis adaptativos: nuevas preguntas nacen de resultados anteriores sobre los mismos datos. Su propuesta de *reusable holdout* demuestra que existen mecanismos formales para reutilizar información bajo garantías concretas; no significa que un equipo pueda mirar libremente el conjunto reservado y seguir llamándolo intacto.

Para un flujo editorial pequeño, una política sencilla suele ser más auditable:

- limita quién puede abrir los resultados de confirmación;
- devuelve solo métricas previamente acordadas antes de la revisión final;
- registra cada consulta y cada cambio provocado por ella;
- retira o renueva el conjunto tras usos definidos;
- incorpora datos futuros únicamente con reglas de procedencia y consentimiento aplicables;
- evita que ejemplos confirmatorios terminen copiados en prompts, fixtures o excepciones.

Google resume la misma intuición de forma operativa: entrenamiento, validación y prueba cumplen funciones distintas, y los conjuntos de validación y prueba se «desgastan» con el uso repetido. En OSINT, además, una fuente viva puede cambiar. Conserva captura, fecha, digest y versión del corpus para distinguir desgaste analítico de deriva real.

## Limitaciones y falsos positivos

Un conjunto reservado no arregla un muestreo malo. Si contiene solo PDF limpios, no estimará el comportamiento sobre escaneos. Si excluye silenciosamente descargas fallidas, medirá facilidad de acceso y no cobertura. Si documentos emparentados cruzan particiones, habrá fuga aunque los nombres de archivo sean distintos.

La validación cruzada tampoco es un conjuro. Sus pliegues deben respetar grupos, tiempo y dependencia. La versión anidada estima un procedimiento de selección, pero puede ser costosa y variable con muestras pequeñas. Un test independiente reduce un tipo de sesgo; no certifica que la población futura sea igual ni que las etiquetas sean correctas.

La inferencia selectiva ofrece herramientas más especializadas para ajustar inferencias después de buscar asociaciones. Taylor y Tibshirani subrayan que medir una asociación después de encontrarla en los mismos datos exige considerar el proceso de selección. Aplicar esos métodos correctamente requiere supuestos y competencia estadística; añadir la expresión «corregido por selección» sin describir el mecanismo no aporta una garantía.

Evita estos atajos:

- elegir con una métrica y estimar con la misma cifra máxima;
- probar variantes hasta que una supere al control y ocultar las anteriores;
- abrir el conjunto reservado para decidir un umbral «pequeño»;
- crear una nueva partición después de conocer todos los casos difíciles;
- mezclar páginas, versiones o entidades relacionadas entre conjuntos;
- informar solo el promedio sin denominadores ni tipos críticos;
- tratar la ausencia de diferencia como equivalencia demostrada;
- presentar rendimiento técnico como verdad de las conclusiones OSINT;
- automatizar la promoción o publicación porque un intervalo cruza un umbral.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa datos sintéticos para desarrollar y minimiza el contenido real autorizado.
- No amplíes la recogida ni consultes más a terceros solo para aumentar la muestra.
- Separa credenciales, almacenamiento y logs de desarrollo y confirmación.
- Redacta tokens, URLs firmadas, consultas sensibles e identificadores personales.
- Agrupa sin crear perfiles innecesarios de personas o comunidades vulnerables.
- Define retención, acceso y eliminación antes de abrir el corpus.
- Versiona etiquetas y registra quién cambió una decisión y por qué.
- No uses acusaciones o atribuciones como simples filas de entrenamiento.
- Revisa términos de servicio, licencias y finalidad de reutilización.
- Mantén una puerta humana para impacto, publicación y atribución.

## Alternativas y siguientes pasos

Si solo hay pocos casos críticos, una comparación ciega caso por caso puede ser más útil que estimar un promedio. Si el corpus es pequeño pero tiene grupos claros, considera remuestreo agrupado o validación cruzada anidada con asesoramiento adecuado. Si el entorno cambia rápidamente, una evaluación prospectiva en sombra sobre datos futuros puede representar mejor el despliegue. Y si el objetivo es descubrir fallos, etiqueta la fase como exploratoria y reserva cualquier afirmación de mejora para otra evaluación.

El takeaway accionable es concreto: toma la última tabla en la que elegiste «el mejor» pipeline y añade tres columnas: **dato usado para elegir**, **dato independiente para estimar** y **número de decisiones influidas por cada conjunto**. Si la misma muestra ocupa las tres, congela al candidato y diseña una confirmación que respete grupos, tiempo y procedencia. Informa después tanto la cifra ganadora como la confirmatoria: la distancia entre ambas también es un resultado.

Como siguiente tema convendría estudiar el **desgaste del conjunto de evaluación y los límites de consulta**: cómo gobernar un corpus compartido cuando varios equipos lo reutilizan sin convertirlo en una respuesta memorizada.

## Fuentes consultadas

- [Andrews, Kitagawa y McCloskey: Inference on Winners](https://doi.org/10.1093/qje/qjad043)
- [Cawley y Talbot: On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation](https://www.jmlr.org/papers/v11/cawley10a.html)
- [Reunanen: Overfitting in Making Comparisons Between Variable Selection Methods](https://www.jmlr.org/papers/v3/reunanen03a.html)
- [Taylor y Tibshirani: Statistical Learning and Selective Inference](https://doi.org/10.1073/pnas.1507583112)
- [Dwork et al.: The Reusable Holdout — Preserving Validity in Adaptive Data Analysis](https://doi.org/10.1126/science.aaa9375)
- [scikit-learn: validación cruzada anidada frente a no anidada](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html)
- [Google for Developers: dividir los datos de entrenamiento, validación y prueba](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)
