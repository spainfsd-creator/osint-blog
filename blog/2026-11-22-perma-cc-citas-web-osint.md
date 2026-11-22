---
title: "Perma.cc en OSINT: citar la web cambiante sin confundir archivo con prueba"
slug: /perma-cc-citas-web-osint
authors: [osint-writter]
tags: [osint, tooling, data, verification, methodology, privacy]
date: 2026-11-22
image: /img/blog/2026-11-22-perma-cc-citas-web-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una nota de prensa sostiene una afirmación decisiva para una investigación. La citamos hoy; mañana el texto cambia sin aviso y, una semana después, la URL devuelve un error. Conservar una copia permite mostrar qué página consultamos, pero no demuestra que su contenido fuera verdadero. **En OSINT, archivar una fuente y verificar una afirmación son operaciones distintas que deben permanecer enlazadas, no mezcladas.**

![Analista comparando una página web pública activa con una copia archivada y controles de integridad](/img/blog/2026-11-22-perma-cc-citas-web-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/perma-cc-citas-web-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [Perma.cc](https://perma.cc/) para citar páginas públicas que pueden cambiar o desaparecer. El caso, las entidades y los datos son ficticios. No se plantea preservar áreas privadas, eludir controles de acceso ni publicar información personal innecesaria. La meta es que otra persona pueda reconstruir **qué URL se consultó, qué representación quedó archivada, cuándo se creó y qué comprobaciones sostienen la conclusión**.

## Qué es Perma.cc y para qué sirve en OSINT

Perma.cc es un servicio de archivo web orientado a combatir la degradación de las referencias. A partir de una URL crea un **Perma Record**, la copia preservada, y un **Perma Link**, la dirección estable que permite citarla. La [guía oficial](https://perma.cc/docs/perma-link-creation) indica que, al terminar, debemos revisar el registro para comprobar cómo se capturó la página.

Esa revisión importa porque el objeto archivado no equivale automáticamente al objeto que creíamos observar. Una página moderna puede cargar contenido mediante JavaScript, depender de una sesión, mostrar variantes por región o incluir recursos que fallen durante la captura. Perma.cc preserva la página objetivo, pero su [FAQ](https://perma.cc/docs/faq) aclara que no recorre ni conserva las páginas enlazadas desde ella.

En una investigación legítima puede servir para:

- añadir a una cita una representación consultable de la página observada;
- reducir el riesgo de que una corrección o un error 404 rompan la trazabilidad;
- fijar el estado visible de una fuente pública en un momento concreto;
- compartir con revisores un punto de referencia común;
- descargar archivos WARC o WACZ para conservar una copia bajo control propio;
- documentar fallos de captura, exclusiones y diferencias entre página viva y archivo.

No sirve por sí solo para autenticar al autor, certificar la hora en sentido forense, demostrar que el contenido era exacto ni probar que nadie manipuló la página antes de capturarla. Tampoco convierte una afirmación publicada en un hecho corroborado.

### Cuatro objetos que conviene separar

| Objeto | Ejemplo | Qué aporta | Qué no demuestra |
| --- | --- | --- | --- |
| recurso original | `https://ejemplo.test/comunicado` | contexto y ubicación de publicación | que mañana conserve el mismo contenido |
| registro archivado | un Perma Link | representación recuperable creada en una fecha | que la captura sea completa o verdadera |
| observación | «la página muestra 18 adjudicaciones» | lectura concreta y comprobable | que el recuento sea correcto en la fuente primaria |
| corroboración | expediente oficial y dataset independiente | apoyo procedente de otra cadena de evidencia | que todas las fuentes sean realmente independientes |

Si estas capas se guardan en una sola columna llamada `evidencia`, los errores quedan ocultos. Una ficha mínima debe mantenerlas por separado.

## Caso de uso legítimo con un ejemplo ficticio

La asociación ficticia **Observatorio Ribera Clara** revisa la ejecución de un programa municipal de eficiencia energética. La página pública del ayuntamiento afirma que se han completado 18 actuaciones y enlaza una hoja resumen. El equipo necesita citar esa afirmación en un informe, pero sabe que el portal se actualiza cada trimestre.

La pregunta de investigación no es «¿miente el ayuntamiento?», sino una más verificable:

> ¿Qué actuaciones constaban como completadas en la página pública el 22 de noviembre de 2026 y qué documentos primarios respaldaban ese estado?

El equipo crea un registro de la página, revisa visualmente la copia y conserva también la URL original. Después contrasta cada actuación con el portal de contratación y las actas publicadas. El archivo resuelve la primera parte —qué representación se citó—, mientras que la corroboración documental aborda la segunda.

La tabla de trabajo podría contener estos campos:

| campo | contenido ficticio |
| --- | --- |
| `source_url` | URL pública original |
| `archive_url` | Perma Link del registro revisado |
| `observed_at_utc` | fecha y hora de la consulta, con zona |
| `capture_status` | completa, parcial, fallida o no evaluada |
| `claim` | afirmación exacta que se pretende comprobar |
| `locator` | título, sección, párrafo o elemento visible |
| `corroboration` | documentos con procedencia independiente |
| `review_state` | pendiente, corroborada, contradicha o inconclusa |

No se archivan nombres personales incidentales ni anexos ajenos a la pregunta. Si una página contiene datos sensibles, el equipo detiene la captura y evalúa finalidad, base jurídica, exposición y alternativas menos intrusivas.

## Flujo recomendado: de la URL a una cita auditable

### 1. Define la afirmación antes de capturar

Escribe qué necesitas sostener y qué parte de la página contiene la señal. «Guardar el portal» es una tarea abierta; «conservar la tabla de actuaciones marcada como actualizada el 20 de noviembre» permite comprobar si la captura sirve.

Registra antes de navegar:

- finalidad y alcance;
- URL esperada y dominio oficial;
- periodo relevante;
- información que debe excluirse;
- criterio de aceptación de la captura;
- fuentes independientes previstas para corroborar.

### 2. Observa la página viva sin forzar el acceso

Comprueba redirecciones, fecha visible, título, autoría declarada y contexto de publicación. No intentes superar autenticación, `paywalls`, CAPTCHAs ni exclusiones técnicas. Los [términos de Perma.cc](https://perma.cc/terms-of-service) limitan el servicio a material lícitamente accesible y exigen respetar derechos y legislación aplicable.

Anota la hora con zona y, cuando sea relevante, las condiciones que pueden cambiar la respuesta: idioma, región, versión móvil o parámetros de consulta. Evita conservar cookies, identificadores o cadenas de sesión en la URL.

### 3. Crea el registro y revisa el resultado

Introduce la URL en Perma.cc y espera a que termine el trabajo de captura. No registres el enlace como «correcto» solo porque el servicio haya devuelto un identificador. Compara original y copia:

- título y URL final;
- texto que sostiene la afirmación;
- tablas, imágenes o documentos incrustados relevantes;
- mensajes de consentimiento o error que puedan haber tapado contenido;
- fecha visible y elementos dinámicos;
- enlaces que el análisis necesitará abrir por separado.

Asigna un estado explícito. `Parcial` es más útil que un silencio que otro analista interpretará como éxito.

### 4. Conserva la pareja original–archivo

Una cita responsable mantiene la URL original y añade el enlace archivado. El original conserva el contexto actual; la copia muestra la representación utilizada. Guarda también título, fecha de acceso, fecha del registro y una breve nota sobre la revisión.

Cuando la política del proyecto lo requiera, descarga el archivo en WARC o WACZ. La [documentación de la API](https://perma.cc/docs/developer) describe ambos formatos y el acceso a los detalles de captura. Conserva el fichero fuera del repositorio público si contiene material sensible, calcula una huella criptográfica y registra herramienta, fecha y ubicación. La huella ayuda a detectar cambios en **esa copia**; no certifica la veracidad de la página.

### 5. Corrobora la afirmación fuera del archivo

Busca la fuente primaria subyacente: expediente, resolución, dataset, registro oficial o documento firmado. Luego incorpora una procedencia realmente independiente cuando el impacto de la conclusión lo justifique.

Dos capturas del mismo comunicado en servicios distintos son dos representaciones, no dos confirmaciones. Diez artículos que reproducen la misma nota tampoco forman diez fuentes independientes.

### 6. Publica la incertidumbre y permite reconstruir el camino

El informe debe indicar si la captura fue completa, qué parte se usó, qué cambió después y qué no pudo verificarse. Si la página viva contradice el archivo, conserva ambas representaciones y abre una incidencia; no sustituyas silenciosamente el enlace antiguo.

Una formulación prudente sería:

> La página municipal consultada y archivada el 22 de noviembre mostraba 18 actuaciones como completadas. El equipo corroboró 15 en expedientes públicos; dos seguían pendientes de documentación y una presentaba fechas incompatibles.

Eso distingue observación, comprobación y límite.

## Automatización proporcionada, sin convertir la API en una aspiradora

Perma.cc ofrece una API para crear y gestionar registros y lotes. Puede ser útil cuando un informe contiene muchas referencias previamente seleccionadas. Automatizar no autoriza a capturar dominios completos ni elimina la revisión humana.

Un pipeline prudente debería:

1. recibir una lista cerrada de URLs aprobadas;
2. eliminar parámetros de seguimiento y rechazar credenciales incrustadas;
3. limitar ritmo, volumen y reintentos;
4. guardar el identificador y el estado devueltos;
5. esperar a que finalice cada captura;
6. enviar muestras y fallos a revisión visual;
7. bloquear la publicación si falta la afirmación objetivo;
8. registrar quién aprobó el lote y con qué finalidad.

La clave de API debe viajar en la cabecera de autorización, no en el repositorio ni en una URL que pueda acabar en historiales y registros. La documentación oficial mantiene por compatibilidad un mecanismo antiguo mediante parámetro, pero recomienda la cabecera para nuevas integraciones.

## Limitaciones, fallos y falsos positivos

### Una copia visualmente convincente puede estar incompleta

El encabezado puede aparecer mientras falta una tabla cargada después, una imagen puede ser un marcador vacío y una ventana de consentimiento puede ocultar el contenido real. Revisa la afirmación concreta, no la estética general.

### El archivo no preserva el sitio entero

Perma.cc está diseñado para citas de páginas individuales. Si una tabla enlaza 18 expedientes, esos destinos necesitan su propia evaluación y, si procede, registros separados. No infieras que un enlace visible quedó capturado.

### Privado no significa inexistente

La guía explica que un registro puede quedar privado por configuración o por una exclusión específica mediante metadatos o `robots.txt`. También pueden intervenir reclamaciones válidas. Una respuesta no accesible no demuestra que nunca existiera una captura.

### La fecha de archivo no es la fecha del hecho

Una página capturada hoy puede describir un acto de hace meses, haber sido editada ayer o reutilizar una fecha antigua. Mantén separados `event_date`, `published_date`, `modified_date`, `observed_at` y `archived_at`.

### «Permanente» no es una garantía absoluta

Aunque el servicio persigue referencias duraderas, sus términos advierten que no garantizan una duración concreta ni la disponibilidad ininterrumpida. Para material crítico, conserva exportaciones autorizadas, metadatos y un plan de migración.

### El archivo conserva afirmaciones falsas con la misma eficacia

La estabilidad no añade credibilidad. Un registro puede preservar propaganda, una errata o una identidad suplantada. Autenticidad de la procedencia, exactitud del contenido y permanencia de la referencia son preguntas diferentes.

## Buenas prácticas de OPSEC, ética y privacidad

- Captura solo contenido público, pertinente y lícitamente accesible.
- No archives perfiles personales por curiosidad ni construyas historiales sobre personas sin finalidad legítima.
- Minimiza nombres, contactos, parámetros y documentos que no respondan a la pregunta.
- Revisa antes de crear un registro que pueda quedar públicamente accesible.
- No incluyas tokens, URL firmadas, identificadores de sesión ni rutas internas.
- Usa cuentas y claves del proyecto con controles de acceso y rotación.
- Trata la URL enviada al servicio como información revelada a un tercero.
- Documenta exclusiones, retiradas y restricciones en vez de intentar sortearlas.
- Separa la persona que captura de quien valida las conclusiones de mayor impacto.
- Define retención, exportación y eliminación para copias locales.

La [política de privacidad](https://perma.cc/privacy-policy) describe la recopilación de datos de cuenta, actividad e información técnica como la dirección IP. Esa dependencia de un tercero debe formar parte del análisis de riesgo, especialmente cuando la selección de URLs pueda revelar una línea de investigación.

## Checklist operativo

- [ ] La afirmación y la parte exacta de la página están definidas.
- [ ] La URL no contiene credenciales, sesiones ni seguimiento innecesario.
- [ ] El contenido es público, pertinente y lícito de preservar.
- [ ] Se registraron fecha, hora, zona, URL original y contexto.
- [ ] La copia se comparó con la página viva.
- [ ] El estado de captura es explícito: completa, parcial, fallida o pendiente.
- [ ] Los enlaces secundarios necesarios se evaluaron por separado.
- [ ] La afirmación se contrastó con fuentes de procedencia independiente.
- [ ] Los datos personales incidentales se minimizaron.
- [ ] Las exportaciones locales tienen ubicación, control de acceso y huella.
- [ ] La cita conserva tanto el original como el enlace archivado.
- [ ] El informe distingue observación, corroboración e incertidumbre.

## Alternativas y siguientes pasos

Wayback Machine ayuda a descubrir estados históricos que no capturamos nosotros; Archive.today ofrece captura bajo demanda con otro modelo; Browsertrix y WACZ son más adecuados para flujos de archivo web reproducible y de mayor alcance; Hunchly documenta sesiones de navegación; una captura local con WARC puede dar más control cuando existe capacidad de custodia. Ninguna alternativa elimina la obligación de revisar el resultado y corroborar la afirmación.

Perma.cc encaja especialmente bien cuando el producto final necesita **citas web legibles y duraderas**. No tiene por qué convertirse en el repositorio central de evidencias ni en un rastreador masivo.

El takeaway práctico es sencillo: **conserva la representación para que la cita sobreviva, pero valida la procedencia y la afirmación para que la conclusión resista**. Haz una prueba con tres páginas públicas y ficticias o de bajo riesgo: una estática, una dinámica y una con un recurso incrustado. Compara las copias, registra los fallos y decide de antemano qué estado impediría publicar. Como siguiente tema, merecería la pena diseñar una matriz de suficiencia probatoria que indique cuándo una captura, un documento primario y una corroboración independiente bastan para sostener distintos tipos de afirmaciones.

## Fuentes y documentación

- [Perma.cc: guía de inicio y funcionamiento](https://perma.cc/docs/)
- [Perma.cc: creación y gestión de registros](https://perma.cc/docs/perma-link-creation)
- [Perma.cc: preguntas frecuentes y límites de captura](https://perma.cc/docs/faq)
- [Perma.cc: documentación de la API, WARC y WACZ](https://perma.cc/docs/developer)
- [Perma.cc: términos de servicio](https://perma.cc/terms-of-service)
- [Perma.cc: política de privacidad](https://perma.cc/privacy-policy)
- [Harvard Library Innovation Lab: repositorio oficial de Perma.cc](https://github.com/harvard-lil/perma)
