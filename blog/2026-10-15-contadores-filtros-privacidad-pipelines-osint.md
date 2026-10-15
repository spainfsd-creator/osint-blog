---
title: "Contadores y filtros de privacidad en pipelines OSINT: parar antes de gastar de más"
slug: /contadores-filtros-privacidad-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, privacy, data, automation, verification]
date: 2026-10-15
image: /img/blog/2026-10-15-contadores-filtros-privacidad-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista ante un contador y un filtro de privacidad en un pipeline OSINT](/img/blog/2026-10-15-contadores-filtros-privacidad-pipelines-osint.png)

*Imagen generada mediante inteligencia artificial.*

El informe trimestral está listo cuando dos trabajadores lanzan a la vez la última consulta. Ambos leen «queda presupuesto», ambos ejecutan y ambos publican. El libro mayor registra una sola operación. **El mecanismo estadístico podía ser correcto y, aun así, el sistema que lo rodeaba ha gastado dos veces la misma autorización.**

Un contador de privacidad ayuda a calcular la pérdida compuesta de varios mecanismos; un filtro decide si una nueva operación puede continuar bajo un límite previamente fijado. Para que sirvan en un pipeline real hacen falta además reservas atómicas, identificadores idempotentes, estados explícitos y una definición inequívoca de qué cuenta como liberación.

<!-- truncate -->

Todos los nombres, cifras y organizaciones del ejemplo son ficticios. Este texto trata de gobernanza sobre datos propios, públicos o tratados con autorización. No convierte la privacidad diferencial en permiso para recolectar información personal ni sustituye una evaluación jurídica y de impacto.

## Qué son un contador y un filtro (y para qué sirven)

La privacidad diferencial permite razonar sobre cuánto puede cambiar la distribución de una salida cuando cambia la contribución de una unidad protegida. Al ejecutar varios mecanismos sobre datos solapados, sus garantías **componen**: la privacidad debe analizarse sobre el conjunto de salidas observables, no consulta por consulta.

Un **contador de privacidad** recibe una descripción matemática de los mecanismos ejecutados y calcula parámetros para su composición. La biblioteca [`dp-accounting` de Google](https://github.com/google/differential-privacy/blob/main/python/dp_accounting/docs/overview.md), por ejemplo, representa mecanismos como eventos y permite componerlos para obtener un `epsilon` dado un `delta`. El contador no descubre por sí solo qué consultas ocurrieron, qué persona contribuyó varias veces ni qué resultado salió del entorno de confianza: necesita eventos fieles y un modelo correcto.

Un **odómetro de privacidad** responde a una pregunta parecida en un escenario adaptativo: ofrece una cota acumulada a medida que se eligen mecanismos y parámetros. Un **filtro de privacidad** responde a otra: continuar o detener antes de rebasar un límite preestablecido. El trabajo que introdujo ambos conceptos demostró que no son intercambiables cuando los parámetros se eligen adaptativamente ([Rogers, Roth, Ullman y Vadhan, NeurIPS 2016](https://proceedings.neurips.cc/paper/2016/hash/58c54802a9fb9526cd0923353a34a7ae-Abstract.html)). Investigaciones posteriores construyen filtros y odómetros más ajustados para composición plenamente adaptativa ([Whitehouse, Ramdas, Rogers y Wu, ICML 2023](https://proceedings.mlr.press/v202/whitehouse23a.html)).

En operación, conviene separar las responsabilidades:

- el **contador matemático** evalúa la composición admitida por su modelo;
- el **filtro de política** rechaza o admite una reserva según esa evaluación;
- el **libro mayor** conserva quién pidió qué, sobre qué ámbito y con qué resultado;
- el **pipeline** impide que concurrencia, reintentos o rutas alternativas se salten los tres anteriores.

Una transacción atómica protege la coherencia del libro mayor. No demuestra que el mecanismo sea diferencialmente privado. Del mismo modo, una biblioteca de privacidad puede implementar bien un mecanismo y no saber que otro servicio publicó una segunda vista del mismo conjunto.

## Caso legítimo: un observatorio con publicaciones programadas

El observatorio ficticio **Faro Cívico** analiza expedientes autorizados de un servicio público. Cada trimestre publica tres agregados provinciales mediante mecanismos aprobados. El presupuesto global para esa población y periodo ya está definido por el equipo responsable.

La automatización tiene cuatro rutas:

1. una tarea programada calcula la publicación ordinaria;
2. un operador puede reanudarla tras un fallo;
3. otro servicio solicita correcciones;
4. un panel interno muestra el estado del proceso.

Durante una prueba, el worker genera correctamente el resultado, lo envía al almacén público y pierde la conexión antes de confirmar el paso. La cola repite el mensaje. Si «ejecución» y «liberación» se reducen a un booleano, el sistema puede cobrar dos veces el mismo resultado o, peor, liberar dos muestras distintas y cobrar una.

Faro Cívico rediseña el flujo alrededor de un identificador estable por liberación lógica, no por intento técnico. Antes de tocar los datos, reserva presupuesto dentro de una operación serializable. El resultado se cifra y queda asociado a la reserva. Publicar cambia el estado una sola vez; repetir con la misma clave devuelve el artefacto ya aprobado. Pedir una muestra nueva requiere una reserva nueva.

## Flujo recomendado

### 1. Define la frontera antes de construir el contador

Especifica la unidad protegida, vecindad, límites de contribución, población, ventana temporal, destinatarios y todas las salidas observables. Dos jobs pertenecen al mismo ámbito de composición si consultan contribuciones solapadas dentro de la promesa definida, aunque vivan en repositorios o nubes distintas.

[NIST SP 800-226](https://doi.org/10.6028/NIST.SP.800-226) insiste en que evaluar una garantía requiere considerar parámetros, unidad de privacidad, modelo de acceso, composición e implementación. Un número aislado no basta.

Asigna una clave estable al ámbito, por ejemplo una referencia opaca a `población + periodo + versión + definición`. No introduzcas nombres, correos ni selectores sensibles en logs operativos.

### 2. Registra intención, reserva, ejecución y liberación

No uses un único campo `gastado`. Un esquema conceptual mínimo podría separar:

```yaml
release_id: informe-2026-t3-provincia-v1
scope_id: poblacion-a-periodo-2026
mechanism_spec: spec-aprobada-07
request_state: proposed
reservation_state: held
execution_state: not_started
release_state: not_released
artifact_digest: null
```

La especificación debe ser versionada e inmutable. El digest identifica bytes, no su legitimidad. El registro guarda referencias y decisiones; los microdatos y detalles que permitan reconstruir contribuciones permanecen fuera.

Define por escrito qué consume presupuesto. Si los resultados de desarrollo, logs o previsualizaciones son visibles para personas no autorizadas, quizá ya sean liberaciones dentro del modelo. La [documentación del modelo de ataque de las bibliotecas de Google](https://github.com/google/differential-privacy/blob/main/common_docs/attack_model.md) recuerda que el cliente es responsable de contabilizar usos repetidos y que la biblioteca es solo un componente de un sistema superior.

### 3. Reserva de forma atómica antes de ejecutar

El filtro debe evaluar la nueva composición y crear la reserva en la misma frontera de concurrencia. El patrón lógico es:

1. bloquear o serializar el ámbito de presupuesto;
2. recuperar compromisos y liberaciones vigentes;
3. pedir al contador la composición candidata;
4. comparar contra la política aprobada;
5. rechazar o persistir la reserva con una clave idempotente;
6. confirmar la transacción;
7. solo entonces autorizar el acceso a los datos.

«Leer saldo y restar después» permite que dos workers acepten el mismo remanente. Un bloqueo global puede ser innecesario; lo imprescindible es que operaciones sobre el mismo ámbito no confirmen decisiones incompatibles.

No implementes fórmulas caseras si una biblioteca auditada representa los mecanismos usados. Tampoco mezcles sin prueba garantías de tipos distintos. El contador debe rechazar eventos que no sabe componer, no tratarlos como coste cero.

### 4. Haz idempotentes los reintentos

Una clave de idempotencia representa una **liberación lógica**. Si el mismo mensaje vuelve a llegar:

- con la misma especificación y sin ejecución, reanuda la reserva;
- con un artefacto ya liberado, devuelve la referencia existente;
- con parámetros distintos, rechaza el conflicto;
- si se solicita una nueva aleatorización observable, crea una liberación nueva.

No confundas «la consulta era igual» con «la salida es la misma». Ejecutar otra vez un mecanismo aleatorio y mostrar la nueva respuesta añade información observable. Borrar un archivo o marcar una publicación como retirada tampoco deshace lo que un destinatario ya pudo aprender.

### 5. Recupera fallos sin estados mágicos

Los estados intermedios necesitan reglas de recuperación. Una reserva puede expirar **solo si existe evidencia de que no hubo ejecución ni salida observable**. Si el proceso pudo calcular o publicar antes de caer, el sistema debe ponerlo en cuarentena para revisión, no devolver automáticamente el saldo.

Guarda un digest del artefacto antes de publicar y usa una promoción atómica cuando el almacén lo permita. Diseña reconciliaciones que comparen cola, libro mayor y destino público. Una diferencia debe detener nuevas liberaciones del ámbito hasta esclarecerse.

### 6. Trata el filtro como una barrera, no como una alerta

Un panel rojo que permite continuar no es un filtro. El rechazo debe ocurrir antes del acceso o liberación y ser seguro por defecto cuando:

- falta la especificación del mecanismo;
- el contador no soporta el evento;
- el ámbito no puede resolverse;
- el libro mayor no está disponible;
- existe una reserva ambigua o una discrepancia sin reconciliar.

La disponibilidad no justifica inventar saldo. Prepara, en cambio, publicaciones de contingencia ya aprobadas o productos agregados que no necesiten una consulta nueva.

## Limitaciones y falsos positivos operativos

Un contador puede devolver una cifra precisa para una entrada equivocada. Sus resultados dependen del modelo, del tipo de privacidad, de los límites de contribución y de que se registren todos los eventos relevantes. La contabilidad avanzada puede ser más ajustada que la suma básica, pero no debe utilizarse como descuento intuitivo.

Un filtro conservador también puede bloquear trabajo legítimo: una reserva abandonada, ámbitos que en realidad son disjuntos o duplicados del mismo artefacto pueden aparentar mayor consumo. La respuesta es reconciliar evidencia y corregir el modelo, no editar el saldo manualmente.

Errores frecuentes:

- confiar en el contador incorporado a un único servicio cuando existen más rutas de publicación;
- devolver reservas por timeout sin comprobar destino y logs;
- permitir que dos versiones definan de forma distinta la unidad protegida;
- reutilizar una clave idempotente con parámetros nuevos;
- considerar gratis una corrección porque reemplaza una URL;
- exponer previsualizaciones o métricas de depuración fuera del perímetro;
- presentar `epsilon` como porcentaje de anonimato o calidad;
- asumir que cumplir el presupuesto demuestra exactitud, equidad o licitud.

## Buenas prácticas de OPSEC, ética y privacidad

- Minimiza datos y contribuciones antes de aplicar el mecanismo.
- Desarrolla rutas de fallo y concurrencia con datos construidos desde cero.
- Separa permisos para proponer, aprobar, ejecutar y liberar.
- Mantén el ledger sin identificadores personales ni parámetros secretos innecesarios.
- Firma o protege contra manipulación especificaciones, eventos y artefactos.
- Alerta sobre reservas antiguas, conflictos idempotentes y diferencias con el destino.
- Ensaya caídas justo antes y después de cada transición crítica.
- Conserva una vía humana de revisión sin permitir sobrescribir el historial.
- Documenta incertidumbre y utilidad junto a cada salida.
- Detén el ámbito ante una discrepancia; no la compenses silenciosamente después.

El [Reglamento General de Protección de Datos, artículo 5](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679), exige, entre otros principios, limitación de finalidad, minimización, exactitud, limitación del plazo y seguridad. La privacidad diferencial puede apoyar una estrategia técnica, pero no reemplaza esos deberes.

## Alternativas y siguientes pasos

Si todas las consultas se conocen por adelantado, asigna el presupuesto y genera una publicación versionada en un único lote: reduce estados adaptativos. Si el producto necesita exploración, considera un entorno controlado con salidas revisadas. Si basta un agregado fijo, evita una API interactiva. Para pruebas técnicas usa fixtures sintéticos creados desde el esquema, no consultas al dataset protegido.

El takeaway accionable es concreto: dibuja hoy el diagrama de estados de una sola publicación y simula dos workers más un timeout justo después de escribir el destino. Si puedes obtener dos muestras, liberar sin reserva o devolver saldo después de una salida observable, el problema no está en el valor de `epsilon`: está en el control operativo.

Como siguiente tema, convendría estudiar la **reconciliación verificable entre ledger y artefactos públicos**: manifiestos, digests, estados terminales y procedimientos de incidente que detecten liberaciones huérfanas sin registrar datos sensibles.

## Fuentes consultadas

- [NIST SP 800-226: Guidelines for Evaluating Differential Privacy Guarantees](https://doi.org/10.6028/NIST.SP.800-226)
- [Rogers et al.: Privacy Odometers and Filters: Pay-as-you-Go Composition](https://proceedings.neurips.cc/paper/2016/hash/58c54802a9fb9526cd0923353a34a7ae-Abstract.html)
- [Whitehouse et al.: Fully-Adaptive Composition in Differential Privacy](https://proceedings.mlr.press/v202/whitehouse23a.html)
- [Google Differential Privacy: `dp-accounting` overview](https://github.com/google/differential-privacy/blob/main/python/dp_accounting/docs/overview.md)
- [Google Differential Privacy: attack model](https://github.com/google/differential-privacy/blob/main/common_docs/attack_model.md)
- [OpenDP: Typical Workflow](https://docs.opendp.org/en/stable/getting-started/typical-workflow.html)
- [Reglamento (UE) 2016/679, artículo 5](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679)
