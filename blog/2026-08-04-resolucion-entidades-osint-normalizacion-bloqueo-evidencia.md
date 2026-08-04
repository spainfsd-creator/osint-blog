---
title: "Resolución de entidades en OSINT: normalización, bloqueo y evidencia sin fusionar homónimos"
slug: /resolucion-entidades-osint-normalizacion-bloqueo-evidencia
authors: [osint-writter]
tags: [osint, investigation, verification, data, methodology, privacy]
date: 2026-08-04
image: /img/blog/2026-08-04-resolucion-entidades-osint.png
---

![Ilustración editorial de una analista OSINT comparando registros, alias, identificadores y contradicciones en una matriz explicable](/img/blog/2026-08-04-resolucion-entidades-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/resolucion-entidades-osint-normalizacion-bloqueo-evidencia.m4a)


Dos listas públicas contienen a `Aleksandar Petrović`. Una añade un segundo apellido; otra translitera el nombre como `Aleksandr Petrovic`. Comparten país, pero las fechas de nacimiento no encajan y solo uno de los registros tiene identificador oficial. Un buscador difuso puede devolver una puntuación alta. Una investigación responsable debe hacer algo bastante más difícil: **explicar por qué compara ambos registros, qué datos apoyan la unión, qué datos la contradicen y cuándo debe negarse a fusionarlos**.

<!-- truncate -->

La resolución de entidades —también llamada *entity resolution* o *record linkage*— sirve para decidir si dos registros describen a la misma persona, empresa, buque u objeto. No es una máquina de producir identidades. Es un proceso de reducción de incertidumbre que necesita datos proporcionados, reglas documentadas y revisión humana, especialmente si una coincidencia puede provocar una acusación, un bloqueo o cualquier otra decisión adversa.

Todos los nombres, organizaciones e identificadores del ejemplo son ficticios.

## Qué es la resolución de entidades y para qué sirve

En OSINT rara vez recibimos una identidad limpia y universal. Una misma organización puede aparecer con razón social, marca, abreviatura, nombre traducido y denominaciones antiguas. Una persona puede figurar con varios alfabetos, orden de apellidos distinto, iniciales o fechas incompletas. Al mismo tiempo, dos sujetos diferentes pueden compartir nombre y país.

Resolver entidades consiste en comparar registros y clasificarlos, como mínimo, en tres grupos:

- **coincidencia confirmada**, respaldada por identificadores o un conjunto robusto de señales compatibles;
- **posible coincidencia**, que merece revisión pero conserva contradicciones o campos desconocidos;
- **no coincidencia**, porque existen incompatibilidades suficientes o falta una base razonable para unirlos.

La distinción entre deduplicación y enlace también ayuda. La **deduplicación** busca copias de una entidad dentro de una misma colección. El **enlace de registros** cruza colecciones distintas. En ambos casos el error más peligroso suele ser el mismo: tratar similitud textual como identidad.

Herramientas como [Splink](https://moj-analytical-services.github.io/splink/) implementan enlace probabilístico a escala y explican el modelo de Fellegi-Sunter que sustenta su metodología. [Dedupe](https://docs.dedupe.io/en/stable/) aprende pesos y reglas de bloqueo a partir de pares etiquetados por personas. [OpenSanctions](https://www.opensanctions.org/matcher/) documenta un enfoque basado en señales explicables: una coincidencia de nombre puede verse reforzada por identificadores compatibles o penalizada por fechas, países y otros atributos contradictorios. Ninguna de estas herramientas elimina la necesidad de conocer los datos y validar el resultado.

## Caso de uso legítimo: cruzar dos listas de proveedores

Imaginemos que una ONG revisa la integridad de sus proveedores antes de renovar contratos. La lista interna contiene a `Aurora Logística del Norte SL`, con NIF ficticio `ES-B00000014`, domicilio mercantil en León y fecha de constitución en 2019. Una fuente pública devuelve estos candidatos:

| Candidato | Nombre | Identificador | País | Fecha | Primera lectura |
|---|---|---|---|---|---|
| `P-01` | Aurora Logistica Norte S.L. | `ES-B00000014` | ES | 2019 | Identificador y contexto compatibles |
| `P-02` | Aurora Logística del Norte SA | `ES-A00000481` | ES | 1998 | Nombre cercano, identificador incompatible |
| `P-03` | Aurora North Logistics Ltd | desconocido | GB | desconocida | Traducción plausible, evidencia insuficiente |

`P-01` es un candidato fuerte, pero todavía hay que volver al registro oficial y comprobar que el identificador no fue copiado por una fuente secundaria. `P-02` no debe fusionarse solo porque el nombre se parezca: el tipo societario, el identificador y la cronología contradicen la unión. `P-03` queda sin resolver; traducir palabras no demuestra relación jurídica.

La pregunta útil no es «¿qué porcentaje de similitud tienen los nombres?», sino esta:

> ¿Qué combinación de identificadores, atributos, fechas y fuentes permite confirmar, mantener abierta o descartar cada hipótesis de identidad?

## Flujo recomendado paso a paso

### 1. Define la entidad, la decisión y el coste del error

Antes de comparar, fija el tipo de entidad y el uso del resultado. No se ponderan igual una empresa y una persona; tampoco una tarea de limpieza interna y una comprobación que puede suspender un pago.

Escribe dos riesgos por separado:

- **falso positivo**: fusionar sujetos distintos;
- **falso negativo**: dejar separados registros de la misma entidad.

Cuanto mayor sea el impacto sobre una persona u organización, más conservador debe ser el umbral automático y más clara la revisión humana.

### 2. Conserva el dato original y normaliza en columnas nuevas

Nunca sustituyas la evidencia por su versión limpia. Guarda el valor original, la fuente, la fecha de acceso y cada transformación aplicada. Después crea campos derivados para comparar:

- mayúsculas y minúsculas uniformes;
- espacios y puntuación normalizados;
- formas societarias separadas del nombre base;
- fechas expresadas en un formato común;
- países codificados de manera consistente;
- alias y transliteraciones conservados como valores distintos;
- identificadores sin separadores ornamentales, pero con su esquema y jurisdicción.

Eliminar tildes puede ayudar a generar candidatos; no autoriza a borrar la grafía original. Traducir o transliterar también introduce decisiones. Registra qué sistema utilizaste y conserva ambas formas.

### 3. Genera candidatos con reglas de bloqueo

Comparar cada registro con todos los demás crece rápidamente y produce ruido. El **bloqueo** reduce el espacio de pares: solo compara registros que cumplen al menos una regla preliminar. La [documentación de Splink sobre reglas de bloqueo](https://moj-analytical-services.github.io/splink/topic_guides/blocking/blocking_rules.html) recalca que los pares candidatos son los que satisfacen alguna de esas reglas.

Para empresas ficticias podríamos proponer bloques como:

1. mismo identificador registral normalizado;
2. mismo país y primeros tokens significativos del nombre;
3. mismo dominio corporativo aportado por una fuente oficial;
4. nombre transliterado compatible y mismo año de constitución.

Usa varias reglas complementarias. Una demasiado estricta puede perder cambios de nombre; una demasiado amplia recrea casi todas las comparaciones y multiplica falsos positivos. La [guía de Dedupe sobre comparaciones y bloqueo](https://docs.dedupe.io/en/latest/how-it-works/Making-smart-comparisons.html) muestra precisamente que combinar predicados sirve para construir bloques más útiles para cada conjunto de datos.

### 4. Compara señales, no solo cadenas

Para cada par candidato construye una matriz visible:

| Señal | Estado | Fuerza orientativa | Motivo |
|---|---|---|---|
| Identificador oficial | coincide | muy alta | Es específico del esquema y la jurisdicción |
| Nombre normalizado | parecido | media | Puede variar o compartirse |
| Fecha de constitución | coincide | media-alta | Refuerza, pero una fuente puede estar desactualizada |
| País | coincide | baja-media | Millones de entidades lo comparten |
| Tipo societario | contradice | media | Puede indicar otra entidad o una transformación jurídica |
| Domicilio | desconocido | ninguna | La ausencia no equivale a contradicción |

Separa siempre **coincidencia**, **contradicción**, **ausencia** y **dato no comparable**. Un campo vacío no debería recibir el mismo tratamiento que dos identificadores oficiales incompatibles.

El enfoque probabilístico de [Fellegi-Sunter explicado por Splink](https://moj-analytical-services.github.io/splink/topic_guides/theory/fellegi_sunter.html) asigna más peso a acuerdos raros y discriminantes que a acuerdos comunes. También parte de supuestos que deben revisarse, como la independencia entre comparaciones. En la práctica, nombre, domicilio y país pueden estar correlacionados; una puntuación no debe presentarse como una probabilidad infalible si el modelo no está calibrado para esos datos.

### 5. Aprende y calibra con pares representativos

Si usas aprendizaje automático, etiqueta ejemplos reales del dominio: coincidencias fáciles, homónimos, cambios de razón social, transliteraciones y casos fronterizos. `Dedupe` utiliza ejemplos humanos para aprender pesos y reglas, mientras que OpenSanctions publica información sobre sus [datos de entrenamiento de pares](https://www.opensanctions.org/docs/opensource/pairs/), lo que ilustra el valor de conservar juicios trazables.

Divide los pares etiquetados para entrenar y evaluar. Mide por separado precisión y exhaustividad; una única cifra puede ocultar que el sistema encuentra muchas coincidencias a costa de unir inocentes. Revisa además resultados por idioma, alfabeto, país, calidad de la fuente y tipo de entidad.

### 6. Decide con zonas, no con un umbral mágico

Una política sencilla puede usar tres zonas:

- **alta confianza**: pasa a verificación de fuente primaria antes de fusionar;
- **revisión manual**: un analista inspecciona señales y contradicciones;
- **rechazo provisional**: no se fusiona, aunque el par puede conservarse para auditoría.

Los límites deben calibrarse con datos etiquetados y con el coste del error del caso. La [guía de ajuste de OpenSanctions](https://www.opensanctions.org/docs/api/tuning/) recuerda que un flujo de *matching* no se comporta como una búsqueda de texto: devolver una larga lista de resultados no es necesariamente útil. Registra el algoritmo, la configuración y el umbral utilizados en cada ejecución.

### 7. Verifica en la fuente primaria y deja una pista de auditoría

Antes de afirmar que dos registros son la misma entidad:

1. abre el documento o registro primario;
2. comprueba el significado y la vigencia de los identificadores;
3. conserva URL, fecha de consulta y, cuando sea proporcionado, una copia o hash;
4. documenta qué señales resolvieron el caso;
5. registra quién revisó la decisión y cuándo;
6. permite separar de nuevo una unión errónea.

Una tabla final debería incluir `registro_a`, `registro_b`, `decisión`, `señales_a_favor`, `contradicciones`, `campos_desconocidos`, `fuentes`, `fecha`, `regla_o_modelo` y `revisor`. La explicación es parte del resultado, no una decoración posterior.

## Limitaciones y falsos positivos

### Los nombres no son identificadores

Distancias de edición, similitud fonética y solapamiento de tokens detectan variantes útiles, pero también acercan homónimos. Los nombres muy frecuentes requieren más evidencia, no menos. Un alias encontrado en una base agregada debe rastrearse hasta su procedencia.

### Los identificadores también necesitan contexto

Un número puede estar mal copiado, reciclado, truncado o pertenecer a otro esquema. Guarda prefijo, jurisdicción, tipo y fuente. Dos valores distintos pueden demostrar incompatibilidad; un valor idéntico en una web secundaria no confirma por sí solo la identidad.

### El tiempo cambia las entidades

Empresas que se fusionan, cambian de nombre o trasladan domicilio no son simples duplicados. Modela intervalos de validez y relaciones como `antes llamada`, `absorbida por` o `filial de`, en lugar de colapsar toda la historia en una sola fila.

### Los datos etiquetados heredan sesgos

Un modelo entrenado sobre nombres occidentales o registros completos puede rendir peor con otros alfabetos, convenciones patronímicas o campos ausentes. Evalúa subgrupos relevantes y crea una vía de revisión y corrección. No conviertas una baja calidad de datos en sospecha sobre el sujeto.

## Buenas prácticas de OPSEC, ética y privacidad

- Trata solo los datos necesarios para una finalidad legítima y documentada.
- Evita enriquecer perfiles personales por curiosidad o buscar familiares para completar huecos.
- Separa el entorno de pruebas del expediente real y usa datos sintéticos al diseñar reglas.
- Restringe acceso, retención y exportación de identificadores personales.
- No envíes datos sensibles a servicios externos sin base legal, autorización y evaluación del proveedor.
- Mantén revisión humana antes de decisiones adversas y un canal para corregir errores.
- Informa con grados de confianza y enumera las contradicciones, no solo la puntuación final.
- Conserva la procedencia de cada atributo y respeta licencias, términos de uso y límites de consulta.

## Alternativas y siguientes pasos

La herramienta depende del volumen y del tipo de problema:

- una hoja de cálculo y una matriz explícita pueden bastar para decenas de pares;
- `OpenRefine` ayuda a normalizar, agrupar y reconciliar datos con revisión visual;
- `Dedupe` resulta útil cuando se dispone de ejemplos humanos representativos;
- `Splink` permite construir enlace probabilístico reproducible sobre conjuntos grandes;
- `OpenSanctions` ofrece señales y algoritmos orientados a entidades de listas de interés, pero sus resultados deben volver a las fuentes originales;
- identificadores sectoriales como `LEI`, `IMO`, `DOI` u `ORCID` ayudan cuando su ámbito encaja y su procedencia está verificada.

No empieces por la plataforma. Empieza por el daño que causaría una unión errónea, los campos realmente disponibles y la evidencia mínima que aceptarás.

## Checklist antes de fusionar dos registros

- [ ] El tipo de entidad y la finalidad del cruce están definidos.
- [ ] Se conservaron valores originales, fuentes y fechas.
- [ ] Normalización y transliteración son reproducibles.
- [ ] Las reglas de bloqueo no dependen de una única grafía.
- [ ] Coincidencias, contradicciones y ausencias se puntuaron por separado.
- [ ] Los umbrales se calibraron con pares representativos.
- [ ] Se revisaron sesgos por idioma, país y calidad de datos.
- [ ] La fuente primaria confirma los identificadores decisivos.
- [ ] Una persona revisó los casos de impacto alto o ambiguos.
- [ ] La decisión puede auditarse, corregirse y deshacerse.

## Fuentes consultadas

- [Splink: documentación y guía de inicio](https://moj-analytical-services.github.io/splink/)
- [Splink: reglas de bloqueo](https://moj-analytical-services.github.io/splink/topic_guides/blocking/blocking_rules.html)
- [Splink: modelo de Fellegi-Sunter](https://moj-analytical-services.github.io/splink/topic_guides/theory/fellegi_sunter.html)
- [Dedupe: documentación estable](https://docs.dedupe.io/en/stable/)
- [Dedupe: comparaciones y reglas de bloqueo](https://docs.dedupe.io/en/latest/how-it-works/Making-smart-comparisons.html)
- [OpenSanctions: algoritmos de matching](https://www.opensanctions.org/matcher/)
- [OpenSanctions: ajuste del algoritmo](https://www.opensanctions.org/docs/api/tuning/)

La takeaway accionable es esta: **una coincidencia de nombre genera un candidato; una identidad exige señales compatibles, contradicciones resueltas y procedencia verificable**. Para practicar, toma dos pequeñas tablas sintéticas, conserva sus valores originales y construye primero la matriz de decisión a mano. El siguiente paso natural será medir la calidad del enlace con un conjunto de referencia sin esconder los errores detrás de una puntuación media.
