---
title: "Frictionless Data Package en OSINT: validar tablas sin validar conclusiones"
slug: /frictionless-data-package-osint-validacion-tabular
authors: [osint-writter]
tags: [osint, methodology, data, verification, tooling, privacy]
date: 2026-09-20
image: /img/blog/2026-09-20-frictionless-data-package-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una persona analista revisando tablas, esquemas y controles de validación](/img/blog/2026-09-20-frictionless-data-package-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un portal de contratación publica doce CSV. Un mes después cambia dos cabeceras, sustituye las comas decimales por puntos y deja una fecha imposible entre miles de filas correctas. La descarga sigue abriendo en una hoja de cálculo y el análisis produce cifras con aspecto convincente. **El peligro no es que el fichero esté roto, sino que falle de forma silenciosa.**

[Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) permite acompañar un conjunto de datos con una descripción legible por máquinas: qué recursos contiene, dónde están, qué columnas se esperan y qué reglas deben cumplir. En una investigación OSINT puede convertir supuestos dispersos en un contrato comprobable. No demuestra que los datos sean verdaderos, completos o actuales; solo ayuda a detectar cuándo no cumplen las reglas que hemos declarado.

<!-- truncate -->

## Qué es Frictionless Data Package y para qué sirve

Un Data Package es una colección coherente de recursos descrita por un fichero `datapackage.json`. Ese descriptor contiene una lista obligatoria de `resources` y puede añadir título, licencia, fuentes, versión y otra información útil. Cada recurso apunta a datos locales, remotos o incluidos en el propio JSON.

Para trabajo tabular intervienen tres capas relacionadas:

- **Data Package** agrupa y describe el conjunto.
- **Data Resource** identifica cada fichero o tabla, su ruta, formato, codificación y, opcionalmente, tamaño o hash.
- **Table Schema** declara columnas, tipos, formatos, valores ausentes, claves y restricciones como obligatoriedad o unicidad.

Si el CSV usa punto y coma, varias filas de cabecera u otras convenciones, **CSV Dialect** permite declararlas en lugar de confiar en una inferencia heurística. Esta separación importa: el dialecto explica cómo leer los caracteres; el esquema explica qué significan estructuralmente los campos.

El resultado no es un contenedor binario ni una base de datos. Es un contrato portable alrededor de los datos. Puede viajar junto a los CSV, guardarse en Git, validarse en una canalización y ser entendido por herramientas distintas.

## Caso de uso legítimo: revisar contratos de Villa Ejemplo

Imaginemos una investigación ficticia sobre contratos de mantenimiento del municipio de Villa Ejemplo. El portal publica dos tablas: expedientes y adjudicaciones. El equipo necesita comprobar que una actualización mensual no rompe el análisis ni introduce relaciones imposibles.

La copia de trabajo minimizada tiene esta estructura:

```text
contratos-villa-ejemplo/
├── datapackage.json
├── README.md
├── data/
│   ├── expedientes.csv
│   └── adjudicaciones.csv
└── notas/
    └── adquisicion.md
```

`notas/adquisicion.md` registra URL, consulta, paginación, fecha y hora UTC, licencia y método de descarga. El paquete no sustituye esa ficha: un `path` indica dónde está un recurso, pero no conserva por sí solo la respuesta HTTP ni explica todos los límites de la adquisición.

Un descriptor simplificado podría ser:

```json
{
  "name": "contratos-villa-ejemplo",
  "title": "Contratos públicos de Villa Ejemplo",
  "sources": [
    {
      "title": "Portal público de Villa Ejemplo",
      "path": "https://datos.example/contratos"
    }
  ],
  "resources": [
    {
      "name": "expedientes",
      "path": "data/expedientes.csv",
      "format": "csv",
      "encoding": "utf-8",
      "schema": {
        "fields": [
          {
            "name": "expediente_id",
            "type": "string",
            "constraints": {"required": true, "unique": true}
          },
          {
            "name": "fecha_publicacion",
            "type": "date"
          },
          {
            "name": "importe_eur",
            "type": "number",
            "constraints": {"minimum": 0}
          }
        ],
        "primaryKey": "expediente_id"
      }
    }
  ]
}
```

Todos los nombres y datos del ejemplo son sintéticos. La regla `minimum: 0` puede ser razonable para ese recurso concreto, pero no debe copiarse a ciegas: abonos, rectificaciones o ajustes contables podrían admitir valores negativos en otro conjunto.

## Flujo recomendado, paso a paso

### 1. Preservar la adquisición antes de normalizar

Guarda una copia inmutable de lo descargado y calcula un resumen criptográfico. Trabaja sobre un derivado, no sobre el único original. Conserva también la URL exacta, UTC, cabeceras relevantes, parámetros, paginación y cualquier error observado.

Si el descriptor apunta a una URL remota, el contenido puede cambiar entre validaciones. Para resultados reproducibles, fija una copia adquirida legalmente y deja el remoto como fuente, no como única dependencia.

### 2. Perfilar los datos sin confundir inferencia con decisión

Cuenta filas, columnas, nulos aparentes, valores distintos y rangos. Busca cabeceras duplicadas, filas vacías, codificaciones mixtas y separadores inesperados. La inferencia automática puede proponer tipos, pero una columna con identificadores numéricos quizá deba seguir siendo texto para conservar ceros iniciales.

Empieza con pocas reglas que puedas justificar. Añade una descripción a los campos ambiguos y documenta unidades, zona horaria y semántica de valores ausentes. Diferencia `0`, cadena vacía, `NA`, `null` y «dato no publicado»: no son equivalentes.

### 3. Declarar recursos, dialecto y esquema

Para cada recurso fija un nombre estable, ruta, formato y codificación. Si el CSV no sigue las convenciones esperadas, declara su dialecto: delimitador, carácter de cita, terminador de línea o filas de cabecera.

En Table Schema usa tipos y formatos explícitos cuando aporten control real. Aplica restricciones como `required`, `unique`, `minimum`, `maximum`, `minLength` o patrones solo cuando procedan de una regla conocida. Las claves primarias y foráneas ayudan a comprobar relaciones, pero una unión válida no demuestra que dos entidades del mundo real sean la misma.

### 4. Validar con una herramienta fijada

El proyecto oficial ofrece Frictionless Framework para línea de comandos y Python. En un entorno aislado, tras instalar y fijar la dependencia según la política del equipo, una validación básica es:

```bash
frictionless validate datapackage.json
```

Guarda el informe junto con la versión de la herramienta, el entorno y la hora UTC. Un resultado reproducible necesita saber qué se validó y con qué. No pegues automáticamente la versión más reciente en una investigación activa sin ensayarla sobre datos sintéticos.

### 5. Corregir el dato o el contrato, nunca ocultar el fallo

Clasifica cada error. Una celda extra puede ser corrupción; un tipo incorrecto puede revelar que el esquema era demasiado estricto; una clave duplicada puede representar una actualización legítima que exige una clave compuesta.

No cambies el CSV solo para obtener un informe verde. Conserva el original, crea un derivado, registra la transformación y explica por qué se modificó. Si corriges el esquema, documenta la decisión como parte del método.

### 6. Añadir controles sobre la pregunta investigada

La validación estructural es la base, no el final. Añade pruebas de dominio: cobertura temporal esperada, recuentos por periodo, duplicados semánticos, totales de control, consistencia entre tablas y comparación con publicaciones oficiales independientes.

Por ejemplo, el esquema puede aceptar todos los importes como números positivos mientras falta un trimestre completo. Esa ausencia no se detectará si no has declarado o comprobado la cobertura esperada.

### 7. Repetir y comparar cambios

Valida cada nueva adquisición antes de ejecutar el análisis. Compara descriptor, esquema, recuentos y errores con la entrega anterior. Un cambio de columna puede ser una migración anunciada; una caída brusca de filas puede ser un fallo de descarga; una lista sin cambios puede ocultar que el portal dejó de actualizarse.

Integra la comprobación en una canalización solo después de entender los fallos. La automatización debe detener resultados dudosos y producir evidencia revisable, no borrar filas problemáticas en silencio.

## Limitaciones y falsos positivos

### Un esquema válido no prueba la verdad

Una fecha bien formada puede ser falsa. Un importe dentro del rango puede pertenecer al expediente equivocado. Una clave única puede haber sido inventada. Frictionless verifica coherencia respecto del contrato, no autenticidad, intención ni interpretación factual.

### El contrato puede estar mal diseñado

Una restricción demasiado rígida genera falsos positivos; una demasiado laxa deja pasar errores. Las reglas deben derivarse de documentación, observación y conocimiento del dominio, con excepciones registradas. Inferir un esquema de una muestra pequeña y tratarlo como verdad suele congelar accidentes del fichero.

### La completitud necesita una expectativa externa

El paquete sabe qué recursos declara, no cuáles debería haber publicado la fuente. Tampoco descubre por sí mismo páginas omitidas por la paginación, filtros defectuosos o periodos ausentes. Mantén un inventario esperado y controles de cobertura.

### Hash, licencia y procedencia tienen alcance limitado

El campo `hash` de un recurso puede ayudar a detectar cambios de bytes si se calcula y verifica de forma consistente. No identifica al autor ni demuestra autenticidad. Del mismo modo, declarar una licencia no concede derechos que el publicador no tenga, y enumerar una fuente no prueba que el recurso proceda realmente de ella.

### Las implementaciones no son idénticas

Comprueba qué versión de las especificaciones y qué extensiones admite tu herramienta. Ensaya codificación, fechas, decimales, valores ausentes, claves y ficheros grandes. Conserva casos de prueba: la portabilidad se verifica, no se presupone.

## Buenas prácticas de OPSEC, ética y privacidad

- Recoge solo datos necesarios para una finalidad legítima y documentada.
- Separa adquisición original, copia de análisis y paquete publicable.
- No introduzcas cookies, tokens, rutas locales, correos privados ni identidades de fuentes protegidas en el descriptor.
- Trata paquetes ajenos y URLs remotas como entrada no confiable; valida rutas y limita red, tamaño, tiempo y redirecciones.
- No abras CSV desconocidos directamente en una hoja de cálculo: neutraliza el riesgo de fórmulas en copias destinadas a ese uso.
- Revisa que descripciones, ejemplos, errores y logs no revelen datos personales excluidos de las tablas.
- Fija permisos mínimos y procesa adjuntos o formatos complejos en un entorno aislado.
- Publica datos agregados o sintéticos cuando el detalle individual no sea necesario.
- Documenta retención, acceso y borrado; convertir datos en un paquete no legitima conservarlos indefinidamente.
- Distingue siempre observaciones, transformaciones e inferencias.

## Lista de control antes de aceptar el paquete

- [ ] Cada recurso tiene origen, UTC, método y licencia documentados.
- [ ] La copia original se conserva separada de cualquier normalización.
- [ ] Rutas, formatos, codificación y dialecto están declarados.
- [ ] Los tipos preservan identificadores, ceros iniciales, precisión y zona horaria.
- [ ] Los valores ausentes tienen una semántica explícita.
- [ ] Claves y restricciones responden a reglas justificadas.
- [ ] La validación termina sin errores inexplicados y su informe queda archivado.
- [ ] Recuentos y cobertura se comparan con una expectativa externa.
- [ ] Las relaciones críticas se contrastan con fuentes primarias o independientes.
- [ ] El paquete publicable no contiene secretos ni datos personales innecesarios.
- [ ] El equipo puede repetir la validación en un entorno limpio.
- [ ] Un resultado verde se presenta como conformidad estructural, no como verdad.

## Alternativas y siguientes pasos

Para un único CSV pequeño, un `README`, un esquema y un script de validación pueden ser suficientes. JSON Schema encaja mejor cuando el objeto principal es JSON no tabular. [Great Expectations](/great-expectations-osint-calidad-datos) ofrece suites y validaciones orientadas a canalizaciones. [RO-Crate](/ro-crate-osint-paquete-evidencia) describe relaciones y procedencia con mayor riqueza; [BagIt](/bagit-osint-transferencia-evidencia) se centra en transferir cargas con manifiestos; [OCFL](/ocfl-osint-preservacion-versionada) organiza preservación versionada.

No acumules formatos por prestigio. Elige Frictionless cuando necesites que varias personas o herramientas compartan un contrato compacto para recursos, tablas y reglas de validación.

El takeaway accionable: toma hoy un CSV público no sensible, conserva el original, declara tres columnas y dos restricciones justificadas, introduce un error en una copia y guarda el informe de validación. Después elimina una semana completa de datos. Si el segundo fallo pasa inadvertido, ya has encontrado el control de cobertura que falta en tu metodología.

Como siguiente tema, convendría estudiar cómo diseñar pruebas de deriva de esquema y cobertura temporal sin convertir cada cambio legítimo de una fuente en una falsa alarma.

## Fuentes consultadas

- [Data Package Specification](https://specs.frictionlessdata.io/data-package/)
- [Data Resource Specification](https://specs.frictionlessdata.io/data-resource/)
- [Table Schema Specification](https://specs.frictionlessdata.io/table-schema/)
- [CSV Dialect Specification](https://specs.frictionlessdata.io/csv-dialect/)
- [Frictionless Framework: Validating Data](https://framework.frictionlessdata.io/docs/guides/validating-data.html)
- [Repositorio oficial de Frictionless Framework](https://github.com/frictionlessdata/frictionless-py)
