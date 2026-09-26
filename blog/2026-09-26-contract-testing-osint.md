---
title: "Contract testing en OSINT: detectar cambios de interfaz antes de contaminar el análisis"
slug: /contract-testing-osint
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-26
image: /img/blog/2026-09-26-contract-testing-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comprobando el contrato entre la adquisición de datos públicos y un pipeline OSINT](/img/blog/2026-09-26-contract-testing-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/contract-testing-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El informe mensual sigue saliendo, el gráfico conserva su aspecto impecable y ninguna tarea termina con error. Hay un problema: el portal público cambió `importe_adjudicado` por `importe`, empezó a entregar algunas cifras como texto y añadió paginación. El pipeline aceptó la respuesta, rellenó ausencias con cero y publicó una caída que nunca ocurrió. **El fallo más peligroso no siempre rompe el proceso; a veces lo deja producir una respuesta perfectamente creíble.**

El *contract testing* comprueba el acuerdo observable entre dos piezas que intercambian datos. En un flujo OSINT, una frontera especialmente útil está entre la adquisición y la transformación: qué solicitud se hace, qué respuesta se acepta y qué condiciones deben cumplirse antes de calcular nada. No demuestra que la fuente sea verdadera ni que esté completa. Evita que un cambio técnico silencioso se disfrace de hallazgo factual.

<!-- truncate -->

## Qué es un contrato y para qué sirve

Un contrato de datos es una descripción verificable de lo que una parte necesita de otra. Puede incluir el método y la ruta HTTP, parámetros, estado esperado, tipo de contenido, campos obligatorios, tipos, claves, reglas de paginación y supuestos semánticos. El consumidor es nuestro adaptador de adquisición; el proveedor puede ser una API, una descarga CSV o una página que publica datos estructurados.

La documentación de [Pact](https://docs.pact.io/) define las pruebas de contrato como comprobaciones de un punto de integración: los mensajes enviados o recibidos deben ajustarse a un entendimiento compartido. En entornos donde controlamos consumidor y proveedor, Pact permite describir interacciones desde las necesidades del consumidor y verificarlas contra el proveedor. En OSINT abierto normalmente **no controlamos el portal**, por lo que no podemos exigirle que ejecute nuestra verificación. Sí podemos conservar un contrato local, probar nuestro consumidor con fixtures y ejecutar sondas prudentes sobre el servicio público.

Conviene separar tres capas:

1. **Contrato de transporte:** URL o ruta, método, códigos aceptables, `Content-Type`, codificación, límites y paginación.
2. **Contrato estructural:** columnas o propiedades requeridas, tipos, nulabilidad, claves y forma de los registros.
3. **Contrato semántico:** unidad monetaria, zona horaria, significado de estados, cobertura temporal y criterio de actualización.

JSON Schema permite expresar restricciones estructurales sobre documentos JSON. Su vocabulario de validación incluye tipos y otras reglas; además, una propiedad solo es obligatoria cuando aparece en `required`. [OpenAPI](https://spec.openapis.org/oas/latest.html) puede describir operaciones, respuestas, medios y esquemas de una API. Para tablas, el modelo [CSV on the Web del W3C](https://www.w3.org/TR/tabular-data-model/) ofrece una base para describir columnas, dialecto y metadatos. Ningún formato sustituye la comprensión del dominio: que `importe` sea un número no aclara por sí solo si incluye impuestos.

## Caso legítimo: el portal de Villa Serena

Imaginemos una investigación de transparencia sobre la contratación agregada del ayuntamiento ficticio de **Villa Serena**. El portal ofrece `GET /api/adjudicaciones`, con páginas de hasta 100 registros. El equipo solo necesita datos institucionales: expediente, lote, fecha, procedimiento, estado e importe. No pretende perfilar empleados ni proveedores individuales.

El adaptador guarda cada respuesta cruda con URL, parámetros, hora UTC, cabeceras relevantes y hash. Antes de transformar, verifica un contrato mínimo:

- la respuesta es satisfactoria y declara JSON;
- existe una lista `results`;
- cada elemento contiene `expediente_id`, `fecha_adjudicacion`, `estado` e `importe_eur`;
- `importe_eur` es numérico o nulo según una regla explícita;
- la fecha usa un formato aceptado y se conserva su valor original;
- `next` es una URL o `null`;
- el número de páginas y registros queda registrado;
- la cobertura declarada no retrocede sin generar una alerta.

Un esquema reducido podría empezar así:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["results", "next"],
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "expediente_id",
          "fecha_adjudicacion",
          "estado",
          "importe_eur"
        ],
        "properties": {
          "expediente_id": {"type": "string", "minLength": 1},
          "fecha_adjudicacion": {"type": "string"},
          "estado": {"type": "string"},
          "importe_eur": {"type": ["number", "null"]}
        }
      }
    },
    "next": {"type": ["string", "null"]}
  }
}
```

Este ejemplo es deliberadamente tolerante con propiedades nuevas: añadir un campo que no usamos no debería detener la investigación. También evita tratar `format: date` como una garantía semántica suficiente. Después de la estructura hay que comprobar calendario, zona horaria, intervalos y significado documental.

## Flujo recomendado: de la expectativa al bloqueo seguro

### 1. Define lo que realmente consume el análisis

Empieza por la pregunta investigable y recorre el pipeline hacia atrás. Si el agregado solo utiliza fecha, estado, procedimiento e importe, el contrato no necesita congelar veinte campos decorativos. Los contratos excesivamente estrictos generan ruido y empujan al equipo a ignorar alertas.

Para cada requisito escribe:

- por qué existe;
- qué parte del pipeline depende de él;
- qué cambio sería compatible;
- qué cambio exige detenerse;
- qué evidencia conservar al fallar.

### 2. Fija fixtures representativos y minimizados

Conserva ejemplos sintéticos o anonimizados que incluyan el camino normal y las fronteras: valor nulo, importe cero, coma decimal si el portal publica CSV, página vacía, último enlace de paginación y un estado desconocido. Un fixture es una entrada de prueba, no una copia eterna de datos personales.

Incluye también respuestas incompatibles creadas de forma controlada:

- falta una columna requerida;
- `importe_eur` llega como texto;
- la respuesta HTML de mantenimiento devuelve estado 200;
- `next` apunta repetidamente a la misma página;
- cambia el separador o la codificación del CSV;
- una fecha carece de zona o precisión conocida.

La prueba debe confirmar que el adaptador rechaza, pone en cuarentena o marca cada situación según una política explícita. Rellenar automáticamente un campo crítico suele ocultar el incidente.

### 3. Prueba el consumidor sin depender de la red

Ejecuta el código real de adquisición y parseo contra una respuesta simulada. No pruebes únicamente que el fixture cumple el esquema: comprueba también que el adaptador construye la solicitud correcta, sigue la paginación prevista y entrega a transformación una estructura canónica.

Una secuencia mínima sería:

```text
fixture compatible ──> adaptador ──> contrato pasa ──> snapshot aceptado
fixture incompatible ─> adaptador ─> contrato falla ─> cuarentena + alerta
```

En un sistema bajo control compartido, una herramienta de contrato dirigido por el consumidor puede verificar el proveedor. Frente a una fuente pública ajena, esa segunda mitad se sustituye por una sonda de integración limitada y por observación del dato descargado. No conviertas una API de terceros en un banco de carga.

### 4. Verifica la fuente viva con una sonda prudente

Programa una petición pequeña, cacheable y respetuosa con límites y condiciones de uso. Registra estado, tipo de contenido, esquema observado, campos desconocidos, contador, paginación y tiempo de respuesta. Si la fuente ofrece OpenAPI o metadatos tabulares oficiales, conserva también su versión o hash.

No basta con comparar una respuesta completa byte a byte: los valores cambian legítimamente. Compara la **forma y las invariantes relevantes**. Una nueva propiedad suele ser compatible; eliminar una propiedad consumida, cambiar su tipo o alterar la unidad exige revisión.

### 5. Falla antes de transformar y conserva el original

La validación debe ocurrir después de guardar el cuerpo original y antes de normalizarlo. Así evitamos dos errores:

- perder la respuesta que explica el incidente;
- transformar una incompatibilidad hasta que parezca un dato válido.

Cuando falle el contrato, aparta el snapshot, emite una alerta con el `diff` estructural y detén solo los productos afectados. No sobrescribas el último conjunto válido. Etiquetar una publicación anterior como «datos actuales» cuando la adquisición ha fallado también sería engañoso.

### 6. Clasifica el cambio antes de adaptar

Una taxonomía sencilla ayuda al triage:

| Cambio observado | Tratamiento inicial |
|---|---|
| Campo nuevo no consumido | aceptar y registrar |
| Campo requerido ausente | bloquear transformación |
| Número convertido en texto | bloquear; investigar contrato y fuente |
| Nuevo valor de estado | cuarentena semántica o categoría `desconocido` visible |
| Orden distinto de columnas | aceptar si el parser usa nombres |
| Unidad o zona horaria modificada | bloquear hasta documentar conversión |
| Paginación nueva | bloquear si no se garantiza cobertura |

«Compatible» significa compatible con este consumidor, no correcto en términos factuales. El proveedor puede respetar perfectamente el esquema y publicar un dato incompleto.

### 7. Versiona contrato, adaptador y evidencia

Guarda juntos el contrato, los fixtures, la versión del adaptador y el hash del snapshot. Cuando aceptes un cambio, registra la decisión: qué se observó, qué documentación lo respalda, qué pruebas se añadieron y desde qué fecha se aplica. Reprocesar datos históricos con una regla nueva requiere conservar la distinción entre adquisición original y derivado posterior.

## Qué comprobar además del esquema

Los errores más costosos suelen vivir fuera de `type` y `required`. Añade controles de observabilidad sin confundirlos con verdades universales:

- **Cobertura:** primera y última fecha, páginas esperadas y registros por página.
- **Identidad:** claves vacías, duplicadas o reutilizadas.
- **Dominio:** valores nuevos de estado, moneda o procedimiento.
- **Magnitud:** cambios abruptos tratados como alertas, no como fallos automáticos.
- **Temporalidad:** zona, precisión, retraso de publicación y revisiones retroactivas.
- **Procedencia:** URL final, redirecciones, licencia y metadatos publicados.

Una regla como «siempre habrá más de mil registros» es frágil y puede convertir un cambio real en error técnico. Formula umbrales como detectores que solicitan revisión, no como mecanismos que fuerzan el dato a parecerse al pasado.

## Limitaciones y falsos positivos

El contrato solo protege expectativas expresadas. Puede pasar mientras la fuente omite expedientes, cambia una definición sin modificar el tipo o publica cifras erróneas. También puede fallar ante una ampliación legítima si hemos prohibido campos o valores que no nos afectan.

Otros límites importantes:

- una muestra pequeña puede no revelar páginas posteriores incompatibles;
- un `Content-Type` correcto no garantiza que el cuerpo lo sea;
- JSON Schema valida estructura, no intención ni veracidad;
- OpenAPI puede estar desactualizado respecto al servicio desplegado;
- los cambios semánticos requieren documentación o contacto con el publicador;
- una prueba contra producción puede fallar por red, cuota o mantenimiento;
- adaptar automáticamente tipos puede destruir la señal de que algo cambió.

Por eso conviene informar por separado de fallo de red, incompatibilidad de transporte, cambio estructural, alerta semántica y anomalía estadística. Mezclarlos en un único «pipeline roto» dificulta responder con proporcionalidad.

## Buenas prácticas de OPSEC, ética y privacidad

- Consulta únicamente fuentes públicas y respeta términos, cuotas, `robots.txt` cuando proceda y ventanas de actualización.
- Usa peticiones mínimas; las pruebas de contrato no justifican escaneos ni carga agresiva.
- No guardes tokens, cookies o cabeceras sensibles dentro de fixtures o logs.
- Prefiere datos ficticios para pruebas y minimiza snapshots con información personal.
- Separa credenciales de adquisición, almacenamiento de originales y entorno de tests.
- Evita incluir identificadores personales en alertas; enlaza al artefacto protegido cuando sea imprescindible.
- Define retención para respuestas crudas, fallos y derivados.
- Trata una incompatibilidad como incidente técnico, no como indicio automático de ocultación o manipulación.
- Exige revisión humana antes de publicar conclusiones sensibles.

## Lista de control

- [ ] La frontera consumidor/proveedor está identificada.
- [ ] El contrato contiene solo requisitos que usa el pipeline.
- [ ] Transporte, estructura y semántica se documentan por separado.
- [ ] Hay fixtures compatibles e incompatibles con datos ficticios.
- [ ] El código real del consumidor se ejecuta en la prueba.
- [ ] La paginación, codificación y tipo de contenido están cubiertos.
- [ ] La respuesta original se conserva antes de validar.
- [ ] Un fallo crítico detiene la transformación y pone el snapshot en cuarentena.
- [ ] Los campos nuevos no consumidos no rompen el flujo sin motivo.
- [ ] Valores de dominio desconocidos quedan visibles, no se recodifican en silencio.
- [ ] La sonda viva es pequeña, limitada y trazable.
- [ ] Contrato, adaptador, fixtures y decisiones están versionados.
- [ ] Un contrato verde se presenta como compatibilidad técnica, no como verdad.

## Alternativas y siguientes pasos

[Soda Core](/soda-core-osint-contratos-datos-deriva-esquema) ayuda a vigilar calidad y deriva sobre datos consultables; [dbt](/dbt-osint-pruebas-transformaciones) prueba modelos una vez que el dato ha entrado en la capa de transformación. Las [pruebas diferenciales](/pruebas-diferenciales-osint-pipelines) comparan implementaciones, las [pruebas metamórficas](/pruebas-metamorficas-osint-invariantes) expresan relaciones entre ejecuciones y el [mutation testing](/mutation-testing-pipelines-osint) comprueba si los tests detectan cambios peligrosos. El contrato ocupa otra frontera: **decide si la entrada es compatible antes de dejarla avanzar**.

No necesitas desplegar un broker para empezar. El takeaway accionable es escoger hoy una adquisición crítica y escribir cinco condiciones: estado, tipo de contenido, dos campos imprescindibles y regla de paginación. Crea después un fixture que viole cada condición y exige que el pipeline se detenga conservando el original. Si una respuesta incompatible termina convertida en una tabla normal, ya has localizado el siguiente control que falta.

Como próximo tema, merece la pena estudiar **pruebas de caos controladas en pipelines OSINT**: simular timeouts, respuestas truncadas y almacenamiento no disponible sin tocar fuentes reales ni confundir resiliencia técnica con validez factual.

## Fuentes consultadas

- [Pact: introducción a las pruebas de contrato](https://docs.pact.io/)
- [Pact: cómo funciona el contrato entre consumidor y proveedor](https://docs.pact.io/getting_started/how_pact_works)
- [JSON Schema: vocabulario de validación Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation)
- [JSON Schema: propiedades de objetos y campos obligatorios](https://json-schema.org/understanding-json-schema/reference/object)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [W3C: Model for Tabular Data and Metadata on the Web](https://www.w3.org/TR/tabular-data-model/)
