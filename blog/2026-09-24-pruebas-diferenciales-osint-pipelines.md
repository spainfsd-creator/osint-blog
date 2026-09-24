---
title: "Pruebas diferenciales en OSINT: comparar pipelines sin confundir acuerdo con verdad"
slug: /pruebas-diferenciales-osint-pipelines
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-24
image: /img/blog/2026-09-24-pruebas-diferenciales-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando dos pipelines independientes sobre fuentes públicas](/img/blog/2026-09-24-pruebas-diferenciales-osint.png)

*Imagen generada mediante inteligencia artificial.*

Dos scripts procesan el mismo lote de contratos públicos. Uno calcula 1.248 expedientes y el otro, 1.251. La diferencia parece pequeña, pero tres filas pueden cambiar una serie temporal, una alerta o una conclusión. ¿Cuál está bien? La respuesta responsable no es elegir el resultado que más nos gusta: es convertir la discrepancia en una pista reproducible y volver a la fuente.

Las **pruebas diferenciales** ejecutan una misma entrada —o entradas equivalentes bajo un contrato— mediante dos implementaciones y comparan sus salidas. En OSINT son útiles para descubrir errores silenciosos en extracción, normalización, uniones y agregados. No demuestran que una salida sea verdadera. Dos pipelines pueden coincidir porque comparten el mismo supuesto equivocado.

<!-- truncate -->

## Qué son las pruebas diferenciales y para qué sirven

William M. McKeeman describió en 1998 una estrategia de prueba basada en alimentar programas comparables con numerosos casos y examinar las diferencias. La idea resuelve parcialmente el **problema del oráculo**: cuando no conocemos de antemano la respuesta correcta, otra implementación puede actuar como referencia provisional.

El patrón básico es sencillo:

```text
misma adquisición fijada
        │
        ├── pipeline A ──> salida A normalizada ──┐
        │                                         ├──> comparación ──> discrepancias
        └── pipeline B ──> salida B normalizada ──┘
```

La independencia importa. Comparar dos funciones que llaman al mismo parser, usan la misma tabla intermedia y copian la misma regla de negocio produce una segunda salida, pero apenas una segunda opinión.

En sistemas de bases de datos, este enfoque tiene precedentes prácticos. La documentación de pruebas de [SQLite](https://www.sqlite.org/testing.html) describe varios arneses desarrollados de forma independiente y pruebas con optimizaciones activadas y desactivadas. El proyecto [SQLancer](https://github.com/sqlancer/sqlancer) implementa distintos oráculos para detectar resultados incoherentes, incluidos enfoques que comparan consultas, predicados o planes relacionados. Son ejemplos de ingeniería de software, no recetas para declarar verdadera una investigación.

En un pipeline OSINT, las pruebas diferenciales ayudan a detectar:

- filas perdidas por paginación o límites de API;
- diferencias de zona horaria, codificación o separador decimal;
- uniones que multiplican registros;
- tratamiento desigual de valores vacíos, `NULL` y cero;
- redondeos incompatibles;
- filtros o deduplicaciones aplicados en una sola ruta;
- cambios de esquema que una implementación tolera y otra oculta.

## Caso de uso legítimo: contratos municipales ficticios

Supongamos una investigación de transparencia sobre el gasto mensual del ayuntamiento ficticio de **Villa Serena**. El portal ofrece un CSV público con estos campos:

```csv
id_expediente,fecha,proveedor,importe_eur,estado
VS-001,2026-07-02,Servicios Norte SL,1200.00,adjudicado
VS-002,2026-07-18,Cooperativa Río,850.50,adjudicado
VS-003,2026-07-31,Servicios Norte S.L.,,anulado
```

Queremos contar expedientes adjudicados y sumar sus importes por mes. Construimos dos rutas deliberadamente distintas:

- **Pipeline A:** lector CSV y agregación en Python.
- **Pipeline B:** importación a SQLite y consulta SQL.

Ambas reciben exactamente el mismo fichero fijado por hash. El ejemplo usa datos inventados y no atribuye conducta a ninguna entidad real.

### Define el contrato antes de comparar

Sin contrato, cualquier diferencia puede explicarse después a conveniencia. Para este caso acordamos:

1. la unidad es un `id_expediente` único;
2. solo entra `estado = adjudicado`, sin distinguir mayúsculas tras eliminar espacios exteriores;
3. una fecha debe ser ISO `AAAA-MM-DD` y se agrupa por mes civil;
4. `importe_eur` se interpreta como decimal, nunca como binario de coma flotante;
5. un importe vacío no se convierte automáticamente en cero: genera una incidencia;
6. la salida contiene mes, número de expedientes, suma y lista ordenada de IDs;
7. cualquier duplicado de ID se reporta antes de agregar.

La lista de IDs es crucial. Comparar solo el total puede ocultar errores que se compensan: una fila añadida y otra perdida pueden conservar el mismo recuento.

## Flujo recomendado paso a paso

### 1. Fija una adquisición común

Descarga una sola vez dentro de los límites y condiciones de la fuente. Guarda:

- URL y parámetros;
- instante UTC de inicio y fin;
- código HTTP y cabeceras relevantes;
- fichero original sin modificar;
- hash criptográfico;
- versión o identificador de snapshot, si existe;
- notas sobre paginación, cobertura y licencia.

No compares una descarga de las 09:00 con otra de las 11:00 si la fuente es viva: una discrepancia podría ser una actualización legítima. La recomendación [PROV-O del W3C](https://www.w3.org/TR/prov-o/) ofrece un vocabulario formal para expresar entidades, actividades y derivaciones; una tabla de procedencia sencilla suele bastar para un caso pequeño.

### 2. Diseña rutas realmente independientes

La independencia no exige lenguajes distintos, pero sí reducir fallos comunes. Algunas combinaciones útiles son:

| Ruta A | Ruta B | Qué diversifica |
|---|---|---|
| parser CSV de Python | importador de SQLite | parser, tipos y agregación |
| API JSON | exportación CSV oficial | formato y canal de entrega |
| consulta SQL | agregación en memoria | motor y plan de ejecución |
| transformación nueva | implementación estable congelada | regresiones entre versiones propias |

Evita presentar dos endpoints que dependen del mismo backend como fuentes independientes. También evita descargar datos sensibles en un servicio externo solo para obtener diversidad técnica.

### 3. Conserva salidas crudas y crea una vista comparable

No compares directamente HTML, JSON o CSV serializados si el orden y el formato no tienen significado. Produce dos capas:

- **salida cruda**, tal como la emitió cada pipeline;
- **vista canónica**, limitada a los campos que el contrato declara comparables.

Para JSON existe el [JSON Canonicalization Scheme, RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), que define serialización determinista y ordenación de propiedades. No conviene improvisar una canonicalización que borre diferencias significativas. Ordenar un objeto puede ser inocuo; ordenar una lista de eventos puede destruir la cronología.

Un registro comparable para el ejemplo podría ser:

```json
{"conteo":2,"expedientes":["VS-001","VS-002"],"mes":"2026-07","total_centimos":205050}
```

Convertir euros a céntimos exactos evita tolerancias arbitrarias. Cuando la magnitud sea genuinamente aproximada —por ejemplo, coordenadas calculadas— documenta tolerancia absoluta, relativa y unidad antes de ejecutar la prueba.

### 4. Compara por capas, no con un único `diff`

Una comparación útil avanza de lo general a lo específico:

1. esquema y tipos;
2. cobertura temporal;
3. conjunto de claves;
4. duplicados por clave;
5. valores por registro;
6. agregados;
7. orden, solo si tiene semántica.

Ejemplo de informe:

```text
snapshot: sha256:…
pipeline_a: python-csv / configuración fijada
pipeline_b: sqlite / esquema de importación fijado

claves_solo_a: [VS-127]
claves_solo_b: [VS-204, VS-319]
valores_distintos:
  - id: VS-088
    campo: importe_centimos
    a: 1099
    b: 1098
```

Ese informe permite volver a cuatro filas concretas. «Los totales no coinciden» no ofrece la misma trazabilidad.

### 5. Reduce la discrepancia

Cuando aparece una diferencia, crea el caso mínimo que aún la reproduce:

- conserva solo las filas implicadas;
- ejecuta ambas rutas con la misma configuración;
- identifica la primera etapa en la que divergen;
- registra entrada, salida, logs y versiones;
- convierte el caso en una prueba de regresión.

No modifiques el original. El caso reducido es un derivado y debe enlazar con su adquisición mediante hash y notas de procedencia.

### 6. Vuelve a una referencia externa

La discrepancia indica «algo requiere explicación», no «A tiene razón». Para resolverla:

- consulta el registro individual en la fuente primaria;
- revisa el diccionario de datos y la semántica del campo;
- comprueba si el proveedor publicó correcciones;
- busca una tercera implementación solo si aporta independencia real;
- documenta la decisión y conserva el contraejemplo.

Si A y B coinciden, realiza igualmente muestreo contra la fuente. El acuerdo reduce una clase de riesgo; no valida autenticidad, cobertura ni interpretación.

## Un arnés mínimo y auditable

El coordinador puede tratar cada pipeline como una caja negra. Cada comando recibe un snapshot local y escribe JSON Lines canónico:

```python
from pathlib import Path
import json
import subprocess

snapshot = Path("fixtures/contratos.csv")

def ejecutar(comando: list[str]) -> list[dict]:
    salida = subprocess.run(
        [*comando, str(snapshot)],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout
    registros = [json.loads(line) for line in salida.splitlines() if line]
    return sorted(registros, key=lambda x: (x["mes"], x["expedientes"]))

a = ejecutar(["python", "pipeline_csv.py"])
b = ejecutar(["python", "pipeline_sqlite.py"])

if a != b:
    raise SystemExit("Discrepancia: conservar salidas y reducir el caso")
```

El fragmento muestra orquestación, no una solución completa. En producción hay que fijar entorno y dependencias, limitar recursos, validar el esquema de salida y guardar ambos artefactos antes de salir. Tampoco conviene ejecutar código de terceros o contenido descargado sin aislamiento.

## Cómo clasificar una discrepancia

| Categoría | Pregunta de triage | Respuesta prudente |
|---|---|---|
| Adquisición | ¿Ambos vieron exactamente los mismos bytes? | repetir sobre snapshot fijado |
| Parser | ¿interpretan igual codificación, fechas y vacíos? | inspeccionar fila y contrato |
| Normalización | ¿una ruta cambia caja, acentos o identificadores? | preservar valor original y derivado |
| Unión | ¿una relación uno-a-muchos multiplicó filas? | medir cardinalidad antes y después |
| Agregado | ¿hay redondeo, `NULL` o desbordamiento? | comparar registros y subtotales |
| Orden | ¿el orden importa o es ruido de serialización? | canonicalizar solo donde proceda |
| Fuente | ¿el dato primario es ambiguo o cambió? | registrar incertidumbre, no forzar igualdad |

## Limitaciones y falsos positivos

### El acuerdo puede ser un fallo compartido

Dos rutas pueden usar el mismo snapshot incompleto, la misma definición errónea de «adjudicado» o una biblioteca común defectuosa. Mapea dependencias compartidas y corrobora una muestra con la fuente primaria.

### La diferencia puede ser semántica, no un bug

SQLite y Python pueden ordenar valores nulos de manera distinta; dos exportaciones pueden reflejar instantes diferentes; una API puede devolver importes corregidos. Antes de corregir código, comprueba si el contrato era demasiado vago.

### Canonicalizar demasiado oculta evidencia

Eliminar espacios, acentos, zona horaria o duplicados para «hacer coincidir» salidas puede borrar precisamente la señal investigable. Conserva siempre original, transformación y motivo.

### Una mayoría no crea verdad

Tres pipelines que coinciden no constituyen una votación factual. Si los tres consumen el mismo error upstream, la unanimidad es decorativa.

### La cobertura sigue siendo parcial

Una prueba diferencial solo explora las entradas ejecutadas y los campos comparados. Un conjunto verde no demuestra que la fuente sea completa, auténtica o representativa.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa fuentes abiertas o accesos expresamente autorizados.
- Trabaja con fixtures ficticios o minimizados al depurar.
- No envíes datasets con datos personales a comparadores de terceros.
- Aísla parsers y conversores que procesen ficheros no confiables.
- Limita CPU, memoria, tiempo y acceso a red de cada pipeline.
- Revisa que logs y diffs no publiquen filas completas innecesariamente.
- Separa observación, transformación, discrepancia e inferencia.
- No conviertas una divergencia técnica en acusación sobre una persona u organización.
- Aplica retención limitada a snapshots, derivados y artefactos de CI.
- Si el hallazgo puede causar daño, exige revisión humana antes de difundirlo.

## Lista de control

- [ ] La pregunta investigable y la unidad de análisis están definidas.
- [ ] Ambos pipelines reciben los mismos bytes fijados por hash.
- [ ] La adquisición conserva URL, UTC, parámetros, cobertura y licencia.
- [ ] Las rutas reducen dependencias y supuestos compartidos.
- [ ] El contrato especifica tipos, vacíos, duplicados, fechas y redondeo.
- [ ] Las salidas crudas se guardan antes de canonicalizar.
- [ ] Se comparan claves y registros, no solo totales.
- [ ] Las tolerancias numéricas tienen justificación y unidad.
- [ ] Cada discrepancia conserva un caso mínimo reproducible.
- [ ] El triage vuelve a fuente primaria y documentación.
- [ ] Los fixtures y logs están minimizados.
- [ ] El acuerdo se presenta como consistencia parcial, no como verdad.

## Alternativas y siguientes pasos

Las [pruebas metamórficas](/pruebas-metamorficas-osint-invariantes) comparan ejecuciones relacionadas de una misma implementación y resultan útiles cuando no existe una segunda ruta. Los `unit tests` son mejores cuando conocemos una salida exacta. [dbt](/dbt-osint-pruebas-transformaciones) añade pruebas alrededor de modelos SQL, mientras que [Soda Core](/soda-core-osint-contratos-datos-deriva-esquema) vigila contratos y calidad de fuentes consultables.

No hace falta adoptar un framework complejo para empezar. El takeaway accionable es escoger hoy un agregado crítico, fijar diez filas ficticias, implementarlo una vez en código y otra en SQL, y comparar esquema, claves, registros y total. Introduce después un vacío, un duplicado y un valor con decimales. Cada divergencia debe terminar en una regla explícita o en una incertidumbre documentada, nunca en un parche para que el `diff` quede verde.

Como siguiente tema, merece la pena estudiar **mutation testing en pipelines OSINT**: introducir fallos controlados para comprobar si nuestra batería de pruebas detecta transformaciones peligrosas sin tocar datos reales.

## Fuentes consultadas

- [William M. McKeeman, Differential Testing for Software (1998)](https://citeseerx.ist.psu.edu/document?doi=fc881e8d0432ea8e4dd5fda4979243cac5e4b9e3&repid=rep1&type=pdf)
- [SQLite: How SQLite Is Tested](https://www.sqlite.org/testing.html)
- [SQLancer, repositorio y oráculos de prueba](https://github.com/sqlancer/sqlancer)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
