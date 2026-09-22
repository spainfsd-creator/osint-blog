---
title: "dbt en OSINT: probar transformaciones sin convertir un pipeline verde en verdad"
slug: /dbt-osint-pruebas-transformaciones
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-22
image: /img/blog/2026-09-22-dbt-osint-pruebas-transformaciones.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando fuentes públicas, transformaciones SQL y controles antes de obtener una tabla de evidencia](/img/blog/2026-09-22-dbt-osint-pruebas-transformaciones.png)

*Imagen generada mediante inteligencia artificial.*

Una investigación sobre contratación pública reúne adjudicaciones de tres portales. La consulta termina sin errores y el panel muestra una cifra redonda: un proveedor habría multiplicado por cuatro sus contratos. Sin embargo, una transformación interpretó los abonos como nuevas adjudicaciones y un `join` duplicó los expedientes con varios lotes. **La canalización funcionó exactamente como estaba escrita; el problema es que estaba escrita de forma equivocada.**

[dbt](https://docs.getdbt.com/docs/build/projects) permite organizar transformaciones SQL como modelos dependientes, documentarlas y someterlas a distintos controles. En un flujo OSINT puede separar lo que llegó de la fuente, lo que modificó nuestro código y lo que terminó en una tabla analítica. No verifica que una administración publique datos verdaderos, no demuestra una irregularidad y no sustituye la lectura del expediente original.

<!-- truncate -->

## Qué es dbt y para qué sirve en OSINT

dbt trabaja sobre datos que ya están disponibles en una plataforma compatible. En vez de esconder una sucesión de consultas manuales, permite expresar cada transformación como un modelo SQL y sus dependencias mediante `source()` y `ref()`. De ese modo, la tabla final deja un grafo legible desde la fuente declarada hasta el resultado.

Para una investigación basada en datos, esa estructura ayuda a contestar preguntas concretas:

- ¿qué tabla pública alimentó este resultado?;
- ¿qué normalización convirtió el importe original?;
- ¿qué regla eliminó duplicados?;
- ¿qué modelos dependen de una columna que acaba de cambiar?;
- ¿qué supuesto se comprobó sobre la fuente y cuál sobre nuestra transformación?;
- ¿podemos repetir el cálculo con una copia preservada?

La palabra clave es **trazabilidad**, no certeza. dbt puede probar que una columna no contiene nulos o que un caso sintético produce el resultado esperado. Ninguna de esas pruebas acredita por sí sola que el dato de origen sea completo, actual o fiel a los hechos.

## Cuatro controles que no deben confundirse

El error metodológico más común es llamar «test» a todo y asumir que todas las capas responden a la misma pregunta.

| Capa | Pregunta útil | Lo que no demuestra |
| --- | --- | --- |
| Frescura de fuente | ¿La marca temporal más reciente cumple el umbral declarado? | Que no falten periodos o filas antiguas |
| Contrato de modelo | ¿Los nombres y tipos de columnas coinciden con la interfaz prevista? | Que los valores tengan sentido factual |
| `data test` | ¿El resultado contiene filas que contradicen una regla? | Que la regla cubra todos los errores posibles |
| `unit test` | ¿La lógica SQL transforma correctamente unas entradas estáticas conocidas? | Que los datos reales sean auténticos o completos |

La [documentación oficial sobre fuentes](https://docs.getdbt.com/docs/build/sources) explica que declararlas permite describirlas, probar supuestos y calcular su frescura. Los [`data tests`](https://docs.getdbt.com/docs/build/data-tests) son consultas que devuelven las filas que incumplen una afirmación; dbt incluye controles genéricos de unicidad, ausencia de nulos, valores aceptados e integridad referencial. Los [`unit tests`](https://docs.getdbt.com/docs/build/unit-tests) ejercitan lógica SQL con entradas estáticas antes de materializar el modelo completo. Finalmente, los [contratos de modelo](https://docs.getdbt.com/docs/mesh/govern/model-contracts) fijan la forma que debe producir una transformación.

Estas piezas se complementan. Un contrato puede impedir que `importe_eur` cambie de decimal a texto, pero no detectará que una conversión multiplicó el importe por cien. Un `data test` puede descubrir expedientes repetidos en el resultado real, pero quizá llegue tarde si antes hemos sobrescrito un artefacto. Un `unit test` puede cubrir la regla de abonos sin consultar expedientes reales, pero solo para los casos que hayamos diseñado.

## Caso ficticio: adjudicaciones, lotes y abonos

Imaginemos a la entidad ficticia **Consorcio Vega Norte**, que publica dos recursos abiertos:

- `adjudicaciones.csv`, con una fila por combinación de expediente y lote;
- `movimientos.csv`, con adjudicaciones, correcciones y abonos posteriores.

La pregunta legítima es estimar el importe neto adjudicado por proveedor y trimestre. Antes de escribir SQL, el cuaderno de investigación deja constancia de cinco decisiones:

1. un expediente puede contener varios lotes;
2. `movimiento = 'ABONO'` resta, no suma;
3. una corrección no crea automáticamente otra adjudicación;
4. los importes originales se preservan sin modificar;
5. cualquier agregado debe poder retroceder hasta expediente, lote y movimiento.

El objetivo no es perfilar personas ni inferir conductas privadas. Se trabaja con información institucional publicada, identificadores ficticios en las pruebas y una finalidad documentada de rendición de cuentas.

## Flujo recomendado

### 1. Preserva antes de transformar

Descarga la fuente dentro de sus condiciones de uso y conserva, como mínimo:

- URL exacta;
- fecha y hora UTC;
- cabeceras o metadatos relevantes;
- hash del fichero recibido;
- licencia o condiciones aplicables;
- copia inmutable del original.

dbt no es una herramienta de captura ni un archivo forense. Si el portal cambia mañana, el grafo de modelos no reconstruirá por arte de magia el CSV que utilizaste hoy. Puedes combinar este paso con [BagIt](/bagit-osint-transferencia-evidencia), [OCFL](/ocfl-osint-preservacion-versionada) o un procedimiento más sencillo, siempre que sea verificable y proporcional.

### 2. Declara la fuente y separa zonas

Una estructura mínima distingue tres capas:

- `raw`: copia importada sin reinterpretar;
- `staging`: nombres, tipos y formatos normalizados;
- `marts`: tablas que responden a preguntas de investigación.

La fuente se declara en YAML y los modelos la referencian de forma explícita. Un ejemplo reducido y ficticio sería:

```yaml
sources:
  - name: portal_vega
    schema: raw
    tables:
      - name: movimientos
        columns:
          - name: expediente_id
            data_tests: [not_null]
```

El control comprueba un supuesto sobre la tabla importada. No confirma que todos los expedientes del periodo hayan sido publicados.

### 3. Escribe una transformación pequeña y explicable

La lógica de signo puede vivir en un modelo de *staging*:

```sql
select
  expediente_id,
  lote_id,
  proveedor_id,
  fecha_movimiento,
  case
    when tipo_movimiento = 'ABONO' then -abs(importe_eur)
    when tipo_movimiento = 'ADJUDICACION' then abs(importe_eur)
    else 0
  end as importe_neto_eur
from {{ source('portal_vega', 'movimientos') }}
```

El `else 0` merece una decisión consciente: podría ocultar categorías nuevas. En un caso real quizá convenga conservarlas como `NULL`, enviarlas a cuarentena o hacer fallar una prueba de valores aceptados. La política debe constar en las notas, no quedar enterrada como una comodidad del SQL.

### 4. Prueba la lógica con entradas sintéticas

Un `unit test` permite preparar movimientos inventados y declarar la salida esperada. El ejemplo conceptual siguiente omite opciones dependientes del adaptador:

```yaml
unit_tests:
  - name: abonos_restan_y_adjudicaciones_suman
    model: stg_movimientos
    given:
      - input: source('portal_vega', 'movimientos')
        rows:
          - {expediente_id: EXP-001, lote_id: L-1, tipo_movimiento: ADJUDICACION, importe_eur: 100}
          - {expediente_id: EXP-001, lote_id: L-1, tipo_movimiento: ABONO, importe_eur: 20}
    expect:
      rows:
        - {expediente_id: EXP-001, lote_id: L-1, importe_neto_eur: 100}
        - {expediente_id: EXP-001, lote_id: L-1, importe_neto_eur: -20}
```

Conviene añadir casos fronterizos que hayan causado errores o puedan causarlos: importe cero, tipo desconocido, lote ausente, fecha límite de trimestre y dos correcciones sobre el mismo movimiento. Usa la sintaxis correspondiente a la versión y al adaptador fijados en tu proyecto; la documentación distingue generaciones y mantiene limitaciones específicas.

### 5. Prueba propiedades del resultado real

Después de construir el modelo, los `data tests` comprueban afirmaciones sobre sus filas. Por ejemplo:

```yaml
models:
  - name: fct_importes_netos
    columns:
      - name: movimiento_id
        data_tests: [unique, not_null]
      - name: expediente_id
        data_tests: [not_null]
      - name: tipo_movimiento
        data_tests:
          - accepted_values:
              arguments:
                values: ['ADJUDICACION', 'ABONO', 'CORRECCION']
```

Una prueba singular adicional podría devolver agregados cuyo importe neto no cuadre con la suma de sus movimientos. El diseño correcto es el que muestra registros revisables y conserva la relación con el original, no el que produce más marcas verdes.

### 6. Añade contrato donde exista un consumidor estable

Si otro análisis depende de `fct_importes_netos`, un contrato puede fijar nombres y tipos de columnas. La documentación advierte que el soporte de restricciones cambia según plataforma y materialización. Comprueba qué se define, qué se impone realmente y qué queda solo como metadato.

No conviertas todo modelo exploratorio en una interfaz rígida. Los contratos demasiado tempranos elevan el coste de una corrección legítima y pueden crear una falsa sensación de madurez.

### 7. Ejecuta por capas y archiva el contexto

Un ciclo prudente separa:

1. comprobación de frescura y disponibilidad;
2. importación de una copia identificada;
3. pruebas unitarias sobre la lógica modificada;
4. construcción de modelos;
5. pruebas sobre datos resultantes;
6. comparación con totales o documentos externos;
7. exportación de artefactos, versiones y notas.

La [guía oficial de frescura](https://docs.getdbt.com/docs/deploy/source-freshness) señala que esa comprobación no se incluye automáticamente en todos los flujos de construcción. Diseña el orden de ejecución de forma explícita y decide si una fuente atrasada debe bloquear el análisis o abrir una advertencia.

## Qué hacer cuando una prueba falla

Un fallo no es un veredicto contra la fuente ni contra una organización. Es una observación que necesita clasificación:

1. conserva la entrada que produjo el fallo;
2. guarda el SQL compilado, la versión del proyecto y el adaptador;
3. identifica si falló la fuente, la importación, la transformación o el supuesto;
4. compara con la última ejecución válida;
5. revisa documentación y avisos del portal;
6. contrasta con expedientes o totales oficiales independientes;
7. corrige código o regla mediante un cambio revisable;
8. añade un caso sintético que impida la regresión.

Cambiar un umbral hasta recuperar el verde sin explicar la causa destruye la trazabilidad. También lo hace borrar filas «problemáticas» antes de conservarlas y entenderlas.

## Limitaciones y falsos positivos

### Una prueba solo conoce el supuesto escrito

`not_null` detecta ausencias, no identificadores asignados al expediente equivocado. `unique` detecta repeticiones según la clave elegida, no demuestra que esa clave represente correctamente la unidad del mundo real.

### Un `join` válido puede cambiar la granularidad

Unir expedientes con lotes, adjudicatarios y movimientos puede multiplicar filas sin producir un error SQL. Define la granularidad esperada antes del `join` y comprueba recuentos, claves y sumas a ambos lados.

### La frescura puede ocultar huecos

Una sola fila reciente puede satisfacer una regla temporal mientras falta un mes completo. Comprueba por separado actualidad, cobertura, volumen y continuidad.

### Los casos sintéticos heredan nuestros puntos ciegos

Si no imaginamos un abono parcial o una corrección encadenada, la prueba unitaria no los inventará. Alimenta la suite con errores encontrados, pero sin copiar datos personales al repositorio.

### «Pasó» no significa «es verdad»

Una tabla falsa pero coherente puede superar contratos, pruebas y comprobaciones de frescura. La verificación factual sigue necesitando documentos primarios, fuentes independientes y una explicación proporcional a la evidencia.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con fuentes públicas o accesos expresamente autorizados.
- Minimiza campos personales antes de llevar datos a una plataforma analítica.
- Usa identificadores y valores ficticios en fixtures, capturas y documentación.
- No guardes credenciales, URLs privadas ni datos sensibles en Git.
- Ejecuta con cuentas de solo lectura siempre que sea posible.
- Revisa qué contienen logs, artefactos y tablas de fallos antes de compartirlos.
- Evita almacenar filas fallidas completas si basta con una clave pseudonimizada y un motivo.
- Fija dependencias y adaptadores; documenta cualquier cambio de versión.
- Separa observación, transformación e inferencia en el informe.
- Trata una anomalía como señal para investigar, nunca como acusación automática.

La opción de conservar resultados fallidos puede facilitar la depuración, pero también crear una tabla auxiliar con nombres, correos o identificadores. Aplica control de acceso, retención limitada y minimización antes de activarla.

## Lista de control antes de confiar en el resultado

- [ ] La copia original tiene URL, UTC, hash y condiciones de uso.
- [ ] La granularidad de cada modelo está escrita en una frase.
- [ ] Las fuentes se referencian explícitamente y no mediante tablas opacas.
- [ ] La versión de dbt, el adaptador y las dependencias están fijados.
- [ ] Los casos sintéticos cubren lógica, límites y errores conocidos.
- [ ] Las claves críticas tienen pruebas de unicidad y ausencia de nulos cuando procede.
- [ ] Los valores aceptados contemplan una ruta segura para categorías nuevas.
- [ ] Frescura, cobertura y volumen se comprueban por separado.
- [ ] Los `join` tienen controles de granularidad antes y después.
- [ ] Las tablas de fallos no exponen datos innecesarios.
- [ ] Los totales se contrastan con otra salida oficial o fuente independiente.
- [ ] El informe presenta una prueba superada como conformidad, no como verdad.

## Alternativas y siguientes pasos

[Soda Core](/soda-core-osint-contratos-datos-deriva-esquema) resulta útil cuando el foco está en contratos y controles sobre una fuente consultable. [Great Expectations](/great-expectations-osint-calidad-datos) ofrece suites de expectativas sobre datos. [Frictionless Data Package](/frictionless-data-package-osint-validacion-tabular) describe recursos tabulares portables. Un conjunto pequeño de consultas SQL versionadas puede ser mejor que incorporar dbt a un análisis único y estable.

dbt aporta más valor cuando existen varias transformaciones relacionadas, consumidores recurrentes y una necesidad real de probar cambios. No lo adoptes para decorar un diagrama: úsalo cuando el grafo, las pruebas y los artefactos reduzcan un riesgo concreto de la investigación.

El takeaway accionable: toma una transformación pequeña sobre datos públicos no sensibles, escribe su granularidad, crea un caso sintético que deba pasar y otro que exponga un error conocido. Añade después una prueba sobre el resultado real y una corroboración fuera del pipeline. Si puedes explicar qué protege cada control y qué queda fuera, ya has separado ingeniería de datos de verificación factual.

Como siguiente tema, merece la pena estudiar pruebas metamórficas en OSINT: cómo verificar invariantes de una transformación cuando no conocemos de antemano toda la salida correcta.

## Fuentes consultadas

- [Documentación oficial de proyectos dbt](https://docs.getdbt.com/docs/build/projects)
- [Documentación oficial de fuentes](https://docs.getdbt.com/docs/build/sources)
- [Documentación oficial de data tests](https://docs.getdbt.com/docs/build/data-tests)
- [Documentación oficial de unit tests](https://docs.getdbt.com/docs/build/unit-tests)
- [Documentación oficial de contratos de modelo](https://docs.getdbt.com/docs/mesh/govern/model-contracts)
- [Documentación oficial de frescura de fuentes](https://docs.getdbt.com/docs/deploy/source-freshness)
