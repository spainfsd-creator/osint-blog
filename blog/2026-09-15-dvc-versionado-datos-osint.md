---
title: "DVC en OSINT: versionar datos sin confundir un hash con la verdad"
slug: /dvc-versionado-datos-osint
authors: [osint-writter]
tags: [osint, data, methodology, verification, tooling, privacy]
date: 2026-09-15
image: /img/blog/2026-09-15-dvc-versionado-datos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando versiones fechadas de datos públicos y sus transformaciones reproducibles](/img/blog/2026-09-15-dvc-versionado-datos-osint.png)

*Imagen generada mediante inteligencia artificial.*

El lunes descargas 40.000 filas de un portal público; el jueves son 39.742 y una conclusión importante desaparece. Tu script sigue en Git, pero el CSV original se llamaba `datos_finales_2.csv`, alguien lo sustituyó y nadie sabe qué versión alimentó la tabla publicada. El problema no es calcular otra vez: es demostrar **qué datos entraron, qué transformación se ejecutó y qué artefacto salió**.

[DVC](https://dvc.org/doc/start) permite asociar versiones de ficheros y directorios de datos con revisiones de Git sin guardar necesariamente esos objetos pesados dentro del repositorio. En una investigación OSINT puede conectar fuentes preservadas, código y resultados reproducibles. No certifica la autenticidad de una fuente, no concede permiso para conservar datos y no convierte una coincidencia en un hecho.

<!-- truncate -->

## Qué es DVC y para qué sirve

DVC es una herramienta de código abierto orientada al versionado de datos y a canalizaciones reproducibles. Al ejecutar `dvc add`, el dato queda representado por un pequeño fichero `.dvc` que sí se versiona con Git, mientras el objeto se almacena en una caché y el original se añade a `.gitignore`. La [documentación sobre ficheros `.dvc`](https://dvc.org/doc/user-guide/project-structure/dvc-files) describe campos como la ruta, el tamaño y la suma de comprobación.

La separación es sencilla:

- **Git** conserva código, notas, configuración no secreta y metadatos de DVC;
- la **caché de DVC** conserva objetos direccionados por contenido en el equipo;
- un **remoto de DVC** puede sincronizar esos objetos con almacenamiento externo;
- `dvc.yaml` y `dvc.lock` describen y fijan etapas, dependencias y resultados de una canalización.

La [guía de almacenamiento remoto](https://dvc.org/doc/user-guide/data-management/remote-storage) deja claro que DVC no proporciona el almacén: admite distintos servicios y ubicaciones aportados por el usuario. Esto importa en OSINT. Un remoto no es «la nube» en abstracto, sino un sistema concreto con permisos, retención, cifrado, registros de acceso y jurisdicción que debemos evaluar.

DVC encaja especialmente bien cuando una investigación contiene datos demasiado grandes o cambiantes para Git, pero todavía necesita una relación auditable entre una revisión del análisis y sus entradas. Para unas pocas tablas pequeñas, Git o un archivo WARC bien documentado pueden bastar. Añadir infraestructura sin necesidad también crea deuda.

## Caso de uso legítimo: comparar contratos públicos que cambian

Imaginemos que analizamos adjudicaciones publicadas por tres organismos para comprobar, de forma agregada, cómo evolucionó el gasto en un servicio. Usaremos nombres e identificadores ficticios y solo fuentes oficiales abiertas. No buscamos perfiles personales ni inferimos conductas privadas.

El 15 de septiembre descargamos tres CSV y registramos para cada uno:

- URL exacta y organismo responsable;
- fecha y hora de consulta en UTC;
- parámetros, filtros y paginación aplicados;
- licencia o condiciones de reutilización;
- cabeceras HTTP relevantes y nombre original;
- suma SHA-256 calculada aparte para el manifiesto de adquisición.

Una estructura mínima podría ser:

```text
caso-contratos/
├── data/
│   ├── raw/           # adquisiciones preservadas
│   ├── derived/       # normalizaciones y uniones
│   └── publishable/   # tablas minimizadas para difusión
├── scripts/
├── sources.csv
├── dvc.yaml
├── dvc.lock
└── README.md
```

La carpeta `raw` no se edita. Si el portal corrige una descarga, incorporamos la nueva adquisición como una versión diferente y anotamos el cambio observado. Así podemos volver al conjunto empleado en un informe sin fingir que la versión anterior sigue siendo la vigente.

## Flujo recomendado: del dato vivo al resultado trazable

### 1. Definir alcance, permisos y criterio de descarte

Antes de instalar nada, escribe la pregunta, el periodo, las fuentes autorizadas y los datos que no necesitas. Decide qué identificador permite unir registros y qué coincidencias requerirán revisión. Si una tabla contiene datos personales innecesarios, minimízala antes de enviarla a almacenamiento compartido.

También define la política de conservación. Versionar cada cambio puede chocar con una obligación de borrado o perpetuar información corregida. DVC facilita recuperar objetos; la legitimidad de conservarlos depende del caso, la normativa y los controles del equipo.

### 2. Inicializar DVC sin exponer secretos

La guía oficial propone instalar la herramienta de forma aislada con `uv` o `pipx`. En un repositorio Git nuevo o existente:

```bash
uv tool install dvc
dvc init
git add .dvc .dvcignore
git commit -m "Inicializar versionado de datos"
```

No copies credenciales en `.dvc/config`. La [documentación de configuración](https://dvc.org/doc/user-guide/project-structure/configuration) indica que ese fichero está pensado para Git y no debe contener contraseñas, claves SSH ni información sensible. Las opciones locales y secretos deben quedar fuera del repositorio, por ejemplo mediante configuración `--local` y el mecanismo seguro del proveedor.

### 3. Preservar una adquisición y su manifiesto

Después de descargar de forma respetuosa y comprobar que el fichero corresponde a la respuesta esperada:

```bash
sha256sum data/raw/contratos-2026-09-15.csv >> sources.sha256
dvc add data/raw
git add data/raw.dvc data/.gitignore sources.csv sources.sha256
```

El hash que DVC guarda para gestionar contenido no sustituye el manifiesto de adquisición ni la firma de una fuente. Una suma solo permite detectar si dos secuencias de bytes coinciden. No demuestra quién publicó el fichero, cuándo fue verdadero ni si está completo.

El manifiesto debería enlazar cada objeto con su URL, UTC, licencia y método de obtención. El fichero `.dvc` responde «qué versión de bytes»; las notas de procedencia responden «de dónde salió y en qué contexto».

### 4. Configurar un remoto con mínimo privilegio

Para un laboratorio ficticio, un remoto local permite practicar sin subir nada a terceros:

```bash
mkdir -p ../almacen-dvc-laboratorio
dvc remote add -d laboratorio ../almacen-dvc-laboratorio
dvc push
```

En un equipo real, el remoto podría ser almacenamiento de objetos, SSH u otra opción compatible. Antes de usarlo, verifica:

- cifrado en tránsito y en reposo;
- acceso de mínimo privilegio y autenticación separada;
- retención, copias, borrado y recuperación;
- registros de acceso y respuesta ante incidentes;
- residencia de datos y contrato aplicable;
- aislamiento entre material sensible y publicable.

Un nombre de remoto y una URL pueden compartirse; las credenciales, no. Tampoco asumas que «privado» equivale a autorizado.

### 5. Declarar transformaciones como una canalización

Una investigación reproducible debe separar adquisición, limpieza, análisis y exportación. DVC permite definir etapas en `dvc.yaml`; la [guía de canalizaciones](https://dvc.org/doc/user-guide/pipelines/defining-pipelines) distingue comandos, dependencias y salidas.

```bash
dvc stage add -n normalizar \
  -d scripts/normalizar.py \
  -d data/raw \
  -o data/derived/contratos.csv \
  python scripts/normalizar.py
```

El script debe conservar los valores originales, producir un registro de exclusiones y detenerse cuando fallen supuestos críticos: monedas ausentes, identificadores inválidos, duplicados inesperados o cambios de esquema. Una salida limpia sin controles puede ser perfectamente reproducible y perfectamente errónea.

Añade después una etapa independiente que genere solo material publicable. Esa frontera ayuda a impedir que correos, rutas internas, tokens, coordenadas sensibles o columnas auxiliares terminen en un informe.

### 6. Reproducir y revisar qué cambió

Tras cambiar código o datos:

```bash
dvc status
dvc repro
git diff -- dvc.yaml dvc.lock sources.csv
```

`dvc repro` examina dependencias y salidas para ejecutar las etapas necesarias, según su [referencia oficial](https://dvc.org/doc/command-reference/repro). Aun así, la reproducibilidad depende de más elementos: versión del intérprete, dependencias bloqueadas, configuración regional, zona horaria, servicios externos y aleatoriedad controlada.

Antes de aceptar el resultado, revisa recuentos de filas, exclusiones, uniones y cambios de esquema. Si el total varía, pregunta primero si cambió la fuente, el código, la configuración o la cobertura. DVC ayuda a localizar la diferencia; no la interpreta por ti.

### 7. Publicar en el orden correcto

Comprueba que el remoto recibió los objetos antes de confirmar en Git los metadatos que los referencian:

```bash
dvc push
git add dvc.yaml dvc.lock data/raw.dvc data/.gitignore
git commit -m "Versionar adquisición y canalización"
git push
```

Después prueba la recuperación desde un clon limpio y con una cuenta de permisos equivalentes:

```bash
dvc pull
dvc repro
```

Que funcione en el portátil del autor no basta. Una restauración ensayada revela credenciales implícitas, objetos que nunca se subieron, rutas absolutas y dependencias no declaradas.

## Limitaciones y falsos positivos

### Un hash no autentica una fuente

Dos copias con el mismo hash contienen los mismos bytes bajo el algoritmo usado. Eso no acredita que el portal sea oficial, que el documento no estuviese manipulado antes de adquirirlo o que represente toda la población. Conserva contexto y corrobora afirmaciones relevantes en fuentes independientes.

### Una versión no equivale a una fecha del mundo real

El momento del commit, la hora de descarga y la fecha declarada dentro de un CSV son eventos diferentes. Regístralos por separado y normaliza las zonas horarias. No conviertas el orden de commits en una cronología factual.

### Restaurar datos no restaura todo el entorno

DVC puede devolver las entradas correctas y aun así obtener otro resultado por dependencias, servicios externos, configuración o ejecución no determinista. Bloquea el entorno, conserva pruebas y ejecuta en limpio.

### El remoto puede estar incompleto o indisponible

Un `.dvc` en Git es una referencia, no una copia del objeto. Si nunca se ejecutó `dvc push`, si el remoto se purgó o si perdimos acceso, la revisión histórica puede no recuperarse. Verifica restauraciones y copias según el riesgo.

### La deduplicación no es una política de privacidad

Un dato eliminado del directorio visible puede permanecer en cachés, remotos o revisiones anteriores. Antes de tratar material personal, diseña acceso, retención y borrado. Las tareas de limpieza como `dvc gc` pueden eliminar datos no utilizados y exigen especial cuidado; consulta siempre su [documentación](https://dvc.org/doc/command-reference/gc) y prueba el alcance antes de operar sobre un remoto.

## Buenas prácticas de OPSEC, ética y privacidad

- Recopila solo lo necesario para una finalidad legítima y documentada.
- Separa datos originales, derivados y publicables con permisos distintos.
- Mantén secretos en configuración local o gestores de credenciales, nunca en Git.
- Usa cuentas de servicio con mínimo privilegio y rota sus credenciales.
- Registra UTC, URL, método, licencia y hash de cada adquisición.
- Evita consultas agresivas; respeta límites, condiciones de uso y restricciones técnicas.
- No publiques cachés, remotos ni manifiestos que revelen rutas o datos sensibles.
- Prueba el borrado y la restauración, no solo la subida.
- Trata las coincidencias aproximadas como candidatas, no como identidades.
- Explica qué datos faltan y qué no puede demostrar el análisis.

## Lista de control antes de citar un resultado

- [ ] La pregunta, el alcance y la base para tratar los datos están documentados.
- [ ] Cada adquisición tiene procedencia, UTC, filtros, licencia y hash.
- [ ] Los originales son inmutables y están separados de los derivados.
- [ ] Los secretos no aparecen en `.dvc/config`, scripts, logs ni historial de Git.
- [ ] El remoto aplica mínimo privilegio, retención y cifrado adecuados.
- [ ] Las dependencias y salidas de cada etapa están declaradas.
- [ ] Los controles de filas, esquema, duplicados y exclusiones son visibles.
- [ ] El flujo se ha reproducido desde un entorno limpio.
- [ ] Se ha comprobado que todos los objetos referenciados existen en el remoto.
- [ ] La conclusión distingue integridad de bytes, autenticidad y veracidad.

## Alternativas y siguientes pasos

DVC no es la única opción. Git puede bastar para datos pequeños y textuales; Git LFS desplaza objetos grandes fuera del historial Git ordinario, aunque no describe por sí solo una canalización; un almacén con versionado nativo puede resolver la retención de objetos; y sistemas como lakeFS se orientan a versionar datos directamente a escala de infraestructura. La elección depende del volumen, el patrón de acceso, los permisos y el coste operativo.

Como complemento, [Jupyter y Jupytext](/jupyter-jupytext-osint-cuadernos-reproducibles) ayudan a explicar el análisis; [Great Expectations](/great-expectations-osint-calidad-datos) formaliza controles; y [Datasette y SQLite](/datasette-sqlite-osint-trazabilidad-consultable) facilita consultar conjuntos publicables. Ninguna pieza sustituye una buena política de procedencia.

## Conclusión: versiona también tus dudas

La utilidad de DVC en OSINT no está en poner otro acrónimo en el repositorio. Está en poder señalar una revisión y responder: estos fueron los bytes, esta fue su procedencia, este código los transformó, estos controles fallaron o pasaron y este resultado salió. Empieza con una sola adquisición pública: crea su manifiesto, añádela a DVC, súbela a un remoto de laboratorio y demuestra que puedes recuperarla desde cero.

El siguiente paso natural será diseñar una prueba de restauración en integración continua que verifique metadatos y datos sintéticos sin llevar fuentes sensibles a ejecutores de terceros.
