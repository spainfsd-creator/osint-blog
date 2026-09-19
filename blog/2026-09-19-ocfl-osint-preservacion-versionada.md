---
title: "OCFL en OSINT: preservar versiones sin confundir historial con verdad"
slug: /ocfl-osint-preservacion-versionada
authors: [osint-writter]
tags: [osint, methodology, tooling, verification, data, privacy]
date: 2026-09-19
image: /img/blog/2026-09-19-ocfl-osint-preservacion-versionada.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando versiones, inventarios y sumas de comprobación en un repositorio OCFL](/img/blog/2026-09-19-ocfl-osint-preservacion-versionada.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/ocfl-osint-preservacion-versionada.m4a)


*Imagen generada mediante inteligencia artificial.*

Una investigación sobre contratación pública lleva tres años acumulando capturas web, CSV, notas y correcciones. El informe final sigue disponible, pero nadie sabe qué ficheros pertenecían a la primera entrega, cuándo se sustituyó una tabla ni si la copia conservada mantiene los mismos bytes. **Guardar mucho no equivale a preservar bien; conservar la historia exige una estructura verificable.**

[OCFL](https://ocfl.io/1.1/spec/) —*Oxford Common File Layout*— define cómo organizar objetos digitales versionados de forma transparente e independiente de una aplicación concreta. Puede ayudar a mantener una colección OSINT comprensible y comprobable a largo plazo. No certifica la autenticidad de una fuente, no decide qué debe conservarse y no convierte una sucesión de versiones en una cronología verdadera de los hechos.

<!-- truncate -->

## Qué es OCFL y para qué sirve

La especificación OCFL describe el objeto «en reposo»: sus ficheros, inventarios y versiones dentro de un sistema de archivos o de un almacenamiento de objetos que presente una jerarquía equivalente. La versión publicada vigente es la [especificación 1.1](https://ocfl.io/1.1/spec/), fechada el 7 de octubre de 2022 y actualizada el 7 de noviembre de 2024. El borrador de trabajo no debe tratarse como una versión publicada.

Su objetivo es que el contenido sea completo, legible por personas y máquinas, robusto ante errores y migraciones, versionable y portable entre tecnologías de almacenamiento. Una idea central es la **reconstruibilidad**: el repositorio debería poder recuperarse desde lo almacenado sin depender de la aplicación que lo gestionaba.

Un objeto mínimo tiene una declaración de conformidad, un inventario JSON protegido por su propio resumen criptográfico y al menos un directorio de versión:

```text
objeto-villa-ejemplo/
├── 0=ocfl_object_1.1
├── inventory.json
├── inventory.json.sha512
└── v1/
    ├── inventory.json
    ├── inventory.json.sha512
    └── content/
        ├── README.md
        ├── fuentes/contratos.csv
        └── notas/adquisicion.md
```

El `manifest` del inventario relaciona resúmenes criptográficos con rutas físicas. Cada bloque `state` relaciona esos mismos resúmenes con las rutas lógicas visibles en una versión. Esa separación permite conservar un único flujo de bytes aunque su nombre lógico cambie o aparezca en más de una ruta. Las versiones usan una secuencia continua —`v1`, `v2`, `v3`— y los directorios ya creados se consideran inmutables.

OCFL no prescribe qué constituye un objeto ni cuándo merece una versión nueva. Tampoco aporta por sí mismo metadatos descriptivos suficientes. Esas son decisiones locales que deben quedar escritas antes de construir el repositorio.

## Caso de uso legítimo: una serie de expedientes públicos

Imaginemos una unidad de investigación que estudia, con datos públicos, la evolución de contratos de parques en el municipio ficticio de Villa Ejemplo. Cada trimestre descarga el conjunto oficial, conserva la respuesta original, normaliza fechas e importes y publica una tabla agregada. A veces el portal corrige registros antiguos sin explicar el cambio.

El equipo define un objeto OCFL para la colección y una política sencilla:

- `v1` contiene la adquisición inicial, su ficha de procedencia y el código de transformación;
- `v2` incorpora una descarga posterior y documenta qué registros cambiaron;
- `v3` corrige un error del propio análisis sin sobrescribir las versiones anteriores;
- cada versión lleva fecha con zona horaria, mensaje y agente responsable;
- los datos personales irrelevantes se excluyen antes del ingreso;
- la copia publicable y el archivo restringido se gestionan como ámbitos distintos.

La versión más reciente puede reconstruirse combinando los contenidos introducidos en ella y en las anteriores, según el estado lógico declarado. El inventario permite saber qué bytes sostienen cada ruta en cada versión. Sin embargo, si el portal publicó un dato erróneo, OCFL preservará fielmente ese error. La verificación factual sigue necesitando fuentes primarias, contexto y corroboración independiente.

## Flujo recomendado, paso a paso

### 1. Definir el objeto y la política de versión

Antes de elegir software, escribe la unidad de preservación. ¿Un objeto representa un caso, una fuente, una entrega o una colección anual? Un objeto gigantesco dificulta validaciones y recuperación; miles de objetos diminutos pueden complicar la gestión.

Define también qué provoca una versión: una nueva adquisición, una corrección documentada, una transformación reproducible o un cambio de metadatos relevante. Evita crear versiones por procesos internos sin significado y, en el extremo contrario, acumular cambios heterogéneos en una única versión opaca.

### 2. Separar originales, derivados y documentación

Prepara una copia de ingreso. Distingue las respuestas originales de los derivados, el código, las notas metodológicas y los resultados publicables. Incluye un `README` con pregunta, alcance, exclusiones y responsables; registra para cada adquisición URL, consulta, fecha y hora UTC, licencia, método y condiciones observadas.

No incorpores cookies, tokens, rutas personales, agendas completas ni identidad de fuentes protegidas. Preservar a largo plazo amplifica el coste de una mala decisión de privacidad.

### 3. Usar una implementación y validar, no fabricar JSON a mano

La especificación es precisa: exige rutas seguras, inventarios coherentes, secuencias de versión continuas y resúmenes compatibles. Para una prueba aislada resulta útil leer un ejemplo; para producción conviene usar una implementación mantenida y un validador que informe con los [códigos oficiales de validación](https://ocfl.io/1.1/spec/validation-codes.html).

La comunidad mantiene una [lista de implementaciones](https://ocfl.io/) y el proyecto oficial incluye [objetos de prueba](https://github.com/OCFL/fixtures) para comprobar validadores. Una herramienta que puede crear objetos no debe darse por conforme automáticamente: fija versión, prueba exportación y restauración, y documenta el resultado.

### 4. Crear la primera versión desde una zona de trabajo

No modifiques directamente el almacenamiento OCFL. Ensambla la versión en una zona temporal, revisa contenido y metadatos, y pide al cliente que realice una escritura transaccional. Las [notas de implementación](https://ocfl.io/1.1/implementation-notes/) recomiendan tratar con cuidado las actualizaciones y evitar dejar un objeto a medio escribir.

Tras el ingreso, valida al menos:

- declaración de conformidad del objeto y, si existe, de la raíz;
- estructura y sintaxis de todos los inventarios;
- suma del `inventory.json` de la raíz y de cada versión;
- correspondencia entre `manifest`, `state` y ficheros reales;
- continuidad de versiones y ausencia de rutas ambiguas;
- cálculo real de los resúmenes de contenido, no solo comparación entre JSON.

### 5. Añadir cambios como una versión nueva

Una versión OCFL usa *forward deltas*: solo necesita almacenar contenido nuevo que no estuviera ya en el objeto, mientras el inventario describe el estado lógico completo. Un cambio de nombre sin cambio de bytes puede reutilizar el contenido existente. Una eliminación desaparece del nuevo `state`, pero la versión anterior sigue siendo reconstruible.

Incluye un mensaje concreto, por ejemplo: «Incorporada descarga pública de 2026-09-19 y corregido el separador decimal del derivado». Evita mensajes como «actualización» que no ayudan a interpretar el historial. La marca `created` registra la creación de la versión OCFL; no demuestra cuándo ocurrió el hecho descrito por la fuente.

### 6. Validar de forma periódica y ensayar la recuperación

La fijación no es un acto único. Programa comprobaciones por lotes, registra herramienta, versión, alcance, resultado y UTC, y conserva el informe fuera del propio objeto cuando necesites una referencia independiente. La especificación admite SHA-256 o SHA-512 para direccionamiento por contenido y recomienda SHA-512; MD5 y SHA-1 quedan limitados a valores de fijación heredados.

Una validación correcta solo indica coherencia con el inventario y con la especificación. Complementa el control con copias separadas, supervisión del almacenamiento, pruebas de restauración y procedimientos de respuesta. Al menos una vez, reconstruye una versión antigua en un destino limpio y compara su estado lógico esperado.

## Limitaciones y falsos positivos

### Integridad no es autenticidad

Un resumen coincidente prueba que unos bytes corresponden al valor registrado. No prueba quién creó el fichero, si la web era veraz ni si la selección está completa. Además, un atacante con acceso para modificar contenido e inventario podría recalcular ambos; por eso puede ser útil conservar resúmenes o registros de auditoría en un sistema independiente.

### Una versión no es necesariamente un momento del mundo

`created` señala cuándo se creó la versión del objeto. La descarga pudo hacerse antes, el documento pudo publicarse mucho antes y el hecho investigado pudo ocurrir en otra fecha. Mantén por separado tiempo de observación, tiempo declarado por la fuente, tiempo del evento y tiempo de preservación.

### El historial puede ser completo y la colección, sesgada

OCFL conserva lo que se ingresa. No revela automáticamente páginas que faltaron, filtros defectuosos ni exclusiones no documentadas. Registra el universo esperado, criterios de selección, errores de adquisición y cobertura conocida.

### La deduplicación tiene fronteras

El direccionamiento por contenido puede evitar duplicados dentro de un objeto, pero la especificación no promete deduplicación global entre objetos. Tampoco comprime por arte de magia formatos voluminosos. Modelado, tamaño de objetos y costes de almacenamiento requieren medición propia.

### No es una interfaz de publicación

OCFL es una disposición de preservación, no un buscador, una base de datos analítica ni una web pública. Construye índices y servicios de acceso como capas reemplazables; no hagas que sus datos sean imprescindibles para comprender lo preservado.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja solo con una finalidad legítima y un alcance documentado.
- Minimiza datos antes del ingreso; no confíes en poder borrarlos sin rastro después.
- Separa archivo restringido, conjunto de análisis y producto publicable.
- Usa identificadores internos que no expongan nombres sensibles en rutas físicas.
- Limita permisos de lectura y escritura; valida desde cuentas sin privilegios excesivos.
- No almacenes secretos en inventarios, mensajes de versión, logs ni nombres de fichero.
- Documenta retención, revisión de acceso y borrado autorizado, incluido el tratamiento de copias.
- Registra inferencias como inferencias; no las mezcles con observaciones primarias.
- Prueba migraciones y restauraciones con datos sintéticos antes de tocar una colección real.

## Lista de control antes de preservar una colección

- [ ] La unidad de objeto y el disparador de versión están definidos.
- [ ] Originales, derivados, código, notas y resultados están diferenciados.
- [ ] Procedencia, consulta, UTC, licencia y método acompañan cada adquisición.
- [ ] Los datos innecesarios y secretos han sido excluidos.
- [ ] La implementación declara compatibilidad con la versión OCFL elegida.
- [ ] La escritura se realiza mediante una zona de trabajo y un proceso controlado.
- [ ] El objeto pasa una validación estructural y criptográfica completa.
- [ ] Una versión antigua se puede reconstruir en un destino limpio.
- [ ] Los informes de validación quedan registrados con herramienta y UTC.
- [ ] Existen copias separadas y una prueba de recuperación periódica.
- [ ] La interpretación factual se corrobora fuera del mecanismo de preservación.

## Alternativas y siguientes pasos

[BagIt](/bagit-osint-transferencia-evidencia) resulta más sencillo para transferir una carga y comprobarla al recibirla. [RO-Crate](/ro-crate-osint-paquete-evidencia) describe con más riqueza entidades, relaciones y contexto. Git y DVC pueden encajar mejor en código y canalizaciones de datos; WARC conserva respuestas web. Estas herramientas resuelven capas distintas y pueden combinarse si existe una necesidad explícita.

No adoptes OCFL para una carpeta efímera de tres ficheros. Empieza cuando necesitas conservar estados sucesivos, validar a lo largo del tiempo y poder abandonar la aplicación actual sin perder la inteligibilidad del archivo.

El takeaway accionable: crea un objeto de prueba con datos sintéticos, añade una segunda versión que renombre un fichero y modifique otro, valida ambas y reconstruye `v1` en una carpeta limpia. Si no puedes explicar cada ruta lógica y cada bloque del inventario, todavía no estás listo para preservar evidencia real.

Como siguiente tema, convendría comparar OCFL, BagIt y RO-Crate sobre un mismo expediente ficticio: preservación versionada, transferencia íntegra y descripción semántica son necesidades complementarias, no sinónimos.

## Fuentes consultadas

- [Oxford Common File Layout Specification v1.1](https://ocfl.io/1.1/spec/)
- [OCFL Implementation Notes v1.1](https://ocfl.io/1.1/implementation-notes/)
- [OCFL Specification v1.1 Change Log](https://ocfl.io/1.1/spec/change-log.html)
- [OCFL Validation Codes v1.1](https://ocfl.io/1.1/spec/validation-codes.html)
- [Repositorio oficial de la especificación OCFL](https://github.com/OCFL/spec)
- [OCFL Test Fixtures](https://github.com/OCFL/fixtures)
