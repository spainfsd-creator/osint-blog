---
title: "Software Heritage en OSINT: preservar código, versiones y procedencia sin confundir archivo con prueba"
slug: /software-heritage-osint-codigo-preservado-swhid-procedencia
authors: [osint-writter]
tags: [osint, investigation, tooling, verification, methodology, privacy]
date: 2026-08-18
image: /img/blog/2026-08-18-software-heritage-osint-codigo-preservado.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT comparando un repositorio vivo, una captura histórica, identificadores criptográficos y una cronología de procedencia](/img/blog/2026-08-18-software-heritage-osint-codigo-preservado.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/software-heritage-osint-codigo-preservado-swhid-procedencia.m4a)


*Imagen generada mediante inteligencia artificial.*

Una empresa afirma que una función crítica ya existía cuando ganó un contrato público. Su repositorio muestra hoy el código y una etiqueta con el nombre correcto, pero ambas cosas pudieron cambiar después. Una captura aislada tampoco basta: necesitamos saber **qué objeto observamos, en qué visita fue archivado y si el contenido coincide byte a byte**. Software Heritage ayuda a fijar esas preguntas; no convierte automáticamente un repositorio preservado en prueba de autoría, fecha de creación o cumplimiento contractual.

<!-- truncate -->

Consultada el **18 de agosto de 2026**, la documentación oficial define [Software Heritage](https://www.softwareheritage.org/) como una infraestructura dedicada a recopilar, preservar y compartir código fuente disponible públicamente. Para OSINT responsable, su archivo puede servir para recuperar estados históricos, distinguir objetos de software y citar contenido mediante identificadores persistentes.

Todos los nombres, repositorios, contratos y hechos del caso práctico son ficticios. El método está pensado para investigación académica, periodismo, respuesta a incidentes y *due diligence* proporcionada; no para perfilar desarrolladores, explotar secretos expuestos ni eludir controles de acceso.

## Qué es Software Heritage y para qué sirve en OSINT

Software Heritage no es simplemente otra forja. GitHub, GitLab o una instancia propia alojan proyectos vivos y facilitan su desarrollo; el archivo conserva objetos recogidos de distintos orígenes y visitas. Esa separación importa cuando un repositorio desaparece, cambia de nombre, reescribe referencias o ya no muestra el estado que motivó una afirmación.

El [modelo de datos](https://docs.softwareheritage.org/devel/swh-model/data-model.html) permite razonar con varias piezas:

- **origen (*origin*):** la URL desde la que se obtuvo el software;
- **visita (*visit*):** un intento fechado de recuperar ese origen;
- **captura (*snapshot*):** el estado observado de sus ramas y etiquetas durante una visita;
- **revisión (*revision*):** un cambio con su árbol, metadatos y relaciones de historial;
- **publicación (*release*):** un objeto que apunta a otro objeto, normalmente asociado a una versión publicada;
- **directorio (*directory*):** un árbol de nombres y objetos;
- **contenido (*content*):** los bytes de un archivo.

No son sinónimos. La URL del origen responde **de dónde se intentó recoger**; la visita, **cuándo lo observó el archivador**; la captura, **qué referencias vio**; y el contenido, **qué bytes conserva**. Ninguna de esas capas demuestra por sí sola cuándo se escribió una idea, quién controlaba una cuenta o qué código llegó a producción.

### SWHID: identificar antes de interpretar

Los [SoftWare Hash IDentifiers o SWHID](https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html) identifican objetos mediante una forma como:

```text
swh:1:<tipo>:<identificador_intrinseco>
```

Los tipos de núcleo documentados son `snp`, `rel`, `rev`, `dir` y `cnt`. El identificador incorpora una huella calculada a partir del objeto. Además, puede llevar calificadores como `origin`, `visit`, `anchor`, `path` o `lines` para conservar contexto y señalar una ruta o líneas concretas.

Ese contexto evita una trampa frecuente. Un mismo archivo puede aparecer en varios repositorios o revisiones; un SWHID de contenido permite comprobar igualdad del objeto, pero no escoge automáticamente la procedencia relevante. Para una cita sólida conviene guardar el SWHID núcleo y, cuando corresponda, el origen, la visita, el ancla, la ruta y el intervalo de líneas.

## Caso de uso legítimo: verificar una entrega de software

Imagina que el ayuntamiento ficticio de **Puerto Claro** adjudicó en 2024 un contrato para publicar una biblioteca de cálculo ambiental. En 2026, el proveedor **Nébula Datos SL** afirma que la versión `2.1` ya incluía un control de integridad exigido en el pliego. La forja actual muestra una etiqueta `v2.1`, un fichero `integrity.py` y una nota de publicación aparentemente coherente.

La pregunta prudente no es «¿Software Heritage demuestra que la empresa cumplió?», sino una secuencia más pequeña:

1. ¿El origen estaba archivado y qué visitas existen?
2. ¿Qué captura conservó las referencias visibles en cada visita?
3. ¿A qué revisión y directorio apuntaba entonces `v2.1`?
4. ¿El fichero concreto ya estaba en ese árbol y cuál es su SWHID?
5. ¿La documentación contractual identifica esa misma versión o artefacto?
6. ¿Hay fuentes independientes que expliquen qué se desplegó y cuándo?

Un hallazgo útil podría ser: «La visita archivada el 12 de noviembre observó una referencia `v2.1` que resolvía a este árbol, donde estaba este contenido». Sería excesivo escribir: «El archivo prueba que el control funcionaba en producción desde esa fecha». La visita fecha la observación del archivador, no la creación material ni el despliegue.

## Flujo recomendado, paso a paso

### 1. Congela la pregunta y el alcance

Define de antemano qué afirmación vas a comprobar, qué repositorio público es pertinente y qué periodo importa. Guarda la URL exacta, fecha y hora UTC, finalidad, base legal cuando proceda y criterios de descarte. Evita descargar historiales completos si un directorio o fichero responde a la pregunta.

### 2. Conserva primero el origen vivo

Registra la URL, referencias visibles, identificadores nativos y documentos asociados. Si el origen es público y no aparece en el archivo, la interfaz [Save Code Now](https://archive.softwareheritage.org/save/) permite solicitar su archivado. Una solicitud aceptada o una visita programada no garantizan una captura inmediata, completa ni exitosa; anota el estado que devuelve el servicio.

No uses esta función para forzar la ingestión de material privado, credenciales filtradas o contenido cuya publicación resulte dudosa. Preservar más no siempre es preservar mejor.

### 3. Separa visita de fecha del código

En el archivo, revisa el historial de visitas y sus estados. La [API web](https://docs.softwareheritage.org/devel/swh-web/uri-scheme-api.html) documenta consultas de visitas por origen y devuelve, entre otros campos, fecha, estado, tipo y captura asociada. Una visita puede ser completa, parcial, estar en curso o carecer de captura válida.

Crea una tabla mínima:

| Campo | Qué anotar | Qué no demuestra |
|---|---|---|
| Origen | URL canónica consultada | Propiedad del proyecto |
| Visita | Fecha UTC, estado y tipo | Fecha de creación del código |
| Captura | SWHID y referencias observadas | Que cada rama estuviera completa |
| Revisión o *release* | SWHID, objetivo y metadatos | Autoría material o despliegue |
| Directorio o contenido | SWHID, ruta y tamaño | Licencia, seguridad o intención |

### 4. Fija el objeto adecuado

Escoge el nivel que responde a tu pregunta:

- usa `cnt` para citar bytes concretos de un fichero;
- usa `dir` para un árbol de código reproducible;
- usa `rev` cuando el contexto de una revisión sea esencial;
- usa `rel` si investigas una publicación etiquetada;
- usa `snp` para el mapa de referencias observado en una captura.

La documentación recomienda con frecuencia un SWHID de directorio para referenciar un artefacto de código robusto y añadir un ancla cuando se necesita recuperar el contexto. No pegues solo una URL larga en tus notas: conserva también el identificador como dato separado.

### 5. Verifica el contenido, no solo el visor

Resuelve el SWHID en la interfaz o mediante el endpoint de resolución documentado. Descarga únicamente el objeto necesario. El **Vault** puede reconstruir determinados objetos como paquetes descargables, pero un paquete reconstruido no tiene por qué coincidir byte a byte con un archivo comprimido distribuido originalmente: puede representar el mismo árbol con otro empaquetado.

Cuando el impacto lo justifique:

1. conserva el fichero o directorio recuperado sin modificar;
2. registra su tamaño y una huella moderna adicional para tu expediente;
3. recalcula localmente el SWHID con una herramienta compatible;
4. compara rutas, contenido y estructura con el objeto citado;
5. guarda la respuesta, la hora y cualquier error de resolución.

El objetivo es demostrar que analizaste el objeto identificado, no solo una representación visual cambiante.

### 6. Corrobora tiempo, autoría y uso fuera del archivo

Contrasta la captura con el repositorio original, registros de paquetes, notas firmadas, documentación de publicación, DOI, Software Bill of Materials, expedientes de contratación o evidencias de despliegue autorizadas. Lee cada fuente según lo que realmente puede afirmar.

Un nombre y correo en una revisión son metadatos, no una verificación de identidad. Una etiqueta puede haberse creado después. Una fecha de autor puede diferir de la fecha de integración. Una coincidencia de contenido prueba igualdad del objeto; no explica necesariamente quién lo escribió primero ni bajo qué condiciones se usó.

### 7. Redacta en capas de certeza

Separa siempre:

- **observado:** «el archivo conserva este contenido»;
- **contexto:** «aparece bajo esta ruta y ancla en esta captura»;
- **corroborado:** «el registro de publicación independiente enlaza la misma versión»;
- **inferido:** «es consistente con que el componente existiera antes de la entrega»;
- **no demostrado:** «no acredita qué binario se desplegó ni quién escribió cada línea».

Esta estructura hace que el informe pueda corregirse si aparece una visita anterior, una procedencia distinta o documentación contractual más precisa.

## Limitaciones y falsos positivos

- **Cobertura incompleta:** no todo el código público está archivado ni todas las visitas terminan con éxito.
- **Retraso de recogida:** la fecha de visita puede ser posterior a la creación o publicación real.
- **Capturas parciales:** referencias ausentes pueden deberse al cargador, al origen o al estado de la visita.
- **Historia reescrita:** una forja viva y una captura antigua pueden discrepar sin que una de ellas sea necesariamente fraudulenta.
- **Objetos compartidos:** el mismo contenido puede existir en muchos orígenes; igualdad no implica procedencia exclusiva.
- **Metadatos no autenticados:** autor, correo, mensaje y fecha pueden ser erróneos, importados o manipulados.
- **Etiqueta frente a *release*:** una referencia de la forja no equivale siempre a un objeto `rel` archivado.
- **Artefacto frente a fuente:** un árbol preservado no identifica automáticamente el paquete o binario desplegado.
- **Licencia incierta:** que el código sea accesible no significa que pueda reutilizarse sin revisar derechos y licencias.
- **Información sensible:** historiales públicos pueden contener datos personales o secretos publicados por error.
- **Retiradas y enmascarado:** ciertos objetos pueden dejar de estar accesibles por motivos jurídicos o de protección de datos.
- **Ausencia no concluyente:** no encontrar un objeto no demuestra que nunca existiera.

## Buenas prácticas de OPSEC, ética y privacidad

La [política de contenido](https://www.softwareheritage.org/legal/content-policy/) explica que el archivo recoge código fuente públicamente accesible y su historia, y contempla solicitudes relacionadas con derechos y protección de datos. Los [términos de acceso masivo](https://www.softwareheritage.org/legal/bulk-access-terms-of-use/) prohíben usos que perjudiquen injustificadamente la privacidad o seguridad y advierten de límites técnicos y de exactitud.

- Minimiza la recogida y limita el análisis a una finalidad legítima.
- No conviertas nombres y correos históricos en perfiles de desarrolladores.
- No publiques secretos, tokens, claves o datos personales hallados en código antiguo.
- Si aparece una credencial, detén la difusión, documenta lo imprescindible y usa un canal responsable de notificación.
- Respeta cuotas, términos, licencias y mecanismos de retirada; no intentes sortearlos.
- Guarda los identificadores técnicos separados de notas sensibles y controla el acceso al expediente.
- Solicita revisión humana antes de atribuir conducta, incumplimiento o autoría.
- Ofrece a las partes una forma concreta de responder y corregir errores.

## Checklist de validación

- [ ] La pregunta, el periodo y la finalidad están definidos.
- [ ] He guardado la URL exacta del origen y la hora UTC.
- [ ] Distingo fecha del código, fecha de revisión y fecha de visita.
- [ ] La visita tiene estado y captura documentados.
- [ ] He elegido el tipo de SWHID adecuado para la afirmación.
- [ ] Conservo núcleo, calificadores, ruta y ancla cuando corresponden.
- [ ] He verificado el objeto recuperado, no solo una captura de pantalla.
- [ ] He separado código fuente, paquete, binario y despliegue.
- [ ] Autoría, licencia y cronología tienen corroboración independiente.
- [ ] He anotado candidatos descartados, vacíos y explicaciones alternativas.
- [ ] No expongo credenciales ni datos personales irrelevantes.
- [ ] La conclusión dice con claridad qué no puede demostrarse.

## Alternativas y siguientes pasos

Software Heritage funciona mejor junto a otras fuentes:

- la forja original y sus registros de auditoría para el estado vivo y su administración;
- registros como npm, PyPI, Maven Central o crates.io para publicaciones de paquetes;
- **Sigstore** para verificar determinadas firmas y registros de transparencia;
- **SPDX** o **CycloneDX** para describir componentes en un SBOM, sin asumir que la lista sea completa;
- **DataCite** o **Zenodo** para DOI, depósitos y metadatos de resultados de investigación;
- **Internet Archive** para documentación web asociada;
- el expediente contractual, el sistema de compilación y registros autorizados para demostrar entrega o despliegue.

El takeaway accionable es este: toma un repositorio público y no sensible, elige una visita, identifica una captura y baja hasta un directorio concreto. Registra **origen, visita, captura, SWHID, ancla, ruta y corroboración**. Si una columna queda vacía, no la rellenes con intuición: convierte el vacío en una limitación explícita.

Como siguiente tema, sería útil estudiar **Sigstore** para separar identidad declarada, firma, certificado, registro de transparencia y verificación de un artefacto sin confundir firma válida con software seguro.

## Fuentes consultadas

- [Documentación de Software Heritage](https://docs.softwareheritage.org/)
- [Modelo de datos de Software Heritage](https://docs.softwareheritage.org/devel/swh-model/data-model.html)
- [Especificación y uso de SWHID](https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html)
- [API web: visitas, objetos y resolución](https://docs.softwareheritage.org/devel/swh-web/uri-scheme-api.html)
- [Política de contenido](https://www.softwareheritage.org/legal/content-policy/)
- [Términos de uso para acceso masivo](https://www.softwareheritage.org/legal/bulk-access-terms-of-use/)
