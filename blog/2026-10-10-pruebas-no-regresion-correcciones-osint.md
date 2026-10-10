---
title: "Pruebas de no regresión en OSINT: convertir una corrección en un test sin guardar el dato sensible"
slug: /pruebas-no-regresion-correcciones-osint
authors: [osint-writter]
tags: [osint, methodology, testing, verification, automation, privacy]
date: 2026-10-10
image: /img/blog/2026-10-10-pruebas-no-regresion-correcciones-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista que comprueba que un error corregido no vuelve a un pipeline OSINT](/img/blog/2026-10-10-pruebas-no-regresion-correcciones-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/pruebas-no-regresion-correcciones-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Un equipo corrige una cifra, regenera el informe y da el incidente por cerrado. Tres semanas después, una refactorización reactiva la misma ruta defectuosa y el dato vuelve a aparecer. **La segunda publicación ya no es solo el mismo error: es la prueba de que la primera corrección no dejó una defensa ejecutable.**

Una prueba de no regresión convierte un fallo conocido en una comprobación que debe pasar antes de volver a publicar. En OSINT, el reto adicional consiste en conservar la forma del problema sin copiar al repositorio nombres, documentos, ubicaciones ni acusaciones del caso real.

<!-- truncate -->

Todas las entidades, cifras, rutas y registros de este artículo son ficticios. El método está pensado para fuentes públicas o autorizadas, transformaciones propias y pruebas aisladas; no justifica recolectar más datos personales, conservar material retirado ni ensayar sobre sistemas ajenos.

## Qué es una prueba de no regresión

Es un test creado a partir de un comportamiento que ya fue declarado incorrecto. Debe fallar con la implementación antigua, pasar con la corrección y seguir ejecutándose cuando cambien el parser, la consulta, las dependencias o el formato de salida.

Conviene separar cuatro piezas:

1. **Defecto:** la causa técnica que permitió el resultado incorrecto.
2. **Contraejemplo:** la entrada mínima que activa ese defecto.
3. **Oráculo:** la propiedad o salida esperada que distingue lo aceptable de lo erróneo.
4. **Ámbito:** las etapas y productos que quedan protegidos por el test.

Un ticket que dice «se corrigió el total» documenta una decisión. Un fixture sintético más una aserción reproducible comprueban que el fallo no reaparece en la parte cubierta. Ninguno de los dos demuestra que la fuente sea verdadera o que no existan otros errores.

El modelo [PROV-O del W3C](https://www.w3.org/TR/prov-o/) permite distinguir revisión, derivación e invalidación. Esa separación resulta útil para enlazar el test con la versión corregida sin tratar el artefacto viejo como vigente ni incrustar su contenido en cada registro.

## Caso legítimo: la fila que volvió dos veces

El observatorio ficticio **Atlas Cívico** publica estadísticas agregadas sobre subvenciones culturales. Una fuente cambia el separador decimal y el parser interpreta `84,5` como `845`. El total regional se infla, un gráfico hereda el error y el equipo publica después una corrección.

El incidente real contenía razón social, municipio y número de expediente. Nada de eso es necesario para probar el defecto. El equipo reduce el caso a dos filas inventadas:

```csv
zona,importe
Norte,"84,5"
Sur,"10,0"
```

La propiedad relevante es pequeña: con la configuración regional declarada, la suma debe ser `94.5`, no `855`. La prueba también verifica que un valor ambiguo no se publique silenciosamente cuando falta esa configuración.

El fixture conserva la estructura que provocó el fallo —coma decimal, comillas y agregación—, pero no conserva la identidad del expediente. El test protege la transformación; la nota de corrección y el registro de procedencia explican el impacto editorial.

## Flujo recomendado

### 1. Congela la descripción antes de arreglar

Registra qué se observó, en qué versión, qué salida quedó afectada y qué comportamiento se considera correcto. Conserva hashes o referencias controladas cuando sea necesario para auditoría, pero no pegues el payload sensible en el ticket.

Primero demuestra el fallo en un entorno aislado. Si el supuesto test ya pasa con el código defectuoso, el contraejemplo no reproduce la causa o la aserción vigila otra cosa.

### 2. Reduce el caso hasta su mecanismo causal

Elimina columnas, filas y metadatos uno por uno. Tras cada reducción, confirma que la versión defectuosa continúa fallando. Detente cuando quitar otra pieza cambie el mecanismo.

Reducir no consiste en sustituir nombres y dejar intacta una combinación identificable. [NIST SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) trata la desidentificación como una cuestión de técnicas y gobernanza, y recuerda que existe riesgo de reidentificación. En la práctica, construye valores nuevos que ejerciten la misma rama lógica y revisa el conjunto completo, no solo cada campo por separado.

Una ficha mínima puede dejar esta trazabilidad sin revelar el caso:

```yaml
regression_id: reg-2026-10-10-decimal-comma
source_incident: corr-2026-10-10-01
fixture: tests/fixtures/decimal_comma.csv
property: "la suma respeta la configuración regional declarada"
sensitive_source_copied: false
old_version_fails: true
fixed_version_passes: true
```

Es una estructura de ejemplo, no un estándar.

### 3. Elige el oráculo más estrecho que sea útil

Evita afirmar «el informe es correcto». Comprueba propiedades observables:

- el parser acepta o rechaza un formato explícito;
- el total coincide con las filas válidas;
- una fila inválida entra en cuarentena y no en la salida pública;
- el orden de entrada no cambia una agregación que deba ser conmutativa;
- la salida no contiene campos prohibidos;
- la versión corregida es la única marcada como vigente.

Los snapshots completos son cómodos, pero pueden aprobar cambios irrelevantes o esconder una diferencia importante entre cientos de líneas. Para una corrección, combina aserciones semánticas pequeñas con un snapshot solo cuando la representación completa sea parte del contrato.

### 4. Convierte el contraejemplo en test permanente

Con `pytest`, la parametrización permite ejecutar la misma comprobación sobre varios casos documentados. La [documentación oficial de parametrización](https://docs.pytest.org/en/stable/example/parametrize.html) muestra cómo suministrar entradas distintas a una misma prueba. Un ejemplo deliberadamente simple sería:

```python
import pytest

@pytest.mark.parametrize(
    ("rows", "decimal_mark", "expected"),
    [
        (["84,5", "10,0"], ",", 94.5),
        (["84.5", "10.0"], ".", 94.5),
    ],
)
def test_sum_respects_declared_decimal_mark(rows, decimal_mark, expected):
    assert parse_and_sum(rows, decimal_mark=decimal_mark) == expected
```

El fragmento ilustra el contrato; no es un parser listo para producción. El código real debe controlar codificación, separadores de campos, redondeo, valores ausentes, límites y errores explícitos.

Si el fallo apareció mediante generación automática, no confíes solo en una caché local. La guía de [Hypothesis sobre repetición de fallos](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html) explica que su base de ejemplos ayuda durante el desarrollo, pero recomienda un `@example` explícito cuando una entrada debe ejecutarse siempre. Conserva un caso legible y estable; usa la generación para seguir buscando variantes.

### 5. Prueba la propiedad y el camino de publicación

Un test unitario puede demostrar que `parse_and_sum` devuelve `94.5` y, aun así, el informe puede leer una tabla antigua. Añade comprobaciones proporcionales en varias capas:

| Capa | Pregunta de no regresión |
| --- | --- |
| Parser | ¿Interpreta el formato o falla de forma explícita? |
| Transformación | ¿El cálculo cumple la propiedad corregida? |
| Contrato de datos | ¿Esquema, nulos y rangos siguen siendo aceptables? |
| Derivado | ¿Gráfico e informe usan la versión nueva? |
| Publicación | ¿La URL pública sirve el artefacto verificado? |

Para modelos SQL, la [documentación de unit tests de dbt](https://docs.getdbt.com/docs/build/unit-tests) recomienda entradas estáticas para lógica compleja, errores ya reportados y casos límite. Sus data tests cumplen otra función: formulan aserciones sobre los datos producidos, como unicidad, valores nulos o relaciones, según la [guía oficial de data tests](https://docs.getdbt.com/docs/build/data-tests). Ninguna herramienta sustituye la comprobación editorial del significado.

### 6. Ejecuta el test en el punto que pueda bloquear la regresión

Una prueba que solo vive en el portátil de quien corrigió el incidente no protege la publicación. Inclúyela en la suite versionada y ejecútala antes de fusionar o desplegar la transformación afectada. Si el coste es alto, separa una suite rápida obligatoria de otra extensa programada, pero conserva el contraejemplo corregido en la ruta obligatoria.

El test debe producir un fallo accionable: identificador de regresión, propiedad incumplida y etapa afectada. No vuelques las filas reales ni secretos en logs de integración continua.

### 7. Cierra con una prueba negativa

Antes de dar por terminada la corrección:

1. ejecuta el test sobre la versión anterior y confirma que falla;
2. ejecútalo sobre la versión corregida y confirma que pasa;
3. altera intencionadamente el fixture para comprobar que la aserción detecta la diferencia;
4. ejecuta el camino de publicación con datos sintéticos;
5. enlaza test, corrección y derivados regenerados.

Este pequeño ensayo evita tests decorativos que siempre pasan. No necesitas conservar en producción la versión vulnerable; basta un entorno controlado o una mutación equivalente que demuestre la sensibilidad del test.

## Limitaciones y falsos positivos

### Un caso mínimo puede reducir demasiado

Si eliminas la codificación, el orden o la combinación de campos que causaba el defecto, quizá pruebes otro problema. Documenta qué pieza activa cada rama y conserva una explicación humana breve.

### Pasar el test no valida el caso completo

La prueba cubre una propiedad conocida. No certifica exhaustividad, independencia de fuentes ni verdad factual. Mantén controles de calidad, revisión proporcional y corroboración separadas.

### Los fixtures envejecen

Un cambio legítimo de contrato puede volver obsoleta la salida esperada. Actualizar el test exige explicar qué cambió y por qué; regenerar snapshots a ciegas convierte la aprobación en rutina.

### La prueba puede ser inestable

Relojes, red, aleatoriedad, orden no definido y servicios externos generan resultados intermitentes. La documentación de [Hypothesis sobre fallos inestables](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html) señala que un fallo que no puede reproducirse impide reducir y reutilizar con fiabilidad el ejemplo. Fija tiempo y aleatoriedad, usa dobles locales y reserva la red para pruebas de integración controladas.

### Sintético no significa anónimo por definición

Una fila inventada puede seguir reproduciendo una combinación única, una acusación o un patrón reconocible. Evalúa necesidad y riesgo, evita valores derivados de una sola persona y aplica retención también al repositorio de tests.

## Buenas prácticas de OPSEC, ética y privacidad

- Conserva en el fixture solo la estructura necesaria para activar el defecto.
- Usa nombres, dominios, coordenadas e identificadores inequívocamente ficticios.
- Separa evidencia restringida, registro de incidente y suite de pruebas.
- No descargues de nuevo contenido retirado para fabricar un test.
- Impide que CI publique fixtures, logs o artefactos de depuración.
- Revisa diffs para detectar secretos y datos personales antes del commit.
- Fija versiones y configuración cuando afecten al resultado.
- Declara qué cubre la prueba y qué queda fuera.
- Exige intervención humana proporcional cuando una salida pueda afectar a personas.
- Retira fixtures que ya no sean necesarios, dejando la justificación del control sustituto.

## Alternativas y siguientes pasos

Para una transformación pequeña, un CSV sintético y dos aserciones pueden ser suficientes. Si el problema depende de muchas combinaciones, añade property-based testing; si dos implementaciones deberían coincidir, usa pruebas diferenciales; si no conoces una salida exacta pero sí una relación estable, aplica pruebas metamórficas. Ya hay entradas específicas sobre esas técnicas en este blog: la no regresión aporta otra cosa, **la memoria ejecutable de un fallo confirmado**.

Cuando el error cruce varias etapas, enlaza el test con el grafo de impacto descrito en [verificación de derivados](/verificacion-derivados-osint). Así podrás saber qué suite debe bloquear cada regeneración y qué URL pública debe verificarse antes de cerrar.

## Checklist de cierre

- [ ] El defecto y el comportamiento correcto están descritos.
- [ ] La versión anterior falla con el contraejemplo.
- [ ] La versión corregida pasa.
- [ ] El fixture es mínimo, sintético y revisado como conjunto.
- [ ] La aserción expresa una propiedad, no una promesa de verdad total.
- [ ] El test está versionado y se ejecuta antes de publicar.
- [ ] Los logs no exponen el caso real.
- [ ] Se prueban también cuarentena, error o rechazo cuando corresponda.
- [ ] Los derivados afectados leen la versión vigente.
- [ ] La cobertura y sus límites quedan documentados.

El takeaway accionable es directo: toma la última corrección de tu pipeline, construye el contraejemplo sintético más pequeño que haga fallar la versión anterior y añádelo a la ruta obligatoria de CI. Si la prueba no distingue el código viejo del corregido, aún no has creado una barrera de no regresión; solo has escrito un recuerdo.

Como siguiente tema, convendría estudiar la **caducidad y mantenimiento de fixtures OSINT**: cómo retirar casos obsoletos sin borrar la memoria del incidente ni convertir la suite en un archivo de datos innecesario.

## Fuentes consultadas

- [pytest: Parametrizing tests](https://docs.pytest.org/en/stable/example/parametrize.html)
- [Hypothesis: Replaying failed tests](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
- [Hypothesis: Flaky failures](https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html)
- [dbt Developer Hub: Unit tests](https://docs.getdbt.com/docs/build/unit-tests)
- [dbt Developer Hub: Data tests](https://docs.getdbt.com/docs/build/data-tests)
- [NIST SP 800-188: De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final)
- [W3C: PROV-O, The PROV Ontology](https://www.w3.org/TR/prov-o/)
