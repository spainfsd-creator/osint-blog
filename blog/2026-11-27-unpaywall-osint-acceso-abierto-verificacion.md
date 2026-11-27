---
title: "Unpaywall en OSINT: localizar acceso abierto sin confundir disponibilidad con validez"
slug: /unpaywall-osint-acceso-abierto-verificacion
authors: [osint-writter]
tags: [osint, research, verification, data, tooling, privacy]
date: 2026-11-27
image: /img/blog/2026-11-27-unpaywall-osint-acceso-abierto.png
aiDisclosure: generated
humanReviewed: false
---

Una empresa respalda una afirmación comercial con «un estudio científico», pero el enlace conduce a una página de pago. Una búsqueda devuelve un preprint, un manuscrito aceptado en un repositorio y una copia editorial aparentemente libre. Los tres parecen resolver el problema; ninguno demuestra por sí solo que estemos leyendo **la misma versión, con la misma licencia y antes o después de una corrección**. En investigación de fuentes abiertas, encontrar un PDF es solo el comienzo: hay que identificar el objeto, la versión y su procedencia.

![Analista comparando versiones y procedencias de una publicación académica disponible en varios repositorios](/img/blog/2026-11-27-unpaywall-osint-acceso-abierto.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [Unpaywall](https://unpaywall.org/) para localizar copias de acceso abierto de publicaciones con DOI y convertirlas en pistas verificables. La empresa, el producto y el expediente del ejemplo son ficticios. El objetivo no es eludir suscripciones ni redistribuir contenido sin permiso, sino encontrar ubicaciones legales declaradas por editoriales y repositorios, revisar sus diferencias y volver a la fuente primaria antes de publicar una conclusión.

## Qué es Unpaywall y para qué sirve en OSINT

Unpaywall mantiene una base de datos que relaciona recursos identificados por DOI con ubicaciones de acceso abierto. Según su documentación, obtiene información de revistas y repositorios, además de fuentes como Crossref, DataCite, DOAJ y PubMed Central. Sus productos comparten un esquema: cada objeto DOI puede contener cero o más objetos de ubicación abierta, junto con una ubicación considerada preferente.

Para una investigación legítima, permite:

- comprobar si existe una copia abierta conocida para un DOI concreto;
- distinguir una ubicación alojada por la editorial de otra depositada en un repositorio;
- separar versión publicada, manuscrito aceptado y versión enviada;
- registrar URL, licencia, procedencia, fecha de actualización y evidencia de apertura;
- detectar que varias URLs conducen a versiones distintas del mismo trabajo;
- preparar una revisión posterior en la página editorial, el repositorio y los avisos de corrección;
- repetir una consulta mediante API o procesar una lista pequeña de DOI con la herramienta de consulta simple.

Unpaywall **no evalúa la calidad científica** del artículo. Tampoco certifica que una afirmación sea correcta, que la licencia cubra cualquier reutilización, que el fichero siga disponible o que una versión previa incorpore correcciones posteriores. Su función es mucho más concreta: describir ubicaciones abiertas que ha identificado para un recurso con DOI.

### Cinco objetos que conviene mantener separados

| Objeto | Pregunta | Qué puede aportar Unpaywall | Qué exige otra comprobación |
| --- | --- | --- | --- |
| DOI | ¿qué recurso estamos buscando? | identificador normalizado y metadatos básicos | que el DOI citado corresponda realmente a la afirmación |
| ubicación | ¿dónde hay una copia abierta? | URL de destino o PDF, host y evidencia | que la URL entregue hoy el fichero esperado |
| versión | ¿qué etapa del manuscrito es? | versión publicada, aceptada o enviada | diferencias materiales entre los textos |
| licencia | ¿qué reutilización se declara? | licencia detectada o ausencia de ella | interpretación jurídica y condiciones del documento |
| validez | ¿sostiene el estudio la conclusión? | nada por sí solo | lectura crítica, métodos, datos, correcciones y evidencia externa |

La regla práctica es sencilla: **el DOI enlaza identidades; la ubicación enlaza copias; el contenido sostiene —o no— la afirmación**. Saltar de la primera capa a la tercera produce informes muy seguros de sí mismos y muy difíciles de defender.

## Caso de uso legítimo: verificar una afirmación en una contratación pública

El ayuntamiento ficticio de **Valdemora del Río** estudia comprar un sistema para reducir el consumo energético de edificios. La memoria del proveedor afirma que «un ensayo universitario demuestra un ahorro del 35 %» y cita un DOI, pero no adjunta el estudio.

La pregunta de investigación no es «¿hay un PDF gratis?», sino:

> ¿Qué versión de la publicación citada estaba disponible al cerrarse la oferta y qué dice realmente sobre población, intervención, incertidumbre y limitaciones?

El analista recibe autorización para revisar el expediente y crea una tabla de control:

| Campo | Ejemplo ficticio |
| --- | --- |
| afirmación | «reduce un 35 % el consumo» |
| procedencia | memoria técnica, página 42 |
| DOI citado | `10.0000/valdemora.2026.0042` |
| fecha relevante | cierre de ofertas, 2026-10-30 |
| versión localizada | pendiente |
| correcciones o retractación | pendiente |
| conclusión | sin resolver |

El DOI es deliberadamente ficticio y no debe consultarse como si correspondiera a una obra real. En un caso auténtico se usaría el identificador publicado en el expediente, conservando siempre la página y el contexto en que apareció.

## Flujo recomendado, paso a paso

### 1. Conserva la afirmación antes de buscar

Guarda el documento original, la página, la cita exacta y la fecha. Calcula una huella si la política de custodia lo requiere. No reemplaces la frase del proveedor por el título del artículo: son objetos distintos y puede que la memoria exagere, simplifique o cite un resultado secundario.

Resuelve después el DOI mediante `https://doi.org/` y registra a qué página conduce. Un DOI persistente identifica un objeto, pero su página puede cambiar y sus metadatos pueden actualizarse. Conserva la fecha de observación.

### 2. Consulta por DOI, no por la historia que esperas encontrar

La API v2 ofrece una consulta de un recurso mediante `GET /v2/:doi`. La documentación exige incluir una dirección de correo en cada petición y pide limitar el uso a 100.000 llamadas diarias. Para una comprobación puntual, la forma general es:

```bash
curl --get \
  --data-urlencode 'email=analista@example.org' \
  'https://api.unpaywall.org/v2/DOI_CODIFICADO'
```

Sustituye el correo y el DOI por valores adecuados a tu organización y codifica correctamente la ruta. No pegues listas sensibles en servicios externos. Para unos pocos DOI, [Simple Query Tool](https://unpaywall.org/products/simple-query-tool) acepta hasta 500 identificadores y devuelve CSV y JSON Lines; para un flujo recurrente, documenta volumen, finalidad, retención y responsable.

Hay un cambio temporal importante: el endpoint de búsqueda textual de Unpaywall fue retirado el **18 de septiembre de 2026** y devuelve `410 Gone`. La documentación deriva esa búsqueda a OpenAlex. Por tanto, un tutorial que siga proponiendo `/v2/search` está desactualizado; la consulta por DOI de la API v2 continúa siendo el camino documentado para recuperar el objeto correspondiente.

### 3. Guarda la respuesta bruta y extrae solo lo necesario

Registra al menos:

- `doi` y `doi_url`;
- `is_oa` y `oa_status`;
- `best_oa_location`;
- todas las entradas de `oa_locations`;
- `host_type`, `version`, `license` y URLs de cada ubicación;
- `updated` y momento local de la consulta;
- campos nulos, errores y código HTTP.

No fijes tu parser al número exacto de campos. La documentación avisa de que pueden añadirse campos nuevos y de que los marcados como beta pueden cambiar. Conserva el JSON original y transforma una copia para el análisis.

Una tabla minimizada podría quedar así:

| ubicación | host | versión declarada | licencia | comprobación manual |
| --- | --- | --- | --- | --- |
| editorial | `publisher` | publicada | CC BY | abre y coincide |
| repositorio institucional | `repository` | aceptada | no indicada | abre; faltan anexos |
| repositorio temático | `repository` | enviada | CC BY-NC | texto anterior al arbitraje |

La ausencia de licencia no equivale a permiso de reutilización, y una licencia detectada no demuestra que todos los materiales suplementarios estén cubiertos por ella.

### 4. No conviertas `best_oa_location` en un veredicto

Unpaywall elige una ubicación preferente mediante un algoritmo que prioriza, entre otros criterios, contenido alojado por la editorial, versiones más próximas a la versión de registro y determinados repositorios. Es una ayuda de navegación, no una puntuación de credibilidad.

Revisa **todas** las ubicaciones plausibles cuando la diferencia de versión pueda afectar al caso. La copia publicada puede incluir figuras, correcciones o material suplementario ausente en el manuscrito aceptado. A la inversa, un repositorio puede conservar una versión accesible cuando la página editorial cambia.

Para cada URL:

1. abre la página de aterrizaje antes de descargar;
2. identifica repositorio, editor y dominio;
3. comprueba título, autores, DOI y fecha;
4. anota cómo se etiqueta la versión;
5. registra licencia y cualquier embargo;
6. calcula la huella del fichero si debes comparar copias;
7. evita ejecutar contenido activo o macros innecesarias.

### 5. Compara versiones por contenido, no solo por tamaño

Dos PDF con el mismo título pueden diferir en paginación, figuras, tablas, apéndices o conclusiones. Extrae texto en un entorno controlado y compara secciones relevantes, manteniendo siempre los originales.

En el caso ficticio, el manuscrito enviado informa de una reducción media preliminar del 35 %, pero la versión publicada añade el intervalo de incertidumbre y limita el resultado a edificios con una configuración concreta. El hallazgo defendible no sería «el proveedor mintió» ni «el producto funciona», sino algo más preciso:

> La cifra de la oferta coincide con una estimación preliminar, pero omite las condiciones y la incertidumbre presentes en la versión publicada consultada en esta fecha.

Esa conclusión exige leer los documentos. Unpaywall solo ayudó a localizarlos y a ordenar sus ubicaciones.

### 6. Busca correcciones, retractaciones y material asociado

Vuelve a la página editorial y consulta las relaciones del DOI en Crossref, Crossmark u otras fuentes pertinentes. Comprueba:

- correcciones, expresiones de preocupación o retractaciones;
- versiones posteriores del registro;
- anexos, datos y código citados;
- protocolo, preregistro o informe de revisión cuando existan;
- conflicto de interés y financiación declarada;
- fecha en la que cada elemento estuvo disponible.

No deduzcas que `is_oa: true` significa «vigente», «revisado por pares» o «reutilizable sin condiciones». Tampoco conviertas `is_oa: false` en prueba de inexistencia: puede haber una copia que todavía no esté indexada, un DOI incorrecto o un repositorio fuera de cobertura.

### 7. Redacta por capas de evidencia

Separa en el informe:

1. **observación:** la respuesta de Unpaywall y las ubicaciones devueltas;
2. **verificación:** qué entregó cada URL y cómo se identificó la versión;
3. **comparación:** diferencias relevantes entre copias;
4. **corroboración:** estado editorial, datos y fuentes independientes;
5. **inferencia:** qué puede concluirse y con qué incertidumbre.

Incluye fecha, consulta, respuesta, hashes cuando sean proporcionales y una ruta para corregir el informe. Una URL abierta hoy puede desaparecer mañana; una captura sin procedencia tampoco basta.

## Limitaciones y falsos positivos

### La cobertura depende del DOI y de fuentes estructuradas

Unpaywall se orienta a recursos académicos con DOI. Informes técnicos, capítulos antiguos, literatura gris o documentos sin identificador pueden quedar fuera aunque exista una copia legítima. Las páginas personales son más difíciles de indexar de manera fiable que los repositorios estructurados.

### Abierto no significa idéntico

El preprint, el manuscrito aceptado y la versión de registro pueden responder a etapas distintas. Incluso dos ficheros etiquetados de la misma manera pueden variar. Si una cifra o una frase es decisiva, compárala directamente.

### Los estados cambian

Nuevos depósitos, fin de embargos y cambios en páginas editoriales modifican la disponibilidad. La documentación del Data Feed explica que los registros cambian diariamente; una instantánea histórica y una consulta actual no tienen por qué coincidir.

### Los metadatos también contienen errores

DOI mal copiados, licencias ausentes, URLs rotas y clasificaciones imperfectas son posibles. La ubicación «mejor» es una elección algorítmica. Un resultado negativo no demuestra que no exista acceso legítimo, y un resultado positivo no sustituye la inspección del fichero.

### La apertura no valida el estudio

Acceso abierto describe disponibilidad y condiciones, no rigor metodológico. El trabajo puede tener sesgos, una muestra inadecuada, financiación relevante, análisis débiles o una retractación posterior. La lectura crítica sigue siendo imprescindible.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa Unpaywall para encontrar copias legales; no para sortear controles de acceso ni redistribuir ficheros sin permiso.
- Consulta DOI, no nombres de personas o historias sensibles, cuando el identificador resuelva la tarea.
- Recuerda que la API recibe DOI, correo e IP; utiliza una dirección funcional adecuada y revisa la política de privacidad.
- No envíes listados internos de lecturas, expedientes confidenciales o intereses sensibles sin evaluar el riesgo.
- Minimiza y protege respuestas, PDFs y notas; que un artículo sea público no vuelve públicas tus hipótesis.
- Abre documentos en un entorno actualizado y evita macros, enlaces o adjuntos no necesarios.
- Conserva la licencia exacta de cada copia y distingue acceso de permiso de reutilización.
- No infieras identidad, afiliación actual o intención a partir de una autoría aislada.
- Comunica incertidumbre y corrige el informe si cambia la versión o aparece una actualización editorial.
- Respeta límites, condiciones y recursos del servicio; para grandes volúmenes usa el producto adecuado en vez de recorrer el espacio de DOI mediante la API.

## Checklist antes de citar una copia abierta

- [ ] La afirmación original, su página y su fecha están conservadas.
- [ ] El DOI se resolvió y corresponde al objeto citado.
- [ ] La consulta y la respuesta de Unpaywall son reproducibles.
- [ ] Se revisaron todas las ubicaciones relevantes, no solo `best_oa_location`.
- [ ] Host, versión, licencia y fecha están documentados por separado.
- [ ] El fichero descargado coincide en título, autores y DOI.
- [ ] Las diferencias entre preprint, manuscrito aceptado y versión publicada se compararon.
- [ ] Se buscaron correcciones, retractaciones, anexos, datos y código.
- [ ] La conclusión procede del contenido, no del estado de acceso abierto.
- [ ] Un resultado negativo se expresa como ausencia en la cobertura consultada.
- [ ] Los datos de consulta y los documentos se almacenan con retención proporcional.
- [ ] La redacción permite actualizar o retirar la conclusión.

## Alternativas y siguientes pasos

OpenAlex permite buscar obras y ofrece campos de acceso abierto y ubicaciones; Crossref y DataCite ayudan a resolver metadatos y relaciones de DOI; DOAJ aporta contexto sobre revistas de acceso abierto; CORE y BASE facilitan el descubrimiento en repositorios; los repositorios institucionales y la página editorial siguen siendo esenciales para comprobar el fichero real. Ninguna fuente tiene cobertura perfecta ni convierte una coincidencia en validación científica.

Unpaywall destaca como **puente reproducible entre un DOI y sus posibles copias legales**. Su valor OSINT no está en declarar verdadero un estudio, sino en hacer visible qué versión estamos leyendo, dónde apareció y qué debemos comprobar después.

El takeaway práctico es este: **usa Unpaywall para encontrar la puerta, pero identifica la versión, revisa la licencia y lee el documento antes de cruzarla con una conclusión**. Como ejercicio, toma tres DOI de publicaciones propias o autorizadas, compara todas sus ubicaciones y registra qué cambiaría en tu informe si solo hubieras leído la ubicación preferente. El siguiente paso natural sería diseñar un protocolo para detectar y revisar cambios de versión en una bibliografía viva sin volver a evaluar desde cero todo el corpus.

## Fuentes y documentación

- [Unpaywall: REST API](https://data.unpaywall.org/products/api)
- [Unpaywall: formato y esquema de datos](https://unpaywall.org/data-format)
- [Unpaywall: preguntas frecuentes y fuentes](https://data.unpaywall.org/faq)
- [Unpaywall: Simple Query Tool](https://unpaywall.org/products/simple-query-tool)
- [Unpaywall: guía para investigación](https://unpaywall.org/user-guides/research)
- [Unpaywall: Data Feed y cambios de disponibilidad](https://unpaywall.org/products/data-feed)
- [Unpaywall: política de privacidad](https://unpaywall.org/legal/privacy)
