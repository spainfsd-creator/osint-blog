---
title: "Great Expectations en OSINT: automatizar controles de calidad sin automatizar conclusiones"
slug: /great-expectations-osint-calidad-datos
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, automation, data]
date: 2026-09-08
image: /img/blog/2026-09-08-great-expectations-osint-calidad-datos.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando datos públicos mediante controles de esquema, rangos, unicidad y procedencia](/img/blog/2026-09-08-great-expectations-osint-calidad-datos.png)

*Imagen generada mediante inteligencia artificial.*

Un portal público sustituye su CSV mensual sin avisar. La columna `importe` pasa de número a texto, desaparecen varios identificadores y una fecha adopta otro formato. El fichero sigue abriendo y nuestro análisis sigue ejecutándose, pero sus resultados ya no significan lo mismo. **En OSINT, una canalización que no falla puede ser precisamente la que más debería preocuparnos**.

[Great Expectations](https://docs.greatexpectations.io/docs/core/introduction/gx_overview/) —también denominado GX— permite expresar supuestos sobre los datos como pruebas verificables: columnas obligatorias, valores no nulos, rangos plausibles, categorías permitidas o recuentos esperados. No decide si una adjudicación es irregular ni si una fuente dice la verdad. Su utilidad es más concreta: detectar cuándo el material que alimenta una investigación deja de cumplir las condiciones mínimas que habíamos documentado.

<!-- truncate -->

> **Transparencia editorial:** esta entrada ha sido generada mediante inteligencia artificial y se publica sin revisión humana ni *fact-checking* humano. Las fuentes técnicas se consultaron el 8 de septiembre de 2026.

## Qué es Great Expectations y para qué sirve

GX Core es una biblioteca de Python para describir y ejecutar validaciones de datos. Su vocabulario puede parecer amplio al principio, pero responde a una secuencia sencilla:

1. un **Data Context** conserva la configuración, los metadatos y los resultados;
2. un **Data Source** representa la conexión con los datos;
3. un **Data Asset** identifica el conjunto que queremos tratar como unidad lógica;
4. una **Batch Definition** determina qué registros se validan juntos;
5. una **Expectation** formula una condición comprobable;
6. una **Expectation Suite** agrupa varias condiciones;
7. una **Validation Definition** vincula los datos con la suite;
8. un **Checkpoint** ejecuta una o varias validaciones y puede activar acciones.

La [documentación oficial de GX Core](https://docs.greatexpectations.io/docs/core/introduction/gx_overview/) presenta precisamente el patrón «configurar, conectar, definir expectativas y validar». La documentación mostraba la versión `1.22.0` al realizar esta consulta. Conviene comprobar siempre la documentación de la versión instalada antes de copiar un ejemplo: las APIs evolucionan y una receta antigua puede fallar o, peor aún, comprobar algo distinto de lo esperado.

En una investigación legítima, GX encaja bien después de la exploración inicial. VisiData, una hoja de cálculo o un cuaderno ayudan a descubrir la forma real de los datos; una suite de expectativas convierte parte de ese conocimiento en controles repetibles. **Explorar descubre supuestos; validar los vuelve explícitos**.

## Caso de uso legítimo: contratos públicos de Bahía Clara

El ayuntamiento ficticio de **Bahía Clara** publica cada mes un CSV de adjudicaciones. Una organización vecinal quiere estudiar la evolución del gasto por categoría sin señalar a personas ni inferir conductas ilícitas. Antes de agregar importes, define un contrato mínimo de datos:

- deben existir `expediente_id`, `fecha_publicacion`, `importe_eur`, `categoria` y `url_fuente`;
- `expediente_id` no puede estar vacío;
- `importe_eur` debe ser numérico y no negativo;
- `categoria` debe pertenecer al catálogo publicado por el ayuntamiento;
- `url_fuente` debe conservar la procedencia de cada fila;
- el número de registros debe compararse con el histórico, sin imponer un umbral arbitrario;
- una clave repetida debe revisarse, no borrarse automáticamente: podría representar lotes, correcciones o un duplicado real.

Estas reglas no demuestran que el conjunto sea completo. Solo permiten responder preguntas operativas: ¿ha cambiado el esquema?, ¿hay filas que no se pueden rastrear?, ¿un cálculo recibiría valores incompatibles?, ¿merece la pena detener el análisis y volver a la fuente?

La diferencia es crucial:

| Control | Qué detecta | Qué no demuestra |
| --- | --- | --- |
| columna obligatoria | deriva del esquema | que el campo esté bien cumplimentado |
| no nulo | ausencia técnica de valor | que el valor sea verdadero |
| rango | valores incompatibles con una regla | fraude o intención |
| unicidad | claves repetidas | que una fila sea el duplicado incorrecto |
| conjunto permitido | categorías inesperadas | que la taxonomía oficial sea adecuada |
| recuento | cambios de volumen | que falten datos deliberadamente |
| URL de procedencia | posibilidad de volver a la fuente | que la fuente sea completa o fiable |

## Flujo recomendado

### 1. Preserva primero, valida después

Guarda el original sin modificar, junto con:

- URL de descarga;
- fecha y hora en UTC;
- cabeceras HTTP relevantes, si están disponibles;
- hash criptográfico del fichero;
- licencia o condiciones de reutilización;
- identificador interno de adquisición.

Trabaja sobre una copia. Una validación debe poder repetirse contra el mismo artefacto; si el portal cambia el fichero bajo la misma URL, el hash evita confundir dos versiones.

### 2. Perfila una muestra y redacta reglas justificadas

No empieces imponiendo condiciones que «parecen razonables». Revisa la documentación del productor, varias entregas históricas y una muestra estratificada. Para cada regla anota:

- qué riesgo controla;
- qué fuente justifica el umbral;
- si el fallo debe bloquear o solo advertir;
- qué excepciones conocidas existen;
- quién revisará los registros inesperados.

GX permite asignar severidades y admite el parámetro `mostly` para tolerar una proporción de excepciones en determinadas Expectations. Ambas funciones exigen criterio. Un `mostly=0.95` no es rigor por sí mismo: podría normalizar que el 5 % más importante quede sin procedencia.

### 3. Empieza con una validación pequeña y legible

La [guía oficial de instalación](https://docs.greatexpectations.io/docs/core/set_up_a_gx_environment/install_gx/) recomienda un entorno virtual e instala GX Core con `pip install great_expectations`. Este ejemplo abreviado usa nombres y datos ficticios; debe adaptarse y probarse con la versión instalada:

```python
import pandas as pd
import great_expectations as gx

df = pd.read_csv("adjudicaciones_bahia_clara.csv")
context = gx.get_context()

source = context.data_sources.add_pandas(name="portal_bahia_clara")
asset = source.add_dataframe_asset(name="adjudicaciones_mensuales")
batch_definition = asset.add_batch_definition_whole_dataframe("entrega_completa")

suite = context.suites.add(
    gx.ExpectationSuite(name="contrato_adjudicaciones")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="expediente_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="importe_eur", min_value=0
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="categoria",
        value_set=["obras", "servicios", "suministros"],
        severity="warning",
    )
)

validation = context.validation_definitions.add(
    gx.core.validation_definition.ValidationDefinition(
        name="validar_entrega_mensual",
        data=batch_definition,
        suite=suite,
    )
)

result = validation.run(batch_parameters={"dataframe": df})
print(result.success)
```

La [documentación para DataFrames](https://docs.greatexpectations.io/docs/core/connect_to_data/dataframes/) explica que GX admite Data Sources de pandas y Spark; el DataFrame se proporciona en ejecución mediante `batch_parameters`. La suite no debería crecer hasta volverse ilegible. Es preferible empezar con cinco controles defendibles que acumular cincuenta reglas copiadas sin entender su efecto.

### 4. Separa errores técnicos, avisos e incidencias de investigación

Una estrategia práctica usa tres estados:

- **bloqueo técnico**: falta una columna necesaria o el tipo impide calcular;
- **aviso de calidad**: aparece una categoría nueva o cambia mucho el recuento;
- **incidencia de investigación**: una persona revisa la fuente y documenta qué significa el cambio.

El código de salida de una canalización puede detener una publicación automática, pero no debe redactar acusaciones. El paso de «esta fila incumple una expectativa» a «este hecho es relevante» requiere contexto, corroboración y responsabilidad editorial.

### 5. Versiona las suites junto al análisis

Conserva las expectativas, consultas y transformaciones en control de versiones. Registra qué versión de la suite validó cada fichero. Si una taxonomía oficial cambia, crea una modificación explicada; no reescribas silenciosamente los resultados pasados.

Un **File Data Context** persiste configuraciones y resultados en el sistema de archivos, mientras que un contexto efímero vive solo durante la sesión. La [guía de Data Context](https://docs.greatexpectations.io/docs/core/set_up_a_gx_environment/create_a_data_context/) señala que el modo efímero puede encajar en exploración o CI desechable. Para un caso que deba auditarse meses después, la persistencia controlada suele aportar más trazabilidad, siempre que no exponga datos sensibles.

### 6. Automatiza con Checkpoints sin perder supervisión

Cuando las reglas estén probadas, una Validation Definition puede asociar una Batch Definition con una suite. Los **Checkpoints** agrupan validaciones y pueden ejecutar acciones a partir del resultado. Según la [documentación de acciones y resultados](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/), esto permite, por ejemplo, actualizar Data Docs o emitir alertas.

En OSINT responsable, la acción segura por defecto es **poner en cuarentena el derivado y avisar al analista**. No publiques automáticamente un ranking, una atribución o una alerta pública porque haya fallado una regla de datos.

## Limitaciones y falsos positivos

Great Expectations verifica las condiciones que nosotros expresamos. Por eso hereda nuestros puntos ciegos:

- **Reglas incompletas:** un fichero puede superar todas las pruebas y omitir justo los registros que nunca supimos que existían.
- **Umbrales sin contexto:** una caída del 40 % puede ser una incidencia del portal, un periodo vacacional o un cambio de cobertura.
- **Tipos engañosos:** que una fecha sea válida no prueba que represente publicación, firma o actualización.
- **Unicidad mal modelada:** un expediente puede aparecer legítimamente varias veces por lotes o rectificaciones.
- **Valores permitidos obsoletos:** una nueva categoría oficial producirá un fallo correcto técnicamente, pero no una anomalía sustantiva.
- **Resultados voluminosos:** los detalles de filas fallidas pueden contener información personal o sensible.
- **Dependencias y versiones:** una actualización de GX, pandas o del conector puede cambiar compatibilidades; fija y prueba el entorno.

Una validación exitosa significa «los datos observados cumplen estas reglas en esta ejecución». No significa «el dataset es auténtico, completo y verdadero».

## Buenas prácticas de OPSEC, ética y privacidad

- Minimiza columnas y filas antes de validar; no recopiles datos personales «por si acaso».
- Usa datos sintéticos para desarrollar las suites y ejemplos públicos.
- No incluyas valores sensibles en capturas, Data Docs, artefactos de CI o mensajes de error.
- Restringe el acceso a resultados detallados y aplica una política de retención.
- Separa identificadores directos de las tablas analíticas cuando sea posible.
- No pruebes accesos ni fuerces endpoints: valida únicamente datos obtenidos de forma legal y proporcionada.
- Documenta falsos positivos y excepciones sin etiquetar a personas como sospechosas.
- Corrobora las incidencias relevantes con el documento original y otra fuente independiente.
- Ofrece vías de corrección cuando publiques conclusiones sobre organizaciones reales.

La automatización debe reducir errores repetitivos, no aumentar la escala de una recogida invasiva.

## Alternativas y siguientes pasos

- **Pandera** expresa esquemas y comprobaciones cerca de DataFrames de pandas y otros motores compatibles; puede resultar más ligero cuando la validación vive dentro de una biblioteca Python.
- **Pydantic** es útil para validar objetos y registros estructurados, aunque no sustituye todos los controles estadísticos o tabulares.
- **dbt tests** encaja cuando los datos ya se transforman en un almacén analítico gestionado con dbt.
- **Soda Core** ofrece otra aproximación declarativa para comprobaciones de calidad.
- **pruebas propias con pytest** dan máximo control, a costa de diseñar informes, metadatos y convenciones.

La elección depende del lugar donde deban vivir las reglas. GX aporta un vocabulario amplio, suites, resultados y documentación; una función pequeña puede ser mejor para un caso acotado. Lo importante es que cada comprobación tenga justificación, versión, propietario y respuesta prevista.

## Conclusión

El takeaway accionable es este: **elige el próximo dataset recurrente de tu investigación y escribe cinco expectativas antes de automatizar ningún análisis**. Incluye al menos esquema, procedencia, nulos, dominio de valores y una comprobación de volumen comparada con el histórico. Haz que un fallo detenga el derivado, no que produzca una conclusión.

Como siguiente tema, merece la pena comparar Great Expectations y Pandera sobre el mismo CSV ficticio: ergonomía, trazabilidad, informes y coste de mantenimiento sin convertir la herramienta en sustituto del criterio investigador.

## Fuentes consultadas

- [GX Core: visión general y flujo de trabajo](https://docs.greatexpectations.io/docs/core/introduction/gx_overview/)
- [Instalación de GX Core](https://docs.greatexpectations.io/docs/core/set_up_a_gx_environment/install_gx/)
- [Creación y tipos de Data Context](https://docs.greatexpectations.io/docs/core/set_up_a_gx_environment/create_a_data_context/)
- [Conexión a DataFrames de pandas y Spark](https://docs.greatexpectations.io/docs/core/connect_to_data/dataframes/)
- [Creación de Expectations](https://docs.greatexpectations.io/docs/core/define_expectations/create_an_expectation/)
- [Organización de Expectations en suites](https://docs.greatexpectations.io/docs/core/define_expectations/organize_expectation_suites/)
- [Checkpoints, acciones y resultados](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/)
