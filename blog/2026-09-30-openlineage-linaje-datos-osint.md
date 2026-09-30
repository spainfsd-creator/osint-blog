---
title: "OpenLineage en OSINT: seguir el rastro del dato sin confundir procedencia con verdad"
slug: /openlineage-linaje-datos-osint
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-30
image: /img/blog/2026-09-30-openlineage-linaje-datos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista siguiendo el linaje de documentos y transformaciones en un pipeline OSINT](/img/blog/2026-09-30-openlineage-linaje-datos-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/openlineage-linaje-datos-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El informe dice que hay 418 contratos, pero nadie puede responder una pregunta sencilla: **¿qué descarga, qué versión del parser y qué filtros produjeron exactamente esa cifra?** El CSV original sigue en una carpeta, el cuaderno conserva otra copia y la tabla publicada no incluye ninguna pista sobre el camino intermedio. El resultado podría ser correcto; el equipo, sin embargo, ya no puede reconstruirlo ni medir el alcance de un error.

[OpenLineage](https://openlineage.io/) propone un estándar abierto para describir ejecuciones, trabajos, entradas y salidas de un pipeline. Aplicado con prudencia a OSINT, permite responder «de dónde salió este artefacto» y «qué derivados podrían estar afectados si cambia una fuente». No certifica que el dato original sea verdadero, completo o representativo. **El linaje documenta el recorrido técnico; la verificación sigue siendo trabajo de investigación.**

<!-- truncate -->

## Qué es y para qué sirve

OpenLineage representa la actividad de un pipeline mediante eventos. Su [modelo de objetos](https://openlineage.io/docs/spec/object-model/) distingue tres entidades principales:

- un **job** es el proceso lógico, como `normalizar_contratos`;
- un **run** es una ejecución concreta de ese proceso, identificada de forma única;
- un **dataset** es una entrada o salida, desde un fichero bruto hasta una tabla agregada.

Un `RunEvent` puede indicar que una ejecución empieza, termina, falla o se aborta, junto con los datasets consumidos y producidos. Los `JobEvent` y `DatasetEvent` sirven para metadatos de diseño que no pertenecen a una ejecución concreta. Esta separación evita tratar «el script que existe» y «lo que ocurrió hoy al ejecutarlo» como si fueran lo mismo.

El contexto adicional se expresa mediante **facets**. La [especificación de facets](https://openlineage.io/docs/spec/facets/) permite añadir metadatos al job, al run y a los datasets: ubicación y versión del código, esquema, estadísticas de salida, parámetros de ejecución o mensajes de error, entre otros. También admite extensiones propias con un nombre y un esquema versionado.

En una investigación responsable, ese vocabulario puede ayudar a:

- reconstruir qué adquisiciones alimentaron una tabla o gráfico;
- localizar derivados creados por una ejecución defectuosa;
- distinguir un dataset bruto de uno normalizado o agregado;
- comparar la ejecución programada con la realmente observada;
- adjuntar controles de calidad sin mezclarlos con conclusiones factuales;
- detectar huecos de instrumentación antes de necesitar una auditoría.

### Un grafo útil, no una cadena de custodia automática

Un grafo de linaje puede mostrar `respuesta.json → tabla_limpia.parquet → resumen.csv`. Eso no demuestra que la respuesta procediera realmente de la entidad que aparentaba publicarla, que no faltaran páginas, que el significado de un campo fuese el supuesto o que la inferencia final fuese razonable.

Tampoco basta para una cadena de custodia. OpenLineage transporta metadatos sobre el flujo; la preservación exige además conservar originales, hashes, tiempos, condiciones de adquisición, herramientas, controles de acceso y notas interpretativas. Si el emisor se equivoca u omite una dependencia, el grafo heredará ese error.

## Caso legítimo: el observatorio ficticio de Villa Serena

Un observatorio analiza contratos públicos del municipio ficticio de **Villa Serena**. Cada noche descarga páginas JSON desde un portal institucional, guarda las respuestas sin modificarlas, normaliza fechas e importes y publica únicamente estadísticas agregadas. No perfila personas ni automatiza decisiones sobre ellas.

El pipeline tiene cuatro trabajos:

| Job | Entrada | Salida |
| --- | --- | --- |
| `adquirir_portal` | endpoint y cursor autorizados | respuestas JSON inmutables |
| `validar_lote` | respuestas JSON | manifiesto de aceptación o cuarentena |
| `normalizar_contratos` | lote aceptado | tabla Parquet normalizada |
| `publicar_resumen` | tabla normalizada | CSV agregado y gráfico |

Una actualización del normalizador interpreta por error importes con coma decimal como miles. Con linaje de ejecución, el equipo puede localizar el `runId`, la revisión del código y la tabla de salida, y recorrer después los derivados hasta el resumen publicado. Puede retirar lo afectado sin asumir que todo el archivo histórico comparte el fallo.

El grafo no decide si `1.234,50` significa lo mismo en todas las fuentes ni si la cifra declarada es cierta. Solo acota qué transformación produjo qué salida. La decisión editorial requiere volver al contrato de datos, inspeccionar muestras y corroborar con la fuente primaria.

## Flujo recomendado paso a paso

### 1. Dibuja primero el pipeline real

Haz un inventario pequeño de jobs y datasets antes de instalar nada. Nombra fronteras que tengan significado operativo: adquisición, validación, transformación y publicación. Evita registrar como dataset cada variable temporal; un grafo con miles de nodos irrelevantes oculta justo las dependencias que debería aclarar.

Define un `namespace` estable por entorno y nombres comprensibles. Desarrollo, pruebas y producción no deben colisionar. Decide también cuándo un fichero representa un dataset nuevo: una respuesta cruda inmutable y una tabla normalizada sí tienen semánticas distintas.

### 2. Emite eventos alrededor de una transformación pequeña

Empieza por el trabajo que separa datos brutos de datos publicables. Genera un identificador único para la ejecución y conserva el mismo en sus eventos de inicio y final. Registra entradas y salidas con identificadores estables; si falla, emite el estado correspondiente y no declares una salida que nunca se completó.

Un esquema conceptual mínimo —deliberadamente abreviado— sería:

```json
{
  "eventType": "COMPLETE",
  "eventTime": "2026-09-30T03:15:08Z",
  "run": {"runId": "018ficticio-0000-7000-8000-000000000001"},
  "job": {
    "namespace": "villa-serena/produccion",
    "name": "normalizar_contratos"
  },
  "inputs": [
    {"namespace": "archivo-local", "name": "lote/2026-09-30"}
  ],
  "outputs": [
    {"namespace": "almacen-analitico", "name": "contratos_normalizados"}
  ],
  "producer": "https://investigacion.example/esquemas/lineage/v1"
}
```

Los identificadores son ficticios y no deben copiarse como diseño universal. La especificación completa, sus esquemas y las bibliotecas cliente son la referencia; el objetivo del ejemplo es hacer visibles job, run, entradas y salidas sin introducir datos personales.

### 3. Fija versión, cobertura y resultado

Relaciona la ejecución con la revisión exacta del código y la configuración pertinente. Registra conteos que ayuden a diagnosticar cobertura —páginas solicitadas, aceptadas, rechazadas y filas producidas—, pero no metas documentos enteros o consultas sensibles dentro del evento.

OpenLineage ofrece una [facet de métricas de calidad](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_metrics/) para recuentos y estadísticas de datasets. Esas métricas ayudan a detectar saltos, nulos o tamaños inesperados. Un conteo plausible no prueba que la adquisición esté completa; debe compararse con paginación, manifiestos y expectativas explícitas.

### 4. Modela relaciones precisas cuando importe

Inferir que cada entrada alimenta cada salida puede crear relaciones falsas en jobs con varios productos independientes. La [Lineage Job Facet](https://openlineage.io/docs/spec/facets/job-facets/lineage/) permite declarar aristas más precisas entre fuentes y objetivos. Úsala cuando la distinción cambie el análisis de impacto; no inventes linaje de columna si el motor o el código no pueden observarlo de forma fiable.

Prueba después tres preguntas reales:

1. ¿Qué ejecución y revisión produjeron este resumen?
2. ¿Qué salidas dependen del lote que quedó incompleto?
3. ¿Dónde deja el grafo de tener cobertura?

La tercera respuesta es tan valiosa como las otras. Un hueco visible es mejor que una relación inferida con falsa precisión.

### 5. Separa calidad técnica de verificación factual

La [facet de aserciones de calidad](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions/) puede registrar qué prueba se ejecutó, si pasó y cuál era su severidad. Una aserción `importe_no_negativo` o `expediente_id_no_nulo` expresa una condición técnica. No equivale a «el contrato existe», «el adjudicatario está correctamente identificado» o «no falta ninguna modificación posterior».

Mantén por separado:

- **procedencia técnica:** entradas, código, ejecución y salidas;
- **calidad estructural:** esquema, nulos, unicidad y cobertura esperada;
- **corroboración:** contraste con documentos y fuentes independientes;
- **interpretación:** hipótesis, incertidumbre y decisión editorial.

## Limitaciones y falsos positivos

### Instrumentación incompleta

Una integración automática puede reconocer algunas operaciones y omitir otras: un script auxiliar, una exportación manual o una hoja editada fuera del pipeline. La ausencia de una arista no demuestra independencia. Audita la cobertura con fixtures sintéticos y documenta fronteras no observadas.

### Identidades inestables

Si hoy un fichero se llama por ruta local y mañana por URL, el mismo dataset puede aparecer como dos nodos. El problema inverso también existe: un nombre demasiado genérico puede fusionar datasets diferentes. Define namespaces y reglas de identidad antes de acumular historial.

### Eventos perdidos o fuera de orden

El emisor, la red o el backend pueden fallar. Un `START` sin `COMPLETE` no siempre significa que el job siga ejecutándose; quizá se perdió el evento final. Supervisa la propia telemetría y contrástala con el orquestador y los artefactos almacenados.

### Metadatos demasiado sensibles

Parámetros, SQL, rutas, mensajes de error y nombres de datasets pueden revelar selectores, infraestructura o datos personales. Registrar más no siempre mejora la auditabilidad. Minimiza, seudonimiza cuando proceda, aplica retención y restringe el acceso al backend de linaje.

### El grafo parece más concluyente de lo que es

Una visualización limpia invita a leer causalidad o fiabilidad donde solo hay dependencia declarada. Dos datasets conectados no demuestran que la transformación sea correcta, ni que cada fila de salida pueda atribuirse a una fila concreta de entrada. Etiqueta relaciones inferidas, declaradas y observadas cuando tu implementación las distinga.

## Buenas prácticas de OPSEC, ética y privacidad

- Instrumenta tus propios procesos; no añadas carga innecesaria a fuentes públicas.
- Usa datos ficticios para validar el emisor y el backend.
- No registres tokens, cabeceras de autenticación, cuerpos completos ni selectores personales.
- Separa el acceso al grafo de linaje del acceso a los originales sensibles.
- Fija esquemas y versiones del productor para poder interpretar eventos antiguos.
- Conserva hashes y originales fuera del sistema de linaje, con controles adecuados.
- Define retención y borrado para metadatos que puedan revelar patrones de investigación.
- Trata una dependencia como pista de impacto, no como atribución de responsabilidad.
- Documenta jobs manuales y huecos de cobertura en lugar de simular automatización total.
- Exige revisión humana antes de publicar una conclusión sensible.

## Lista de control

- [ ] Jobs y datasets tienen nombres estables y significado operativo.
- [ ] Los entornos usan namespaces distintos.
- [ ] Cada ejecución conserva un identificador coherente entre eventos.
- [ ] Las salidas solo se declaran cuando realmente existen.
- [ ] Código y configuración relevantes quedan versionados.
- [ ] Los originales y sus hashes se preservan fuera del grafo.
- [ ] La cobertura de paginación se mide explícitamente.
- [ ] Los eventos no contienen secretos ni datos personales innecesarios.
- [ ] Las relaciones automáticas se prueban con fixtures sintéticos.
- [ ] Los pasos manuales y las zonas no instrumentadas están documentados.
- [ ] Calidad técnica, corroboración e interpretación permanecen separadas.
- [ ] Una visualización de linaje nunca se presenta como prueba de verdad factual.

## Alternativas y siguientes pasos

Si el objetivo inmediato es empaquetar evidencia y metadatos para intercambio, [RO-Crate](/ro-crate-osint-paquete-evidencia) puede ser un encaje mejor. Para transferir ficheros con manifiestos de integridad está [BagIt](/bagit-osint-transferencia-evidencia); para versionar datasets, [DVC](/dvc-versionado-datos-osint); y para validar transformaciones analíticas, [dbt](/dbt-osint-pruebas-transformaciones). OpenLineage ocupa otra capa: describe ejecuciones y dependencias entre procesos y datasets a medida que el pipeline opera.

El takeaway accionable es pequeño: dibuja hoy cuatro nodos —original, validación, tabla normalizada y publicación— y elige una sola transformación. Emite eventos con un fixture ficticio, provoca un fallo y comprueba que puedes localizar las salidas afectadas sin abrir ningún documento sensible. Si el grafo no refleja lo ocurrido, corrige la instrumentación antes de ampliarlo.

Como próximo tema, merece la pena estudiar **observabilidad de datos en OSINT**: cómo combinar linaje, frescura, volumen y contratos sin convertir un panel verde en una garantía de completitud o verdad.

## Fuentes consultadas

- [OpenLineage: sitio y documentación oficial](https://openlineage.io/)
- [OpenLineage: modelo de objetos](https://openlineage.io/docs/spec/object-model/)
- [OpenLineage: facets y extensibilidad](https://openlineage.io/docs/spec/facets/)
- [OpenLineage: Lineage Job Facet](https://openlineage.io/docs/spec/facets/job-facets/lineage/)
- [OpenLineage: Data Quality Metrics Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_metrics/)
- [OpenLineage: Data Quality Assertions Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions/)
