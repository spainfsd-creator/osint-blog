---
title: "Soda Core en OSINT: detectar deriva de esquema sin convertir cada cambio en una crisis"
slug: /soda-core-osint-contratos-datos-deriva-esquema
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-21
image: /img/blog/2026-09-21-soda-core-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista conectando contratos de datos, controles de frescura y notas de investigación mediante un puente](/img/blog/2026-09-21-soda-core-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/soda-core-osint-contratos-datos-deriva-esquema.m4a)


*Imagen generada mediante inteligencia artificial.*

El portal de contratación de un ayuntamiento publica cada madrugada una tabla de adjudicaciones. Un lunes, `importe` pasa de número a texto; el miércoles desaparecen dos días enteros; el viernes aparece una columna nueva que no afecta al análisis. Los tres sucesos son cambios, pero **solo una metodología que separe estructura, frescura, cobertura y significado evitará tratarlos como si fueran la misma alarma**.

[Soda Core](https://github.com/sodadata/soda-core) permite expresar expectativas sobre un conjunto de datos en un contrato YAML y verificarlas desde la línea de comandos o mediante su API. En un flujo OSINT puede detectar pronto que una fuente pública ya no tiene la forma o la calidad mínima que necesita nuestro análisis. No determina si la fuente dice la verdad, no explica por qué cambió y no convierte una anomalía en prueba de manipulación.

<!-- truncate -->

## Qué es Soda Core y para qué sirve

Soda Core es un motor de verificación de calidad y contratos de datos. Su [formato de contrato](https://docs.soda.io/reference/contract-language-reference) permite declarar el conjunto que se va a comprobar, las columnas esperadas y controles como esquema, número de filas, frescura, ausencias, duplicados o valores válidos.

En la versión 4, vigente al publicar esta entrada, el proyecto ofrece una CLI y una API de Python. Los paquetes se distribuyen por fuente de datos —por ejemplo, PostgreSQL o DuckDB— y la [referencia oficial de conectores](https://docs.soda.io/reference/data-source-reference-for-soda-core) debe consultarse antes de diseñar el flujo. El repositorio tiene código disponible bajo Elastic License 2.0; conviene revisar sus condiciones si se plantea ofrecer el software como servicio gestionado.

Hay documentación abundante de Soda Core v3 que usa **SodaCL**, ficheros `checks.yml` y el comando `soda scan`. Sigue siendo útil para instalaciones heredadas, pero no debe mezclarse a ciegas con los contratos y comandos de v4. Antes de copiar un ejemplo, identifica la generación de la herramienta y fija la dependencia que realmente has probado.

Para una investigación, el contrato cumple tres funciones prácticas:

- hace explícitos los supuestos que antes vivían en una libreta o en la cabeza de quien analiza;
- transforma roturas silenciosas en resultados repetibles de aprobación o fallo;
- deja un artefacto versionable que otra persona puede revisar junto con la consulta, la fecha y la copia adquirida.

La herramienta comprueba expectativas contra datos. **La decisión sobre qué expectativa es razonable sigue siendo humana y contextual.**

## Caso de uso legítimo: adjudicaciones de Villa Ejemplo

Imaginemos un proyecto ficticio de rendición de cuentas sobre las adjudicaciones públicas de Villa Ejemplo. El portal oficial entrega un CSV diario. El equipo conserva cada respuesta original, registra URL y hora UTC, normaliza una copia y carga la tabla resultante en una base aislada.

El análisis necesita responder preguntas agregadas —volumen mensual, procedimiento e importes—, no perfilar personas. Por eso excluye campos personales innecesarios y trabaja con una tabla mínima:

| Campo | Uso | Riesgo que queremos detectar |
| --- | --- | --- |
| `expediente_id` | unir revisiones del mismo expediente | ausencias y duplicados |
| `fecha_publicacion` | ordenar y medir cobertura | retraso o huecos temporales |
| `importe_eur` | calcular agregados | cambio de tipo, nulos o negativos |
| `procedimiento` | comparar categorías | etiquetas inesperadas |
| `fuente_url` | volver al registro oficial | pérdida de trazabilidad |

Un contrato v4 simplificado podría tener esta forma:

```yaml
dataset: osint_local/expedientes/public/adjudicaciones

checks:
  - schema:
      allow_extra_columns: true
      allow_other_column_order: true
  - row_count:
      threshold:
        must_be_greater_than: 0
  - freshness:
      column: fecha_publicacion
      threshold:
        unit: day
        must_be_less_than: 3

columns:
  - name: expediente_id
    data_type: varchar
    checks:
      - missing:
      - duplicate:
  - name: fecha_publicacion
    data_type: timestamp
    checks:
      - missing:
  - name: importe_eur
    data_type: decimal
    checks:
      - missing:
      - invalid:
          valid_min: 0
  - name: procedimiento
    data_type: varchar
  - name: fuente_url
    data_type: varchar
    checks:
      - missing:
```

Es un ejemplo didáctico, no una plantilla universal. Los nombres de tipo dependen de los metadatos que devuelve la fuente conectada. La política permite columnas adicionales y otro orden porque ninguno de esos cambios rompe este análisis; en cambio, exige que las cinco columnas críticas existan con tipos compatibles.

Ese detalle evita una mala práctica común: convertir cualquier evolución del portal en incidente. Una columna descriptiva nueva puede ser inocua; borrar `expediente_id` o convertir `importe_eur` en texto sí rompe supuestos centrales.

## Flujo recomendado

### 1. Preserva antes de verificar

Descarga la respuesta original sin editarla y registra, como mínimo:

- URL y parámetros de consulta;
- fecha y hora UTC;
- código HTTP, tipo de contenido y tamaño;
- hash de la copia adquirida;
- licencia o condiciones de reutilización;
- herramienta y versión usadas.

Soda debe trabajar contra una copia controlada o una base de análisis. No sustituye la preservación de la respuesta ni documenta por sí solo cómo llegó cada fila hasta la tabla.

### 2. Define el contrato desde la pregunta de investigación

No empieces añadiendo todos los controles posibles. Escribe qué columnas sostienen la conclusión y qué roturas la invalidarían. Clasifica cada regla:

- **bloqueante**: falta una clave, cambia un tipo crítico o la tabla queda vacía;
- **advertencia**: aparece una categoría nueva o el volumen se desvía moderadamente;
- **informativa**: se añade una columna que todavía no usa el análisis.

En el contrato anterior, `allow_extra_columns: true` expresa una elección: admitir ampliaciones sin ocultar que las columnas enumeradas siguen siendo obligatorias. Si tu exportación depende del orden exacto, esa tolerancia ya no sería apropiada.

### 3. Prueba la sintaxis y la conexión por separado

En un entorno aislado, con el paquete adecuado instalado y fijado según la política del equipo, la CLI actual permite probar primero el contrato:

```bash
soda contract test --contract contract.yml
```

Después se comprueba la configuración de la fuente:

```bash
soda data-source test --data-source ds_config.yml
```

Y, por último, se ejecuta la verificación local:

```bash
soda contract verify --data-source ds_config.yml --contract contract.yml
```

No incluyas contraseñas en Git. La configuración oficial admite variables de entorno; usa credenciales de solo lectura, acceso mínimo y una base separada de los originales. Si publicas resultados en un servicio externo, evalúa antes qué metadatos, muestras o filas fallidas podrían salir de tu entorno.

### 4. Separa deriva, frescura y cobertura

Una prueba de esquema responde «¿siguen existiendo estas columnas y tipos?». Una prueba de frescura mide cuánto tiempo ha pasado desde la marca temporal más reciente. Ninguna de las dos demuestra que todos los periodos esperados estén presentes.

| Señal | Lo que puede indicar | Lo que no demuestra |
| --- | --- | --- |
| cambia el tipo de `importe_eur` | rotura de ingestión o rediseño de la fuente | intención de ocultar importes |
| el máximo de fecha tiene cuatro días | retraso, calendario no laborable o fallo de publicación | que falten exactamente cuatro días de datos |
| cae el número de filas | periodo incompleto, nuevo filtro o cambio real de actividad | cuál de esas causas es correcta |
| aparece una columna | evolución compatible o nueva semántica | que debamos incorporarla al análisis |
| pasan todos los controles | conformidad con las reglas declaradas | verdad, exhaustividad o autenticidad |

Para medir cobertura temporal, añade consultas explícitas sobre el calendario esperado: recuentos por día, primera y última fecha, periodos ausentes y comparación con el calendario administrativo. Un máximo reciente puede convivir con un agujero en mitad del mes.

### 5. Ensaya cambios conocidos con datos sintéticos

Antes de automatizar, crea copias de prueba y provoca de forma controlada:

1. una columna crítica eliminada;
2. un importe convertido en texto;
3. una columna opcional nueva;
4. el último día ausente;
5. una semana intermedia ausente;
6. un duplicado de clave;
7. un valor negativo imposible según la regla elegida.

Guarda el resultado de cada ejecución. Si dos fallos conceptualmente distintos producen una alerta indistinguible, todavía falta información operativa. Si un cambio legítimo bloquea siempre el flujo, el contrato es demasiado rígido o la política de excepciones no está definida.

### 6. Automatiza con una salida revisable

Ejecuta la verificación después de adquirir y cargar la copia, no contra una fuente cambiante mientras se analiza. Archiva el contrato, el resultado, la versión de Soda, la identidad de la tabla y la marca UTC. Una canalización puede detener la publicación de un informe derivado, pero no debería borrar ni sobrescribir el original que causó el fallo.

Cuando una regla falle:

1. conserva la adquisición afectada;
2. repite solo para descartar un fallo transitorio documentado;
3. compara con la última copia válida;
4. revisa avisos y documentación de la fuente;
5. contrasta con otra salida oficial o fuente independiente;
6. clasifica el cambio antes de ajustar el contrato.

Editar la expectativa para que una ejecución vuelva a verde sin explicar la causa destruye precisamente la memoria que el contrato debía aportar.

## Limitaciones y falsos positivos

### Un contrato conoce nuestras reglas, no el mundo

Soda puede comprobar que `importe_eur` es decimal y no negativo. No sabe si el importe fue cargado en la moneda correcta, pertenece al expediente adecuado o fue corregido después por el organismo. Una fila falsa pero bien formada puede superar todos los controles.

### La frescura no equivale a completitud

La comprobación de frescura se apoya en el valor temporal más reciente. Una sola fila actual puede hacerla pasar aunque falten miles de registros previos. La cobertura requiere reglas adicionales y, cuando sea posible, totales de control publicados por la fuente.

### Los umbrales envejecen

Un portal diario puede suspender publicaciones en festivos; una serie mensual puede cambiar su calendario; un organismo puede migrar su plataforma. Los umbrales necesitan propietario, justificación, fecha de revisión y excepciones registradas. No deben ajustarse automáticamente hasta silenciar toda variación.

### Los tipos dependen del conector

El contrato compara los tipos con los metadatos que expone la fuente. Dos motores pueden representar de forma distinta una misma intención lógica. Prueba el contrato en el motor real y evita copiar nombres de tipos de otro conector.

### Algunas capacidades pertenecen a generaciones distintas

La documentación v3 describe comprobaciones de evolución de esquema basadas en mediciones previas y funciones vinculadas a Soda Cloud. En v4, un contrato puede fijar directamente el esquema esperado. Son modelos relacionados, pero no intercambiables. Verifica siempre versión, licencia, disponibilidad local o en la nube y requisitos del conector.

### La alerta puede revelar demasiado

Una fila fallida puede contener nombres, identificadores o URLs internas. Minimiza datos antes del control, limita la captura de muestras, separa secretos de configuración y revisa qué se registra o publica. Calidad de datos y privacidad no son objetivos opuestos: un sistema observante también debe observar sus propias filtraciones.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja solo con fuentes y accesos autorizados; no uses la herramienta para forzar endpoints ni eludir controles.
- Prefiere copias locales y cuentas de solo lectura a consultas repetidas sobre sistemas de terceros.
- Recoge solo campos necesarios para una pregunta legítima y documentada.
- Usa entidades y valores ficticios en pruebas, capturas y documentación.
- Conserva secretos fuera del repositorio y rota cualquier credencial expuesta.
- Limita logs, muestras de filas fallidas y resultados compartidos.
- Trata una anomalía como señal para investigar, no como acusación.
- Documenta cambios aceptados: causa, evidencia, responsable y fecha.
- Mantén separado lo observado, lo transformado y lo inferido.
- Permite que otra persona reproduzca la comprobación sin acceder a datos personales innecesarios.

## Lista de control antes de confiar en una verificación

- [ ] El original está preservado con URL, UTC, método y hash.
- [ ] La versión de Soda y el conector están fijados y documentados.
- [ ] El contrato corresponde a la sintaxis de esa generación.
- [ ] Cada regla responde a una necesidad de investigación escrita.
- [ ] Las columnas críticas y las opcionales se distinguen explícitamente.
- [ ] Frescura, cobertura temporal y volumen se prueban por separado.
- [ ] Los días no laborables y otras excepciones legítimas están modelados.
- [ ] El flujo se ha ensayado con cambios sintéticos conocidos.
- [ ] Las credenciales son de solo lectura y no están en Git.
- [ ] Los logs y las filas fallidas no exponen datos innecesarios.
- [ ] Un fallo conserva la copia y abre una revisión; no borra evidencia.
- [ ] Un resultado correcto se presenta como conformidad, no como verdad.

## Alternativas y siguientes pasos

[Frictionless Data Package](/frictionless-data-package-osint-validacion-tabular) resulta útil para describir recursos, dialectos CSV y esquemas portables alrededor de ficheros. [Great Expectations](/great-expectations-osint-calidad-datos) ofrece otro enfoque para expectativas y validaciones en canalizaciones. Un script SQL pequeño puede ser suficiente para una tabla estable; dbt encaja si las transformaciones ya viven en ese ecosistema. La mejor herramienta es la que deja reglas comprensibles, resultados archivables y una ruta clara de revisión.

Soda Core aporta valor cuando el conjunto ya se consulta mediante una fuente compatible y queremos convertir supuestos de calidad en un contrato ejecutable. No lo añadas solo para conseguir un panel: empieza con tres fallos que realmente pondrían en riesgo tu conclusión.

El takeaway accionable: toma una copia pública no sensible, define una columna crítica, una regla de frescura y una consulta de cobertura. Después ensaya un cambio legítimo y dos roturas. Si el flujo distingue los tres casos y conserva suficiente contexto para explicarlos mañana, el contrato ya está trabajando para la investigación y no al revés.

Como siguiente tema, convendría estudiar contratos de datos frente a pruebas sobre transformaciones: dónde termina la calidad de la fuente y empieza la responsabilidad de nuestra propia canalización.

## Fuentes consultadas

- [Repositorio oficial de Soda Core](https://github.com/sodadata/soda-core)
- [Referencia oficial del lenguaje de contratos](https://docs.soda.io/reference/contract-language-reference)
- [Verificar un contrato con Soda Core](https://docs.soda.io/data-testing/git-managed-data-contracts/verify-a-contract)
- [Referencia oficial de la CLI](https://docs.soda.io/reference/cli-reference)
- [Referencia de fuentes de datos para Soda Core](https://docs.soda.io/reference/data-source-reference-for-soda-core)
- [Documentación oficial de SodaCL y Soda Core v3](https://docs.soda.io/soda-documentation/soda-v3/soda-cl-overview)

