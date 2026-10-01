---
title: "Observabilidad de datos en OSINT: detectar silencios sin confundir un panel verde con la verdad"
slug: /observabilidad-datos-osint
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-10-01
image: /img/blog/2026-10-01-observabilidad-datos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un equipo OSINT observando la salud de un pipeline de datos públicos](/img/blog/2026-10-01-observabilidad-datos-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/observabilidad-datos-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El cuadro de mando sigue en verde, la actualización nocturna terminó sin errores y el informe muestra 312 contratos nuevos. Hay un problema: la fuente publicaba normalmente entre 900 y 1.200 registros cada lunes. **El pipeline funcionó; la adquisición llegó incompleta y nadie estaba mirando el silencio.**

La observabilidad de datos sirve para detectar ese tipo de anomalías operativas. Combina señales sobre frescura, volumen, esquema, distribución, ejecución y procedencia para responder qué cambió, cuándo empezó y qué resultados podrían estar afectados. En OSINT no demuestra que una fuente sea verdadera ni que el universo observado esté completo. Permite saber si nuestros datos se comportan como esperábamos y cuándo debemos detener una conclusión para investigar.

<!-- truncate -->

## Qué es y para qué sirve

Observar no es acumular gráficos. Un sistema es observable cuando sus señales permiten formular preguntas nuevas sobre su estado sin tener que añadir instrumentación después de cada incidente. El [manual introductorio de OpenTelemetry](https://opentelemetry.io/docs/concepts/observability-primer/) describe métricas, logs y trazas como señales complementarias para entender el comportamiento de un sistema. En un pipeline OSINT podemos adaptar esa idea:

- las **métricas** resumen recuentos, edades, nulos, duplicados o duraciones;
- los **logs estructurados** explican decisiones, errores y límites de paginación;
- las **trazas o identificadores de ejecución** conectan adquisición, transformación y publicación;
- el **linaje** señala qué entradas y procesos produjeron cada salida;
- los **contratos y expectativas** hacen explícito qué comportamiento consideramos normal.

La palabra importante es *comportamiento*. Una alerta puede indicar que una API devolvió menos filas, que apareció una columna o que el último registro tiene dos días de antigüedad. Ninguna de esas señales explica por sí sola la causa. Puede haber un fallo propio, un cambio legítimo del portal, un festivo, una corrección retrospectiva o una reducción real de actividad.

La observabilidad aporta tres capacidades prácticas:

1. **Detección:** advertir una desviación antes de que contamine un informe.
2. **Diagnóstico:** acotar si el problema está en la fuente, la descarga, el parser o la transformación.
3. **Impacto:** localizar qué tablas, gráficos o conclusiones dependen del lote sospechoso.

No sustituye la corroboración documental. Una ejecución perfecta puede procesar una fuente sesgada; una alerta ruidosa puede coincidir con datos completamente válidos.

## Caso de uso legítimo: un observatorio ficticio de contratación

Imaginemos que un equipo de investigación descarga cada noche adjudicaciones de un portal público de `Villa Norte`, una administración inventada. Conserva la respuesta original, normaliza los registros y publica agregados semanales. No busca perfilar personas: fiscaliza gasto público con campos empresariales y administrativos necesarios.

Su primera versión solo comprueba el código de salida. Si la descarga responde `200` y el parser no lanza una excepción, el job queda verde. Ese criterio deja varios agujeros:

- una página de mantenimiento también puede responder `200`;
- la paginación puede detenerse en la primera página;
- el portal puede retrasar una carga sin avisar;
- una columna puede cambiar de tipo y convertirse silenciosamente en texto vacío;
- una deduplicación defectuosa puede reducir el volumen sin romper el proceso;
- una categoría nueva puede quedar agrupada como `desconocida`.

El equipo define entonces un conjunto pequeño de señales por lote:

| Dimensión | Señal | Pregunta que ayuda a responder |
| --- | --- | --- |
| Frescura | edad del registro más reciente y hora de adquisición | ¿la fuente se ha actualizado cuando suele hacerlo? |
| Volumen | filas por lote, páginas recorridas y bytes recibidos | ¿hemos adquirido una cantidad plausible? |
| Esquema | columnas, tipos y campos obligatorios | ¿la interfaz cambió de forma incompatible? |
| Distribución | proporción de nulos, categorías y rangos | ¿los valores se desplazaron de forma inesperada? |
| Ejecución | duración, reintentos y errores por etapa | ¿dónde empezó la degradación? |
| Procedencia | URL, instante, hash, versión del código e ID de ejecución | ¿podemos reconstruir el resultado afectado? |

El lunes aparecen 312 filas. La alerta de volumen se activa, pero frescura y esquema permanecen normales. El registro estructurado revela que solo se recorrieron dos páginas, frente a seis o siete habituales. Esa combinación no prueba que falten contratos, aunque sí justifica poner el lote en cuarentena y revisar la paginación antes de actualizar el informe.

## Flujo recomendado

### 1. Define el objeto observado y su ritmo real

Empieza por un dataset y una decisión concreta, no por una plataforma. Anota:

- quién publica la fuente y con qué cadencia declarada u observada;
- qué significa una fila y cuál es su granularidad;
- qué timestamp representa publicación, modificación y adquisición;
- qué ventanas tienen fines de semana, festivos o cierres administrativos;
- qué derivados consumen esos datos.

La [documentación de frescura de dbt](https://docs.getdbt.com/docs/deploy/source-freshness) muestra por qué la frecuencia del control debe guardar relación con el umbral que pretende vigilar. En OSINT, un chequeo cada 24 horas no puede detectar con precisión un retraso de una hora. Tampoco tiene sentido imponer un SLA horario a una fuente que publica mensualmente.

Evita llamar «retraso» a todo lo que no se actualiza. La frescura debe medirse contra una expectativa explícita y contextual: calendario, zona horaria, ventanas de publicación y posibles datos que llegan tarde.

### 2. Instrumenta la adquisición antes de medir el resultado

Registra una fila de control por ejecución con datos que no expongan secretos:

```json
{
  "run_id": "2026-10-01T01:00:00Z-vn-contratos",
  "source": "portal-publico-villa-norte",
  "started_at": "2026-10-01T01:00:00Z",
  "finished_at": "2026-10-01T01:03:12Z",
  "http_responses": 7,
  "pages_seen": 7,
  "raw_bytes": 1842201,
  "raw_sha256": "valor-ficticio",
  "parser_revision": "commit-ficticio",
  "status": "complete"
}
```

El ejemplo es deliberadamente ficticio. En producción, separa logs operativos de los documentos originales y controla el acceso a ambos. Los [logs estructurados de OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/logs/) facilitan validar y correlacionar campos estables; no hace falta registrar cuerpos, tokens, cabeceras de autenticación ni selectores personales.

### 3. Añade controles simples y explicables

Empieza con reglas que el equipo pueda interpretar:

- el lote contiene al menos una fila cuando el calendario prevé publicación;
- el número de páginas coincide con el declarado por la respuesta o se explica la diferencia;
- el campo identificador no es nulo y mantiene su unicidad esperada;
- el timestamp más reciente no supera una edad acordada;
- las columnas críticas existen y conservan tipos compatibles;
- la proporción de filas rechazadas queda registrada.

La referencia de [contratos de Soda](https://docs.soda.io/reference/contract-language-reference) contempla comprobaciones de esquema, recuento de filas y frescura. [Great Expectations](https://docs.greatexpectations.io/docs/core/define_expectations/) formula las expectativas como aserciones verificables sobre los datos. Ambas ideas son útiles aunque el equipo implemente controles propios: convertir supuestos implícitos en reglas versionadas y resultados conservables.

No copies umbrales de otro proyecto. «Más de cero filas» detecta un vacío total, pero no una descarga truncada. «Menos del 5 % de nulos» puede ser razonable para un identificador obligatorio y absurdo para un campo opcional. Cada regla necesita propietario, justificación y respuesta prevista.

### 4. Construye una línea base sin tratarla como ley

Guarda series temporales de los controles: filas, páginas, duración, nulos y categorías. Compara el lote actual con ventanas equivalentes, como el mismo día de la semana, y conserva hitos que expliquen cambios conocidos.

Una línea base ayuda a descubrir desviaciones, pero hereda la historia de la fuente. Si el portal llevaba meses omitiendo una provincia, la estabilidad de esa omisión no la vuelve correcta. Además, una campaña electoral, una reforma normativa o un cierre trimestral pueden cambiar legítimamente el patrón.

Usa umbrales de advertencia y error con una zona intermedia. La advertencia pide contexto; el error puede poner en cuarentena la salida. No dejes que una anomalía estadística publique automáticamente una acusación.

### 5. Correlaciona señales antes de diagnosticar

Una sola métrica suele admitir muchas explicaciones. Combina señales:

- **frescura alta + volumen cero:** posible retraso de fuente, filtro temporal o error de adquisición;
- **esquema nuevo + nulos crecientes:** parser incompatible o campo recién introducido;
- **duración corta + menos páginas:** paginación truncada o respuesta prematura;
- **volumen normal + distribución anómala:** cambio real, clasificación nueva o transformación defectuosa;
- **todo verde + queja documental:** los controles no cubren la dimensión que importa.

El último caso es esencial. La ausencia de alerta solo significa que las reglas ejecutadas no vieron una desviación. No garantiza cobertura total.

### 6. Diseña el triage y la cuarentena

Cada alerta debe indicar:

1. qué control falló y con qué valor;
2. cuál era el umbral y por qué existe;
3. qué ejecución y originales están implicados;
4. qué derivados podrían estar afectados;
5. quién revisa y qué condiciones permiten publicar.

Conserva el lote sospechoso sin mezclarlo con la versión publicada. Repite la adquisición solo si puedes distinguirla de la original mediante otro `run_id`, tiempo y hash. Si el segundo intento difiere, preserva ambos: borrar el primero elimina precisamente la evidencia necesaria para entender el incidente.

### 7. Cierra el incidente con aprendizaje verificable

Documenta causa, alcance, decisión y cambio de control. Si el portal añadió paginación por cursor, incorpora un fixture sintético que reproduzca el caso. Si el lunes festivo causó ruido, ajusta el calendario sin silenciar todos los lunes. Si no conoces la causa, escribe «causa no determinada» y limita las conclusiones.

El objetivo no es que el panel vuelva a verde cuanto antes. Es que el equipo pueda explicar por qué confía —o no— en el siguiente resultado.

## Limitaciones y falsos positivos

### Una fuente estable puede estar incompleta

Frescura, volumen y esquema pueden ser impecables mientras el publicador excluye registros, corrige sin historial o aplica criterios desconocidos. La observabilidad ve el comportamiento accesible, no el universo ausente. Contrasta con documentación oficial, recuentos publicados y fuentes independientes cuando existan.

### La estacionalidad parece una anomalía

Festivos, cierres presupuestarios, campañas y calendarios académicos alteran los patrones. Una comparación ingenua con «ayer» genera ruido. Segmenta por periodos comparables y conserva el contexto que justificó cada excepción.

### Los timestamps no significan lo mismo

`published_at`, `updated_at`, `loaded_at` y `observed_at` responden a preguntas distintas. Medir frescura sobre la fecha de adquisición puede declarar reciente un documento antiguo; medirla sobre un campo corregible puede hacer que todo el lote parezca nuevo. Define la semántica y conserva las zonas horarias.

### El control puede fallar junto al pipeline

Si la métrica de filas se calcula sobre la misma tabla truncada, ambos componentes pueden coincidir en una cifra incorrecta. Siempre que sea proporcionado, compara señales independientes: bytes del original, páginas declaradas, manifiestos del proveedor y filas normalizadas.

### Demasiadas alertas destruyen la atención

Un umbral sensible sin proceso de respuesta crea fatiga. Mide cuántas alertas fueron accionables, elimina duplicados y agrupa síntomas de una misma ejecución. Reducir ruido no significa subir todos los umbrales: puede requerir mejor contexto y reglas más específicas.

## Buenas prácticas de OPSEC, ética y privacidad

- Instrumenta tu pipeline; no aumentes la carga sobre una fuente pública solo para alimentar un panel.
- Respeta términos, límites de uso, robots y ventanas de consulta aplicables.
- No incluyas secretos, cookies, cuerpos completos ni datos personales innecesarios en logs o alertas.
- Usa identificadores de ejecución y referencias internas en lugar de copiar registros sensibles a herramientas externas.
- Restringe el acceso a paneles: las métricas y nombres de datasets pueden revelar líneas de investigación.
- Define retención separada para telemetría, originales y productos derivados.
- Prueba reglas y notificaciones con fixtures ficticios antes de conectarlas a casos reales.
- Conserva las excepciones con motivo, autoría y caducidad; una desactivación temporal no debe volverse permanente por olvido.
- Exige revisión humana antes de publicar conclusiones sensibles o atribuciones.
- Describe incertidumbre y cobertura: «no observamos» no equivale a «no existe».

## Lista de control

- [ ] Cada dataset tiene propietario, granularidad y cadencia documentados.
- [ ] Se distinguen tiempos de publicación, modificación y adquisición.
- [ ] Cada ejecución conserva ID, estado, hash del original y versión del código.
- [ ] Se miden frescura, volumen, esquema y rechazos con umbrales justificados.
- [ ] La paginación tiene un control independiente del recuento final.
- [ ] Advertencia, error y cuarentena tienen respuestas definidas.
- [ ] Los paneles no contienen secretos ni datos personales innecesarios.
- [ ] Las alertas enlazan con originales y derivados afectados sin duplicarlos.
- [ ] Festivos y estacionalidad se modelan de forma explícita.
- [ ] Los controles se ensayan con datos sintéticos y fallos conocidos.
- [ ] Los incidentes cierran con causa, alcance y prueba de regresión cuando es posible.
- [ ] Un estado verde nunca se presenta como verificación factual.

## Alternativas y siguientes pasos

Si el problema principal es describir dependencias entre ejecuciones y datasets, [OpenLineage](/openlineage-linaje-datos-osint) ofrece un vocabulario específico. Para expresar aserciones de calidad están [Great Expectations](/great-expectations-osint-calidad-datos) y [Soda Core](/soda-core-osint-contratos-datos-deriva-esquema); para probar transformaciones, [dbt](/dbt-osint-pruebas-transformaciones); y para vigilar cambios en páginas públicas, [changedetection.io](/changedetection-io-osint-monitorizar-cambios-web). La observabilidad coordina esas señales alrededor de preguntas operativas y decisiones de publicación.

El takeaway accionable es sencillo: elige hoy una adquisición recurrente y registra durante una semana cinco valores —hora del último dato, filas, páginas, bytes y rechazos— junto con un ID de ejecución. Define una sola alerta con respuesta humana. Si no puedes explicar qué harías cuando se active, todavía no tienes un control: solo tienes una cifra.

Como próximo tema, merece la pena estudiar **presupuestos de error para pipelines OSINT**: cómo decidir cuánta demora, pérdida o degradación puede tolerarse antes de detener una publicación, sin copiar mecánicamente los SLO del mundo del software.

## Fuentes consultadas

- [OpenTelemetry: introducción a la observabilidad](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry: logs y correlación de señales](https://opentelemetry.io/docs/concepts/signals/logs/)
- [dbt: source freshness](https://docs.getdbt.com/docs/deploy/source-freshness)
- [Soda: referencia del lenguaje de contratos](https://docs.soda.io/reference/contract-language-reference)
- [Great Expectations: definir Expectations](https://docs.greatexpectations.io/docs/core/define_expectations/)
- [OpenLineage: métricas de calidad de datos](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_metrics/)
