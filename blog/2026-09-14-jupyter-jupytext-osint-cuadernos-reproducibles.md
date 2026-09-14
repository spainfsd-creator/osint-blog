---
title: "Jupyter y Jupytext en OSINT: cuadernos reproducibles sin convertir el análisis en una caja negra"
slug: /jupyter-jupytext-osint-cuadernos-reproducibles
authors: [osint-writter]
tags: [osint, methodology, data, verification, tooling, privacy]
date: 2026-09-14
image: /img/blog/2026-09-14-jupyter-jupytext-osint-cuadernos-reproducibles.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista documentando fuentes, transformaciones y controles de un cuaderno reproducible](/img/blog/2026-09-14-jupyter-jupytext-osint-cuadernos-reproducibles.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/jupyter-jupytext-osint-cuadernos-reproducibles.m4a)


*Imagen generada mediante inteligencia artificial.*

Tres hojas de cálculo públicas parecen demostrar que una empresa ganó contratos por 8,4 millones de euros. El total encaja, el gráfico impresiona y la conclusión cabe en un titular. Dos semanas después, otra persona intenta repetir el cálculo y obtiene 6,1 millones: una tabla se había actualizado, dos identificadores se trataron como empresas distintas y una celda del análisis se ejecutó fuera de orden. El problema no era la falta de datos; era la falta de **procedencia, estado y pasos repetibles**.

[Jupyter](https://docs.jupyter.org/en/stable/what_is_jupyter.html) permite combinar explicación, código y resultados en un cuaderno computacional. [Jupytext](https://jupytext.readthedocs.io/en/latest/paired-notebooks.html) puede emparejar ese cuaderno con una representación de texto más fácil de revisar en Git. Bien usados, ambos ayudan a transformar una exploración OSINT en un análisis auditable. Mal usados, producen una caja negra vistosa que conserva datos sensibles, depende de variables invisibles y solo funciona en el ordenador de su autor.

<!-- truncate -->

## Qué son y para qué sirven

Un fichero `.ipynb` no es una grabación completa de la investigación. Es un documento JSON que reúne celdas, metadatos, código, texto y, cuando se guardan, salidas y contadores de ejecución. La [especificación de nbformat](https://nbformat.readthedocs.io/en/latest/format_description.html) describe esa estructura. El kernel mantiene variables en memoria durante la sesión, de modo que una celda puede depender de otra ejecutada antes aunque aparezca después en pantalla.

Esa interactividad es magnífica para explorar datos y peligrosa para documentar conclusiones. Un cuaderno puede mostrar un resultado correcto que ya no se obtiene al reiniciarlo. También puede ocultar una decisión importante en una celda antigua, mezclar entradas originales con datos corregidos a mano o incrustar en las salidas más información de la que pretendíamos publicar.

En un flujo OSINT legítimo, un cuaderno resulta especialmente útil para:

- importar tablas y registros públicos sin alterar los originales;
- normalizar fechas, nombres o identificadores de forma explícita;
- calcular agregados y detectar valores atípicos;
- producir tablas de control y visualizaciones;
- enlazar cada resultado con su fuente y transformación;
- permitir que otra persona repita el proceso en un entorno controlado.

Jupytext añade una pieza práctica: conserva las entradas del cuaderno como Markdown o como un script con separadores de celdas. Su documentación explica que los cuadernos emparejados actualizan tanto el `.ipynb` como la representación de texto al guardar. El texto genera diferencias mucho más legibles en control de versiones; el `.ipynb` mantiene la experiencia interactiva y, si se decide conservarlas, las salidas.

## Caso de uso legítimo: revisar adjudicaciones públicas

Imaginemos una investigación ficticia sobre `Servicios Ejemplo Norte, S. L.`. El objetivo no es perfilar a sus empleados ni buscar información privada, sino comprobar cuánto dinero público figura adjudicado a esa entidad en tres portales oficiales.

Disponemos de:

- tres CSV descargados de portales públicos;
- las URL de origen y la hora de consulta en UTC;
- el hash SHA-256 de cada descarga;
- un diccionario que relaciona los nombres de columna de cada portal;
- un identificador fiscal ficticio, `B00000000`, para evitar unir empresas solo porque sus nombres se parecen.

La carpeta de trabajo podría separar claramente lo recibido, lo derivado y lo publicable:

```text
caso-adjudicaciones/
├── data/
│   ├── raw/                 # originales, solo lectura
│   └── derived/             # tablas generadas por el cuaderno
├── notebooks/
│   ├── 01-normalizacion.ipynb
│   └── 01-normalizacion.py  # pareja Jupytext revisable
├── reports/
├── sources.csv              # URL, UTC, hash, licencia y notas
├── requirements.lock
└── README.md
```

El cuaderno no debería limitarse a mostrar el total final. Debe enseñar cuántas filas entraron por fuente, qué registros se descartaron y por qué, cómo se trataron las monedas y qué coincidencias requirieron revisión manual. Una tabla de control como esta vale más que un gráfico elegante:

| Control | Resultado ficticio | Decisión |
|---|---:|---|
| Filas descargadas | 1.248 | Conservar recuento por fuente |
| Filas con identificador exacto | 37 | Incluir |
| Coincidencias solo por nombre | 4 | Revisar, no sumar automáticamente |
| Importes sin moneda explícita | 2 | Excluir hasta verificar |
| Duplicados entre portales | 6 | Resolver por expediente y órgano |

Así, si el total cambia, sabremos si cambió la fuente, la regla de normalización o el conjunto de registros aceptados.

## Flujo recomendado: del original al resultado repetible

### 1. Definir la pregunta antes de programar

Escribe en la primera celda qué quieres comprobar, qué queda fuera y qué criterio refutaría tu hipótesis. Por ejemplo: «sumar importes adjudicados a un identificador fiscal concreto entre dos fechas; no atribuir sociedades por similitud de nombre». Esto evita que una exploración abierta termine justificando retrospectivamente la primera correlación llamativa.

### 2. Preservar fuentes y procedencia

Descarga únicamente datos que estés autorizado a consultar. Conserva los originales sin editarlos y registra, como mínimo:

- URL exacta y organismo responsable;
- fecha y hora de consulta en UTC;
- nombre y tamaño del fichero;
- hash criptográfico;
- licencia o condiciones de reutilización;
- filtros aplicados por el portal;
- observaciones sobre paginación, cobertura y campos ausentes.

Un hash demuestra que dos copias contienen los mismos bytes; **no demuestra que la fuente sea auténtica ni que sus datos sean correctos**. La procedencia necesita contexto y corroboración.

### 3. Aislar el entorno

Trabaja en un entorno virtual o contenedor separado y registra las dependencias realmente utilizadas. Una instalación inicial de laboratorio puede ser tan sencilla como:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install jupyterlab jupytext nbconvert pandas
```

Después fija las dependencias con el mecanismo adoptado por tu equipo y conserva el fichero de bloqueo. No presentes un listado sin versiones como garantía de reproducibilidad: es solo el punto de partida.

### 4. Emparejar el cuaderno con texto

Jupytext permite, por ejemplo, mantener un `.ipynb` junto a un script en formato `percent`, donde cada celda queda delimitada de forma visible:

```bash
jupytext --set-formats ipynb,py:percent notebooks/01-normalizacion.ipynb
```

Antes de confirmar cambios, sincroniza las representaciones y revisa el diff:

```bash
jupytext --sync notebooks/01-normalizacion.ipynb
git diff -- notebooks/01-normalizacion.py
```

El objetivo no es añadir una herramienta por moda, sino hacer visibles las reglas. La documentación de [cuadernos emparejados](https://jupytext.readthedocs.io/en/latest/paired-notebooks.html) advierte además de los conflictos si dos editores guardan simultáneamente: conviene guardar, recargar y reconciliar con cuidado.

### 5. Hacer explícitas las entradas y salidas

Una celda no debería depender de una ruta personal como `/home/alicia/Descargas/final_ahora_si.csv`, de una clave pegada en el código ni de una variable creada manualmente horas antes. Usa rutas relativas, configuración separada y secretos fuera del repositorio.

Cada transformación debe leer una entrada declarada y producir una salida definida. Resulta útil incluir aserciones que detengan el análisis cuando cambian supuestos esenciales:

```python
assert contratos["moneda"].notna().all(), "Hay importes sin moneda"
assert contratos["expediente"].is_unique, "Existen expedientes duplicados"
assert set(contratos["fuente"]) == {"portal_a", "portal_b", "portal_c"}
```

Las aserciones no validan la verdad externa de los datos, pero evitan que una anomalía silenciosa atraviese el flujo.

### 6. Reiniciar y ejecutar de principio a fin

Antes de compartir resultados, reinicia el kernel y ejecuta todas las celdas en orden. Para una comprobación automatizada, [nbconvert](https://nbconvert.readthedocs.io/en/stable/execute_api.html) puede ejecutar el cuaderno y guardar el resultado:

```bash
jupyter nbconvert \
  --to notebook \
  --execute notebooks/01-normalizacion.ipynb \
  --output-dir build/notebooks
```

Ejecuta sobre una copia o escribe en un directorio de construcción: conservar el cuaderno fuente separado del resultado reduce confusiones. Un proceso limpio que falla es información valiosa; revela una dependencia oculta, una fuente desaparecida o un supuesto no documentado.

### 7. Revisar antes de publicar

Haz una revisión específica de privacidad y seguridad. Busca nombres, correos, tokens, cookies, rutas locales, consultas históricas, coordenadas sensibles y datos personales que hayan quedado en salidas o metadatos. La documentación de seguridad de Jupyter recuerda que los cuadernos ejecutan código arbitrario: no ejecutes un cuaderno ajeno sin inspeccionarlo y aislarlo.

Decide de forma consciente qué publicar:

- representación de texto con la lógica revisable;
- entorno o dependencias bloqueadas;
- datos abiertos redistribuibles o un script para obtenerlos;
- manifiesto de fuentes y hashes;
- resultados depurados de información innecesaria;
- README con instrucciones y limitaciones.

## Limitaciones y falsos positivos

### Reproducible no significa verdadero

Diez analistas pueden repetir exactamente una suma construida sobre registros incompletos. La repetibilidad demuestra que el procedimiento produce el mismo resultado bajo ciertas condiciones; la veracidad exige evaluar autoridad, cobertura, actualidad y corroboración de las fuentes.

### El estado oculto puede sobrevivir a la vista

Los contadores de ejecución desordenados son una señal, no una prueba completa. Variables mutadas, archivos temporales, cachés y servicios externos pueden alterar el resultado. La prueba más útil es ejecutar desde un entorno limpio con entradas preservadas.

### Las fuentes vivas cambian

Una API puede corregir datos, paginar de otra manera o retirar registros. Si solo guardamos la URL, quizá sea imposible reconstruir el conjunto visto. Cuando la licencia y la normativa lo permitan, conserva una copia original; en caso contrario, registra el máximo contexto posible y explica la limitación.

### La unión aproximada fabrica relaciones

Normalizar mayúsculas, tildes o formas societarias facilita comparar, pero también puede fusionar entidades distintas. Conserva el valor original, documenta la regla y separa coincidencias exactas, candidatas y rechazadas. Nunca conviertas una similitud de nombre en identidad confirmada.

### Las salidas también filtran información

Aunque el código sea inocuo, una tabla previa, un mensaje de error o los metadatos de una imagen pueden revelar datos personales o rutas internas. Limpiar salidas reduce exposición, pero no sustituye una revisión del fichero y del historial de Git.

## Buenas prácticas de OPSEC, ética y privacidad

- Aplica minimización: recopila y conserva solo lo necesario para la pregunta legítima.
- No subas secretos al cuaderno ni a sus salidas; usa variables de entorno o almacenes de credenciales.
- Separa el repositorio privado de trabajo del paquete público y revisa también el historial.
- Abre cuadernos ajenos como código potencialmente peligroso; inspecciona primero y ejecuta en aislamiento.
- Evita automatizar consultas agresivas: respeta condiciones de uso, límites de tasa y robots cuando corresponda.
- Documenta las intervenciones manuales; no «arregles» una fila sin conservar el valor original y la razón.
- Publica incertidumbre, excepciones y registros excluidos, no solo la cifra final.
- Si aparecen datos personales, evalúa necesidad, proporcionalidad y base jurídica antes de tratarlos o difundirlos.

## Lista de control antes de firmar una conclusión

- [ ] La pregunta, el alcance y el criterio de descarte están escritos.
- [ ] Cada fuente tiene URL, UTC, hash, licencia y notas de cobertura.
- [ ] Los originales están separados y no se modifican.
- [ ] Las dependencias están fijadas en un fichero de entorno.
- [ ] El cuaderno no contiene secretos ni rutas personales.
- [ ] Las reglas de limpieza y unión son visibles en el diff.
- [ ] Las coincidencias aproximadas se revisan por separado.
- [ ] El análisis se ejecuta desde cero sin intervención manual.
- [ ] Los recuentos de control y exclusiones aparecen junto al resultado.
- [ ] Una segunda persona puede seguir el README sin conocer el estado de la sesión original.

## Alternativas y siguientes pasos

Jupyter no es obligatorio. Un script pequeño, una consulta SQL o una canalización declarativa pueden ser más apropiados cuando el proceso ya está estabilizado. [Datasette y SQLite](/datasette-sqlite-osint-trazabilidad-consultable) funcionan bien para publicar y consultar conjuntos tabulares; [OpenRefine](/openrefine-osint-limpieza-datos-reconciliacion-contexto) resulta útil para explorar reconciliaciones con revisión humana; [Great Expectations](/great-expectations-osint-calidad-datos) ayuda a formalizar controles de calidad repetibles.

El patrón sensato suele ser progresivo: explorar en un cuaderno, convertir las transformaciones estables en funciones o scripts, añadir pruebas y conservar el cuaderno como explicación ejecutable. Jupytext sirve de puente, no de sello de calidad.

## Conclusión: que el resultado pueda discutir contigo

Un buen cuaderno OSINT no intenta deslumbrar. Permite localizar la fuente, repetir la transformación, detectar dónde cambia un total y discutir cada decisión sin depender de la memoria del analista. Empieza hoy con una mejora pequeña: reinicia tu último cuaderno, ejecútalo de arriba abajo y anota todo lo que tuviste que corregir a mano. Esa lista es el mapa de tu deuda metodológica.

El siguiente paso natural será automatizar una prueba de reproducción en integración continua sin descargar de nuevo datos personales ni depender de fuentes vivas en cada ejecución.

