---
title: "DuckDB en OSINT: consultar datasets públicos en local sin confundir velocidad con evidencia"
slug: /duckdb-osint-datasets-publicos-local
authors: [osint-writter]
tags: [osint, tooling, data, investigation, verification, privacy]
date: 2026-11-09
image: /img/blog/2026-11-09-duckdb-osint-datasets-publicos.png
aiDisclosure: generated
humanReviewed: false
---

Un portal publica varios años de contratos en CSV, otro ofrece el catálogo de proveedores en Parquet y una tercera fuente conserva las resoluciones en PDF. La pregunta parece sencilla: ¿qué adjudicaciones necesitan revisión? El problema empieza cuando una fecha ambigua cambia de mes a día, un identificador pierde sus ceros iniciales o una unión multiplica filas sin avisar. **Consultar millones de registros con rapidez no sirve de mucho si no podemos explicar qué fichero, qué esquema y qué decisión produjeron cada resultado.**

![Analista consultando datasets públicos en local mediante un flujo visual de procedencia y validación](/img/blog/2026-11-09-duckdb-osint-datasets-publicos.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo presenta un uso responsable de **DuckDB** para analizar datos abiertos o material obtenido con autorización. El caso es ficticio y los nombres, importes e identificadores no corresponden a personas ni entidades reales. El objetivo no es perfilar individuos, sino construir un flujo local, reproducible y revisable que separe el dato bruto de la interpretación.

## Qué es DuckDB y para qué sirve en OSINT

[DuckDB](https://duckdb.org/docs/stable/) es un motor de base de datos analítica embebido. Puede ejecutarse desde su cliente de línea de comandos o integrarse en lenguajes como Python y R, sin desplegar un servidor separado para cada investigación. Su SQL permite consultar directamente ficheros como CSV, JSON y Parquet, además de tablas guardadas en una base DuckDB.

Para una investigación OSINT, esa combinación resulta útil cuando necesitamos:

- perfilar un conjunto público antes de decidir cómo limpiarlo;
- cruzar ediciones mensuales o anuales sin importarlas a una plataforma remota;
- conservar consultas como artefactos revisables;
- trabajar con columnas concretas de ficheros Parquet grandes;
- producir tablas derivadas manteniendo el vínculo con los originales;
- limitar la exposición de datos que no deben salir del entorno de trabajo.

DuckDB no es una herramienta de atribución ni un verificador de hechos. Una consulta puede ejecutarse perfectamente sobre datos incompletos, una columna mal interpretada o dos entidades unidas por una clave defectuosa. Su valor está en hacer el análisis tabular más manejable; la calidad de la conclusión sigue dependiendo de la procedencia, la semántica y la corroboración.

### Leer sin importar no significa leer sin supuestos

La [documentación del lector CSV](https://duckdb.org/docs/stable/data/csv/overview) explica que DuckDB puede detectar delimitador, cabecera y tipos mediante un *sniffer*. Es una ayuda de exploración, no un contrato de datos. El detector trabaja sobre una muestra por defecto y algunas representaciones son ambiguas: `01-02-2026` puede significar 1 de febrero o 2 de enero; `001234` puede ser un identificador textual, no el número `1234`.

En un análisis publicable conviene explorar primero y declarar después los tipos, formatos y valores nulos relevantes. La inferencia automática reduce fricción; no documenta la intención del productor.

Parquet sí contiene esquema y metadatos, pero tampoco certifica el significado ni la veracidad de sus columnas. DuckDB puede aplicar **proyección** y **filtros** al lector Parquet para evitar leer datos innecesarios, según su [documentación oficial](https://duckdb.org/docs/stable/data/parquet/overview). Esa optimización mejora el rendimiento; no demuestra que el filtro responda a la pregunta de investigación.

## Caso de uso legítimo: revisar contratación pública ficticia

La organización ficticia **Observatorio del Estuario** quiere revisar contratos de mantenimiento publicados por una administración imaginaria. Ha descargado dos recursos públicos:

- `contratos_2025.csv`, con expedientes, fechas, adjudicatarios e importes;
- `proveedores.parquet`, con identificadores normalizados y categorías declaradas.

La pregunta no es «¿quién parece sospechoso?», sino una mucho más estrecha y verificable:

> ¿Qué expedientes superan el umbral interno de revisión, aparecen divididos en varias líneas próximas y pueden vincularse de forma inequívoca al mismo proveedor?

Antes de consultar, el equipo crea un manifiesto de adquisición:

| Campo | Ejemplo ficticio | Finalidad |
| --- | --- | --- |
| URL de origen | `https://datos.ejemplo/contratos_2025.csv` | volver a la publicación primaria |
| fecha y hora | `2026-11-09T09:00:00+01:00` | fijar la observación |
| estado HTTP | `200` | documentar la descarga |
| tipo y tamaño | `text/csv`, tamaño observado | detectar sustituciones evidentes |
| hash SHA-256 | valor calculado localmente | identificar los bytes analizados |
| licencia y notas | condiciones del portal | delimitar reutilización |

La consulta trabaja sobre una copia de solo lectura. Los nombres de proveedor no se convierten en acusaciones y cualquier coincidencia se contrasta con el expediente primario.

## Flujo recomendado paso a paso

### 1. Fija originales y contexto de adquisición

Descarga cada fichero una sola vez para la ejecución, conserva sus bytes y calcula un hash con una herramienta del sistema. Guarda junto a él la URL, la fecha, las cabeceras relevantes, la licencia y cualquier aviso del portal sobre cobertura o actualización.

No uses una URL viva como única referencia de un resultado que debe poder reproducirse: mañana podría servir otros bytes bajo el mismo nombre. Si consultas un recurso remoto directamente, registra también qué versión observaste y considera guardar una copia permitida por su licencia.

Mantén tres zonas separadas:

```text
raw/       originales inmutables y manifiestos
work/      base DuckDB, vistas y resultados provisionales
publish/   tablas minimizadas y notas aptas para compartir
```

Esta separación evita que una exportación corregida sobrescriba el material de partida.

### 2. Inspecciona el esquema antes de calcular

Para un CSV, comienza tratando como texto las columnas cuyo significado pueda perderse:

```sql
DESCRIBE
SELECT *
FROM read_csv(
  'raw/contratos_2025.csv',
  all_varchar = true,
  header = true,
  strict_mode = true
);
```

`all_varchar = true` no es obligatorio, pero resulta prudente durante el perfilado de identificadores, códigos postales o importes con formatos regionales. Después se pueden crear conversiones explícitas y separar los rechazos.

Para Parquet, DuckDB ofrece funciones que exponen esquema y metadatos. Por ejemplo:

```sql
DESCRIBE SELECT * FROM read_parquet('raw/proveedores.parquet');

SELECT file_name, num_rows, num_row_groups, format_version
FROM parquet_file_metadata('raw/proveedores.parquet');
```

La [referencia de metadatos Parquet](https://duckdb.org/docs/stable/data/parquet/metadata) permite inspeccionar filas, grupos, esquema y estadísticas. Trátalos como metadatos declarados dentro del fichero, no como una firma de autenticidad.

### 3. Convierte con reglas visibles y conserva rechazos

En vez de ocultar problemas con conversiones permisivas, produce una vista normalizada y otra de incidencias:

```sql
CREATE OR REPLACE VIEW contratos_normalizados AS
SELECT
  expediente,
  proveedor_id,
  try_strptime(fecha_adjudicacion, '%d/%m/%Y')::DATE AS fecha,
  try_cast(replace(importe_eur, ',', '.') AS DECIMAL(18,2)) AS importe_eur,
  fuente_url
FROM read_csv(
  'raw/contratos_2025.csv',
  all_varchar = true,
  header = true,
  strict_mode = true
);

CREATE OR REPLACE VIEW conversiones_rechazadas AS
SELECT *
FROM contratos_normalizados
WHERE fecha IS NULL OR importe_eur IS NULL;
```

El ejemplo supone un formato ficticio y simplificado. En datos reales hay que estudiar separadores de miles, moneda, valores especiales y zonas horarias. Un `NULL` producido por `try_cast` debe quedar visible: no es un cero ni permiso para excluir silenciosamente la fila.

La opción `ignore_errors` puede parecer cómoda, pero saltarse líneas sin un inventario de rechazos rompe la contabilidad. Si una fuente contiene errores estructurales, corrige el contrato de lectura o utiliza el mecanismo de almacenamiento de rechazos con límites y revisión explícitos.

### 4. Define claves y cardinalidades antes de unir

Una unión por nombre normalizado puede fusionar homónimos. Una unión por identificador puede fallar si una fuente mezcla tipos, jurisdicciones o versiones. Antes de hacer el `JOIN`, mide:

- nulos y duplicados en cada clave;
- unicidad esperada en cada lado;
- cobertura de coincidencias;
- filas sin pareja;
- multiplicación de registros tras la unión.

```sql
WITH antes AS (
  SELECT count(*) AS filas
  FROM contratos_normalizados
),
unidos AS (
  SELECT c.*, p.categoria
  FROM contratos_normalizados AS c
  LEFT JOIN read_parquet('raw/proveedores.parquet') AS p
    ON c.proveedor_id = p.proveedor_id
)
SELECT
  (SELECT filas FROM antes) AS filas_antes,
  count(*) AS filas_despues,
  count(*) FILTER (WHERE categoria IS NULL) AS sin_correspondencia
FROM unidos;
```

Si `filas_despues` aumenta, no lo llames «más cobertura» hasta explicar la cardinalidad. Puede haber varias versiones de un proveedor, claves repetidas o un error de modelado.

### 5. Formula señales, no veredictos

La regla de revisión debe ser reproducible y modesta. Por ejemplo, agrupar expedientes del mismo proveedor en una ventana definida puede localizar candidatos para comprobación documental. No demuestra fraccionamiento deliberado, conflicto de interés ni delito.

Registra para cada fila candidata:

- los identificadores de los registros de origen;
- la consulta SQL y su versión;
- el hash de cada fichero leído;
- el criterio exacto y sus parámetros;
- las exclusiones y conversiones fallidas;
- la evidencia primaria que confirma o contradice la señal.

El producto publicable debería decir «cumple el criterio de revisión X» en vez de «es irregular» cuando todavía no existe evidencia suficiente.

### 6. Haz la salida determinista

SQL no garantiza un orden útil si no se declara. Añade `ORDER BY` a las exportaciones, fija redondeos y zonas horarias, y evita depender de la posición física de las filas.

```sql
COPY (
  SELECT expediente, proveedor_id, fecha, importe_eur
  FROM contratos_normalizados
  WHERE importe_eur >= 50000
  ORDER BY fecha, expediente
) TO 'publish/candidatos_revision.parquet'
  (FORMAT PARQUET, COMPRESSION ZSTD);
```

Guarda la consulta en control de versiones y acompaña la salida con un manifiesto nuevo. El hash del resultado identifica esa exportación, pero no prueba que la consulta sea conceptualmente correcta.

### 7. Compara totales y casos de control

Antes de publicar, reconcilia como mínimo:

- filas y claves distintas por fichero;
- sumas por periodo y moneda;
- nulos, duplicados y rechazos;
- coincidencias y no coincidencias de cada unión;
- cambios frente a una ejecución anterior comparable;
- casos sintéticos positivos y negativos.

Un caso positivo comprueba que el pipeline detecta una condición diseñada para ser visible. Uno negativo comprueba que no marca una condición cercana pero no equivalente. Ambos prueban comportamiento técnico, no la verdad completa del mundo real.

## Rendimiento sin perder el control

DuckDB puede consultar Parquet leyendo solo las columnas necesarias y empujando filtros hacia el escaneo. También puede acceder a recursos HTTP/S3 mediante la extensión `httpfs`, tal como documenta la [guía de ficheros remotos](https://duckdb.org/docs/stable/core_extensions/httpfs/overview). En OSINT conviene usar estas capacidades con límites:

- prefiere consultas acotadas y respeta condiciones de uso y capacidad del proveedor;
- no presupongas que una URL remota es inmutable;
- evita incluir credenciales en scripts, historial de terminal o resultados;
- registra las extensiones habilitadas y su procedencia;
- usa `EXPLAIN` y `EXPLAIN ANALYZE` para entender planes y cardinalidades, no como evidencia factual.

Los trabajos mayores que la memoria pueden usar disco temporal. La [documentación de ajuste](https://duckdb.org/docs/stable/guides/performance/how_to_tune_workloads) explica el *spilling* y sus límites. En un equipo de investigación compartido, fija de manera consciente memoria, hilos, directorio temporal y tamaño máximo; un fallo por falta de recursos es preferible a llenar el disco que guarda la evidencia.

## Limitaciones y falsos positivos

### Inferencia de tipos equivocada

Una muestra puede no contener el valor que revela que la columna era texto. Una fecha ambigua puede interpretarse sin error técnico. Declara tipos y formatos cuando afectan a la conclusión.

### Ausencias convertidas en ceros

Un campo vacío, un valor no publicado y un importe cero son estados diferentes. Si se fusionan, los agregados parecen completos aunque hayan perdido incertidumbre.

### Uniones que fabrican volumen

Una relación muchos-a-muchos puede multiplicar importes y recuentos. Comprueba cardinalidad y conserva una tabla de no coincidencias y ambigüedades.

### Datos actualizados bajo la misma URL

Repetir la misma consulta contra una URL no garantiza repetir el análisis. Los bytes, el esquema o la cobertura temporal pueden haber cambiado.

### Optimización confundida con validación

Que DuckDB lea solo dos columnas y descarte grupos de filas correctamente es una propiedad del plan. No valida la definición de esas columnas ni la política que produjo los registros.

### SQL correcto sobre una pregunta incorrecta

Un umbral arbitrario o una ventana temporal mal justificada puede producir una lista precisa e irrelevante. La revisión metodológica debe preceder a la optimización.

## Buenas prácticas de OPSEC, ética y privacidad

- Analiza únicamente datos públicos o material para el que exista autorización y una finalidad legítima.
- Minimiza columnas desde el principio; no copies nombres, contactos o identificadores personales si una clave técnica basta.
- Trabaja sobre copias y ejecuta DuckDB con una cuenta sin privilegios, nunca como `root`.
- No ejecutes SQL recibido de terceros. La [política de seguridad de DuckDB](https://duckdb.org/security) recuerda que SQL puede leer y escribir ficheros, acceder a red, cargar extensiones y consumir recursos.
- Aísla ficheros no confiables. El modelo de seguridad del proyecto asume que los ficheros de datos proceden de un escritor confiable; un archivo manipulado debe abrirse en un entorno desechable y limitado, no junto al expediente principal.
- Revisa las extensiones antes de instalarlas: se ejecutan dentro del proceso anfitrión con sus privilegios.
- Separa credenciales, originales, base de trabajo y exportaciones publicables.
- Cifra los soportes cuando el conjunto contenga información sensible y elimina temporales conforme a la política del caso.
- Evita rankings de personas y atribuciones de intención basadas solo en patrones estadísticos.
- Corrige públicamente los derivados si cambia una fuente o se descubre un error de esquema, unión o interpretación.

## Checklist operativo

- [ ] La pregunta y el criterio de revisión están escritos antes de consultar.
- [ ] Cada fichero tiene URL, fecha, licencia, tamaño y hash.
- [ ] Los originales permanecen separados y sin sobrescritura.
- [ ] Tipos, fechas, nulos, moneda y codificación están declarados.
- [ ] Las conversiones fallidas y líneas rechazadas son contables.
- [ ] Las claves y cardinalidades se han medido antes del `JOIN`.
- [ ] Totales, duplicados y no coincidencias se reconcilian.
- [ ] Las consultas y parámetros están versionados.
- [ ] Las salidas usan orden explícito y manifiesto propio.
- [ ] Hay controles positivos, negativos y revisión de muestras.
- [ ] Cada señal vuelve a documentos o registros primarios.
- [ ] Recursos, temporales, red y extensiones están limitados.
- [ ] La publicación minimiza datos personales y expresa incertidumbre.

## Alternativas y siguientes pasos

SQLite y Datasette encajan bien cuando se necesita una base pequeña, durable y consultable o una interfaz de publicación. OpenRefine facilita la limpieza exploratoria y la reconciliación con revisión humana. Polars o pandas son útiles cuando la transformación se expresa mejor mediante código. Un almacén de datos gestionado puede ser apropiado para equipos grandes, controles de acceso centralizados y cargas continuas, a cambio de mayor complejidad y exposición potencial.

DuckDB ocupa un espacio especialmente cómodo entre la hoja de cálculo y la infraestructura analítica: consultas SQL locales, lectura directa de formatos columnares y un artefacto fácil de versionar alrededor de los datos, aunque la base binaria no sustituya a los scripts y manifiestos legibles.

El takeaway práctico es este: **usa DuckDB para reducir el coste de preguntar, no para rebajar el estándar de prueba**. Fija los originales, declara el esquema, mide cada unión, conserva rechazos y obliga a que toda señal regrese a una fuente primaria. Como siguiente tema, sería útil estudiar particionado y publicación de extractos minimizados: cómo compartir una tabla verificable sin entregar todo el corpus ni romper su procedencia.

## Fuentes oficiales consultadas

- [DuckDB: documentación estable](https://duckdb.org/docs/stable/)
- [DuckDB: importación y opciones del lector CSV](https://duckdb.org/docs/stable/data/csv/overview)
- [DuckDB: lectura de ficheros Parquet](https://duckdb.org/docs/stable/data/parquet/overview)
- [DuckDB: consulta de metadatos Parquet](https://duckdb.org/docs/stable/data/parquet/metadata)
- [DuckDB: acceso a ficheros remotos con `httpfs`](https://duckdb.org/docs/stable/core_extensions/httpfs/overview)
- [DuckDB: ajuste de cargas y procesamiento mayor que memoria](https://duckdb.org/docs/stable/guides/performance/how_to_tune_workloads)
- [DuckDB: modelo de seguridad](https://duckdb.org/security)
