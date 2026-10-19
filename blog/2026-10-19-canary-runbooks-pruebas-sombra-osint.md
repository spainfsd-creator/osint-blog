---
title: "Canary runbooks y pruebas en sombra en OSINT: validar cambios sin convertir el ensayo en un incidente"
slug: /canary-runbooks-pruebas-sombra-osint
authors: [osint-writter]
tags: [osint, methodology, tradecraft, automation, verification, privacy]
date: 2026-10-19
image: /img/blog/2026-10-19-canary-runbooks-pruebas-sombra-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una nueva versión del pipeline clasifica cien documentos públicos sin errores técnicos y termina más deprisa que la anterior. El equipo está a punto de activarla para todo el archivo cuando una comparación revela el problema: el sistema nuevo descarta como duplicadas varias correcciones legítimas. **El proceso funciona; la decisión que produce, no.** Publicarlo de golpe habría convertido una mejora rutinaria en una pérdida silenciosa de evidencia.

![Analista OSINT comparando un flujo estable con un canary en sombra y una puerta de parada](/img/blog/2026-10-19-canary-runbooks-pruebas-sombra-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Los *canary runbooks* y las pruebas en sombra permiten observar una automatización nueva con alcance mínimo antes de confiarle efectos reales. No sustituyen la revisión humana ni demuestran que una conclusión sea verdadera. Sirven para formular una pregunta más modesta y útil: **¿se comporta el cambio como esperábamos, sobre una muestra representativa, sin ampliar la recogida ni afectar a las personas investigadas?**

Todos los nombres, dominios, documentos e identificadores del ejemplo son ficticios. Este artículo se refiere a fuentes públicas, datos sintéticos o sistemas propios y autorizados. No propone duplicar tráfico sensible hacia servicios de terceros ni automatizar atribuciones sobre personas.

## Qué son un canary runbook y una prueba en sombra

Un **canary** es una ejecución parcial y limitada en el tiempo de un cambio. Convive con una versión estable —el control— y se evalúa antes de ampliar su alcance. El [SRE Workbook de Google](https://sre.google/workbook/canarying-releases/) insiste en tres capacidades: aislar una parte de la población, evaluar si el candidato es bueno o malo e integrar esa evaluación en la decisión de continuar.

Una **prueba en sombra** ejecuta el candidato con una copia de la entrada, pero no deja que su salida controle el resultado real. En infraestructura web también se llama *traffic mirroring*: la [documentación de Istio](https://istio.io/latest/docs/tasks/traffic-management/mirroring/) describe el envío fuera del camino crítico y el descarte de la respuesta de la copia. Trasladado a OSINT, el flujo estable sigue publicando, etiquetando o avisando; el flujo sombra solo produce observaciones comparables en un destino aislado.

El **runbook** expresa el contrato del ensayo: alcance, datos permitidos, versión estable y candidata, métricas, duración, responsables, criterios de parada y procedimiento de reversión. Su parte ejecutable puede recoger resultados y aplicar límites, pero no debe decidir por sí sola una atribución, una acusación o una acción que afecte a una persona.

Las dos técnicas responden a riesgos distintos:

- la sombra descubre divergencias sin dar autoridad a la versión nueva;
- el canary comprueba una fracción pequeña con efectos cuidadosamente acotados;
- la promoción gradual amplía el alcance solo cuando la evidencia satisface condiciones escritas de antemano.

No todos los flujos necesitan las tres fases. Si una herramienta solo transforma una copia local, la sombra puede ser suficiente. Si envía alertas o publica artefactos, conviene mantener una puerta humana antes del primer efecto real.

## Caso legítimo: el clasificador que confundía correcciones con duplicados

El observatorio ficticio **Lupa Cívica** mantiene un archivo de resoluciones públicas. Su pipeline estable descarga documentos desde una lista autorizada, conserva la URL y el momento de observación, calcula una huella, extrae texto y agrupa versiones. El equipo prepara un extractor nuevo que promete tratar mejor los PDF escaneados.

Antes de sustituir el flujo estable, construye un corpus sintético y una muestra autorizada de documentos ya públicos. Incluye pares deliberadamente difíciles:

- dos ficheros idénticos servidos desde URLs diferentes;
- una resolución y su corrección posterior;
- un PDF reescaneado cuyo texto es equivalente, pero cuyos bytes cambian;
- una página de error guardada por accidente con extensión `.pdf`;
- un documento sin fecha legible;
- una copia truncada.

Durante la prueba en sombra, ambos pipelines reciben el mismo manifiesto de entrada. El estable mantiene sus efectos habituales en un entorno de ensayo; el candidato escribe en otro almacén sin enviar avisos ni modificar el índice público. Cada salida conserva `input_id`, versión del código, regla aplicada, digest y razón de la decisión.

El candidato reduce los fallos de OCR, pero agrupa una corrección con el documento inicial porque normaliza en exceso la portada. La tasa global de éxito parece mejor y el tiempo medio baja. Solo una métrica semántica —«correcciones conservadas como versiones diferenciadas»— detecta la regresión.

Lupa Cívica no promociona. Etiqueta el resultado como **inconcluso**, conserva los artefactos mínimos del ensayo, añade ese par al conjunto de regresión y modifica la regla. La parada no demuestra que el extractor sea malo; demuestra que aún no existe evidencia suficiente para darle autoridad.

## Flujo recomendado

### 1. Escribe un contrato de comparación

Empieza por una hipótesis falsable, no por un porcentaje atractivo. Por ejemplo: «el candidato conservará todas las correcciones conocidas, no aumentará las asociaciones erróneas y reducirá los fallos de extracción sobre el corpus acordado».

Un manifiesto conceptual puede ser así:

```yaml
experiment_id: extractor-pdf-c7
baseline: extractor-estable
candidate: extractor-candidato
mode: shadow-read-only
population: corpus-sintetico-v3
effects_allowed: none
stop_if:
  - correction_lost > 0
  - unexpected_external_request > 0
  - provenance_missing > 0
decision_states: [promote, stop, inconclusive]
```

La configuración no necesita contener consultas, nombres reales ni tokens. Debe enlazar a versiones inmutables de código, reglas y corpus, además de indicar quién puede detener y quién puede promocionar.

### 2. Construye primero una población segura

La muestra debe cubrir la diversidad relevante sin copiar un caso sensible entero. Empieza con datos sintéticos y artefactos públicos controlados. Añade casos límite procedentes de errores pasados, pero minimizados y desidentificados cuando sea necesario.

Una muestra aleatoria puede ocultar clases raras. Combina:

1. ejemplos normales para medir el comportamiento cotidiano;
2. estratos difíciles —idiomas, formatos, ausencia de campos—;
3. regresiones conocidas;
4. entradas adversas seguras, como archivos truncados o esquemas inesperados;
5. controles negativos que el pipeline debe rechazar.

En procesos por lotes, la unidad del canary no tiene por qué ser tráfico. Puede ser una partición temporal, una fuente autorizada, un tipo documental o un conjunto de identificadores sintéticos. La guía de Google sobre [procesamiento fiable de datos](https://sre.google/workbook/data-processing/) recomienda segmentar la población y detectar pronto los fallos para limitar el impacto.

### 3. Aísla efectos, secretos y destinos

El candidato debe ejecutarse con credenciales de solo lectura siempre que sea posible. Bloquea correo, webhooks, publicación, escritura en el índice estable y cualquier acción sobre terceros. Si necesita escribir resultados, usa un destino efímero con retención definida.

Copiar entradas reales hacia un servicio diferente puede crear una nueva cesión de datos, romper términos de uso o ampliar innecesariamente la exposición. «Solo es una sombra» no elimina esas obligaciones. Prefiere reproducir manifiestos y artefactos mínimos dentro del mismo perímetro autorizado; sustituye selectores personales por fixtures sintéticos.

### 4. Compara significado, no solo disponibilidad

Errores, latencia y consumo son útiles, pero un pipeline OSINT puede responder `200` y producir una conclusión peor. Separa métricas por versión y registra denominadores. Compara al menos:

- cobertura: entradas procesadas, omitidas y no observables;
- procedencia: salidas que conservan fuente, tiempo, versión y transformación;
- divergencia: decisiones distintas entre control y candidato;
- falsos positivos y falsos negativos sobre casos etiquetados;
- estabilidad: misma entrada y configuración, misma salida esperada;
- privacidad: campos retenidos, volcados a logs o enviados fuera del perímetro;
- efectos: intentos de escritura, aviso o publicación, aunque hayan sido bloqueados.

Una tasa agregada puede esconder una clase pequeña y crítica. Publica siempre recuentos junto a porcentajes y desglosa los estratos definidos en el contrato. Google advierte además que una métrica debe ser representativa y atribuible al cambio; comparar «antes» y «después» sin un control simultáneo mezcla la variación temporal con el efecto del candidato.

### 5. Define parada, incertidumbre y promoción

No reduzcas la decisión a verde o rojo. Usa tres estados:

- **promover:** se alcanza el tamaño mínimo de muestra y se cumplen todos los umbrales;
- **detener:** se cruza un límite de seguridad o una regresión crítica;
- **inconcluso:** faltan datos, una métrica no está disponible o la divergencia no puede explicarse.

Las plataformas de entrega progresiva materializan esta idea. [Argo Rollouts](https://argo-rollouts.readthedocs.io/en/stable/features/analysis/) distingue análisis correctos, fallidos e inconclusos; estos últimos pausan en vez de fingir una decisión. Su documentación de [estrategia canary](https://argo-rollouts.readthedocs.io/en/stable/features/canary/) permite combinar pesos, pausas y abortos. No es necesario usar Kubernetes para adoptar el patrón: el valor está en expresar el estado y su consecuencia de forma inequívoca.

Promociona por etapas pequeñas. Primero habilita una fuente o lote de bajo riesgo; después amplía solo si siguen presentes el control, la observación independiente y la reversión. No ejecutes varios experimentos solapados sobre la misma población: contaminan la atribución de las divergencias.

### 6. Conserva una comparación reproducible

Guarda el manifiesto, las versiones, los identificadores de entrada, las métricas crudas necesarias y la decisión. No hace falta retener todo el contenido. Un resumen por estrato y una muestra mínima de divergencias pueden bastar si cada resultado remite al artefacto autorizado durante su plazo de conservación.

La promoción debe quedar separada de quien preparó el candidato cuando el impacto sea relevante. Los [entornos de despliegue de GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) ilustran controles como revisores requeridos, prevención de autoaprobación y reglas de protección. Son mecanismos de software, no garantías editoriales, pero ayudan a impedir que el mismo actor proponga, evalúe y publique sin fricción.

## Checklist antes de promover

- [ ] El objetivo y la hipótesis están escritos antes de observar resultados.
- [ ] Control y candidato reciben entradas equivalentes e identificables.
- [ ] La muestra incluye casos normales, raros, negativos y regresiones conocidas.
- [ ] El candidato no puede publicar, avisar ni modificar el índice estable durante la sombra.
- [ ] Las llamadas externas están bloqueadas o expresamente autorizadas.
- [ ] Las métricas separan versiones, estratos, recuentos y porcentajes.
- [ ] Hay umbrales absolutos para procedencia, privacidad y efectos inesperados.
- [ ] «Sin datos» produce un estado inconcluso, nunca una aprobación implícita.
- [ ] Existe una persona con autoridad de parada y otra puerta para la promoción.
- [ ] La reversión se ha ensayado con fixtures sintéticos.
- [ ] El registro del experimento evita contenido personal y secretos.
- [ ] Se ha definido cuándo borrar salidas y copias auxiliares.

## Limitaciones y falsos positivos

Un canary pequeño puede no contener el formato que romperá mañana. Una sombra puede cambiar el rendimiento del sistema por duplicar trabajo. Un control antiguo puede estar equivocado: coincidir con él no convierte al candidato en correcto. Y dos pipelines pueden compartir la misma dependencia defectuosa, produciendo un acuerdo engañoso.

También hay divergencias legítimas. Un extractor nuevo puede representar mejor una fecha ambigua o separar correctamente dos entidades antes fusionadas. Clasifica las diferencias por causa y revisa una muestra; no maximices el acuerdo como si fuera la verdad.

Evita estos atajos:

- usar datos reales sensibles porque «producción es la única muestra representativa»;
- enviar copias a un proveedor nuevo sin revisar finalidad, contrato y retención;
- medir solo velocidad, coste o ausencia de excepciones;
- promocionar con una muestra diminuta o elegida después de ver el resultado;
- ocultar fallos bajo un promedio global;
- permitir que la versión sombra emita notificaciones reales;
- tratar una pausa por falta de métricas como éxito;
- conservar indefinidamente entradas y salidas del ensayo;
- automatizar acusaciones, atribuciones o decisiones sobre personas.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa fixtures sintéticos por defecto y minimiza cualquier muestra real autorizada.
- Separa credenciales, redes, destinos y logs del control y del candidato.
- Aplica solo lectura y denegación de salida salvo excepciones explícitas.
- Redacta tokens, consultas sensibles, URLs firmadas e identificadores personales.
- Versiona reglas y corpus para explicar por qué dos ejecuciones difieren.
- Revisa términos de servicio, licencias y límites antes de replicar consultas.
- No aumentes la frecuencia de acceso a una fuente por duplicar el pipeline.
- Establece límites de tiempo, volumen, coste y almacenamiento.
- Haz que el estado desconocido detenga la promoción.
- Mantén el juicio humano en atribución, impacto y publicación.

## Alternativas y siguientes pasos

Si el pipeline todavía no es reproducible, empieza con **replay offline** sobre fixtures versionados. Si solo cambia una regla, una prueba diferencial puede comparar salidas sin desplegar otro servicio. Para operaciones de alto impacto, un entorno azul/verde mantiene dos versiones aisladas y permite una conmutación controlada. Cuando el riesgo sea principalmente editorial, una doble revisión ciega de una muestra puede revelar más que otra capa de automatización.

El takeaway accionable es concreto: toma una automatización OSINT que quieras cambiar y escribe hoy cinco líneas —población, efecto prohibido, métrica semántica, criterio de parada y estado inconcluso—. Ejecútala después sobre diez fixtures sintéticos en modo solo lectura y compara cada divergencia con el control. Si no puedes explicar qué dato autoriza la promoción, la respuesta correcta todavía es parar.

Como siguiente tema convendría estudiar los **experimentos secuenciales y el sesgo de parada**: cómo evitar que mirar continuamente una métrica nos haga promocionar por una fluctuación afortunada.

## Fuentes consultadas

- [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/)
- [Google SRE Workbook: Data Processing Pipelines](https://sre.google/workbook/data-processing/)
- [Istio: Traffic Mirroring](https://istio.io/latest/docs/tasks/traffic-management/mirroring/)
- [Argo Rollouts: Analysis and Progressive Delivery](https://argo-rollouts.readthedocs.io/en/stable/features/analysis/)
- [Argo Rollouts: Canary Deployment Strategy](https://argo-rollouts.readthedocs.io/en/stable/features/canary/)
- [GitHub Docs: Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
