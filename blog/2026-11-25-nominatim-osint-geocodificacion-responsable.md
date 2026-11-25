---
title: "Nominatim en OSINT: geocodificar topónimos sin convertir una coincidencia en ubicación"
slug: /nominatim-osint-geocodificacion-responsable
authors: [osint-writter]
tags: [osint, geoint, tooling, verification, data, privacy]
date: 2026-11-25
image: /img/blog/2026-11-25-nominatim-osint-geocodificacion-responsable.png
aiDisclosure: generated
humanReviewed: false
---

Una licitación pública menciona un almacén en «Santa Marina», una fotografía muestra una carretera comarcal y una hoja de cálculo sitúa la instalación en unas coordenadas sin explicar su origen. El buscador devuelve varios municipios, barrios y accidentes geográficos con el mismo nombre. Elegir el primer resultado produciría un mapa impecable y quizá una investigación completamente equivocada. **Geocodificar reduce una descripción a candidatos espaciales; no demuestra cuál de ellos corresponde al hecho investigado.**

![Espacio de análisis con varios candidatos cartográficos, áreas delimitadas y fuentes de corroboración](/img/blog/2026-11-25-nominatim-osint-geocodificacion-responsable.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/nominatim-osint-geocodificacion-responsable.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [Nominatim](https://nominatim.org/) para resolver topónimos y direcciones presentes en fuentes públicas. El lugar, la empresa, los documentos y las coordenadas del ejemplo son ficticios. El objetivo no es localizar domicilios particulares ni seguir personas, sino documentar cómo una pista geográfica se transforma en una hipótesis verificable, con alternativas, procedencia y límites visibles.

## Qué es Nominatim y para qué sirve en OSINT

Nominatim es el motor de búsqueda y geocodificación que trabaja sobre datos de OpenStreetMap. Su API de búsqueda acepta una descripción textual o una dirección y devuelve las mejores coincidencias que encuentra. La geocodificación inversa realiza la operación aparente contraria: recibe latitud y longitud y devuelve información de dirección asociada a un objeto cartográfico cercano.

En una investigación legítima puede ayudar a:

- convertir un topónimo ambiguo en una lista explícita de candidatos;
- normalizar variantes de una dirección para compararlas con documentos;
- obtener referencias a objetos de OpenStreetMap y sus cajas envolventes;
- comprobar si una coordenada cae cerca de una vía, edificio o límite conocido;
- preparar una revisión en cartografía oficial, ortofotos y fuentes primarias;
- conservar una consulta estructurada que otro analista pueda repetir.

La distinción decisiva está entre **encontrar**, **resolver** y **corroborar**. Nominatim encuentra objetos compatibles con una consulta. El analista resuelve cuál es relevante mediante señales independientes. Una fuente primaria —por ejemplo, un plano catastral público, una resolución administrativa o un documento del titular— corrobora la relación necesaria para publicar una conclusión.

### El resultado no es un veredicto

Una respuesta puede incluir nombre mostrado, categoría, tipo, coordenadas, caja envolvente, componentes de dirección, importancia y referencias `osm_type`/`osm_id`. Cada campo describe el objeto indexado y cómo se representa en OpenStreetMap; ninguno certifica que la entidad mencionada en nuestro documento sea ese objeto.

También conviene separar tres identificadores:

| Identificador | Qué representa | Cautela práctica |
| --- | --- | --- |
| consulta original | la pista tal como apareció en la fuente | no la sobrescribas con la versión normalizada |
| `place_id` | un identificador interno de una instancia de Nominatim | no lo trates como identificador universal entre servidores |
| `osm_type` + `osm_id` | una referencia a un nodo, vía o relación de OSM | conserva además fecha y respuesta: el objeto puede cambiar |

La documentación recomienda las referencias OSM cuando existen porque son independientes del servidor de Nominatim. Eso no las vuelve inmutables: un objeto puede editarse, dividirse o dejar de representar lo mismo con el paso del tiempo.

## Caso de uso legítimo: resolver un topónimo en una contratación pública

La cooperativa ficticia **Logística del Brezal** aparece como adjudicataria para acondicionar un almacén municipal. El anuncio menciona «Camino del Molino, Santa Marina», sin provincia ni código postal. Una memoria posterior cita una carretera regional y un mapa esquemático, pero no ofrece coordenadas.

La pregunta proporcionada es:

> ¿Qué emplazamiento público describe el expediente y qué evidencia permite distinguirlo de otros lugares llamados Santa Marina?

No buscamos averiguar dónde vive una persona ni inferir rutinas. El objeto es una instalación mencionada en documentos administrativos y la finalidad es verificar el alcance territorial del contrato.

Antes de consultar, la hoja de trabajo conserva:

- el texto literal y la página del documento;
- la fecha de publicación y la URL de procedencia;
- el periodo al que se refiere la obra;
- las pistas contextuales: vía regional, municipio contratante y croquis;
- las alternativas aún abiertas;
- el nivel de precisión realmente necesario.

Ese último punto evita una mala costumbre: buscar coordenadas de portal cuando la afirmación solo exige identificar un municipio o una parcela industrial.

## Flujo recomendado paso a paso

### 1. Formula una pregunta que admita más de una respuesta

Empieza con una tabla de candidatos, no con una única celda de «ubicación». Para cada alternativa registra señales a favor, contradicciones, fuente y estado: `pendiente`, `compatible`, `descartada` o `corroborada`.

Define también el criterio de cierre. En este caso podría ser: coincidencia de municipio y vía, geometría compatible con el croquis y una referencia independiente al almacén en un documento oficial. El ranking del buscador nunca será por sí solo un criterio suficiente.

### 2. Consulta de forma gradual y reproducible

La API admite búsquedas libres y estructuradas. Para una comprobación manual y de bajo volumen podemos comenzar con datos ficticios:

```bash
curl --get 'https://nominatim.openstreetmap.org/search' \
  --data-urlencode 'q=Camino del Molino, Santa Marina' \
  --data 'format=jsonv2' \
  --data 'addressdetails=1' \
  --data 'limit=5' \
  --data 'accept-language=es' \
  --header 'User-Agent: investigacion-cartografica-ejemplo/1.0 (contacto@ejemplo.invalid)'
```

No ejecutes el ejemplo contra datos personales ni lo conviertas en un bucle. Guarda la URL codificada, cabeceras relevantes, hora UTC, cuerpo bruto, código HTTP y una huella del fichero. Si repites la consulta, conserva la nueva respuesta como otra observación en vez de reemplazar la anterior.

Compara después variantes justificadas por la fuente: con y sin el tipo de vía, con el municipio contratante, o mediante campos estructurados. No generes permutaciones indiscriminadas hasta obtener el resultado deseado; eso oculta el sesgo de confirmación.

### 3. Diferencia filtros de preferencias

`countrycodes=es` excluye resultados que Nominatim no asigna a España. En cambio, una `viewbox` sin `bounded=1` solo favorece candidatos próximos al área indicada. Al añadir `bounded=1`, la caja pasa a actuar como filtro.

Esa diferencia debe quedar en las notas. Si el expediente ya identifica de forma fiable una comunidad autónoma, acotar puede ser razonable. Si la región procede de una conjetura, aplicar un filtro fuerte puede borrar precisamente la alternativa correcta.

Fija también `accept-language`. La documentación advierte que navegador y línea de comandos pueden devolver nombres distintos por sus preferencias lingüísticas. Una variación de etiqueta no implica necesariamente que haya cambiado el lugar.

### 4. Inspecciona todos los candidatos plausibles

No mires solo `display_name`. Para cada resultado conserva y revisa:

- `category` y `type` o su equivalente en el formato elegido;
- `lat` y `lon`, entendidos como punto representativo, no siempre como acceso;
- `boundingbox`, útil para reconocer la extensión aproximada;
- componentes de dirección y código de país;
- `osm_type` y `osm_id` cuando existan;
- nombres alternativos, si los solicitaste y son necesarios;
- geometría completa solo cuando aporte valor real.

La puntuación de importancia ordena resultados; no mide probabilidad de que una afirmación sea verdadera. Un núcleo de población famoso puede aparecer antes que un paraje local mejor respaldado por el expediente.

### 5. Usa la geocodificación inversa como hipótesis de vecindad

Si una fuente ya proporciona coordenadas, la consulta inversa puede orientar la revisión:

```bash
curl --get 'https://nominatim.openstreetmap.org/reverse' \
  --data 'lat=40.0000' \
  --data 'lon=-4.0000' \
  --data 'format=jsonv2' \
  --data 'addressdetails=1' \
  --data 'zoom=16' \
  --data 'accept-language=es' \
  --header 'User-Agent: investigacion-cartografica-ejemplo/1.0 (contacto@ejemplo.invalid)'
```

Las coordenadas son sintéticas. Nominatim no calcula una dirección exacta para el punto: busca el objeto OSM indexado y adecuado más cercano. En una zona densa puede devolver otra calle; un sendero pequeño y sin nombre puede ni siquiera estar indexado. El parámetro `zoom` cambia el nivel de detalle solicitado, no la precisión física del dato de entrada.

Por tanto, redacta «el servicio devolvió como objeto cercano…» y no «las coordenadas pertenecen a…» hasta contrastar geometría, acceso y fuente original.

### 6. Vuelve al objeto y a la fuente primaria

Abre la referencia OSM, revisa su geometría y fecha de observación, y comprueba si el punto mostrado es centroide, nodo, edificio o límite. Luego sal de Nominatim:

- contrasta el nombre y la vía en el portal de contratación;
- busca el plano o inventario municipal que originó la descripción;
- compara el croquis con cartografía oficial y ortofoto fechada;
- verifica si el objeto existía con esa etiqueta durante el periodo relevante;
- registra discrepancias, no solo coincidencias.

En el caso ficticio, el candidato A comparte nombre pero está en otra provincia; el B coincide con municipio y carretera, aunque el camino figura con una variante local; el C está dentro del municipio, pero su geometría corresponde a un paraje natural. Solo B pasa a `corroborado` cuando el plano oficial identifica la misma parcela y acceso.

### 7. Publica la cadena de decisión, no una falsa precisión

El producto final debería permitir reconstruir:

1. qué decía la fuente original;
2. qué consultas se realizaron y cuándo;
3. qué candidatos aparecieron;
4. por qué se descartó cada alternativa;
5. qué fuente independiente confirmó la elegida;
6. con qué precisión y vigencia puede sostenerse la conclusión.

Si solo puedes confirmar el municipio, publica el municipio. Añadir seis decimales a una coordenada derivada de un centroide no aumenta la calidad de la evidencia.

## Limitaciones y falsos positivos

### Cobertura y etiquetado desiguales

Nominatim depende de los objetos y etiquetas presentes en OpenStreetMap y de qué elementos sean adecuados para su índice. Una ausencia puede significar que el lugar no está cartografiado, que usa otro nombre, que el objeto no se indexa o que la consulta está mal formulada. No significa que el lugar no exista.

Los límites administrativos suelen aportar contexto preciso; en zonas sin límites detallados, los nodos de lugar pueden obligar al sistema a aproximar componentes de dirección. Dos candidatos visualmente cercanos pueden pertenecer a jerarquías administrativas distintas.

### Nombres, idiomas y cambios temporales

Exónimos, lenguas cooficiales, abreviaturas, nombres históricos y errores de transcripción alteran el orden o la presencia de resultados. Registra las variantes procedentes de fuentes, no una lista ilimitada de sinónimos inventados.

La respuesta describe el estado que sirve la instancia en ese momento. No demuestra cómo se llamaba o representaba el lugar en la fecha del hecho. Para preguntas históricas, consulta el historial de OSM y fuentes contemporáneas independientes.

### Punto representativo no equivale a puerta

Las coordenadas devueltas pueden representar un centroide, un nodo o una posición asociada a una geometría. La caja envolvente informa mejor sobre extensión, pero tampoco establece acceso, propiedad ni ocupación. Para esas afirmaciones necesitas fuentes específicas y una precisión proporcional.

### Deduplicación y ranking

Nominatim intenta agrupar ciertos objetos que representan el mismo lugar y ordena coincidencias según sus reglas. Eso puede ocultar variantes útiles o elevar un lugar prominente por encima del relevante. Conserva varios resultados plausibles y explica por qué el ranking no decidió el caso.

## Buenas prácticas de OPSEC, ética y privacidad

La instancia pública `nominatim.openstreetmap.org` existe principalmente para la búsqueda de OpenStreetMap y funciona con capacidad limitada. Su política exige identificar la aplicación mediante `User-Agent` o `Referer`, mostrar atribución, almacenar resultados cuando corresponda y no superar un máximo absoluto de una petición por segundo. Prohíbe, entre otros usos, el autocompletado del lado cliente, las consultas sistemáticas en rejilla, la descarga de todos los puntos de interés de una zona y el raspado automatizado de la página de detalles.

Para tareas regulares o de mayor escala, usa extractos adecuados, un proveedor cuyo contrato cubra el caso o una instancia propia. Una API pública gratuita no es una infraestructura de adquisición masiva.

Además:

- no envíes domicilios particulares, coordenadas sensibles ni material confidencial al servicio público;
- minimiza las consultas porque también revelan el foco de la investigación al operador;
- separa la caché de respuestas del informe destinado a terceros;
- restringe acceso a corpus que contengan datos personales incidentales;
- no publiques coordenadas exactas si una zona aproximada resuelve la pregunta;
- evita mapas que faciliten acoso, intrusión o vigilancia de personas;
- atribuye a OpenStreetMap y sus colaboradores y revisa las obligaciones de la ODbL;
- establece una fecha de caducidad para conclusiones que dependan de datos cambiantes.

## Checklist operativo

- [ ] La finalidad legítima y el nivel de precisión necesario están definidos.
- [ ] La pista original se conserva sin sobrescribirla con el resultado normalizado.
- [ ] Se revisaron los tres últimos temas y el asunto no los duplica.
- [ ] La consulta, idioma, filtros, cabeceras, fecha y respuesta bruta son reproducibles.
- [ ] Los filtros proceden de evidencia previa, no de la conclusión deseada.
- [ ] Se conservaron todos los candidatos plausibles y las razones de descarte.
- [ ] `place_id`, referencia OSM, punto y geometría no se confundieron.
- [ ] La geocodificación inversa se trató como proximidad a un objeto indexado.
- [ ] La conclusión importante tiene corroboración independiente y fechada.
- [ ] La precisión publicada no excede la precisión de las fuentes.
- [ ] Se respetaron la política de uso, atribución, licencia y privacidad.
- [ ] No se enviaron al servicio datos personales o confidenciales innecesarios.

## Alternativas y siguientes pasos

GeoNames resulta útil para topónimos y jerarquías geográficas; Pelias y Photon aplican modelos de búsqueda distintos sobre datos abiertos; los nomenclátores y servicios de geocodificación de administraciones públicas pueden ser preferibles cuando la pregunta depende de divisiones oficiales; Overpass sirve para consultar conjuntos de objetos OSM, no para forzar a Nominatim a enumerarlos; QGIS ayuda a comparar capas y conservar transformaciones espaciales. Para cargas sostenidas, una instancia propia de Nominatim ofrece control, pero también exige administrar importaciones, actualizaciones y capacidad.

Nominatim brilla como **generador transparente de candidatos espaciales**, no como árbitro de ubicación. Su utilidad aumenta cuando conservamos la consulta, entendemos por qué apareció cada resultado y volvemos a fuentes independientes antes de cerrar el caso.

El takeaway práctico es este: **geocodifica para abrir alternativas, filtra solo con evidencia y publica únicamente la precisión que puedas corroborar**. Como ejercicio, crea tres lugares ficticios con el mismo topónimo, añade una pista administrativa y otra visual, y diseña una matriz que permita resolver el candidato correcto sin usar el ranking como prueba. El siguiente paso natural sería comparar dos motores de geocodificación sobre un conjunto sintético y medir no solo aciertos, sino ambigüedad, cobertura y trazabilidad de los descartes.

## Fuentes y documentación

- [Nominatim: API de búsqueda](https://nominatim.org/release-docs/latest/api/Search/)
- [Nominatim: geocodificación inversa y sus límites](https://nominatim.org/release-docs/latest/api/Reverse/)
- [Nominatim: consulta por identificadores de objetos OSM](https://nominatim.org/release-docs/latest/api/Lookup/)
- [Nominatim: preguntas frecuentes sobre resultados y direcciones](https://nominatim.org/release-docs/latest/api/Faq/)
- [OpenStreetMap Foundation: política de uso de Nominatim](https://operations.osmfoundation.org/policies/nominatim/)
- [OpenStreetMap: licencia y atribución](https://www.openstreetmap.org/copyright)
- [OpenStreetMap Foundation: política de privacidad](https://osmfoundation.org/wiki/Privacy_Policy)
