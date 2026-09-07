---
title: "VisiData en OSINT: explorar datos tabulares sin perder la procedencia"
slug: /visidata-osint-explorar-datos-tabulares
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-09-07
image: /img/blog/2026-09-07-visidata-osint-datos-tabulares.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista explorando tablas públicas, frecuencias y uniones con etiquetas de procedencia](/img/blog/2026-09-07-visidata-osint-datos-tabulares.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/visidata-osint-explorar-datos-tabulares.m4a)


*Imagen generada mediante inteligencia artificial.*

Un portal de contratación publica tres ficheros: adjudicaciones en CSV, proveedores en JSON y centros de gasto en SQLite. Antes de abrir un cuaderno de Python, ya necesitamos saber si faltan años, si un importe está guardado como texto o si una unión multiplicará filas. **El primer riesgo no es técnico: es empezar a cruzar datos sin entender su forma ni conservar de dónde salió cada registro**.

[`VisiData`](https://www.visidata.org/) ofrece una respuesta muy práctica: una interfaz de terminal para abrir, perfilar, filtrar y combinar datos tabulares de manera interactiva. No sustituye la verificación ni convierte una coincidencia en evidencia. Sirve para inspeccionar el terreno con rapidez y dejar visibles las decisiones que luego deberán reproducirse y justificarse.

<!-- truncate -->

## Qué es VisiData y para qué sirve

VisiData es una herramienta libre y de código abierto, con licencia GPLv3, que representa cada fuente o resultado como una **hoja**. Está pensada para manejarse con el teclado: se abre un fichero, se asignan tipos a las columnas, se crean facetas o tablas de frecuencias, se seleccionan filas y se derivan nuevas hojas sin abandonar la terminal.

Según su [documentación de formatos](https://www.visidata.org/docs/formats/), admite de forma nativa, entre otros, CSV, TSV, JSON y SQLite; otros formatos pueden exigir dependencias adicionales. La [página de versiones](https://www.visidata.org/releases/) identifica `v3.4`, publicada el 30 de junio de 2026, como la entrega más reciente al revisar este artículo el 7 de septiembre de 2026.

En una investigación legítima resulta útil para:

- reconocer columnas, tipos, nulos y valores inesperados antes de automatizar;
- localizar duplicados, categorías raras y distribuciones anómalas;
- comparar varios ficheros públicos sin importarlos primero a una hoja de cálculo;
- comprobar qué claves permitirían una unión y qué filas quedarían fuera;
- preparar una transformación reproducible antes de pasar a SQL, Python o una visualización.

Su ventaja principal no es «hacer magia con datos», sino acortar la distancia entre recibir un dataset y formular preguntas sensatas sobre él.

## Caso de uso legítimo: auditar un conjunto ficticio de contratos

Imaginemos que el municipio ficticio de **Villa Serena** publica:

- `adjudicaciones_2025.csv`, con identificador, fecha, importe y proveedor;
- `proveedores.json`, con identificador fiscal ficticio, razón social y localidad;
- `centros.sqlite`, con códigos de unidad y denominaciones administrativas.

El objetivo es evaluar la calidad del conjunto antes de calcular concentración de adjudicaciones. No buscamos datos personales ni intentamos atribuir conductas a nadie. Queremos contestar preguntas de control:

1. ¿Todos los importes se interpretan como números?
2. ¿Hay identificadores vacíos o repetidos?
3. ¿Las fechas cubren el periodo anunciado?
4. ¿Cuántas adjudicaciones no encuentran proveedor al cruzar las tablas?
5. ¿Una misma clave produce varias correspondencias y, por tanto, infla el resultado?

Podemos empezar con una copia de trabajo:

```bash
vd adjudicaciones_2025.csv proveedores.json centros.sqlite
```

La [guía de uso](https://www.visidata.org/docs/usage/) confirma que `vd fichero.csv` abre una fuente y que también se puede canalizar entrada tabular desde otro comando. Esto no significa que debamos abrir a ciegas cualquier fichero descargado: primero hay que registrar URL, fecha de adquisición, licencia, hash y alcance declarado.

## Flujo recomendado

### 1. Congela originales y crea una ficha de procedencia

Guarda los originales como solo lectura y trabaja sobre copias. Para cada fuente anota:

| Campo | Ejemplo ficticio |
|---|---|
| URL de origen | `https://datos.villaserena.example/adjudicaciones.csv` |
| Descarga | `2026-09-07T08:15:00+02:00` |
| Cobertura declarada | 2025 |
| Formato | CSV UTF-8 |
| Hash | SHA-256 de la descarga |
| Licencia | La indicada por el portal |

El hash demuestra que dos copias son iguales a nivel de bytes; no demuestra que el contenido sea completo ni verdadero. Conserva también la página que describe el dataset, porque el fichero rara vez explica por sí solo filtros, unidades o retrasos de publicación.

### 2. Perfila antes de corregir

Abre cada fuente por separado. Comprueba encabezados, separadores, codificación y número de filas. Después asigna tipos explícitos a fechas, enteros o importes. Una cifra alineada como texto puede ordenar `1000` antes que `200`; una conversión fallida puede revelar símbolos monetarios, separadores decimales mixtos o una nota introducida en la columna equivocada.

Las tablas de frecuencia y los estadísticos descriptivos permiten detectar:

- categorías con variantes ortográficas;
- valores dominantes que podrían ser un código por defecto;
- nulos concentrados en un año o una fuente;
- importes extremos que merecen volver al registro original;
- fechas fuera de la cobertura anunciada.

El [índice de recetas oficial](https://www.visidata.org/docs/) reúne operaciones para frecuencias, tablas dinámicas, estadísticos, selección, búsqueda y columnas derivadas. Úsalas como exploración, no como veredicto.

### 3. Separa observación, transformación e interpretación

No sobrescribas inmediatamente el valor recibido. Mantén, por ejemplo:

- `proveedor_original`: texto exacto de la fuente;
- `proveedor_normalizado`: espacios y mayúsculas homogeneizados;
- `id_fuente`: identificador publicado;
- `decision_union`: aceptada, rechazada o pendiente;
- `nota`: motivo breve y comprobable.

Así puedes corregir `SERVICIOS NORTE, S.L.` y `Servicios Norte SL` para agrupar, sin afirmar que son la misma entidad únicamente por su parecido. La normalización crea candidatos; la identidad requiere una clave estable o corroboración en la fuente competente.

### 4. Cuenta las claves antes de unir

Antes del cruce, calcula la frecuencia del identificador en ambos lados. Si una clave aparece dos veces en adjudicaciones y tres en proveedores, una unión sin control podría producir seis filas. Esa multiplicación no es un hallazgo: es la consecuencia del modelo de datos.

La [documentación oficial sobre uniones](https://www.visidata.org/docs/join/) explica los tipos disponibles, incluidos `inner`, `full`, `diff`, `append` y `concat`. También señala que `append` y `concat` añaden una columna oculta `origin_sheet`, útil para conservar la procedencia de cada fila. En un expediente OSINT conviene hacer visibles esas columnas y registrar:

- hojas participantes;
- columnas marcadas como clave;
- cardinalidad esperada (`1:1`, `1:N` o `N:M`);
- filas sin correspondencia;
- filas adicionales creadas por duplicados;
- tipo de unión y criterio de aceptación.

La hoja `diff` puede servir para revisar ausencias entre fuentes. Pero «no aparece» significa solamente «no se encontró con esta clave, en estas copias y en esta fecha».

### 5. Conserva el registro de comandos

VisiData registra en el **Command Log** las órdenes que modifican hojas guardables. Su [documentación de comandos](https://www.visidata.org/docs/api/commands.html) indica que ese registro puede reproducirse. Es una ayuda valiosa para explicar qué filtros, selecciones o transformaciones se aplicaron.

Aun así, un log no es autosuficiente. Guárdalo junto con:

- la versión de VisiData y las dependencias relevantes;
- los hashes de entrada;
- las opciones de carga;
- las decisiones manuales que no se deducen del comando;
- los resultados exportados y sus hashes;
- una nota sobre errores o advertencias observados.

Reproducible no equivale a correcto: también se puede repetir perfectamente una decisión equivocada.

### 6. Exporta un derivado, nunca una verdad definitiva

Guarda el resultado con un nombre nuevo y comprueba el recuento de filas, los encabezados y la codificación. La documentación advierte que los cargadores y guardadores varían según el formato, y ofrece una opción `safety_first` que prioriza la sanitización de entrada y salida a costa de rendimiento. No presupongas que todos los formatos preservan tipos, metadatos o columnas ocultas de la misma manera.

Antes de publicar una tabla derivada, elimina campos innecesarios, evalúa el riesgo de reidentificación y documenta las transformaciones. Si el resultado alimentará un informe, conserva una ruta verificable desde cada cifra agregada hasta las filas y fuentes de origen.

## Checklist de verificación

Antes de aceptar un resultado, comprueba:

- [ ] Los originales están intactos y tienen URL, fecha, licencia y hash.
- [ ] Los tipos de columna se han asignado y revisado explícitamente.
- [ ] Los nulos y errores de conversión están contabilizados.
- [ ] Las claves se han perfilado en ambos lados antes de unir.
- [ ] La cardinalidad observada coincide con la esperada.
- [ ] Se han revisado filas sin correspondencia y multiplicaciones.
- [ ] Los nombres normalizados conservan su valor original.
- [ ] Las decisiones manuales tienen motivo y estado de confianza.
- [ ] El registro de comandos y la versión de la herramienta se archivan.
- [ ] Las conclusiones importantes vuelven a fuentes primarias independientes.

## Limitaciones y falsos positivos

### Una interfaz rápida también acelera los errores

Los atajos permiten explorar millones de celdas con agilidad, pero una selección incorrecta o un tipo mal asignado puede propagarse sin que el resultado «parezca» roto. Detente en puntos de control y compara recuentos antes y después.

### El formato condiciona lo que ves

CSV no incorpora un esquema universal: separadores, comillas, saltos de línea y codificación pueden alterar la carga. JSON puede contener estructuras anidadas; SQLite puede reunir varias tablas con relaciones que no son evidentes en una hoja aislada. Consulta siempre la documentación del productor.

### Coincidencia no significa identidad

Dos proveedores con el mismo nombre pueden ser entidades distintas; dos nombres diferentes pueden corresponder a la misma entidad. Una clave también puede cambiar, reutilizarse o contener errores. Marca las coincidencias como hipótesis hasta contrastarlas.

### Una frecuencia no explica una causa

Una categoría muy abundante puede reflejar el diseño del sistema, una política de publicación o un valor por defecto. Un valor raro puede ser un error de captura. La estadística descriptiva señala dónde mirar; no sustituye el contexto.

### El log necesita su entorno

La reproducción puede depender de la versión, plugins, configuración, ruta y contenido exacto de las fuentes. Archiva el entorno suficiente para que otra persona pueda repetir el proceso sin adivinar.

## OPSEC, ética y privacidad

VisiData trabaja en local, lo que reduce la necesidad de enviar datasets a servicios externos, pero no elimina el riesgo. Un fichero público puede combinarse con otros hasta revelar información que no era obvia por separado.

- Aplica minimización: importa y conserva solo los campos necesarios.
- Separa identificadores directos de las tablas de análisis cuando sea posible.
- Evita introducir datos sensibles en capturas, terminales compartidos o historiales de shell.
- Revisa fórmulas o contenido peligroso antes de abrir exportaciones en otras aplicaciones.
- No conviertas una anomalía estadística en una acusación pública.
- Respeta licencias, condiciones de acceso, normativa de protección de datos y expectativas razonables de privacidad.
- Si investigas una organización real, comunica hallazgos proporcionadamente y ofrece evidencia verificable, no volcados masivos.

El principio operativo es sencillo: **que una fuente sea abierta no significa que todo tratamiento o toda publicación sean responsables**.

## Alternativas y siguientes pasos

- **OpenRefine** ofrece una interfaz visual potente para limpieza, clustering y reconciliación de entidades.
- **SQLite** y **DuckDB** permiten consultas declarativas y repetibles sobre conjuntos mayores.
- **Datasette** facilita explorar y publicar bases SQLite con una interfaz web controlada.
- **csvkit** resulta cómodo para inspecciones y transformaciones encadenadas desde shell.
- **pandas** o **Polars** encajan cuando el flujo necesita automatización, pruebas y lógica más compleja.

No son sustitutos absolutos. VisiData funciona muy bien como banco de inspección rápida; SQL o código suelen ser mejores para una canalización estable; OpenRefine destaca cuando hay que revisar visualmente muchas decisiones de limpieza.

## Conclusión

El takeaway accionable es este: abre el próximo dataset con una **hoja de control de procedencia** y no ejecutes ninguna unión hasta haber contado sus claves en ambos lados. Con VisiData puedes descubrir en minutos los nulos, tipos y duplicados que arruinarían horas de análisis, pero el valor probatorio seguirá dependiendo de cómo documentes, corrobores y limites tus conclusiones.

Como siguiente tema, merece la pena estudiar cómo diseñar pruebas de calidad de datos con Great Expectations o Pandera para convertir estas comprobaciones exploratorias en controles repetibles.

## Fuentes consultadas

- [VisiData: sitio oficial](https://www.visidata.org/)
- [VisiData: instalación](https://www.visidata.org/install/)
- [VisiData: versiones](https://www.visidata.org/releases/)
- [VisiData: documentación y recetas](https://www.visidata.org/docs/)
- [VisiData: formatos compatibles](https://www.visidata.org/docs/formats/)
- [VisiData: combinación de datasets](https://www.visidata.org/docs/join/)
- [VisiData: registro y API de comandos](https://www.visidata.org/docs/api/commands.html)
