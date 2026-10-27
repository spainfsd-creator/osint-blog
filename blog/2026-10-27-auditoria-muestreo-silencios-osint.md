---
title: "Auditoría por muestreo de silencios en OSINT: encontrar fallos cuando no hay alertas"
slug: /auditoria-muestreo-silencios-osint
authors: [osint-writter]
tags: [osint, methodology, monitoring, verification, data, privacy]
date: 2026-10-27
image: /img/blog/2026-10-27-auditoria-muestreo-silencios-osint.png
aiDisclosure: generated
humanReviewed: false
---

El panel lleva una semana en verde. No hay errores, no hay avisos y nadie ha abierto un incidente. Sin embargo, un boletín que debía aportar cuarenta documentos dejó de aparecer el martes. **El sistema no los marcó como fallidos porque nunca supo que existían: el silencio parecía éxito.**

![Analista comparando un universo de registros con una muestra independiente para localizar omisiones](/img/blog/2026-10-27-auditoria-muestreo-silencios-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Una auditoría por muestreo de silencios busca falsos negativos entre los elementos sobre los que el detector no avisó. No consiste en revisar unas cuantas alertas cerradas como correctas, sino en seleccionar unidades desde una población independiente, reconstruir qué debería haber ocurrido y comprobar si el pipeline omitió una fuente, un documento, un campo o una condición material.

Todos los nombres, portales, documentos y resultados del caso son ficticios. El método se limita a fuentes públicas o sistemas propios y autorizados. Muestrear para evaluar cobertura no autoriza vigilancia sobre personas, recopilación indiscriminada ni eludir controles de acceso.

## Qué es auditar el silencio (y para qué sirve)

Un sistema de monitorización solo observa aquello que entra en su campo de visión. Si una descarga falla antes de crear un registro, si el inventario esperado está incompleto o si una regla descarta un formato desconocido, puede no quedar ningún error que contar. La ausencia de alertas mide entonces el comportamiento del propio detector, no necesariamente el estado del mundo.

La auditoría de silencios introduce una vía de observación independiente. Para un periodo definido, toma una muestra de unidades que debían ser observables y las reconcilia con lo que el pipeline recibió, procesó y evaluó. Sirve para estimar omisiones, descubrir modos de fallo y decidir si la cobertura conocida permite seguir publicando.

Conviene separar cuatro conceptos:

| Concepto | Pregunta | Ejemplo de evidencia |
| --- | --- | --- |
| universo objetivo | ¿qué hechos o artefactos queríamos cubrir? | calendario oficial, índice público, manifiesto propio |
| marco de muestreo | ¿desde qué lista seleccionamos unidades? | exportación independiente y fechada |
| detector | ¿qué procesó y qué decidió alertar? | ledger de ingesta, versiones y resultados |
| adjudicación | ¿qué debió ocurrir realmente? | original revisado, regla vigente y doble comprobación |

La distinción decisiva es la dirección de la prueba. Para comprobar existencia podemos partir de lo registrado y volver al original. Para comprobar completitud hay que partir de una fuente razonablemente independiente de lo registrado y buscar cada unidad en el sistema. El *Financial Audit Manual* de GAO aplica esta lógica a pruebas de completitud: seleccionar desde una población que debería contener los elementos y rastrearlos hacia el registro evaluado.

## Caso legítimo: el portal que dejó de entrar sin fallar

El observatorio ficticio **Archivo Faro** sigue resoluciones de seis organismos públicos para preparar estadísticas agregadas. Un colector registra descargas, un extractor obtiene fecha y referencia y un panel avisa ante errores HTTP, campos vacíos o caídas bruscas de volumen.

Durante septiembre el panel permanece verde. Como control independiente, el equipo crea un marco semanal a partir de los índices públicos de los seis organismos, sin reutilizar la tabla de ingesta. Selecciona 80 referencias mediante una semilla registrada y las reconcilia con el ledger.

Encuentra tres omisiones, todas del mismo organismo y posteriores a un cambio de paginación. Las páginas omitidas devolvían `200`, pero el colector solo recorría la primera. No hubo error HTTP, el volumen total quedó dentro del rango histórico y los otros cinco portales ocultaron la caída en el agregado.

La muestra no demuestra que solo falten tres documentos ni autoriza a extrapolar sin considerar el diseño. Sí descubre un modo de fallo, identifica el segmento afectado y justifica ampliar la revisión de ese periodo. El equipo pausa únicamente los derivados que dependían del organismo afectado, corrige la navegación, reconstruye el inventario y documenta qué resultados deben recalcularse.

## Flujo recomendado

### 1. Define el silencio que quieres detectar

Escribe una condición observable y una acción asociada. «Buscar cosas que falten» no es un objetivo auditable. Una ficha mínima podría ser:

```yaml
objetivo: estimar_documentos_elegibles_omitidos
unidad: referencia_publicada
periodo: 2026-09-01/2026-09-30
universo: indices_publicos_de_seis_organismos
fallo: elegible_en_origen_y_ausente_del_ledger
decision: ampliar_revision_si_aparece_una_omision_critica
```

Define también qué no cubre la prueba. Una auditoría de ingesta no verifica por sí sola que la extracción semántica sea correcta; una auditoría de fechas no prueba que los nombres estén bien desambiguados.

### 2. Construye un marco independiente y reconciliado

El marco debe aproximar el universo del que quieres hablar. Puede proceder de índices oficiales, calendarios de publicación, listados de objetos en un almacenamiento propio o manifiestos emitidos por el sistema fuente. Captura la fecha, procedencia, reglas de inclusión y un hash cuando resulte apropiado.

No selecciones solo entre filas que ya llegaron al pipeline: una omisión total no puede aparecer en esa lista. Tampoco confundas una lista grande con una lista completa. GAO recomienda comprobar que la población sea válida y completa antes de muestrear; si esa garantía es parcial, la conclusión debe ser igualmente parcial.

Registra diferencias entre el universo conceptual y el marco disponible:

- portales o periodos sin índice;
- documentos retirados o corregidos;
- páginas no accesibles sin autenticación;
- duplicados y republicaciones;
- unidades cuya elegibilidad no puede determinarse;
- intervalos en los que el propio marco estuvo caído.

### 3. Elige azar, riesgo y cobertura conscientemente

Una muestra aleatoria simple permite inferir sobre la población cubierta si cada unidad tiene una probabilidad conocida de selección. Conserva el tamaño del universo, el generador, la semilla, el algoritmo y la lista resultante. Una selección «a ojo» puede servir para descubrir fallos, pero no para estimar una tasa representativa.

El muestreo dirigido sigue siendo útil como capa adicional: revisa fuentes nuevas, formatos raros, lotes posteriores a despliegues y periodos con telemetría débil. No mezcles después ambos resultados como si todos los elementos hubieran tenido la misma probabilidad.

Una estrategia práctica combina:

1. **muestra base aleatoria**, para estimar el comportamiento global;
2. **estratos predefinidos**, para no perder fuentes pequeñas o críticas dentro del volumen total;
3. **muestra dirigida de riesgo**, para explorar hipótesis sin fingir representatividad;
4. **controles deterministas**, para expectativas exactas como «deben llegar seis manifiestos».

Si se sobremuestrea un estrato, hay que conservar sus probabilidades y ponderar cualquier estimación global. El resultado por estrato suele ser más informativo que un único porcentaje.

### 4. Fija tamaño y regla de ampliación antes de revisar

El tamaño depende de la decisión, la precisión deseada, la tasa plausible de omisión, el diseño y el coste de adjudicar. No elijas veinte casos solo porque caben en una mañana y después presentes el resultado como garantía.

Incluso observar cero omisiones deja incertidumbre. Bajo un modelo binomial sencillo e independiente, un límite superior unilateral aproximado del 95 % para la tasa `p`, tras revisar `n` unidades sin fallos, es:

`p_superior = 1 - 0,05^(1/n)`

Con 60 unidades y cero omisiones, el límite ronda el 4,9 %; con 300, ronda el 1,0 %. No significa que la tasa real sea esa ni que el diseño cumpla automáticamente el modelo. NIST recomienda intervalos binomiales exactos cuando hay pocos fallos o muestras pequeñas, precisamente porque las aproximaciones simétricas pueden ser engañosas.

Prerregistra qué hará el equipo si encuentra una omisión: ampliar el estrato, revisar todo el lote afectado, detener un derivado o abrir un incidente. Examinar casos por etapas y parar al obtener un resultado cómodo introduce sesgo si la regla de parada no estaba definida.

### 5. Selecciona de forma reproducible

Congela primero el marco. Asigna a cada unidad un identificador estable que no exponga datos personales y aplica un sorteo verificable. Una opción sencilla consiste en ordenar por el hash de `semilla || identificador`, guardar la semilla y tomar las primeras `n` unidades de cada estrato.

Documenta sustituciones. Si una unidad no está disponible, no elijas manualmente otra «parecida»: marca el estado, aplica la regla prevista y conserva el denominador. La inaccesibilidad puede ser parte del problema que se investiga.

El muestreo sistemático —un inicio aleatorio y cada unidad `k`— puede ser eficiente, pero falla si el orden tiene una periodicidad alineada con `k`. Revisa antes cómo se construyó la lista.

### 6. Adjudica sin mirar primero la decisión del detector

Quien revisa debería comenzar por el artefacto y la regla vigente, no por la etiqueta que produjo el sistema. Para cada unidad registra:

- si era elegible y observable en el periodo;
- si aparece en el ledger de adquisición;
- si fue procesada con la versión prevista;
- si cumplía la condición material de alerta;
- si la alerta se emitió, entregó y recibió;
- evidencia mínima y motivo de la adjudicación;
- estado `indeterminado` cuando falten datos.

Una submuestra con doble revisión ayuda a medir desacuerdos. Si dos personas interpretan de forma distinta la misma regla, el problema puede estar en el contrato de la alerta, no en quien revisa.

### 7. Separa cada punto de pérdida

No reduzcas todo a «alertó/no alertó». Reconstruye la cadena:

```text
esperado -> descubierto -> adquirido -> parseado -> evaluado -> emitido -> entregado
```

Una unidad ausente puede revelar un marco incompleto, un colector que no pagina, un parser que descarta, una regla que no evalúa, una cola que pierde eventos o un canal que no entrega. Cada transición necesita identificadores, marcas temporales y estados suficientes para reconciliar, sin convertir el ledger en una copia innecesaria del contenido.

Google SRE distingue monitorización interna y comprobación externa: la primera explica componentes; la segunda observa síntomas desde fuera. En este contexto, una sonda o reconciliación independiente puede detectar que el pipeline no ve una fuente aunque todas sus métricas internas estén verdes.

### 8. Estima, investiga y decide por separado

Publica recuentos y denominadores por estrato, intervalos compatibles con el diseño, indeterminados y cobertura del marco. No conviertas una estimación estadística en una explicación causal: primero localiza el patrón y después inspecciona versiones, artefactos y transiciones.

Una tabla de cierre útil incluye:

| Estrato | Universo en marco | Revisados | Omisiones | Indeterminados | Acción |
| --- | ---: | ---: | ---: | ---: | --- |
| organismo A | 1.240 | 40 | 0 | 1 | mantener control |
| organismo B | 180 | 30 | 3 | 0 | revisar lote completo |
| organismo C-F | 3.900 | 60 | 0 | 2 | mejorar marco |

No sumes las filas para obtener una tasa global sin respetar probabilidades de selección distintas. La decisión puede ser operativa —contener o ampliar— aunque todavía no exista una estimación precisa.

## Checklist operativo

- [ ] El objetivo, la unidad, el periodo y la definición de omisión están escritos.
- [ ] El marco procede de una vía independiente del detector evaluado.
- [ ] Se han documentado cobertura, huecos, duplicados y retiradas del marco.
- [ ] Cada unidad tiene una probabilidad de selección conocida o se marca como dirigida.
- [ ] La semilla, el algoritmo y los estratos permiten reproducir la muestra.
- [ ] El tamaño y la regla de ampliación se fijaron antes de adjudicar.
- [ ] La revisión parte del original y admite el estado `indeterminado`.
- [ ] Adquisición, procesamiento, evaluación y entrega se comprueban por separado.
- [ ] Los resultados informan recuentos, denominadores e incertidumbre.
- [ ] Cero omisiones no se presenta como prueba de tasa cero.
- [ ] Las acciones contienen solo los productos y periodos afectados.
- [ ] El muestreo minimiza exposición y retención de datos personales.

## Limitaciones y falsos negativos de la propia auditoría

La auditoría hereda los huecos de su marco. Si el índice independiente también omite una publicación, ambos sistemas pueden coincidir y seguir equivocados. Por eso conviene rotar controles: manifiestos del origen, sondas sintéticas propias, recuentos esperados, archivos públicos y revisiones manuales de periodos seleccionados.

Otros límites frecuentes son:

- **eventos raros:** una muestra asequible puede no encontrar una omisión poco frecuente pero grave;
- **dependencia:** documentos del mismo lote comparten causa y no son ensayos independientes;
- **estratos diminutos:** necesitan revisión exhaustiva o decisiones cualitativas;
- **retardo:** una unidad puede estar ausente hoy y llegar legítimamente mañana;
- **contaminación:** quien conoce la salida puede adjudicar de forma sesgada;
- **marcos cambiantes:** correcciones y retiradas alteran el universo tras el sorteo;
- **múltiples auditorías:** repetir pruebas hasta encontrar o descartar un patrón cambia la interpretación;
- **cobertura semántica:** presencia en el ledger no garantiza extracción ni significado correctos.

El objetivo no es certificar que «no falta nada», sino medir qué clase de afirmación permiten los controles disponibles y dónde sigue habiendo incertidumbre.

## Buenas prácticas de OPSEC, ética y privacidad

- Audita fuentes públicas o sistemas para los que exista autorización y finalidad legítima.
- No uses el control de cobertura para ampliar clandestinamente la población investigada.
- Conserva identificadores, hashes y estados antes que copias completas cuando sean suficientes.
- Separa credenciales, contenido restringido y resultados agregados.
- Protege semillas si su publicación permitiría anticipar controles todavía activos; publícalas después cuando la verificabilidad lo aconseje.
- Limita accesos, retención, exportaciones y capturas de casos individuales.
- Respeta licencias, términos, límites, correcciones y retiradas.
- No conviertas una omisión técnica en sospecha sobre una persona u organismo.
- Exige corroboración antes de rectificar o publicar una conclusión.
- Mantén una puerta humana para ampliar, contener y cerrar la auditoría.

## Alternativas y siguientes pasos

Si el universo es pequeño, revisarlo completo puede costar menos que diseñar una muestra. Si existe un contrato exacto de entregas, usa reconciliación determinista. Para fuentes de baja frecuencia, un calendario de eventos esperados y una comprobación por evento suele ser más interpretable. Las sondas sintéticas son útiles para probar rutas conocidas, pero no revelan por sí solas formatos o categorías que nunca imaginamos.

El takeaway accionable es inmediato: elige una alerta crítica y dibuja su cadena desde el universo esperado hasta la entrega. Después toma una muestra reproducible desde una lista independiente y rastrea cada unidad en sentido inverso. **Si la población de la auditoría nace del mismo ledger que quieres evaluar, has medido coherencia interna, no completitud.**

Como siguiente tema convendría estudiar los **controles negativos y positivos en pipelines OSINT**: artefactos sintéticos, canarios y casos imposibles que permiten comprobar que tanto el éxito como el fallo siguen siendo observables sin mezclar material real sensible.

## Fuentes consultadas

- [GAO/CIGIE Financial Audit Manual, volumen 1 (2024)](https://www.gao.gov/assets/gao-24-107278.pdf)
- [GAO: Using Statistical Sampling](https://www.gao.gov/assets/pemd-10.1.6.pdf)
- [NIST/SEMATECH: intervalos de confianza para proporciones](https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm)
- [NIST Risk Management Framework: Monitor](https://csrc.nist.gov/projects/risk-management/about-rmf/monitor-step)
- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [CDC Epi Info: Population Survey or Descriptive Study](https://www.cdc.gov/epiinfo/user-guide/statcalc/samplesize.html)
