---
title: "Open Measures en OSINT: estudiar actividad pública sin confundir volumen con coordinación"
slug: /open-measures-osint-actividad-publica-contexto
authors: [osint-writter]
tags: [osint, socmint, verification, methodology, data, privacy]
date: 2026-11-26
image: /img/blog/2026-11-26-open-measures-osint-actividad-publica.png
aiDisclosure: generated
humanReviewed: false
---

Una campaña vecinal denuncia que un mismo relato apareció de golpe en varias plataformas públicas. Un gráfico enseña un pico enorme, una tabla enumera cuentas muy activas y varias publicaciones repiten enlaces parecidos. La historia parece cerrada: «hubo coordinación». Pero quizá cambió la cobertura del archivo, una consulta mezcló idiomas, una cuenta reenvió contenido ajeno o diez mensajes proceden de una sola conversación. **Medir actividad ayuda a formular hipótesis; no demuestra por sí solo coordinación, autoría ni impacto.**

![Analista revisando consultas, cronologías, procedencia y huecos de cobertura en actividad pública](/img/blog/2026-11-26-open-measures-osint-actividad-publica.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/open-measures-osint-actividad-publica-contexto.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [Open Measures](https://openmeasures.io/) para investigar cómo circula un tema en contenido públicamente accesible. La campaña, las organizaciones, las expresiones y los resultados del ejemplo son ficticios. El objetivo no es vigilar personas, buscar grupos privados ni elaborar listas de adversarios, sino comparar señales agregadas con consultas reproducibles, cobertura explícita y corroboración independiente.

## Qué es Open Measures y para qué sirve en OSINT

Open Measures es una plataforma de investigación de medios sociales e inteligencia de amenazas centrada en contenido público. Su aplicación pública ofrece herramientas de búsqueda, cronología, recuento de enlaces y actividad; la API pública permite consultar los datos en JSON y trabajar con mayor precisión sobre campos concretos.

La utilidad metodológica está en combinar dos niveles:

- una interfaz para explorar términos, intervalos y plataformas;
- datos estructurados para conservar la consulta, revisar resultados y repetir el análisis.

La [documentación de la aplicación pública](https://docs.openmeasures.io/docs/guides/public-app) distingue búsquedas básicas, booleanas y avanzadas. La básica busca términos en el campo de contenido; la booleana combina expresiones; la avanzada puede consultar otros campos del documento. Esa progresión importa: ampliar el poder de la consulta también amplía el riesgo de obtener resultados convincentes por un filtro mal diseñado.

El acceso público tiene límites deliberados. A fecha de publicación, Open Measures indica un máximo de **39 consultas diarias por dirección IP** y muestra datos con **al menos seis meses de antigüedad**. No es, por tanto, un radar gratuito de tiempo real. Tampoco es una copia exhaustiva de cada plataforma: el plan público cubre un subconjunto de la biblioteca completa y cada fuente tiene campos, periodos y patrones de recolección propios.

Puede servir para:

- localizar publicaciones públicas que contienen una expresión;
- comparar la frecuencia de términos a lo largo del tiempo;
- observar qué enlaces aparecen dentro de un conjunto de resultados;
- detectar periodos que merecen una revisión cualitativa;
- contrastar variantes lingüísticas de una narrativa;
- exportar resultados agregados para documentar el análisis;
- construir una lista de hipótesis y pruebas discriminantes.

No permite concluir automáticamente que dos cuentas pertenecen a la misma persona, que una repetición fue coordinada, que un mensaje causó un comportamiento fuera de línea o que lo no encontrado nunca existió.

### Cinco capas que no conviene mezclar

| Capa | Pregunta | Evidencia adecuada | Error frecuente |
| --- | --- | --- | --- |
| colección | ¿qué pudo observar el sistema? | fuente, periodo, campos y notas de cobertura | llamar «Internet» a un subconjunto |
| consulta | ¿qué coincidencias pedimos? | cadena exacta, modo, filtros y fecha | cambiar términos hasta obtener el pico esperado |
| resultado | ¿qué documentos devolvió? | JSON o exportación conservada | tratar cada resultado como publicación independiente |
| patrón | ¿qué forma tiene la actividad? | serie temporal, denominador y muestra revisada | confundir volumen bruto con prevalencia |
| interpretación | ¿qué explicación resiste contraste? | fuentes originales y alternativas rivales | convertir correlación en coordinación |

Esta separación evita que la herramienta se convierta en un oráculo. Open Measures conserva y organiza observaciones; la conclusión sigue necesitando un argumento verificable.

## Caso de uso legítimo: comprobar la difusión de un relato público

La asociación ficticia **Observatorio del Estuario** estudia la conversación pública sobre el proyecto municipal también ficticio «Puerto Limpio». Durante una audiencia, varias personas afirman que la frase «dragado secreto» apareció de forma coordinada en distintas plataformas durante el verano de 2025.

La pregunta investigable no es «¿quién está detrás?», sino:

> ¿Cuándo y dónde aparece la expresión en las colecciones disponibles, qué variantes se observan y qué evidencia adicional sería necesaria para hablar de coordinación?

El equipo fija antes de buscar:

- un periodo compatible con la ventana histórica del acceso público;
- las plataformas realmente disponibles;
- la expresión exacta y variantes semánticas;
- idiomas y grafías relevantes;
- el evento externo que podría explicar un pico;
- criterios para revisar una muestra;
- explicaciones alternativas: noticia, republicación, cambio de cobertura o coincidencia.

Los nombres de campaña, cuentas, enlaces y cifras del ejercicio son inventados. No se intenta identificar a vecinos ni inferir su ideología. El objeto es una narrativa pública y el producto final será agregado.

## Flujo recomendado paso a paso

### 1. Define una afirmación que pueda fallar

«Hay mucha actividad» no es una hipótesis útil. Una formulación mejor sería: «la expresión exacta aparece en más de una plataforma durante el intervalo fijado y los primeros usos no se explican por una misma noticia pública».

Escribe también qué refutaría la hipótesis:

- que casi todos los resultados sean copias de un solo titular;
- que el pico coincida con un cambio documentado en la recolección;
- que las fechas representen ingestión y no publicación;
- que una plataforma concentre prácticamente todo el volumen;
- que la revisión manual revele homónimos o usos irónicos.

Una investigación que no puede perder siempre encontrará lo que esperaba.

### 2. Registra la cobertura antes de mirar el gráfico

Consulta la [guía de fuentes](https://docs.openmeasures.io/docs/guides/sources) para saber qué campo contiene el texto y cuál representa el usuario en cada colección. Los esquemas no son uniformes. La propia documentación advierte, por ejemplo, que el nombre asociado a un mensaje reenviado puede corresponder a quien lo reenvía y no a su autor original.

Crea una ficha por fuente:

| campo | valor que conviene conservar |
| --- | --- |
| plataforma y parámetro API | nombre visible y valor técnico |
| periodo solicitado | inicio, fin y zona horaria |
| ventana observable | primer y último resultado hallado |
| campo de contenido | ruta usada por la consulta |
| campo temporal | significado documentado o pendiente |
| limitaciones | huecos, cambios y dudas conocidas |

La ausencia de resultados solo significa «no apareció en esta consulta sobre esta colección», no «nadie lo publicó».

### 3. Empieza con una consulta mínima y construye variantes

Usa primero la frase ficticia exacta:

```text
"dragado secreto"
```

Después crea familias explícitas, sin añadir términos retrospectivamente porque mejoran la gráfica:

```text
("dragado secreto" OR "dragado oculto") AND (puerto OR estuario)
```

Separa consultas por idioma cuando una traducción pueda cambiar el significado. Documenta inclusiones y exclusiones en una tabla:

| versión | cambio | motivo | efecto observado |
| --- | --- | --- | --- |
| Q1 | frase exacta | máxima precisión inicial | pendiente |
| Q2 | añade variante | sinónimo visto en documentos públicos | pendiente |
| Q3 | añade contexto | reduce homónimos | pendiente |

Las expresiones son ficticias y sirven para enseñar diseño de consultas, no para localizar a una persona o comunidad real.

### 4. Usa cada vista para una pregunta distinta

La [FAQ oficial](https://docs.openmeasures.io/docs/further-reading/faq) explica que las herramientas consultan los mismos conjuntos, pero los presentan de forma diferente:

- **Discover/Search** ayuda a leer resultados concretos y detectar usos distintos;
- **Timeline** muestra volumen a lo largo del tiempo;
- **Link Counter** agrega URL presentes en publicaciones coincidentes;
- **Activity** agrega qué cuentas publicaron más resultados compatibles.

No leas «Activity» como una clasificación de culpables. Una cuenta muy activa puede ser un medio, un archivo, un bot legítimo, un agregador o un usuario que discute la expresión para desmentirla. Un enlace frecuente puede ser la fuente criticada y no la apoyada.

### 5. Guarda la consulta y una respuesta estructurada

Para un análisis repetible, conserva como mínimo:

- URL o endpoint;
- parámetros en su orden lógico;
- fecha y hora de ejecución;
- periodo, intervalo y zona horaria;
- plataforma y modo de consulta;
- código de estado;
- respuesta bruta o exportación;
- huella criptográfica del archivo;
- versión de tu script o cuaderno;
- notas de cobertura vigentes ese día.

La [API pública](https://docs.openmeasures.io/docs/guides/public-api) devuelve el contenido bajo una estructura JSON y permite consultas más finas. Un esquema prudente de trabajo sería:

```python
import hashlib
import json
from pathlib import Path

# "respuesta" representa el JSON obtenido respetando la documentación y los límites.
raw = json.dumps(respuesta, ensure_ascii=False, sort_keys=True).encode()
Path("respuesta-open-measures.json").write_bytes(raw)
print(hashlib.sha256(raw).hexdigest())
```

El ejemplo no incluye credenciales ni automatiza consultas masivas. Su propósito es fijar lo recibido. No eludas el límite rotando direcciones, repitiendo búsquedas innecesarias o disfrazando cabeceras; Open Measures explica que esos abusos perjudican a los usuarios legítimos.

### 6. Normaliza sin borrar el original

Cada plataforma representa autores, fechas, contenido y reenvíos de manera distinta. Crea una capa derivada, pero conserva siempre el documento original y la ruta del campo fuente.

Un registro normalizado puede incluir:

```text
source_platform
source_record_id
observed_timestamp
published_timestamp
content_hash
matched_query_version
original_url
retrieved_at
```

No conviertas un `username` en identidad civil. No unas cuentas entre plataformas solo porque comparten nombre o avatar. Si deduplicas copias, registra el método y conserva la cardinalidad original: deduplicar cambia la pregunta estadística.

### 7. Revisa una muestra antes de contar historias

Diseña una muestra reproducible que incluya:

- resultados próximos al inicio y al máximo de la serie;
- varias plataformas;
- publicaciones con y sin enlaces;
- coincidencias exactas y variantes;
- ejemplos que contradigan la interpretación dominante.

Clasifica función, no intención: publicación original aparente, cita, comentario, refutación, reenvío o coincidencia irrelevante. Si dos personas no pueden aplicar el criterio de forma parecida, el libro de códigos necesita revisión.

### 8. Corrobora fuera del agregador

Open Measures recomienda validar un resultado en la publicación original mediante la URL almacenada o contrastarlo con otras colecciones. Si el original ya no existe, un archivo web puede aportar contexto, siempre que distingamos captura de autenticidad.

Para cada afirmación importante busca:

1. el documento en Open Measures;
2. la publicación original, si sigue accesible;
3. un archivo o captura con procedencia;
4. contexto externo fechado: noticia, comunicado o evento;
5. una explicación rival que produzca el mismo patrón.

Un pico tras una rueda de prensa demuestra compatibilidad temporal, no causalidad. Publicaciones semejantes pueden coordinarse, copiarse espontáneamente o responder al mismo estímulo público.

### 9. Publica denominadores, huecos e incertidumbre

El número bruto de coincidencias no dice qué proporción representa. Cuando sea posible, acompáñalo de un denominador coherente o explica por qué no existe. Evita comparar directamente plataformas con coberturas y unidades distintas.

Una conclusión responsable podría decir:

> La consulta Q2 devolvió actividad concentrada en dos días dentro de las colecciones examinadas. La revisión muestra republicaciones de un mismo enlace y usos críticos de la frase. El patrón justifica analizar procedencia y difusión, pero no permite atribuir coordinación ni impacto.

La palabra «inconcluso» es un resultado válido.

## Limitaciones y falsos positivos

### Cobertura no equivale a población

Las fuentes visibles son una muestra construida por decisiones técnicas y de producto. Pueden faltar periodos, canales, tipos de contenido o plataformas enteras. Además, el nivel público ofrece solo datos históricos y un subconjunto de fuentes. Comparar dos curvas sin auditar su cobertura puede medir la recolección más que la conversación.

### Los campos cambian de significado

Un campo llamado `author`, `username` o `timestamp` no garantiza la misma semántica en todas las fuentes. Puede representar al reenviador, al canal, al creador del objeto o la fecha de ingestión. Consulta la documentación y conserva el documento bruto.

### Buscar texto no equivale a comprenderlo

Una coincidencia puede ser una cita, una negación, una parodia, un enlace sin apoyo o contenido en otro idioma. Las variantes ortográficas mejoran cobertura y también introducen ruido. La revisión cualitativa no es opcional.

### Actividad no equivale a coordinación

La simultaneidad, un enlace común o el vocabulario parecido son señales débiles por separado. Para sostener coordinación hacen falta patrones temporales y relacionales más exigentes, alternativas descartadas y evidencia que no dependa del mismo agregador.

### Ausencia no equivale a inexistencia

Una publicación borrada, no recolectada, fuera de la ventana o almacenada en otro campo puede no aparecer. Formula las conclusiones dentro del universo observado.

## Buenas prácticas de OPSEC, ética y privacidad

Que un mensaje sea público no elimina la obligación de minimizar daño. La recopilación a escala puede transformar fragmentos dispersos en un perfil que la persona nunca esperó que existiera.

- investiga narrativas o riesgos definidos, no vidas privadas;
- evita buscar menores, víctimas o personas vulnerables;
- no intentes entrar en grupos privados ni sortear controles de acceso;
- no publiques listados de usuarios cuando un agregado responde la pregunta;
- elimina identificadores de ejemplos y capturas salvo necesidad pública clara;
- limita conservación, acceso y exportación de datos personales;
- separa observación de inferencia y registra quién aprobó una atribución;
- respeta condiciones, límites y mecanismos contra abuso;
- evalúa riesgo de reidentificación antes de compartir datasets;
- permite correcciones y deja visible la incertidumbre.

La política de privacidad de Open Measures indica que el servicio recibe información de sitios públicos de terceros. Esa base técnica no decide por nosotros si una reutilización concreta es necesaria, proporcionada o legal en nuestra jurisdicción.

## Checklist operativo

- [ ] La finalidad legítima, el alcance y las reglas de parada están escritos.
- [ ] Se revisaron los tres últimos temas y este asunto no los duplica.
- [ ] La fuente, ventana, esquema y huecos de cobertura están documentados.
- [ ] La consulta exacta, sus versiones y sus exclusiones son reproducibles.
- [ ] No se cambió la hipótesis después de mirar el gráfico sin dejar rastro.
- [ ] Se conservaron respuesta bruta, fecha, parámetros y huella.
- [ ] Los reenvíos, duplicados y unidades de análisis se trataron explícitamente.
- [ ] Una muestra incluye coincidencias relevantes, irrelevantes y contradictorias.
- [ ] Las publicaciones importantes se contrastaron en la fuente original.
- [ ] Volumen, prevalencia, influencia, identidad y coordinación no se confundieron.
- [ ] El informe contiene denominadores, cobertura e incertidumbre.
- [ ] Los identificadores personales se minimizaron en datos y producto final.

## Alternativas y siguientes pasos

Para fuentes con API abierta propia, consultar directamente la plataforma puede ofrecer un universo y una semántica más claros, aunque seguirá siendo necesario medir cobertura. Media Cloud resulta útil para comparar cobertura periodística; GDELT permite explorar eventos y medios a gran escala; archivos web ayudan a recuperar contexto histórico; una hoja reproducible en Python, R o DuckDB facilita auditar exportaciones sin enviar datos a terceros.

Open Measures es especialmente valioso como **entorno de descubrimiento y contraste histórico**. Su fortaleza no está en dictar quién coordinó qué, sino en hacer visibles publicaciones, intervalos y enlaces que después debemos validar.

El takeaway práctico es este: **congela la consulta, mide la cobertura, revisa el contenido y reserva las afirmaciones fuertes para evidencia independiente**. Como ejercicio, construye dos consultas sobre una campaña completamente ficticia, añade una variante ambigua y comprueba cómo cambia el resultado antes y después de una revisión manual. El siguiente paso natural sería diseñar una plantilla de auditoría de cobertura que compare, para cada fuente, periodos observables, campos, duplicados y tasas de coincidencias irrelevantes.

## Fuentes y documentación

- [Open Measures: documentación general](https://docs.openmeasures.io/docs)
- [Open Measures: guía de la aplicación pública](https://docs.openmeasures.io/docs/guides/public-app)
- [Open Measures: guía de la API pública](https://docs.openmeasures.io/docs/guides/public-api)
- [Open Measures: fuentes y campos por plataforma](https://docs.openmeasures.io/docs/guides/sources)
- [Open Measures: preguntas frecuentes, acceso y validación](https://docs.openmeasures.io/docs/further-reading/faq)
- [Open Measures: límites introducidos para prevenir abuso](https://openmeasures.io/update-to-public-api)
- [Open Measures: política de privacidad](https://openmeasures.io/legal/privacy-policy)
