---
title: "Presupuestos de error en OSINT: decidir cuándo un pipeline deja de ser publicable"
slug: /presupuestos-error-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-10-02
image: /img/blog/2026-10-02-presupuestos-error-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista evaluando el margen de error de un pipeline OSINT](/img/blog/2026-10-02-presupuestos-error-pipelines-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/presupuestos-error-pipelines-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El boletín municipal se actualiza cada madrugada. Durante tres semanas, nuestro pipeline lo descargó, normalizó y publicó a tiempo. El lunes apareció una tabla impecable con 47 contratos; el portal, sin embargo, había servido solo la primera de cuatro páginas. **La ejecución fue puntual y técnicamente correcta, pero el resultado no era publicable.** Sin una regla acordada de antemano, el equipo solo tenía dos opciones malas: ignorar el hueco o discutir bajo presión cuánto fallo estaba dispuesto a aceptar.

Un presupuesto de error convierte esa discusión en una decisión operativa previa. Define qué significa que una adquisición sea suficientemente fiable, cuánto incumplimiento toleramos durante una ventana y qué haremos cuando el margen se consuma. No mide la verdad de la fuente ni concede permiso para publicar datos dudosos. En OSINT sirve para algo más modesto y útil: **saber cuándo el comportamiento de nuestro propio proceso obliga a frenar, degradar o revisar una publicación**.

<!-- truncate -->

## Qué es un presupuesto de error (y para qué sirve)

En ingeniería de fiabilidad, un indicador de nivel de servicio o **SLI** mide un comportamiento; un objetivo o **SLO** fija el nivel aceptable durante una ventana; y el presupuesto de error es la parte que queda fuera del objetivo. Si el SLO es del 98 %, el margen teórico es del 2 %. Google SRE presenta esta relación como `presupuesto = 1 − SLO` y recomienda acompañarla de una política escrita que determine qué ocurre cuando se agota.

La traducción a OSINT necesita cautela. Nuestro «servicio» no es una API comercial estable: puede depender de portales públicos, calendarios administrativos, documentos irregulares y decisiones editoriales. Por eso conviene medir **resultados observables del pipeline**, no promesas imposibles sobre el universo real.

Un SLI defendible podría responder a una de estas preguntas:

- ¿La adquisición terminó antes de la hora límite?
- ¿Se recorrieron todas las páginas que la propia fuente declaró?
- ¿Cada objeto descargado conserva URL, hora, respuesta y hash?
- ¿El parser rechazó explícitamente lo que no entendía, en vez de inventar valores?
- ¿El artefacto publicado puede reconstruirse desde la captura fijada?

«Hemos encontrado todos los contratos existentes» no es un buen SLI: normalmente no conocemos ese denominador. «Hemos recorrido 4 de las 4 páginas anunciadas por el portal y preservado las respuestas» sí es medible, aunque tampoco demuestre que el portal sea completo.

El presupuesto ayuda a resolver tres tensiones prácticas:

1. Evita tratar cada incidencia menor como una emergencia.
2. Impide normalizar una degradación acumulada solo porque ninguna ejecución aislada parece catastrófica.
3. Da al equipo autorización explícita para detener cambios o publicaciones cuando la fiabilidad observada ya no sostiene el análisis.

## Caso de uso legítimo: un observatorio ficticio de contratación

Imaginemos **Observatorio Río Claro**, un proyecto ficticio que resume cada semana contratos publicados por veinte ayuntamientos. El equipo no perfila personas ni intenta acceder a sistemas: consulta portales abiertos, conserva las páginas públicas y enlaza los documentos originales.

Para el portal de Villa Serena define una unidad de medida sencilla: una **ejecución programada**. Una ejecución es buena solo si cumple a la vez estas condiciones:

- finaliza antes de las 08:00 UTC;
- recorre todas las páginas declaradas por la navegación del portal;
- conserva cada respuesta original y su hash;
- no tiene rechazos de esquema sin revisar;
- produce un manifiesto que enlaza entradas y salidas.

El equipo comienza con un SLO experimental: **el 98 % de las ejecuciones será bueno en una ventana móvil de 50 ejecuciones**. Eso permite una ejecución mala. La cifra no viene de una norma universal: es una hipótesis operativa que el equipo debe justificar con el ritmo de publicación, el impacto de un retraso y la capacidad real de revisión.

Supongamos esta secuencia:

| Día | Resultado | Consumo del presupuesto |
| --- | --- | ---: |
| Lunes | 4/4 páginas, a tiempo | 0 % |
| Martes | 4/4 páginas, 40 minutos tarde | 0 % si sigue antes del límite |
| Miércoles | 1/4 páginas; respuesta truncada | 100 % |
| Jueves | 4/4 páginas, pero parser nuevo omite importes | presupuesto agotado; publicación detenida |

El miércoles consume la única ejecución mala disponible. El jueves no debe convertirse en «otro aviso amarillo»: la política ya acordada obliga a frenar la salida derivada, restaurar o corregir el parser y delimitar qué informes están afectados. El original se conserva; lo que se bloquea es la transformación o publicación no fiable.

Este ejemplo también muestra un límite estadístico. Con poco volumen, un solo evento mueve mucho el porcentaje. La documentación de Google SRE advierte que las alertas basadas en tasa pueden comportarse mal en servicios de tráfico bajo. En un pipeline diario o semanal, es más sensato combinar conteos explícitos, ventanas de calendario y revisión humana que copiar umbrales pensados para millones de peticiones.

## Flujo recomendado: del riesgo a una política que se pueda ejecutar

### 1. Define la decisión antes que la métrica

Empieza por una pregunta operativa: «¿Qué fallo haría que detuviéramos la publicación?». Después elige el indicador mínimo que permita tomar esa decisión. Medir por medir crea paneles; no crea control.

Para una adquisición recurrente, las decisiones habituales son:

- publicar con normalidad;
- publicar con advertencia y alcance reducido;
- retener el derivado hasta revisar;
- volver temporalmente a una versión conocida del pipeline;
- preservar la captura y abrir un incidente sin reintentar de forma destructiva.

### 2. Especifica eventos buenos y malos sin ambigüedad

Escribe una condición reproducible. Por ejemplo:

```text
unidad: ejecución programada del portal Villa Serena
buena: antes de 08:00 UTC AND paginas_visitadas == paginas_declaradas
       AND rechazos_no_revisados == 0 AND manifiesto_presente == true
ventana: últimas 50 ejecuciones
objetivo inicial: 98 % buenas
```

No mezcles en el mismo indicador dimensiones que requieren respuestas diferentes. Un retraso de treinta minutos, una página ausente y un hash que no coincide pueden ser «malos», pero no se diagnostican igual. Conserva las señales componentes aunque exista una regla editorial conjunta.

### 3. Calcula el presupuesto y muestra el denominador

Con 50 ejecuciones y un SLO del 98 %, el presupuesto es una ejecución mala:

```text
presupuesto = total × (1 − SLO)
presupuesto = 50 × (1 − 0,98) = 1 ejecución
```

Publica siempre el denominador, la ventana y la regla de redondeo. Decir «queda el 50 % del presupuesto» sin esos datos oculta si hablamos de miles de eventos o de dos ejecuciones. En ventanas pequeñas, muestra también el conteo bruto.

### 4. Distingue consumo lento de incendio

La **tasa de consumo** o *burn rate* compara la velocidad real de gasto con la velocidad que agotaría el presupuesto exactamente al final de la ventana. Una tasa de 1 consume el margen al ritmo previsto; una tasa muy superior anuncia que se agotará antes.

La técnica de múltiples ventanas descrita por Google SRE combina una señal rápida para fallos intensos con otra más lenta para degradaciones persistentes. En OSINT puede adaptarse sin copiar sus números:

- respuesta inmediata si una ejecución pierde páginas o rompe la trazabilidad;
- ticket de revisión si tres ejecuciones llegan progresivamente más tarde;
- revisión editorial si una fuente cambia su calendario y vuelve obsoleto el SLO.

Las alertas deben conducir a una acción concreta. Si nadie sabe qué hacer al recibirla, el umbral aún no está bien diseñado.

### 5. Escribe la política de agotamiento

Una política mínima para el caso ficticio podría decir:

> Si el presupuesto se agota, se detienen los cambios de parser y la publicación de nuevos derivados de esa fuente. Se permiten correcciones de seguridad, preservación de originales y trabajos destinados a restaurar la fiabilidad. La publicación se reanuda cuando una captura controlada supera las pruebas y el responsable editorial documenta el alcance del incidente.

La política no es un castigo al desarrollador ni una excusa para ocultar datos. Es un acuerdo para cambiar prioridades cuando la evidencia operativa indica que continuar añade riesgo. Debe nombrar responsables, excepciones, criterio de reapertura y fecha de revisión.

### 6. Ensaya con fallos sintéticos

Antes de confiar en el control, prueba tres escenarios sin tocar datos reales:

1. una paginación ficticia anuncia cuatro páginas y solo entrega una;
2. un documento llega después de la hora límite;
3. el parser encuentra una columna nueva y pone el registro en cuarentena.

Comprueba que el evento se clasifica, el presupuesto cambia una sola vez, la alerta llega al canal correcto y la publicación se bloquea cuando corresponde. Guarda los fixtures y las decisiones esperadas como pruebas de regresión.

## Lo que un presupuesto de error no puede demostrar

### No mide la completitud del mundo

Recorrer todas las páginas declaradas solo prueba cobertura respecto a la interfaz observada. La fuente puede ocultar registros, cambiar filtros o publicar tarde. Contrasta totales con boletines, APIs oficiales u otras vistas cuando existan, y documenta el alcance real.

### No convierte un dato falso en aceptable

Un pipeline puede cumplir el 100 % del SLO y transportar una afirmación falsa. Veracidad, autenticidad, representatividad e interpretación requieren corroboración separada. La fiabilidad técnica es necesaria; no es suficiencia probatoria.

### No arregla un indicador mal elegido

Si solo medimos que el proceso terminó con código cero, optimizaremos para ejecuciones verdes aunque falten páginas. El indicador debe acercarse a la experiencia investigadora: obtener a tiempo un artefacto trazable y con la cobertura observable esperada.

### No justifica perseguir «cinco nueves»

Un objetivo demasiado estricto puede crear falsas urgencias, trabajo manual y excepciones silenciosas. Uno demasiado laxo permite publicar degradaciones. Empieza con datos históricos, declara que el objetivo es provisional y revisa tanto los falsos avisos como los fallos que no detectó.

### No debe borrar incidentes del historial

Festivos, mantenimientos anunciados o caídas de terceros pueden explicarse, pero excluirlos retroactivamente para embellecer el porcentaje destruye la utilidad del sistema. Define antes qué queda fuera de alcance y conserva dos vistas: la métrica según política y el registro íntegro de lo ocurrido.

## Buenas prácticas de OPSEC, ética y privacidad

- Mide el proceso, no la vida de las personas que aparecen en las fuentes.
- Usa identificadores de ejecución y hashes; evita copiar nombres, correos o documentos sensibles a paneles y alertas.
- Aplica mínimos privilegios al almacenamiento de capturas y métricas.
- Separa originales, derivados, telemetría y decisiones editoriales.
- No hagas reintentos agresivos: respeta límites, términos de uso y capacidad del servicio público.
- Documenta cambios de alcance y evita que una métrica técnica se use para puntuar a individuos.
- Conserva UTC, zona horaria de la fuente y calendario previsto; un «retraso» sin contexto puede ser un festivo o un cambio legítimo.
- Incluye una vía humana para pausar el sistema cuando el daño potencial no cabe en el indicador.

## Checklist de implantación

- [ ] La unidad de medida es observable y tiene denominador.
- [ ] «Bueno» y «malo» se pueden reproducir con fixtures.
- [ ] La ventana corresponde al ritmo real de publicación.
- [ ] El objetivo se justifica con impacto y datos históricos.
- [ ] El presupuesto muestra porcentaje y conteo bruto.
- [ ] Cada alerta tiene responsable y acción inmediata.
- [ ] La política define parada, excepciones y reapertura.
- [ ] Se preservan originales aunque se bloquee el derivado.
- [ ] Los paneles no contienen datos personales innecesarios.
- [ ] Cumplir el SLO nunca se presenta como prueba de verdad.

## Alternativas y siguientes pasos

Si todavía no sabes qué cambió en la fuente o en el proceso, empieza por [observabilidad de datos](/observabilidad-datos-osint). Si necesitas localizar qué salidas dependen de una ejecución, usa [OpenLineage](/openlineage-linaje-datos-osint). Para expresar controles de esquema y calidad, [Soda Core](/soda-core-osint-contratos-datos-deriva-esquema) o [Great Expectations](/great-expectations-osint-calidad-datos) pueden aportar señales. OpenSLO ofrece una especificación abierta para representar SLI, objetivo, ventana y método de presupuesto, aunque adoptar su formato no sustituye el acuerdo editorial.

El takeaway accionable es concreto: elige una adquisición recurrente, escribe en una página qué cuenta como ejecución buena y simula una paginación incompleta. Si el equipo no sabe si debe publicar, advertir o detenerse, no ajustes el porcentaje todavía: termina primero la política.

Como próximo tema, merece la pena estudiar **postmortems sin culpa para incidentes OSINT**: cómo reconstruir una publicación degradada, delimitar el impacto y convertir las correcciones en pruebas sin exponer fuentes ni buscar culpables.

## Fuentes consultadas

- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [Google SRE Workbook: Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/)
- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Google SRE Workbook: Data Processing Pipelines](https://sre.google/workbook/data-processing/)
- [Google SRE Book: Embracing Risk](https://sre.google/sre-book/embracing-risk/)
- [OpenSLO: especificación](https://openslo.com/specification/)
