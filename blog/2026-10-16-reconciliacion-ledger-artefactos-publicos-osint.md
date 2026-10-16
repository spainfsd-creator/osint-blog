---
title: "Reconciliar ledger y artefactos públicos en OSINT: detectar liberaciones huérfanas"
slug: /reconciliacion-ledger-artefactos-publicos-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, investigation, automation]
date: 2026-10-16
image: /img/blog/2026-10-16-reconciliacion-ledger-artefactos-publicos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista que reconcilia un ledger de auditoría con artefactos públicos y sus huellas digitales](/img/blog/2026-10-16-reconciliacion-ledger-artefactos-publicos-osint.png)

*Imagen generada mediante inteligencia artificial.*

El panel interno dice que el informe nunca salió. Sin embargo, el PDF aparece en el almacenamiento público, una réplica conserva otra copia y el índice de descargas ya lo ha registrado. **Cuando el ledger y el mundo observable discrepan, creer al estado de la aplicación es exactamente el error que una reconciliación debe evitar.**

Reconciliar consiste en comparar de forma periódica tres planos: lo que el sistema quiso liberar, lo que registró como liberado y los bytes que realmente pueden obtener los destinatarios. El objetivo no es decorar cada fichero con un hash, sino descubrir publicaciones huérfanas, sustituciones, duplicados y registros incompletos antes de que una conclusión OSINT se apoye en una procedencia falsa.

<!-- truncate -->

Todos los nombres, identificadores y rutas del ejemplo son ficticios. Este artículo trata de trazabilidad para datos propios, públicos o tratados con autorización. No propone localizar documentos privados ni eludir controles de acceso.

## Qué es la reconciliación verificable (y para qué sirve)

Un pipeline puede mantener un **ledger** —un registro de intenciones, aprobaciones, ejecuciones y publicaciones— y aun así perder contacto con la realidad. Una escritura al destino puede completarse antes de que llegue la confirmación; un operador puede copiar un fichero por una ruta lateral; una CDN puede seguir sirviendo una versión retirada; o una corrección puede reemplazar bytes sin actualizar el registro.

La reconciliación verificable vuelve a observar ambos lados y exige evidencia comparable:

- una identidad estable de la liberación lógica;
- la ubicación o identificador del artefacto público;
- su longitud y digest calculados sobre los bytes exactos;
- la versión de la especificación que autorizó la salida;
- el estado y el momento observados, diferenciados de los declarados;
- una prueba de firma, procedencia o inclusión cuando el modelo de riesgo la requiera.

El [NIST SP 800-92](https://doi.org/10.6028/NIST.SP.800-92) sitúa la generación, transmisión, almacenamiento, acceso y análisis dentro de una práctica completa de gestión de logs. La lección operativa es sencilla: un registro aislado no basta si nadie comprueba su integridad, disponibilidad y relación con otros sistemas.

Tampoco basta un digest. SHA-256 puede responder si dos secuencias de bytes son iguales; no demuestra que el contenido sea verdadero, lícito, completo ni aprobado. Una firma añade quién controlaba una clave o identidad bajo una política concreta. Una atestación puede vincular un artefacto con un proceso. Cada evidencia responde una pregunta distinta.

## Caso legítimo: el informe que existe pero no figura

El observatorio ficticio **Brújula Pública** genera cada mes un agregado sobre contratos abiertos. Los datos de partida son públicos, pero el equipo aplica controles de calidad y evita liberar filas auxiliares usadas durante la depuración.

Una ejecución crea `informe-2026-09.pdf`, calcula su digest y comienza la subida. El objeto llega al almacenamiento, pero el worker pierde la conexión antes de cambiar el ledger de `uploading` a `released`. Un reintento ve el estado incompleto y publica una segunda versión, esta vez sin una nota metodológica incorporada al final. El ledger solo conserva el digest de la segunda.

Al día siguiente, el inventario del destino contiene dos objetos:

1. el artefacto inicial, accesible mediante una URL compartida y ausente del ledger;
2. el artefacto del reintento, registrado como la única liberación oficial.

No hay que decidir cuál «parece bueno» por el nombre o la hora. Brújula congela nuevas publicaciones para ese ámbito, conserva metadatos y logs pertinentes, calcula los digests desde el destino y reconstruye la secuencia. Después clasifica el primer objeto como **liberación huérfana**: existe en el perímetro público pero carece de un estado terminal coherente. La corrección no borra el incidente; añade un evento compensatorio y una referencia al artefacto retirado, porque los destinatarios pudieron haberlo descargado.

## Flujo recomendado

### 1. Define conjuntos y una clave estable

Trabaja con dos conjuntos explícitos:

- **esperados:** liberaciones que el ledger considera terminales y observables;
- **observados:** artefactos que el destino realmente enumera o sirve.

La comparación necesita una clave que sobreviva a reintentos. Un UUID de intento no sirve si cada worker crea uno nuevo. Usa una identidad de liberación lógica derivada de campos no sensibles y estables, como proyecto, periodo, producto y revisión. Separa esa clave del nombre físico para poder mover un objeto sin fingir una nueva publicación.

Un manifiesto conceptual podría ser:

```yaml
release_id: contratos-2026-09-r1
policy_ref: agregado-mensual-v4
destination: public-reports
object_key: 2026/09/informe-r1.pdf
digest:
  algorithm: sha256
  value: "<64 caracteres hexadecimales>"
size_bytes: 184320
ledger_state: released
observed_at: "2026-10-16T05:00:00Z"
```

No incluyas selectores personales, consultas sensibles ni credenciales en el manifiesto. El digest debe calcularse sobre el artefacto final, no sobre un fichero previo a una conversión, compresión o subida que pueda cambiar los bytes.

### 2. Trata el destino como una fuente independiente

Si el reconciliador pregunta a la misma base de datos que alimenta el panel, solo confirma una narración consigo misma. Enumera el destino real mediante una interfaz de solo lectura: almacenamiento de objetos, repositorio, índice público o endpoint de descarga. Cuando haya CDN o réplicas, toma muestras de las rutas que ven los destinatarios.

Recoge como mínimo clave, tamaño, versión del objeto, fecha observada y digest. Una cabecera HTTP puede ayudar, pero un `ETag` no es necesariamente un hash de contenido y su semántica depende del servicio. Calcula una huella criptográfica de los bytes cuando necesites igualdad verificable.

La observación debe ser repetible y acotada. Guarda la configuración del barrido y un resumen de resultados, no copias indiscriminadas de todo el destino. Si el contenido es sensible, verifica dentro del perímetro autorizado y exporta solo identificadores opacos y resultados mínimos.

### 3. Compara por categorías, no con un único booleano

La intersección de ambos conjuntos produce diagnósticos distintos:

| Ledger | Destino | Digest | Clasificación inicial |
| --- | --- | --- | --- |
| Presente | Presente | Coincide | Candidato coherente |
| Presente | Ausente | — | Publicación perdida o retirada fuera de flujo |
| Ausente | Presente | — | Liberación huérfana |
| Presente | Presente | Difiere | Sustitución, corrupción o clave reutilizada |
| Duplicado lógico | Varios objetos | Variable | Reintento no idempotente o réplica no modelada |

«Candidato coherente» no significa «contenido correcto». Aún debes validar autorización, firma, procedencia, caducidad y política. También debes modelar las réplicas legítimas para no convertir toda redundancia en una alerta.

### 4. Encadena procedencia y artefacto

El proyecto [in-toto](https://in-toto.io/docs/getting-started/) registra materiales, productos, comandos y actores de pasos definidos, y permite verificar esa cadena contra un layout firmado. El patrón útil para OSINT es vincular cada transición relevante con el digest del producto que entrega al paso siguiente. Si el renderizador recibió un CSV con digest A y produjo un PDF con digest B, esa relación debe estar en evidencia verificable, no inferida a partir de nombres parecidos.

[SLSA 1.2](https://slsa.dev/spec/v1.2/verifying-artifacts) subraya que la procedencia solo aporta valor cuando alguien la verifica contra expectativas: identidad del constructor, firma, parámetros y relación con el artefacto, entre otros controles. No aceptes cualquier atestación válida; expresa qué identidades, repositorios, procesos y campos son admisibles para ese producto.

En un flujo pequeño no hace falta desplegar toda una infraestructura de cadena de suministro. Un manifiesto firmado y una verificación independiente pueden ser suficientes. La arquitectura debe responder al riesgo, pero la relación `release_id → digest final → evidencia → destino observado` ha de quedar inequívoca.

### 5. Usa transparencia cuando necesites detectar reescrituras

Un log append-only permite publicar compromisos sin autorizar la edición silenciosa del pasado. [Rekor](https://docs.sigstore.dev/logging/overview/) almacena metadatos firmados en un registro resistente a manipulaciones y permite consultar entradas y pruebas. El principio general no depende de una marca: una promesa de inclusión, una prueba de inclusión y una prueba de consistencia no son lo mismo.

El [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162) explica cómo una prueba de inclusión demuestra que una hoja pertenece a un árbol concreto y cómo una prueba de consistencia demuestra que un árbol posterior conserva el prefijo del anterior. Por tanto:

- encontrar un digest en un log prueba inclusión respecto de una raíz verificada;
- no prueba que el fichero fuera correcto ni que no existiera otra versión fuera del log;
- comprobar dos raíces sin prueba de consistencia no demuestra por sí solo que el historial sea append-only;
- una promesa de inclusión debe auditarse después conforme a las garantías del sistema.

Mantén una copia verificable de la evidencia necesaria para auditoría y define la raíz de confianza. Si el verificador descarga clave, política y prueba desde el mismo punto comprometido, la sofisticación criptográfica no evita una vista fabricada.

### 6. Diseña estados de incidente que no borren historia

Ante una discrepancia, detén nuevas liberaciones del ámbito afectado y crea un incidente con referencias a la observación. No cambies `released` a `never_happened`. Usa estados o eventos como:

- `orphan_observed`;
- `digest_mismatch`;
- `destination_missing`;
- `quarantined`;
- `superseded`;
- `withdrawn_after_release`;
- `reconciled`.

Una retirada reduce exposición futura, pero no recupera copias descargadas. El registro debe conservar el intervalo de exposición conocido, las rutas afectadas y la comunicación emitida. Cuando no puedas determinar si hubo acceso, declara la incertidumbre; no conviertas ausencia de telemetría en ausencia de descargas.

### 7. Convierte la reconciliación en un control periódico

Ejecuta el control después de cada lote y también de forma independiente. La comprobación inmediata detecta fallos operativos; el barrido periódico encuentra cambios laterales, retenciones inesperadas y divergencias acumuladas. Usa una cuenta de solo lectura distinta de la identidad que publica.

Mide al menos:

- número y antigüedad de huérfanos;
- objetos esperados ausentes;
- diferencias de digest o tamaño;
- claves lógicas con varias versiones observables;
- evidencias que no verifican o están fuera de política;
- tiempo desde la primera observación hasta contención y resolución.

Alerta por identidad estable, no por cada ejecución, para evitar tormentas. Cada repetición debe añadir una observación al mismo caso hasta que cambie la evidencia.

## Limitaciones y falsos positivos

La consistencia eventual puede hacer que un objeto recién escrito tarde en aparecer en listados o réplicas. Define una ventana de gracia basada en el comportamiento documentado del destino; no la uses para ocultar discrepancias antiguas. Las políticas de ciclo de vida también pueden retirar objetos legítimamente, pero esa transición debe estar representada en el ledger.

Otros errores frecuentes son:

- comparar el hash de un manifiesto con el del artefacto;
- aceptar `ETag` como SHA-256 sin verificar la semántica;
- ignorar normalizaciones, compresión o conversión de finales de línea;
- firmar un digest sin ligar identidad, finalidad y política;
- considerar la fecha del sistema como prueba fiable de publicación;
- borrar una entrada para «hacer cuadrar» los conjuntos;
- registrar solo resultados exitosos y perder fallos parciales;
- verificar una atestación criptográficamente sin comprobar sus expectativas;
- asumir que un log transparente garantiza la veracidad del contenido inscrito.

Una discrepancia también puede ser un fallo del propio reconciliador: permisos incompletos, paginación truncada, reloj desajustado o inventario parcial. Conserva evidencia suficiente para distinguir «no existe» de «no pude observarlo».

## Buenas prácticas de OPSEC, ética y privacidad

- Usa cuentas de lectura con el alcance mínimo y separadas del publicador.
- No vuelques URLs firmadas, tokens ni nombres sensibles en logs o tickets.
- Calcula digests dentro del perímetro autorizado cuando los artefactos no sean públicos.
- Protege ledger, políticas, claves y resultados de auditoría contra modificación no autorizada.
- Mantén separadas las funciones de publicar, aprobar y reconciliar en operaciones de impacto alto.
- Define retención para evidencia y elimina copias auxiliares cuando dejan de ser necesarias.
- Prueba el flujo con artefactos ficticios antes de introducir información real.
- Registra incertidumbre, cobertura y límites de observación.
- Comunica correcciones con precisión y sin amplificar datos que debían retirarse.
- No uses trazabilidad técnica para legitimar una recolección invasiva o una atribución débil.

## Alternativas y siguientes pasos

Para un blog o repositorio pequeño, Git puede ofrecer historial, digests y revisión suficientes si el despliegue está estrechamente ligado a commits verificables y se comprueba el destino. Para publicaciones estáticas, un manifiesto versionado junto al índice puede simplificar el inventario. En entornos mayores, las atestaciones in-toto/SLSA, firmas Sigstore y logs de transparencia añaden separación entre productor, registro y verificador.

Ninguna herramienta sustituye la pregunta central: **¿puedo demostrar que los bytes observables son exactamente los autorizados y explicar cualquier diferencia sin reescribir el pasado?**

El takeaway accionable es concreto: toma hoy diez liberaciones recientes, enumera el destino con una identidad de solo lectura y construye la tabla `release_id`, ubicación, tamaño, digest esperado y digest observado. Si aparece un objeto sin fila, una fila sin objeto o un digest distinto, abre un incidente antes de «arreglar» el ledger.

Como siguiente tema, convendría estudiar los **simulacros de recuperación ante liberaciones huérfanas**: cómo ensayar retirada, comunicación, preservación de evidencia y restauración del pipeline sin usar datos reales.

## Fuentes consultadas

- [NIST SP 800-92: Guide to Computer Security Log Management](https://doi.org/10.6028/NIST.SP.800-92)
- [in-toto: Getting started y reglas de artefactos](https://in-toto.io/docs/getting-started/)
- [SLSA 1.2: Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [Sigstore: Rekor transparency log](https://docs.sigstore.dev/logging/overview/)
- [Sigstore: verificación de firmas y pruebas de inclusión](https://docs.sigstore.dev/cosign/verifying/verify/)
- [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162)
