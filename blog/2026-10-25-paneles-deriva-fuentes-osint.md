---
title: "Paneles de deriva para fuentes OSINT: alertar sin confundir cambio con error"
slug: /paneles-deriva-fuentes-osint
authors: [osint-writter]
tags: [osint, methodology, monitoring, data, verification, privacy]
date: 2026-10-25
image: /img/blog/2026-10-25-paneles-deriva-fuentes-osint.png
aiDisclosure: generated
humanReviewed: false
---

El panel se vuelve rojo a las 06:10. Han desaparecido dos categorías, la mediana de páginas por documento se ha duplicado y el porcentaje de fechas vacías ha subido doce puntos. El equipo puede detener toda la investigación, ignorar la alarma o anunciar que la fuente se ha degradado. **Las tres respuestas serían prematuras: el panel ha detectado un cambio, todavía no su causa ni su significado.**

![Analista ante un panel que separa cambios de esquema, mezcla de fuentes y calidad](/img/blog/2026-10-25-paneles-deriva-fuentes-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Una fuente pública viva no se comporta como un CSV congelado. Cambia plantillas, corrige registros, incorpora organismos, sufre caídas y modifica la forma de paginar. Un panel de deriva sirve para hacer visibles esas variaciones sin convertir cada diferencia estadística en una conclusión sobre la fuente, el pipeline o las personas mencionadas.

Todos los nombres, dominios, documentos y cifras del ejemplo son ficticios. El método se limita a fuentes públicas o sistemas propios y autorizados. Monitorizar una fuente no autoriza a saltarse controles de acceso, recopilar más datos personales de los necesarios ni automatizar atribuciones.

## Qué es un panel de deriva (y para qué sirve)

Un panel de deriva compara una ventana actual con una referencia explícita y muestra señales de que los datos o el proceso ya no se parecen a lo esperado. Su trabajo es formular preguntas investigables: ¿ha cambiado la estructura?, ¿recibimos otra mezcla de documentos?, ¿ha empeorado la extracción?, ¿falta una fuente?, ¿la diferencia procede del calendario?

Conviene separar al menos cuatro capas:

| Capa | Pregunta | Señales posibles | Lo que no demuestra |
| --- | --- | --- | --- |
| disponibilidad | ¿la fuente y el colector están entregando datos? | volumen, latencia, errores HTTP, retraso de publicación | que los documentos sean correctos |
| esquema | ¿la forma sigue siendo compatible? | columnas, tipos, campos obligatorios, estructura HTML | que el significado no haya cambiado |
| mezcla y distribución | ¿llegan proporciones o valores distintos? | organismo, formato, idioma, páginas, tamaños, fechas | que exista una degradación |
| calidad verificada | ¿el resultado sigue cumpliendo la tarea? | errores etiquetados, discrepancias humanas, cobertura y procedencia | que toda variación tenga una única causa |

La documentación de Google recomienda validar esquemas, vigilar valores inesperados y distribuciones, y observar por separado los cortes importantes. Great Expectations distingue igualmente la validación estructural —columnas y tipos— de la calidad semántica. Esa separación evita un error frecuente: un lote puede conservar exactamente el mismo esquema y, aun así, contener fechas interpretadas con otra convención.

NIST encuadra la monitorización como una actividad continua: comparar producción y pruebas, documentar diferencias, combinar pruebas estadísticas con conocimiento del dominio, revisar casos inesperados y medir calidad real cuando aparezca información de referencia. Una alerta es el comienzo de ese circuito, no su veredicto.

## Caso legítimo: el boletín que parecía haberse roto

El observatorio ficticio **Faro Documental** recopila resoluciones públicas de seis organismos. Conserva la URL, la hora de adquisición, el hash, el tipo de respuesta, la versión del extractor y un pequeño conjunto de campos normalizados. Su panel compara cada semana con una referencia móvil de ocho semanas.

Un lunes aparecen tres alertas:

- la proporción de PDF escaneado pasa del 18 % al 41 %;
- los documentos del organismo `O-04` caen casi a cero;
- los valores vacíos en `fecha_resolucion` aumentan del 3 % al 15 %.

El agregado sugiere deterioro, pero la investigación por capas cuenta otra historia. `O-04` ha movido su publicación al martes por un festivo; otro organismo ha digitalizado un archivo histórico compuesto por escaneos; el extractor de fechas falla en esos documentos porque la fecha aparece dentro de la imagen.

La fuente no ha perdido necesariamente calidad. Ha cambiado la mezcla, y ese cambio ha revelado una limitación del pipeline. Faro Documental marca la semana como evento conocido, mantiene la alerta de cobertura hasta recibir el lote del martes y pone en cuarentena solo los campos derivados de los escaneos. Una muestra revisada por dos personas permite estimar después el error del OCR y decidir si hace falta adaptar el flujo.

## Flujo recomendado

### 1. Define la unidad y la decisión antes de dibujar gráficas

Una fila puede ser una página, un documento, una versión o un evento. Si unas semanas cuentan páginas y otras expedientes, el panel detectará la convención de conteo. Escribe la unidad, el momento de observación y la decisión que puede provocar cada señal.

Un contrato mínimo podría ser:

```yaml
monitor: resoluciones-publicas
unit: document_version
event_time: source_publication_time
observed_time: acquired_at_utc
reference: rolling_8_complete_weeks
segments: [source, format, language]
allowed_actions: [annotate, investigate, quarantine_derivative]
forbidden_automatic_actions: [attribute, publish_claim, block_person]
```

Separa siempre la hora que declara la fuente de la hora a la que tú la observaste. Los retrasos de adquisición no deben presentarse como retrasos editoriales sin comprobarlos.

### 2. Conserva una referencia identificable

Una referencia puede ser una versión estable, una ventana temporal anterior o una población acordada. Debe viajar con:

- periodo y criterio de inclusión;
- fuentes cubiertas y ausencias conocidas;
- versión del colector y de las transformaciones;
- tamaños de muestra y segmentación;
- correcciones o incidentes anotados;
- hash o identificador del manifiesto cuando proceda.

Evidently, por ejemplo, calcula la deriva comparando datos actuales con datos de referencia y permite configurar métodos y umbrales por tipo de columna. La herramienta resuelve el cálculo; no decide si la referencia representa una semana normal, una campaña extraordinaria o un periodo ya obsoleto.

Evita una única línea base eterna. Conserva referencias versionadas y, cuando uses una ventana móvil, muestra también una comparación con un periodo estable. Así podrás distinguir una ruptura repentina de un desplazamiento lento que la propia ventana móvil empieza a absorber.

### 3. Comprueba disponibilidad y esquema antes de la estadística

No calcules una sofisticada distancia entre distribuciones si falta media tabla. Empieza por señales baratas y explicables:

- ejecuciones previstas frente a completadas;
- códigos de respuesta y latencia;
- páginas o documentos observados;
- columnas presentes, tipos y orden solo cuando sea relevante;
- porcentaje de nulos y valores imposibles;
- versión del parser y del esquema.

Una columna nueva puede ser compatible; una columna renombrada puede romper el proceso; un tipo que pasa de fecha a texto puede mantener todos los valores visibles y perder la ordenación. Clasifica los cambios como esperados, compatibles, incompatibles o todavía desconocidos. El estado «desconocido» es útil: evita forzar una explicación para cerrar el aviso.

### 4. Mide la mezcla antes de atribuir calidad

Un promedio global cambia cuando cambia la composición. Segmenta por dimensiones relacionadas con el trabajo, no por datos personales que no necesitas:

- fuente u organismo;
- formato y presencia de OCR;
- idioma;
- plantilla o familia documental;
- ventana de publicación;
- vía de adquisición autorizada.

Muestra numeradores y denominadores. «Los nulos se triplicaron» significa algo distinto con 20 documentos que con 20.000. Incluye además la contribución de cada segmento al cambio agregado: quizá ningún segmento haya empeorado y solo haya aumentado el peso del más difícil.

### 5. Elige señales según el tipo de dato

No existe una métrica universal de deriva. Para una categoría puede ser útil comparar proporciones; para una variable numérica, cuantiles o distancias entre distribuciones; para texto, descriptores como longitud, idioma detectado o tasa de OCR pueden ser más interpretables que un único vector opaco.

Herramientas como Evidently incluyen métodos distintos —entre ellos Kolmogórov-Smirnov, chi-cuadrado, Jensen-Shannon, Wasserstein o PSI— y permiten configurarlos por columna. Esa variedad no convierte sus umbrales por defecto en una política. El método, el tamaño muestral y el umbral deben quedar registrados, junto con la razón operativa por la que la diferencia importa.

Con muestras muy grandes, una prueba puede marcar diferencias minúsculas; con muestras pequeñas, puede no detectar un cambio importante. Por eso conviene combinar:

1. una medida de magnitud;
2. incertidumbre o estabilidad entre ventanas;
3. un umbral práctico ligado al proceso;
4. revisión de ejemplos y procedencia;
5. calidad etiquetada cuando esté disponible.

### 6. Diseña alertas con estado, persistencia y propietario

Una alerta útil necesita más que rojo o verde. Registra:

```yaml
alert_id: drift-2026-10-25-07
signal: missing_date_rate
segment: source_O04/scanned_pdf
reference_manifest: ref-8w-2026-10-18
current_window: 2026-10-19/2026-10-25
effect: "+12 percentage points"
sample_size: 184
state: investigating
owner_role: data-quality-on-call
allowed_action: quarantine_date_field
next_check: labeled_sample
```

Usa estados como `observada`, `investigando`, `explicada`, `acción pendiente`, `resuelta` y `falso positivo`. Exige persistencia para señales ruidosas y permite barreras inmediatas para fallos inequívocos, como un campo obligatorio ausente en todo el lote.

El propietario debe saber qué puede hacer. Un aviso de distribución puede abrir una revisión; no debería volver a entrenar, descartar registros ni publicar una acusación por sí solo.

### 7. Investiga con una matriz de hipótesis

Ante una alerta, compara explicaciones alternativas:

| Hipótesis | Comprobación segura |
| --- | --- |
| cambió la fuente | revisar aviso oficial, HTML/PDF y versiones preservadas |
| cambió la mezcla | desglosar por fuente, formato y periodo |
| cambió el colector | comparar versiones y repetir sobre una copia autorizada |
| hubo retraso | contrastar hora de publicación y de adquisición |
| falló la transformación | ejecutar controles sobre original y derivado |
| cambió la realidad observada | buscar corroboración independiente y contexto temporal |

Conserva el original adquirido y genera derivados nuevos; no sobrescribas la evidencia que permite comparar. Si una fuente corrigió el documento, registra la transición en vez de fingir que la primera versión nunca existió.

### 8. Cierra con calidad real y aprendizaje

Cuando lleguen etiquetas verificadas, desacuerdos humanos o correcciones de la fuente, úsalos para comprobar si las señales anticipaban un problema real. Calcula cuántas alertas fueron accionables, cuánto tardaron en resolverse, qué segmentos quedaron sin observar y qué avisos se repiten sin aportar decisión.

Revisa los umbrales con un registro de cambios. Bajar un umbral después de un incidente puede ser razonable; recalcular el historial sin conservar la política anterior borra la evidencia sobre cómo funcionó el panel.

## Un panel mínimo que sí ayuda a investigar

Una primera versión puede caber en una sola página:

1. **Cobertura:** volumen esperado/observado, latencia y fuentes ausentes.
2. **Contrato:** campos, tipos, nulos y versión del esquema.
3. **Mezcla:** proporciones por fuente, formato e idioma con tamaños muestrales.
4. **Distribución:** cuantiles o categorías de cinco variables críticas, con referencia visible.
5. **Calidad:** muestra revisada, error por segmento y fecha de la última etiqueta.
6. **Incidentes:** anotaciones de festivos, migraciones, caídas y cambios de parser.
7. **Decisión:** propietario, estado, acción permitida y evidencia pendiente.

No ordenes el panel únicamente por significación estadística. Coloca primero las señales que pueden invalidar derivados o dejar una fuente fuera de cobertura, y después las que sirven para explorar.

## Checklist operativo

- [ ] La unidad, la población y las dos marcas temporales están definidas.
- [ ] Cada gráfica identifica referencia, ventana actual y tamaño muestral.
- [ ] Disponibilidad, esquema, mezcla y calidad aparecen separadas.
- [ ] Los segmentos responden a una necesidad y minimizan datos personales.
- [ ] Los métodos y umbrales están versionados y justificados.
- [ ] Las alertas tienen estado, propietario y acción permitida.
- [ ] Los incidentes y cambios conocidos se anotan sobre la serie.
- [ ] Una diferencia estadística nunca se presenta sola como degradación.
- [ ] Los originales y las versiones del pipeline siguen siendo recuperables.
- [ ] La calidad etiquetada o la revisión humana cierra el circuito.
- [ ] Las decisiones externas mantienen una puerta humana.

## Limitaciones y falsos positivos

La estacionalidad, los fines de semana, los festivos, una publicación masiva, un cambio legal o una campaña temática pueden modificar una distribución legítimamente. Comparar lunes con domingo o verano con un trimestre completo fabrica anomalías.

También son frecuentes estos errores:

- usar una referencia contaminada por el mismo incidente que se quiere detectar;
- ocultar un segmento pequeño bajo un agregado estable;
- alertar por cada columna sin controlar el volumen de avisos;
- interpretar un valor p como tamaño del efecto;
- tratar ausencia de deriva como prueba de calidad;
- mezclar cambios del colector con cambios de la fuente;
- recalibrar umbrales hasta que el incidente pasado quede perfectamente señalado;
- asumir que toda ausencia es censura o manipulación;
- mostrar ejemplos sensibles en un panel con acceso amplio;
- dejar que una alerta publique, bloquee o atribuya automáticamente.

Un panel puede además quedar ciego a cambios semánticos. Si una categoría conserva el nombre pero cambia su definición, las proporciones pueden parecer estables. Las notas de versión, el muestreo manual y la comparación con documentación oficial siguen siendo necesarios.

## Buenas prácticas de OPSEC, ética y privacidad

- Recoge solo los campos necesarios para medir el proceso.
- Agrega o seudonimiza vistas operativas cuando los ejemplos incluyan personas.
- No copies documentos sensibles dentro del sistema de métricas.
- Separa el panel técnico de los materiales de investigación restringidos.
- Protege URLs, consultas, credenciales, cookies y rutas internas en logs y capturas.
- Define retención para muestras, incidentes y referencias.
- Respeta términos, límites, licencias, correcciones y retiradas de las fuentes.
- Documenta quién puede abrir ejemplos individuales y por qué.
- No conviertas una rareza estadística en sospecha sobre una persona u organismo.
- Exige corroboración y revisión humana antes de publicar consecuencias.

## Alternativas y siguientes pasos

Para una fuente pequeña, una hoja versionada con volumen, nulos, cinco distribuciones y anotaciones puede ser más honesta que una plataforma compleja. Great Expectations resulta útil para contratos y validaciones; Evidently ofrece informes de deriva con datos de referencia. También puedes calcular señales transparentes con SQL o Python y publicar solo los agregados necesarios.

Si todavía no dispones de etiquetas, usa proxies con cautela y programa una muestra humana. Si la fuente cambia poco, los controles contractuales y una revisión periódica pueden bastar. Si cambia muy deprisa, combina ventanas cortas y largas para no confundir ruido inmediato con desplazamientos sostenidos.

El takeaway accionable es este: escoge una fuente recurrente y construye cuatro filas —disponibilidad, esquema, mezcla y calidad— con una referencia identificable, un propietario y una acción permitida. **Si una alerta no dice qué evidencia falta antes de concluir, el panel está decorando incertidumbre, no gestionándola.**

Como siguiente tema convendría estudiar la **calibración de alertas de deriva**: cómo fijar umbrales con costes explícitos, ventanas retrospectivas y un registro de falsos positivos sin ajustar el sistema al incidente que ya conocemos.

## Fuentes consultadas

- [NIST AI RMF Playbook — Measure 2.4](https://airc.nist.gov/airmf-resources/playbook/measure/)
- [NIST: Challenges to the Monitoring of Deployed AI Systems](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation)
- [Google for Developers: Production ML systems — Monitoring pipelines](https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring)
- [Great Expectations: Validate data schema with GX](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/schema/)
- [Evidently: DataDriftPreset API](https://evidentlyai.github.io/evidently/api-reference/main/evidently/presets.html)
