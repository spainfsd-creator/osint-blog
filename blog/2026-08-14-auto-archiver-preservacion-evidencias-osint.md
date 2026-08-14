---
title: "Auto Archiver en OSINT: preservar contenido público sin confundir copia con prueba"
slug: /auto-archiver-preservacion-evidencias-osint
authors: [osint-writter]
tags: [osint, methodology, verification, investigation, tooling, privacy]
date: 2026-08-14
image: /img/blog/2026-08-14-auto-archiver-preservacion-evidencias-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT organizando capturas, vídeos, sellos temporales, hashes y notas de procedencia](/img/blog/2026-08-14-auto-archiver-preservacion-evidencias-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un vídeo público cambia de título, una publicación desaparece y la captura que guardaste ya no permite saber qué URL abriste ni cuándo. El hallazgo quizá era bueno; la preservación, no. En OSINT, **guardar un archivo es solo el principio**: para que otra persona pueda revisarlo necesitas conservar origen, momento, método, resultado y límites.

<!-- truncate -->

[Auto Archiver](https://github.com/bellingcat/auto-archiver), desarrollado por Bellingcat, automatiza esa primera capa de preservación. Recibe URL desde la línea de comandos, un CSV, Google Sheets u otros conectores; intenta extraer páginas y medios; puede enriquecer el resultado con metadatos, miniaturas, hashes o sellos temporales; y lo guarda localmente o en almacenamiento remoto. Es útil para equipos de verificación, redacciones, observatorios y proyectos académicos que trabajan con material abierto y volátil.

Pero conviene fijar la frontera desde el inicio: **una copia no demuestra que el contenido sea verdadero**, un hash no identifica a su autor y una fecha de descarga no equivale a la fecha del suceso. La herramienta ayuda a preservar y documentar; la autenticación, la corroboración y la valoración jurídica requieren pasos adicionales.

Todos los nombres, dominios, identificadores y situaciones del caso práctico son ficticios. El método se limita a material público, pertinente y obtenido de forma legítima.

## Qué es Auto Archiver y para qué sirve

La [documentación oficial](https://auto-archiver.readthedocs.io/en/latest/) define Auto Archiver como una herramienta Python para archivar contenido web de manera segura y verificable. Su valor práctico no está en una única descarga, sino en una tubería configurable que separa funciones:

- los **feeders** entregan las URL, por ejemplo desde CLI, CSV o Google Sheets;
- los **extractors** intentan recuperar la página, imagen, vídeo o publicación;
- los **enrichers** añaden elementos como metadatos, miniaturas, hashes, WACZ o sellos temporales;
- los **storages** conservan los objetos localmente, en Google Drive o en un almacén compatible con S3;
- los **databases** registran estados y resultados en consola, CSV, Sheets u otros destinos;
- los **formatters** crean una salida manejable, como una representación HTML.

Este diseño modular permite construir un flujo proporcional. Una investigación pequeña puede empezar con una URL y almacenamiento local. Un equipo puede usar una hoja compartida como bandeja de entrada, almacenamiento privado y un registro tabular. No hace falta activar todos los módulos: **más artefactos no significan necesariamente mejor evidencia**.

La documentación consultada el **14 de agosto de 2026** muestra la versión `1.2.7` y ofrece instalación mediante paquete Python o contenedor. Comprueba siempre la [guía de instalación vigente](https://auto-archiver.readthedocs.io/en/latest/installation/) antes de desplegarlo; dependencias, plataformas compatibles y módulos pueden cambiar.

## Caso ficticio: una retirada de producto anunciada en abierto

Imagina que la cooperativa ficticia **Puerto Claro** anuncia en su web y en dos perfiles públicos la retirada preventiva de un lote. Tu tarea legítima consiste en documentar qué comunicó la entidad y cómo evolucionó el aviso, no en identificar a clientes ni empleados.

Dispones de cuatro URL públicas:

1. el comunicado corporativo;
2. una publicación social que enlaza al comunicado;
3. un vídeo explicativo del fabricante;
4. la ficha pública del producto afectado.

Si solo haces capturas, puedes perder el vídeo, el HTML, los metadatos de recuperación o la relación entre las piezas. Si solo descargas los archivos, puedes olvidar de dónde procedían. Auto Archiver permite tratar cada URL como una unidad de trabajo y producir un registro consistente.

La pregunta correcta no es «¿puedo guardarlo todo?», sino «¿qué necesito preservar para verificar esta afirmación concreta?». En este caso, la respuesta puede incluir la URL original, el contenido recuperado, la hora de archivo en UTC, el estado del proceso, un hash del fichero y una nota que explique por qué se recogió.

## Flujo recomendado, paso a paso

### 1. Define alcance y criterio de inclusión

Antes de ejecutar nada, escribe una frase verificable: «documentar los comunicados públicos sobre el lote ficticio PC-2408 entre el 10 y el 14 de agosto». Añade qué dominios y cuentas oficiales entran, qué queda fuera y cuándo termina la recogida.

Ese límite evita dos problemas: acumular datos personales irrelevantes y convertir una investigación acotada en vigilancia permanente. Si una URL contiene comentarios de terceros, valora si son necesarios o si basta con preservar el comunicado principal.

### 2. Prepara una entrada mínima y trazable

Para una prueba controlada puedes usar la línea de comandos; para varias URL, un CSV resulta fácil de revisar y versionar. La [configuración oficial](https://auto-archiver.readthedocs.io/en/latest/installation/configurations.html) explica que la primera ejecución puede generar un `orchestration.yaml` y que el orden de los módulos se declara en `steps`.

Una hoja de control debería separar, al menos:

- `source_url`: URL recibida sin acortadores cuando sea posible;
- `collected_at_utc`: momento de la consulta;
- `case_id`: identificador interno no sensible;
- `reason`: afirmación que esa fuente puede ayudar a contrastar;
- `status`: éxito, parcial o fallo;
- `notes`: redirecciones, bloqueo, contenido dinámico o incidencia.

No incluyas credenciales en el CSV ni en un repositorio. La configuración admite autenticación para determinados módulos, pero cualquier secreto exige un almacén y controles de acceso adecuados.

### 3. Empieza con una configuración pequeña

El [repositorio oficial](https://github.com/bellingcat/auto-archiver) documenta dos arranques de alto nivel: una imagen Docker o `pip install auto-archiver`. Tras instalar en un entorno aislado y consultar `auto-archiver --help`, prueba una URL propia o una página creada para el ejercicio.

Una primera tubería razonable contiene:

- feeder de CLI o CSV;
- extractor genérico;
- enriquecedor de metadatos;
- enriquecedor de hash;
- almacenamiento local;
- registro CSV.

No copies comandos antiguos de artículos sin contrastarlos. En la arquitectura actual, el fichero de orquestación distingue módulos y configuraciones, y las opciones de CLI pueden sobrescribir lo guardado.

### 4. Conserva contenido y contexto por separado

El fichero descargado es un artefacto; la ficha de recogida es otro. Mantén juntos, mediante un identificador estable:

- el objeto original recuperado;
- su URL de origen y las redirecciones observadas;
- el instante de recuperación y la zona horaria;
- el módulo y resultado de la extracción;
- el hash calculado;
- los errores y elementos que no se pudieron guardar;
- las notas analíticas, claramente separadas de los datos obtenidos.

El `hash_enricher` ofrece cálculo de hash y la configuración de ejemplo usa `SHA-256`. Ese valor permite comprobar más tarde si **ese fichero** cambió. No prueba quién lo publicó, cuándo se creó originalmente ni si representa un hecho real.

### 5. Elige almacenamiento según el riesgo

La documentación ofrece [almacenamiento local](https://auto-archiver.readthedocs.io/en/latest/modules/autogen/storage/local_storage.html), Google Drive y [almacenamiento S3](https://auto-archiver.readthedocs.io/en/latest/modules/autogen/storage/s3_storage.html). Elige según volumen, sensibilidad, recuperación y trabajo en equipo.

Para una prueba, una carpeta local cifrada y con copia de seguridad puede bastar. Para un equipo, separa permisos de lectura, escritura y administración; habilita versionado o retención cuando proceda; y registra quién exporta o comparte material. No publiques automáticamente el archivo: que la fuente fuese pública no significa que replicarla indefinidamente sea necesaria o responsable.

### 6. Verifica la salida, no solo el estado «éxito»

Abre una muestra de los resultados. Comprueba que el vídeo reproduce, que el audio existe, que la captura corresponde a la URL, que el HTML no es una pantalla de consentimiento y que la marca temporal pertenece a la descarga correcta. Recalcula algunos hashes fuera de la herramienta y compáralos.

En el ejemplo de Puerto Claro, crea una tabla de cobertura:

| Fuente | Contenido | Metadatos | Hash | Revisión visual | Incidencia |
| --- | --- | --- | --- | --- | --- |
| Comunicado | HTML y captura | Sí | Sí | Correcta | Ninguna |
| Publicación | Captura parcial | Parciales | Sí | Correcta | Falta el hilo |
| Vídeo | Vídeo y miniaturas | Sí | Sí | Correcta | Sin subtítulos |
| Ficha | HTML | Sí | Sí | Correcta | Redirección anotada |

La fila parcial no debe maquillarse. Un fallo documentado es más útil que una falsa sensación de completitud.

## Sellos temporales, WACZ y Wayback: qué aportan

Auto Archiver dispone de módulos para [OpenTimestamps](https://auto-archiver.readthedocs.io/en/latest/modules/autogen/enricher/opentimestamps_enricher.html), WACZ y Wayback Machine. Son complementos, no sinónimos.

- Un **hash** detecta cambios en un objeto concreto.
- Un **sello temporal criptográfico** puede ayudar a demostrar que un compromiso sobre ese objeto existía no más tarde de cierto momento, según el mecanismo empleado.
- Un **WACZ** empaqueta contenido web archivado e información de reproducción en un formato interoperable.
- **Wayback Machine** aporta una copia mantenida por un tercero y puede ofrecer capturas anteriores o posteriores.

Ninguno resuelve por sí solo autenticidad, atribución o admisibilidad. Si el caso puede terminar en un procedimiento formal, define el protocolo con asesoramiento jurídico y forense antes de recoger material, no después.

## Limitaciones y falsos positivos

La web moderna es hostil al archivo perfecto. El extractor genérico puede depender de herramientas y reglas que cambian; las plataformas introducen autenticación, contenido dinámico, límites, geobloqueos y medidas anti-bot. Un resultado exitoso puede contener solo una miniatura o una página intermedia. Un fallo puede ser temporal y no significar que el contenido nunca existió.

También aparecen errores analíticos:

- atribuir una cuenta por el nombre visible sin verificar su control;
- confundir la hora de descarga con la hora de publicación;
- asumir que una URL redirigida siempre mostró el mismo contenido;
- tratar metadatos aportados por la plataforma como hechos independientes;
- considerar dos archivos iguales solo porque se parecen visualmente;
- creer que un hash «certifica» la verdad de lo archivado;
- ignorar ediciones, comentarios, contexto previo o contenido incrustado.

Registra versiones, fecha de consulta y configuración utilizada. Si repites la recogida, conserva los resultados como ejecuciones distintas: sobrescribir elimina precisamente la cronología que intentas estudiar.

## OPSEC, ética y privacidad

La automatización amplifica tanto el método como los errores. Aplica estas salvaguardas:

- trabaja con una cuenta y un entorno destinados al proyecto, nunca con perfiles personales innecesarios;
- limita las URL al alcance legítimo y evita espacios privados o credenciales obtenidas sin autorización;
- minimiza datos personales, especialmente comentarios, rostros, teléfonos y ubicaciones incidentales;
- cifra secretos y archivos sensibles; no pegues tokens en comandos que queden en el historial;
- restringe el acceso y fija plazos de conservación y borrado;
- no eludas controles técnicos o condiciones de servicio sin base legal y autorización;
- separa material sin verificar, evidencia corroborada y conclusiones analíticas;
- documenta cualquier transformación, recorte, conversión o transcripción.

La [demostración alojada por Bellingcat](https://auto-archiver.bellingcat.com/) se describe como un prototipo de mejor esfuerzo y advierte que no debe usarse para datos sensibles ni críticos. Para un proyecto serio, evalúa el despliegue propio, la seguridad del almacenamiento y la gobernanza del equipo.

## Alternativas y siguientes pasos

Auto Archiver resulta especialmente útil cuando necesitas una tubería repetible y varios tipos de contenido. Para una sola página, una captura manual acompañada de notas, una exportación WARC/WACZ o un servicio de archivo puede ser suficiente. **Hunchly** ayuda a capturar sesiones de navegación; **Webrecorder** trabaja con archivos web reproducibles; **Wayback Machine** añade una copia de tercero; y herramientas como `yt-dlp`, `ffmpeg` o `wget` cubren tareas concretas cuando se documentan bien.

La alternativa no debe elegirse por número de funciones, sino por la pregunta, el tipo de fuente, el riesgo y la capacidad de otra persona para repetir la revisión.

## Checklist operativo

- [ ] He definido una afirmación y un periodo concretos.
- [ ] Solo recojo URL públicas y pertinentes.
- [ ] Conservo URL, hora UTC, método, estado y notas.
- [ ] Guardo el objeto y su registro de procedencia.
- [ ] Verifico visualmente una muestra y documento fallos.
- [ ] Compruebo hashes de forma independiente.
- [ ] Distingo publicación, descarga, suceso y sello temporal.
- [ ] Protejo secretos y limito accesos.
- [ ] He fijado retención, copia de seguridad y borrado.
- [ ] Corroboro antes de atribuir o publicar conclusiones.

El takeaway es sencillo: **archiva temprano, pero concluye tarde**. Una buena tubería evita perder contenido; una buena investigación conserva además el contexto, admite sus huecos y permite que otra persona reconstruya cada decisión. El siguiente paso natural es profundizar en WACZ y la reproducción verificable de capturas web sin depender de una sola plataforma.

## Fuentes consultadas

- [Repositorio oficial de Bellingcat Auto Archiver](https://github.com/bellingcat/auto-archiver)
- [Documentación oficial de Auto Archiver](https://auto-archiver.readthedocs.io/en/latest/)
- [Configuración y arquitectura modular](https://auto-archiver.readthedocs.io/en/latest/installation/configurations.html)
- [Requisitos de sistema y almacenamiento](https://auto-archiver.readthedocs.io/en/latest/installation/requirements.html)
- [Bellingcat: Preserve Vital Online Content With Bellingcat's Auto Archiver](https://www.bellingcat.com/resources/2022/09/22/preserve-vital-online-content-with-bellingcats-auto-archiver-tool/)
- [Bellingcat: The Open Source Tool That Has Preserved 150,000 Pieces of Online Evidence](https://www.bellingcat.com/resources/2025/08/13/the-open-source-tool-that-has-preserved-150000-pieces-of-online-evidence/)
