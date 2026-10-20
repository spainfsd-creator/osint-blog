---
title: "Experimentos secuenciales en OSINT: mirar una métrica sin promocionar por casualidad"
slug: /experimentos-secuenciales-sesgo-parada-osint
authors: [osint-writter]
tags: [osint, methodology, experimentation, verification, automation, privacy]
date: 2026-10-20
image: /img/blog/2026-10-20-experimentos-secuenciales-sesgo-parada-osint.png
aiDisclosure: generated
humanReviewed: false
---

El canary lleva veinte minutos y su tasa de errores parece mejor que la del flujo estable. Cinco minutos después empeora; luego vuelve a cruzar la línea verde. El equipo refresca el panel hasta encontrar el instante que confirma lo que quería hacer y pulsa «promocionar». **No ha descubierto una mejora: ha convertido el momento de mirar en parte oculta del experimento.**

![Analista OSINT comparando una métrica ruidosa con un flujo de decisión secuencial](/img/blog/2026-10-20-experimentos-secuenciales-sesgo-parada-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/experimentos-secuenciales-sesgo-parada-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Un experimento secuencial permite revisar datos mientras llegan y decidir si continuar, detener o declarar el resultado inconcluso. Pero esa flexibilidad necesita reglas compatibles con observaciones repetidas. Aplicar una y otra vez un test diseñado para una única lectura final y parar justo cuando ofrece el resultado apetecido puede elevar la probabilidad de un falso positivo.

En OSINT el problema no se limita a una cifra estadística. Un pipeline nuevo puede parecer mejor porque hoy recibió documentos fáciles, porque una fuente estuvo caída solo para el control o porque se eligió, después de mirar, la métrica más favorable. La estadística ayuda a ordenar la incertidumbre; no convierte una comparación sesgada en evidencia ni sustituye la revisión de casos concretos.

Todos los nombres, documentos, dominios y resultados del ejemplo son ficticios. El artículo se refiere a datos sintéticos, fuentes públicas o sistemas propios y autorizados. No propone experimentar sobre personas, ampliar la recogida ni automatizar atribuciones o decisiones perjudiciales.

## Qué es un experimento secuencial y para qué sirve

En un diseño de **horizonte fijo**, el tamaño de la muestra y el análisis principal se deciden antes de observar el resultado. Se recogen los datos previstos y se realiza una lectura final. Mirar un panel operativo durante la ejecución no invalida por sí solo el trabajo; el problema aparece cuando esas miradas cambian la decisión estadística sin que el método las contemple.

Un **diseño secuencial** incorpora las lecturas intermedias al plan. En cada punto autorizado puede haber tres salidas:

- detener por evidencia suficiente a favor del candidato;
- detener por daño, inutilidad o imposibilidad de aprender lo necesario;
- continuar hasta la siguiente lectura o hasta el límite máximo.

Los diseños por grupos reservan varias lecturas intermedias y ajustan sus fronteras para controlar el error acumulado. Las funciones de gasto de alfa distribuyen el presupuesto de error entre esas miradas. Otra familia utiliza inferencia válida en cualquier momento: valores *p* siempre válidos, valores *e* o **secuencias de confianza**, intervalos cuya cobertura se formula de manera uniforme a lo largo del tiempo. Johari, Pekelis y Walsh explican por qué los valores *p* convencionales dejan de ser fiables cuando el tamaño muestral se decide mediante monitorización continua; Howard y colaboradores formalizan secuencias de confianza válidas sobre un horizonte temporal no acotado.

No hace falta convertir a todo equipo OSINT en un departamento de estadística. Sí hace falta distinguir entre:

1. una **regla operativa**, como parar inmediatamente si el candidato publica algo prohibido;
2. una **regla de evidencia**, como exigir que una diferencia supere una frontera compatible con las miradas previstas;
3. una **decisión humana**, como valorar si la mejora compensa el riesgo y si los casos divergentes son aceptables.

## Caso legítimo: un extractor que parecía ganar cada viernes

El observatorio ficticio **Lente Pública** archiva boletines oficiales. Su flujo estable detecta nuevas versiones, conserva la URL y el momento de observación, calcula una huella y extrae texto. Un candidato añade un motor OCR distinto. El objetivo declarado es reducir documentos sin texto útil sin perder correcciones ni mezclar versiones.

El primer ensayo coloca ambos extractores en sombra sobre el mismo manifiesto. El panel muestra el porcentaje de páginas con texto. El candidato empieza dos puntos por encima y alguien propone promocionarlo. Sin embargo, la muestra inicial contiene boletines digitales sencillos; los escaneos difíciles llegan más tarde. Además, el equipo ha mirado seis métricas y solo comenta la que favorece al cambio.

Lente Pública reinicia el ensayo con un contrato previo. Define como métrica primaria la proporción de documentos que superan un conjunto mínimo de comprobaciones, estratificada por tipo de entrada. Añade barreras de seguridad sin tolerancia: ninguna corrección conocida puede desaparecer, ninguna petición puede salir hacia destinos no autorizados y toda salida debe conservar procedencia. Fija cuatro lecturas y un máximo de documentos, y encarga a una persona con competencia estadística elegir el método secuencial y sus supuestos.

En la segunda lectura, el OCR candidato mejora la extracción media, pero su secuencia de confianza todavía incluye efectos demasiado pequeños para justificar el cambio. No hay daño y queda muestra disponible: el estado es **continuar**, no «casi aprobado». En la tercera aparece una corrección fusionada con su versión anterior. La barrera de seguridad detiene el ensayo aunque la métrica primaria siga siendo favorable. La decisión no es una derrota estadística; es el contrato funcionando.

## Flujo recomendado

### 1. Escribe la pregunta antes de abrir el panel

Describe población, control, candidato, unidad de análisis y efecto mínimo útil. «El extractor nuevo es mejor» no basta. Una pregunta comprobable sería: «sobre documentos del manifiesto versionado, el candidato reduce fallos de extracción sin aumentar fusiones erróneas ni omitir procedencia».

Separa la hipótesis técnica de la afirmación factual. Un extractor puede recuperar más texto y, aun así, ese texto puede ser ambiguo o falso. El experimento evalúa el comportamiento del sistema, no la verdad de cada documento.

### 2. Define métricas y barreras con funciones distintas

Usa una métrica primaria para la decisión principal y un conjunto pequeño de métricas secundarias para diagnóstico. Las barreras protegen contra daños que no deben compensarse con una media favorable.

Un contrato conceptual podría ser:

```yaml
experiment_id: ocr-shadow-s9
population: manifest-v4-stratified
unit: document
primary_metric: valid_extraction_rate
minimum_useful_effect: predeclared
looks: [25%, 50%, 75%, 100%]
max_documents: predeclared
safety_stop:
  lost_corrections: 0
  unauthorized_requests: 0
  missing_provenance: 0
decisions: [stop, continue, inconclusive]
promotion_requires: human_review
```

«Predeclarado» no significa esconder el valor: el expediente real debe registrar cifras, método, versión de código y responsables. Aquí se omiten deliberadamente porque no existe un umbral universal transferible a cualquier corpus.

### 3. Elige una política de observación compatible con la decisión

Hay tres opciones prácticas:

- **Horizonte fijo:** una lectura inferencial al final; las alarmas de seguridad siguen activas durante todo el ensayo.
- **Lecturas por grupos:** varios puntos intermedios acordados y fronteras calculadas para ellos.
- **Método válido en cualquier momento:** secuencias de confianza u otra técnica diseñada para parada opcional bajo supuestos explícitos.

No fabriques una corrección casera dividiendo un umbral por el número de veces que alguien abrió el panel. El método depende de la variable, la dependencia, la asignación, el horizonte y la pregunta. Si la decisión importa, documenta el procedimiento o pide revisión estadística.

### 4. Conserva control y candidato comparables

Ambos deben recibir las mismas unidades o una asignación aleatoria apropiada. Registra retrasos, caídas de fuentes, reintentos, versiones y exclusiones. Si el candidato procesa PDF de madrugada y el control HTML en horario laboral, la diferencia mezcla sistema y contexto.

Evita contar páginas correlacionadas como si fueran investigaciones independientes. Un boletín de cien páginas puede representar una sola unidad decisoria. La unidad debe seguir el mecanismo que genera la variación y el impacto.

### 5. Trata cada mirada como un evento auditable

Guarda sin datos sensibles innecesarios:

- fracción de información o tamaño acumulado;
- versiones del código, reglas y corpus;
- métricas previstas y sus intervalos o evidencias;
- fronteras aplicables en esa lectura;
- incidencias de calidad y seguridad;
- decisión: parar, continuar o inconcluso;
- persona o rol que la autorizó.

El historial evita reinterpretar el ensayo después de ver el resultado. También permite explicar por qué una cifra que cruzó momentáneamente una línea no activó una promoción.

### 6. Revisa divergencias, no solo agregados

Una media puede mejorar mientras empeora una clase rara y crítica. Muestrea desacuerdos entre control y candidato; revisa correcciones, duplicados, idiomas, OCR difícil y formatos poco frecuentes. Declara los análisis por subgrupos que ya estaban previstos y etiqueta los exploratorios como tales.

La interfaz de Argo Rollouts ofrece estados de análisis exitoso, fallido o inconcluso y puede pausar cuando una métrica no permite decidir. Esa semántica es útil más allá de Kubernetes: **desconocido** debe ser un estado real, no un atajo hacia «continuar por defecto».

### 7. Separa detener de promocionar

Cruzar una frontera puede autorizar el final del experimento, pero no obliga a desplegar. Antes de promocionar, revisa calidad de datos, supuestos, cobertura, divergencias y barreras. Una puerta humana debe confirmar que el efecto es útil, que no se amplió el riesgo y que existe reversión.

## Limitaciones y falsos positivos

Un método secuencial no repara un mal diseño. Sigue fallando si se cambian métricas a mitad del ensayo, se eliminan casos incómodos, se prueban muchos segmentos hasta encontrar uno favorable o se detiene por razones no registradas. Tampoco resuelve automáticamente la multiplicidad entre métricas, candidatos o experimentos sucesivos.

Otras trampas habituales:

- confundir significación estadística con utilidad operativa;
- mirar una métrica primaria y promocionar por otra secundaria;
- ignorar autocorrelación, estacionalidad o cambios de mezcla;
- comparar ventanas temporales distintas;
- detener pronto por beneficio, pero no por daño o inutilidad;
- prolongar el ensayo hasta obtener la respuesta deseada;
- declarar equivalencia porque no apareció una diferencia significativa;
- usar el control como verdad absoluta cuando ambos flujos comparten el mismo defecto;
- aceptar una mejora media que perjudica un formato raro pero crítico;
- reutilizar la muestra de diseño como validación final sin declararlo.

Las secuencias de confianza pueden ser más anchas al principio que un intervalo calculado como si ese instante fuese la única lectura. Ese coste compra validez temporal, no certeza factual. Y un resultado inconcluso puede ser la conclusión correcta cuando el efecto útil es pequeño, la muestra se agota o la calidad impide distinguir sistemas.

## Buenas prácticas de OPSEC, ética y privacidad

- Empieza con fixtures sintéticos y una muestra pública o autorizada mínima.
- No aumentes consultas a terceros solo para engordar el experimento.
- Mantén el candidato en sombra y sin efectos externos durante la comparación.
- Separa credenciales, almacenamiento, logs y destinos del control y el candidato.
- Redacta tokens, consultas sensibles, URLs firmadas e identificadores personales.
- No experimentes con acusaciones, perfiles de personas ni decisiones de alto impacto.
- Predefine barreras de privacidad, procedencia y publicación, no solo de rendimiento.
- Registra exclusiones y datos ausentes; el silencio de una fuente también sesga.
- Limita retención y acceso a muestras, divergencias y artefactos del ensayo.
- Exige revisión humana antes de promover, atribuir o publicar.

## Alternativas y siguientes pasos

Si no hay volumen suficiente para inferencia formal, usa replay sobre un corpus versionado, revisión ciega de divergencias y criterios deterministas de seguridad. Si solo quieres detectar una regresión conocida, una prueba sobre fixtures puede ser más clara que un experimento. Si el cambio afecta a pocos casos críticos, una evaluación caso por caso puede aportar más que una media.

Para lecturas intermedias planificadas, estudia diseños secuenciales por grupos y gasto de alfa. Para monitorización flexible, explora secuencias de confianza y métodos *anytime-valid* con ayuda especializada. En cualquier opción, conserva un límite máximo y una salida inconclusa: «podemos seguir mirando» no significa «debemos seguir recogiendo».

El takeaway accionable es concreto: antes de abrir el próximo dashboard canary, escribe en una página la unidad, la métrica primaria, el efecto mínimo útil, las barreras, cuándo mirarás, cuándo pararás y quién puede promocionar. Añade después una casilla obligatoria: **¿esta regla sigue siendo válida porque hemos mirado hoy?** Si nadie puede responder con el método y sus supuestos, el panel sirve para observar, no para autorizar.

Como siguiente tema convendría estudiar las **guardas para múltiples métricas y múltiples candidatos**: cómo evitar que un experimento disciplinado vuelva a inflar el error al escoger, después, la comparación más favorable.

## Fuentes consultadas

- [Johari, Pekelis y Walsh: Always Valid Inference — Bringing Sequential Analysis to A/B Testing](https://arxiv.org/abs/1512.04922)
- [Howard, Ramdas, McAuliffe y Sekhon: Time-uniform, nonparametric, nonasymptotic confidence sequences](https://doi.org/10.1214/20-AOS1991)
- [Howard, Ramdas, McAuliffe y Sekhon: Time-uniform Chernoff bounds via nonnegative supermartingales](https://doi.org/10.1214/18-PS321)
- [DeMets: Lan-DeMets Alpha-Spending Function](https://doi.org/10.1002/9781118445112.stat06962)
- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)
- [Argo Rollouts: Analysis and Progressive Delivery](https://argo-rollouts.readthedocs.io/en/stable/features/analysis/)
