---
title: "Calibración de alertas de deriva en OSINT: detectar cambios sin entrenar al ruido"
slug: /calibracion-alertas-deriva-osint
authors: [osint-writter]
tags: [osint, methodology, monitoring, data, verification, privacy]
date: 2026-10-26
image: /img/blog/2026-10-26-calibracion-alertas-deriva-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una alerta salta porque el porcentaje de documentos sin fecha pasa del 4 % al 7 %. El equipo interrumpe su trabajo, abre veinte ejemplos y descubre un boletín extraordinario perfectamente válido. Baja el umbral. A la semana siguiente ocurre algo parecido y vuelve a bajarlo. Tres meses después, el panel está en silencio incluso cuando el extractor pierde una fuente completa. **No se ha calibrado la alerta: se la ha entrenado para olvidar cada susto.**

![Analista calibrando umbrales y ventanas de alertas de deriva frente a un registro de resultados](/img/blog/2026-10-26-calibracion-alertas-deriva-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/calibracion-alertas-deriva-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Calibrar una alerta de deriva consiste en elegir, probar y gobernar una regla que transforme una señal de cambio en una acción proporcionada. La regla incluye más que un número: define la población observada, la referencia, la ventana, el tamaño mínimo de muestra, la persistencia, la severidad, el responsable y qué evidencia permite cerrar el aviso.

Todos los nombres, fuentes, documentos y resultados del caso de este artículo son ficticios. El método se limita a datos sintéticos, fuentes públicas o sistemas propios y autorizados. Una alerta identifica una diferencia que merece revisión; no demuestra manipulación, engaño, culpabilidad ni intención.

## Qué es calibrar una alerta (y para qué sirve)

Un detector produce una medida: proporción de nulos, distancia entre distribuciones, caída de volumen, cambio de esquema o discrepancia en una muestra etiquetada. Una política de alerta decide qué hacer con esa medida.

Esa distinción evita dos atajos frecuentes:

- un valor estadísticamente significativo no es automáticamente importante;
- un umbral que funcionó sobre incidentes pasados no garantiza que generalice.

NIST recomienda monitorizar las diferencias entre producción y pruebas, combinar pruebas de hipótesis con conocimiento del dominio, considerar la propagación de errores y asignar responsabilidades claras a la supervisión humana. Su informe sobre monitorización desplegada de 2026 añade una cautela útil: las prácticas validadas siguen dispersas y la cadencia correcta depende del contexto. Por tanto, no existe un umbral universal de deriva que podamos copiar sin justificarlo.

La calibración sirve para responder preguntas operativas:

- ¿qué cambio exige una revisión inmediata y cuál puede esperar?
- ¿cuánto cuesta investigar una falsa alarma?
- ¿qué daño puede causar no detectar un cambio real?
- ¿qué volumen hace estable la señal?
- ¿quién puede confirmar el incidente y con qué evidencia?
- ¿cuándo debe retirarse o recalibrarse la regla?

## Caso legítimo: un umbral que parecía prudente

El observatorio ficticio **Archivo Faro** recopila resoluciones públicas de ocho organismos. Su pipeline extrae fecha, órgano, referencia y tipo documental. El equipo quiere detectar pronto una degradación del campo `fecha_resolucion`.

Durante doce semanas retrospectivas construye una tabla semanal:

| Semana | Documentos | Fechas vacías | Causa revisada | Resultado |
| --- | ---: | ---: | --- | --- |
| S-12 | 840 | 3,8 % | mezcla habitual | normal |
| S-9 | 190 | 8,4 % | festivo y lote pequeño | cambio legítimo |
| S-6 | 910 | 12,1 % | nueva plantilla no soportada | incidente real |
| S-3 | 1.480 | 6,9 % | archivo histórico escaneado | cambio legítimo |
| S-1 | 875 | 10,7 % | fallo de OCR tras despliegue | incidente real |

Una regla simple de «alertar por encima del 6 %» detectaría los dos incidentes, pero también dos cambios legítimos. Elevarla al 10 % reduciría ruido, aunque el aviso llegaría tarde si el fallo afecta inicialmente a un solo organismo.

El equipo deja de buscar el porcentaje mágico y define costes explícitos:

- una falsa alarma consume unos 35 minutos de revisión;
- omitir una fuente completa invalida informes derivados y exige rectificación;
- un cambio pequeño y sostenido puede ser más relevante que un pico aislado;
- con menos de 250 documentos, el porcentaje semanal es demasiado inestable para paginar a nadie;
- una ruptura de esquema tiene mayor urgencia que una variación moderada de distribución.

La política resultante usa dos niveles:

1. **revisión:** más del 6 % durante dos ventanas comparables o una diferencia localizada en un segmento crítico;
2. **incidente:** más del 10 % con al menos 250 documentos, o cualquier ausencia completa de una fuente prevista.

El ejemplo no pretende exportar esos números. Su valor está en hacer visibles el coste, la población mínima, la persistencia, las excepciones y la acción asociada.

## Flujo recomendado

### 1. Define el objeto y la decisión antes de mirar el umbral

Escribe una ficha por alerta:

```yaml
alerta: fechas_vacias
unidad: documento_publicado
poblacion: resoluciones_elegibles
referencia: ocho_semanas_comparables
ventana_actual: una_semana
segmentos: [organismo, formato]
accion_revision: abrir_muestra_y_comprobar_adquisicion
accion_incidente: detener_derivados_afectados
propietario: guardia_datos
```

La ficha impide comparar poblaciones distintas bajo el mismo nombre. Si un portal añade un archivo histórico, ese lote puede necesitar una cohorte separada; si se mezcla con publicaciones corrientes, la alerta medirá composición antes que calidad.

### 2. Construye un historial con resultados adjudicados

Una alerta solo puede evaluarse si sabemos qué ocurrió después. Conserva, como mínimo:

- identificador y versión de la regla;
- referencia, ventana, segmentos y tamaños de muestra;
- valor observado y severidad emitida;
- evidencia revisada;
- clasificación: incidente real, cambio legítimo, dato insuficiente o causa no determinada;
- acción, responsable y tiempo hasta resolución;
- impacto en productos derivados;
- fecha y motivo de cualquier cambio de umbral.

No fuerces cada caso a «verdadero» o «falso». `Causa no determinada` es una salida honesta cuando faltan originales, etiquetas o contexto. Convertir la incertidumbre en falso positivo para mejorar una métrica solo maquilla el sistema.

### 3. Separa el coste de las dos clases de error

Podemos tratar cada aviso como una decisión binaria provisional:

| Resultado | Había cambio material | No había cambio material |
| --- | --- | --- |
| alerta | verdadero positivo | falso positivo |
| no alerta | falso negativo | verdadero negativo |

Google explica que subir un umbral suele reducir falsos positivos y aumentar falsos negativos; bajarlo suele hacer lo contrario. La elección depende del coste, beneficio y riesgo del caso. En OSINT, esos costes rara vez son simétricos.

Una formulación sencilla para comparar políticas es:

`coste = FP × coste_revision + FN × coste_omision + demoras × coste_retraso`

No hace falta fingir una precisión económica inexistente. Puedes usar categorías —bajo, medio, alto— y documentar quién las aprobó. Lo importante es no optimizar únicamente la cantidad de alertas.

### 4. Reproduce las reglas sobre ventanas retrospectivas

Ejecuta cada política candidata sobre un periodo histórico que incluya:

- días y semanas normales;
- festivos y cierres de calendario;
- lotes pequeños y publicaciones masivas;
- cambios conocidos de plantilla o fuente;
- fallos reales del colector o extractor;
- segmentos con distinta frecuencia y formato.

Para cada regla calcula recuentos, no solo porcentajes: verdaderos positivos, falsos positivos, falsos negativos, tiempo de detección y carga de revisión. Informa además el volumen y la cobertura de casos adjudicados. Una precisión del 90 % basada en diez alertas no significa lo mismo que la misma cifra sobre quinientas.

Evita elegir y evaluar el umbral sobre exactamente los mismos incidentes. Reserva un tramo temporal posterior o varias ventanas prospectivas para confirmar que la regla no se limita a reconocer los episodios que inspiraron su diseño.

### 5. Combina ventanas rápidas y lentas

Un pico grande necesita detección temprana; un deterioro pequeño pero persistente necesita memoria. Google SRE propone combinar ventanas cortas y largas en sus alertas basadas en consumo de presupuesto: la ventana larga aporta contexto y la corta permite que el aviso se resuelva con más rapidez. No debemos trasladar sus cifras de servicios web directamente a un pipeline OSINT, pero sí la idea.

Una política prudente puede separar:

- **rápida:** ruptura de esquema, fuente ausente o salto extremo con muestra suficiente;
- **sostenida:** desviación moderada repetida en varias ventanas comparables;
- **informativa:** señal débil que se registra para revisión periódica sin interrumpir al equipo.

En fuentes de bajo volumen, exigir dos ventanas puede retrasar demasiado. Allí conviene usar conteos absolutos, calendario esperado, inspección por evento y revisión humana en lugar de una tasa inestable.

### 6. Define severidad por acción, no por color

Una alerta urgente debe tener una acción inmediata que una persona pueda ejecutar. Google SRE advierte que avisos no accionables y con mala relación señal/ruido provocan fatiga. Para un flujo OSINT, una escala útil sería:

| Nivel | Acción permitida | Ejemplo |
| --- | --- | --- |
| registrar | guardar señal para revisión agrupada | distribución distinta sin impacto confirmado |
| revisar | asignar ticket y muestrear originales | aumento sostenido de nulos |
| contener | pausar solo derivados afectados | fuente prevista ausente |
| escalar | activar respuesta y rectificación | error confirmado ya publicado |

La alerta nunca debería atribuir intención, señalar a una persona ni publicar una conclusión por sí sola.

### 7. Cambia reglas mediante versiones y revisión

Cada ajuste debe conservar:

- versión anterior y nueva;
- evidencia que motivó el cambio;
- comparación retrospectiva de ambas;
- efecto esperado en carga y omisiones;
- fecha de entrada en vigor;
- responsable y fecha de revisión;
- criterio para revertir.

No recalcules el historial como si la regla nueva hubiera existido siempre. Mantén dos vistas: qué habría ocurrido con la regla candidata y qué ocurrió realmente con la vigente. Esa diferencia forma parte de la evidencia operativa.

## Cómo evitar ajustar el sistema al último incidente

Después de una falsa alarma resulta tentador añadir una excepción exacta: «ignorar el organismo O-04 los lunes». Después de una omisión, la tentación contraria es bajar el umbral hasta capturar ese caso. Ambas decisiones pueden ser razonables, pero necesitan una hipótesis más general.

Antes de cambiar una regla, pregunta:

1. ¿el caso revela una categoría repetible o solo una anécdota?
2. ¿la excepción se deriva de un calendario o contrato documentado?
3. ¿qué incidentes anteriores dejaría de detectar?
4. ¿funciona en un periodo que no usamos para diseñarla?
5. ¿podemos resolver la causa en adquisición o extracción en vez de silenciar el síntoma?
6. ¿ha cambiado el coste operativo o solo queremos que el panel vuelva a verde?

Limita también la frecuencia de recalibración. Un cambio urgente puede aplicarse durante un incidente, pero debe quedar como excepción temporal con caducidad y revisión posterior.

## Limitaciones y falsos positivos

Una calibración retrospectiva depende de la calidad del registro. Si solo documentamos las alertas emitidas, no veremos falsos negativos: necesitamos auditorías por muestreo, controles independientes o incidentes descubiertos por otras vías.

Otros límites importantes son:

- **deriva de prevalencia:** cambia la frecuencia de incidentes y con ella la precisión de la alerta;
- **retardo de etiquetas:** la verdad operativa puede conocerse días después;
- **dependencia temporal:** ventanas solapadas no son observaciones independientes;
- **múltiples señales:** probar decenas de métricas aumenta avisos casuales;
- **segmentos pequeños:** un porcentaje extremo puede representar dos documentos;
- **cambios semánticos:** el mismo nombre de campo puede adquirir otro significado sin romper el esquema;
- **silencios desconocidos:** no recibir datos puede parecer estabilidad si no se monitoriza cobertura;
- **automatización circular:** las acciones provocadas por una alerta pueden alterar la señal siguiente;
- **desgaste del historial:** ajustar repetidamente sobre los mismos incidentes sobreestima el rendimiento.

NIST subraya que la monitorización desplegada debe combinar señales técnicas, contexto humano, documentación de errores e impactos y mecanismos de respuesta. Un detector de deriva no sustituye la validación de calidad ni la revisión del mundo al que supuestamente representa.

## Buenas prácticas de OPSEC, ética y privacidad

- Conserva agregados y referencias mínimas; no copies documentos personales al sistema de alertas.
- Protege consultas, URLs sensibles, cookies, tokens y rutas internas en logs y capturas.
- Separa el registro operativo de los materiales restringidos de una investigación.
- Limita el acceso a ejemplos individuales y registra quién los abre.
- Fija retención para muestras, adjudicaciones e incidentes.
- Respeta términos, límites, licencias, correcciones y retiradas de las fuentes.
- No uses segmentos que revelen atributos personales innecesarios.
- Permite clasificar una alerta como indeterminada sin forzar una acusación.
- Exige corroboración antes de convertir una anomalía en afirmación pública.
- Mantén una puerta humana para contener, rectificar o publicar.

## Checklist operativo

- [ ] La unidad, población, referencia y ventana están definidas.
- [ ] Cada regla tiene versión, propietario y fecha de revisión.
- [ ] Los costes de falso positivo, falso negativo y demora son explícitos.
- [ ] El historial incluye casos normales, incidentes y cambios legítimos.
- [ ] Existen conteos y tamaños de muestra, no solo porcentajes.
- [ ] Una ventana independiente confirma la política elegida.
- [ ] Los avisos rápidos y sostenidos tienen acciones distintas.
- [ ] Las fuentes de bajo volumen reciben un tratamiento específico.
- [ ] Los falsos negativos se buscan mediante controles independientes.
- [ ] Las excepciones temporales caducan y dejan rastro.
- [ ] Ninguna alerta atribuye intención ni publica automáticamente.
- [ ] La revisión minimiza exposición de datos personales.

## Alternativas y siguientes pasos

Si apenas hay volumen, una lista versionada de eventos esperados y una revisión semanal puede superar a cualquier detector estadístico. Si la señal es contractual —una columna desaparece o una fuente no llega— usa primero reglas deterministas. Si existen etiquetas fiables, compara políticas mediante precisión, cobertura, tasa de falsas alarmas y demora, siempre desagregadas por fuente relevante.

Para equipos pequeños, basta una tabla de adjudicación y un script reproducible que ensaye varios umbrales sobre ventanas históricas. Herramientas de monitorización pueden calcular distancias y pintar paneles, pero la política de acción, la evidencia de cierre y la responsabilidad siguen perteneciendo al equipo.

El takeaway accionable es este: selecciona una alerta existente y reconstruye sus últimas veinte activaciones. Anota resultado, coste de revisión, demora, volumen y cambio de regla. **Si no puedes explicar qué acción distinta habría provocado otro umbral, todavía no estás calibrando: solo estás moviendo una línea.**

Como siguiente tema sería útil estudiar la **auditoría por muestreo de silencios**: cómo buscar falsos negativos cuando el sistema no genera ningún aviso, sin revisar todo el universo ni convertir ausencia de evidencia en evidencia de ausencia.

## Fuentes consultadas

- [NIST AI RMF Playbook — Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)
- [NIST AI 800-4 — Challenges to the Monitoring of Deployed AI Systems](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation)
- [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Google SRE Workbook — On-call](https://sre.google/workbook/on-call/)
- [Google for Developers — Accuracy, recall, precision and related metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)
