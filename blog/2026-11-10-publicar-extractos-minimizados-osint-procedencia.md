---
title: "Extractos minimizados en OSINT: compartir resultados verificables sin publicar el corpus"
slug: /extractos-minimizados-osint-procedencia
authors: [osint-writter]
tags: [osint, methodology, data, verification, privacy, automation]
date: 2026-11-10
image: /img/blog/2026-11-10-extractos-minimizados-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una investigación encuentra doce contratos que merecen una segunda revisión dentro de un corpus de dos millones de filas. Publicar el fichero completo permitiría repetir el análisis, pero también expondría nombres, teléfonos y combinaciones de datos que no sostienen la conclusión. Publicar solo una captura protegería mejor a terceros, pero impediría comprobar cómo se obtuvieron los doce casos. **El reto no es elegir entre transparencia y privacidad: es diseñar un extracto que revele lo necesario, conserve el camino hasta la fuente y haga visibles sus límites.**

![Analista transformando un gran corpus público en un extracto minimizado con esquema y trazabilidad](/img/blog/2026-11-10-extractos-minimizados-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un método para publicar resultados derivados de datos abiertos o material tratado con autorización. El ejemplo es ficticio. No pretende convertir una receta técnica en asesoramiento jurídico ni afirma que borrar unas columnas anonimice un conjunto de datos: la posibilidad de identificar a alguien depende también del contexto, de los datos auxiliares y de quién recibe el extracto.

## Qué es un extracto minimizado y para qué sirve

Un **extracto minimizado** es un producto de datos creado para una pregunta y una audiencia concretas. Contiene las filas, columnas y nivel de detalle necesarios para comprobar una afirmación, pero excluye elementos que no cumplen esa función o crean un riesgo desproporcionado. Debe ir acompañado de información que permita entender de dónde procede, cómo se transformó y qué no puede demostrar.

No es simplemente:

- el corpus original comprimido;
- una hoja con nombres sustituidos por números;
- el resultado de un `SELECT` sin consulta ni parámetros;
- una tabla redondeada hasta que deja de ser útil;
- una promesa genérica de que «los datos son públicos».

La [Comisión Europea resume el principio de minimización](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en) como tratar datos personales adecuados, pertinentes y limitados a lo necesario para una finalidad. Que un dato pueda encontrarse en Internet no elimina la necesidad de preguntarse para qué se vuelve a publicar, con qué alcance y qué efecto produce al agregarlo.

Un buen extracto intenta mantener cuatro propiedades en tensión:

| Propiedad | Pregunta de control |
| --- | --- |
| utilidad | ¿permite comprobar la afirmación publicada? |
| minimización | ¿cada campo y cada fila tienen una función declarada? |
| procedencia | ¿se puede reconstruir qué fuentes y transformaciones lo produjeron? |
| integridad | ¿podemos detectar una modificación posterior del paquete? |

Un hash ayuda con la última pregunta, pero no responde a las tres anteriores. Identifica unos bytes; no certifica que la selección sea justa, que el esquema sea correcto o que la publicación sea segura.

### Pseudonimizar no equivale a anonimizar

Reemplazar `nombre` por `sujeto_017` reduce la exposición directa, pero puede conservar una ruta de vuelta mediante una tabla de correspondencias o por combinación con fecha, localidad y cargo. La [Comisión Europea](https://commission.europa.eu/law/law-topic/data-protection/data-protection-explained_en) recuerda que los datos seudonimizados que todavía permiten reidentificar a una persona siguen siendo datos personales. El [EDPB distingue](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en) la seudonimización, que reduce la vinculabilidad, de la anonimización efectiva.

Tampoco basta con eliminar identificadores directos. Una fila única que combine municipio pequeño, edad exacta, profesión y día del evento puede señalar a una persona sin incluir su nombre. [NIST SP 800-188](https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance) recomienda definir primero el objetivo y el modelo de compartición, evaluar el riesgo de divulgación y considerar alternativas como datos sintéticos, interfaces de consulta o entornos protegidos. En otras palabras: a veces el extracto público correcto es **ningún extracto fila a fila**.

## Caso de uso legítimo: doce expedientes que requieren revisión

El observatorio ficticio **Cuenca Clara** analiza contrataciones publicadas por una administración imaginaria. Sus fuentes contienen expedientes, lotes, adjudicatarios, importes, fechas, descripciones, correos de contacto y documentación enlazada. El objetivo editorial es sostener una afirmación limitada:

> Doce expedientes superaron un criterio reproducible de revisión por proximidad temporal, objeto similar e importe acumulado; la señal no demuestra irregularidad y exige volver a cada expediente primario.

El corpus íntegro es necesario dentro del entorno de análisis para calcular grupos y denominadores. No todo el corpus es necesario para que un lector compruebe la afirmación. Antes de exportar, el equipo crea una matriz de necesidad:

| Campo candidato | Decisión | Motivo |
| --- | --- | --- |
| identificador público del expediente | conservar | permite regresar a la fuente primaria |
| fecha | conservar por día | interviene en la ventana temporal declarada |
| importe | conservar | interviene en el criterio y en la suma |
| categoría normalizada | conservar | explica la agrupación temática |
| nombre comercial del adjudicatario | sustituir por código estable en el extracto | permite agrupar sin republicar el nombre en la tabla derivada |
| correo y teléfono de contacto | excluir | no intervienen en la afirmación |
| descripción libre completa | excluir; publicar una categoría y una nota metodológica | puede contener datos incidentales y dificulta revisar cambios |
| URL del expediente | conservar | ofrece trazabilidad hasta el registro primario |
| puntuación interna de riesgo | excluir | mezclaría una heurística no explicada con hechos observados |

El código estable no se presenta como anonimización. Si el identificador del expediente lleva a una ficha pública con el adjudicatario, la relación sigue siendo recuperable. Su función es más modesta: reducir la repetición innecesaria de nombres en la tabla y hacer explícito que la unidad analítica es el grupo, no una acusación personal.

## Flujo recomendado

### 1. Escribe la afirmación, la audiencia y el modelo de acceso

La minimización empieza antes del SQL. Documenta:

- qué afirmación debe poder comprobarse;
- quién recibirá el resultado: público general, equipo colaborador o revisor bajo acceso controlado;
- qué unidad representa cada fila;
- qué riesgo produce combinar el extracto con fuentes razonablemente accesibles;
- cuánto tiempo debe permanecer disponible;
- qué alternativa menos reveladora se ha descartado y por qué.

La misma investigación puede necesitar tres salidas diferentes: una tabla pública agregada, un extracto seudonimizado para revisores y el corpus restringido para reproducibilidad interna. «Abrir todo» y «no mostrar nada» no son los únicos modelos.

### 2. Fija los originales y separa las zonas de trabajo

Conserva los ficheros adquiridos como solo lectura y registra, al menos:

- URL o sistema de origen;
- fecha y hora de adquisición;
- licencia o condiciones conocidas;
- tamaño, tipo de contenido y hash criptográfico;
- respuesta HTTP o método de exportación;
- notas sobre paginación, filtros y fallos de descarga.

Trabaja en una zona derivada. El directorio público nunca debe contener por accidente los originales, tablas de correspondencias, credenciales, consultas con secretos ni temporales del editor. Una lista de exclusión ayuda, pero conviene construir el paquete desde una carpeta vacía y revisar su contenido como si ya estuviera en Internet.

### 3. Convierte la necesidad en una consulta versionada

La selección debe ser ejecutable y revisable. Un esquema conceptual podría ser:

```sql
SELECT
  expediente_id,
  fecha,
  importe_eur,
  categoria_normalizada,
  codigo_entidad,
  url_fuente
FROM resultado_verificado
WHERE requiere_revision = true
ORDER BY fecha, expediente_id;
```

El ejemplo no oculta por sí mismo los nombres ni crea los códigos: esas transformaciones deben definirse en pasos anteriores, con parámetros separados y pruebas. Guarda la consulta, la versión del entorno, el identificador de la fuente y el número esperado de filas. Usa un orden explícito para que dos ejecuciones equivalentes no produzcan ficheros distintos por casualidad.

### 4. Prueba la selección por inclusión y por exclusión

No basta con comprobar que las doce filas aparecen. Verifica también:

1. que casos conocidos que cumplen el criterio estén incluidos;
2. que casos cercanos que no lo cumplen estén excluidos por la razón esperada;
3. que las sumas y recuentos reconcilien con el corpus en cada etapa;
4. que una unión no haya multiplicado expedientes;
5. que nulos, zonas horarias, redondeos y duplicados tengan política explícita;
6. que el resultado se regenere desde una copia limpia.

Publica el denominador cuando sea relevante. «Doce señales» se interpreta de forma muy distinta si proceden de veinte registros o de dos millones.

### 5. Evalúa el riesgo de divulgación en contexto

Busca identificadores directos, cuasi-identificadores, valores raros, texto libre y enlaces que deshagan la minimización. Prueba combinaciones plausibles con otras fuentes públicas, sin intentar identificar personas ni ampliar la investigación más allá de lo necesario para evaluar el riesgo.

Preguntas útiles:

- ¿una combinación de campos deja una sola fila?
- ¿el código estable permite seguir a la misma entidad entre publicaciones sin necesidad?
- ¿un hash de correo o teléfono puede probarse por diccionario?
- ¿la precisión temporal o geográfica supera lo que exige la afirmación?
- ¿los valores extremos revelan a alguien aunque se retiren los nombres?
- ¿los metadatos del fichero conservan autor, ruta local o software?
- ¿la URL primaria vuelve a introducir datos que el texto presenta como eliminados?

Si el riesgo residual es alto, agrega categorías, ensancha intervalos, suprime celdas raras, separa entregas, ofrece una consulta limitada o mueve la revisión a un entorno controlado. No prometas «anonimato» sin un análisis defendible y repetible.

### 6. Empaqueta datos, esquema, método y procedencia

Un paquete pequeño y legible puede tener esta forma:

```text
extracto-contratos-2026-11-10/
├── README.md
├── data/
│   └── expedientes_revision.csv
├── schema/
│   └── tabla.schema.json
├── scripts/
│   └── construir_extracto.sql
├── checksums.sha256
└── datapackage.json
```

La especificación [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) define un descriptor `datapackage.json` con los recursos del paquete y metadatos como fuentes y licencias. Su especificación de [Data Resource](https://specs.frictionlessdata.io/data-resource/) contempla tamaño, formato, codificación, esquema y hash. Adoptar el formato no demuestra que el contenido sea seguro o correcto, pero evita esconder decisiones básicas en un correo o en el nombre del fichero.

El `README.md` debería indicar:

- afirmación y alcance;
- fuente o fuentes y momento de adquisición;
- significado de cada fila y columna;
- consulta, parámetros y entorno utilizados;
- transformaciones de minimización;
- conteos antes y después de cada filtro;
- riesgos residuales y usos desaconsejados;
- licencia del derivado y límites impuestos por la fuente;
- contacto y procedimiento de corrección o retirada.

Para sistemas que necesitan intercambiar procedencia de forma estructurada, [W3C PROV-O](https://www.w3.org/TR/prov-o/) ofrece un vocabulario para representar entidades, actividades y agentes. No hace falta desplegar RDF para aplicar la idea esencial: distinguir el recurso original, la actividad que creó el extracto y el artefacto resultante.

### 7. Calcula hashes después de construir el paquete

Genera los hashes sobre los ficheros finales, no sobre versiones intermedias:

```bash
sha256sum data/expedientes_revision.csv \
  schema/tabla.schema.json \
  scripts/construir_extracto.sql \
  > checksums.sha256
sha256sum -c checksums.sha256
```

El manifiesto de hashes permite comprobar integridad durante la transferencia. Para vincular una publicación con una versión concreta, registra además un identificador de versión, fecha y, si procede, commit o depósito persistente. Si cambia la fuente o la lógica, crea una versión nueva y conserva una nota de cambios; no sobrescribas silenciosamente el resultado anterior.

### 8. Haz una revisión adversarial y una reconstrucción limpia

Antes de publicar, asigna a una persona o rol distinto dos tareas:

- **revisión de privacidad**: intentar detectar rutas razonables de reidentificación, datos incidentales y vínculos innecesarios;
- **revisión de reproducibilidad**: reconstruir el extracto desde las fuentes fijadas siguiendo solo el paquete y comprobar filas, esquema y hashes.

Si no hay segundo revisor, automatiza controles y realiza la reconstrucción en un directorio limpio, pero deja constancia de la limitación. Una ejecución exitosa no sustituye la revisión del propósito ni del riesgo.

## Limitaciones y falsos positivos

### El extracto puede conservar el sesgo del corpus

Una selección reproducible puede repetir omisiones, errores y desigualdades de la fuente. El paquete debe declarar cobertura y no convertir «no aparece» en «no existe». Si el portal cambia registros históricos sin versionado, un hash antiguo demuestra qué se analizó, pero no explica por qué cambió.

### La rareza no demuestra relevancia

Filtrar importes extremos, fechas próximas o entidades repetidas crea señales de revisión, no pruebas de conducta impropia. Las reglas deben validarse con expedientes primarios y alternativas inocentes. Publicar una tabla ordenada por una puntuación puede amplificar una sospecha mucho más allá de la fuerza de la evidencia.

### La utilidad y la privacidad cambian con el tiempo

Nuevos datasets pueden hacer identificable un extracto que antes no lo parecía. A la inversa, una fuente retirada puede romper la posibilidad de verificación. Define una fecha de revisión, monitoriza cambios relevantes y conserva capacidad de retirar o reemplazar el paquete sin borrar el historial de correcciones.

### Un esquema no contiene toda la semántica

Declarar una columna como `date` o `number` no explica la zona horaria, el hecho que representa, la política de redondeo ni si un nulo significa «desconocido», «no aplicable» o «suprimido». Añade descripciones humanas y ejemplos ficticios; valida restricciones mecánicas por separado.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja solo con fuentes públicas o datos para los que exista autorización y finalidad legítima.
- No publiques información de contacto, ubicaciones precisas o identificadores personales porque «ya estaban en la fuente».
- Mantén separadas las claves de seudonimización y nunca las incluyas en el paquete público.
- Evita hashes sin secreto de valores predecibles como correos o teléfonos: pueden invertirse mediante prueba de candidatos.
- Limpia metadatos, rutas locales, nombres de usuario, historial de hojas de cálculo y ficheros temporales.
- No subas el corpus a servicios externos de análisis sin revisar autorización, residencia de datos y retención.
- Cifra las entregas restringidas y limita accesos por función y tiempo.
- Publica criterios y limitaciones junto a las señales; ofrece un canal de corrección y retirada.
- No uses códigos estables para construir perfiles longitudinales si la finalidad no lo exige.
- Reevalúa el riesgo cuando se añadan fuentes, columnas o destinatarios.

## Checklist operativo

- [ ] La afirmación, audiencia y finalidad están escritas.
- [ ] Se ha elegido el modelo de acceso menos revelador que conserva utilidad.
- [ ] Los originales tienen origen, fecha, licencia, tamaño y hash.
- [ ] Cada fila y columna del extracto tiene una justificación.
- [ ] Identificadores directos, cuasi-identificadores y texto libre han sido revisados.
- [ ] La seudonimización no se presenta como anonimización.
- [ ] Inclusiones, exclusiones, nulos, uniones y denominadores se han probado.
- [ ] Consulta, parámetros, esquema y entorno están versionados.
- [ ] El paquete se reconstruye desde una copia limpia.
- [ ] Los hashes corresponden a los artefactos finales.
- [ ] Metadatos, temporales, secretos y tablas de correspondencia quedan fuera.
- [ ] Riesgos residuales, licencia y política de corrección están documentados.
- [ ] Existe fecha de revisión, caducidad o criterio de retirada.

## Alternativas y siguientes pasos

Un extracto fila a fila no siempre es la mejor salida. Una tabla agregada puede responder a la pregunta con menos riesgo; un informe con ejemplos ficticios puede explicar el método; una API puede limitar consultas y aplicar controles; un enclave o sala de datos permite revisión bajo acceso restringido; los datos sintéticos sirven para demostrar una estructura, aunque no sustituyen los valores reales al verificar una conclusión concreta.

La decisión debe partir de la finalidad y del adversario razonable, no del formato favorito del equipo. CSV facilita inspección, Parquet conserva tipos y mejora análisis columnares, y una base consultable puede servir a revisores; ninguno resuelve por sí solo la minimización, la procedencia o el riesgo de reidentificación.

El takeaway práctico es este: **publica una prueba revisable de tu afirmación, no una copia automática de todo lo que tuviste que analizar**. Define primero qué debe comprobar el lector, conserva la consulta y el vínculo con las fuentes, elimina lo que no aporta a esa comprobación y prueba el paquete tanto por reproducibilidad como por riesgo de divulgación. Como siguiente tema, convendría estudiar cómo versionar y corregir extractos ya citados sin romper los enlaces ni ocultar qué conclusiones cambiaron.

## Fuentes oficiales consultadas

- [Comisión Europea: principios del tratamiento de datos personales](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en)
- [Comisión Europea: datos personales, seudonimización y protección](https://commission.europa.eu/law/law-topic/data-protection/data-protection-explained_en)
- [EDPB: anonimización y seudonimización](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en)
- [NIST SP 800-188: De-Identifying Government Datasets](https://www.nist.gov/publications/de-identifying-government-datasets-techniques-and-governance)
- [Frictionless Data: especificación Data Package](https://specs.frictionlessdata.io/data-package/)
- [Frictionless Data: especificación Data Resource](https://specs.frictionlessdata.io/data-resource/)
- [W3C: PROV-O](https://www.w3.org/TR/prov-o/)
