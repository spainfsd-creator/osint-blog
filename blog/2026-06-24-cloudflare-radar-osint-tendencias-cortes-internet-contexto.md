---
title: "Cloudflare Radar en OSINT: tendencias, cortes de Internet y contexto sin confundir señal con causa"
slug: /cloudflare-radar-osint-tendencias-cortes-internet-contexto
authors: [osint-writter]
tags: [osint, investigation, verification, infrastructure, data, methodology]
date: 2026-06-24
image: /img/blog/2026-06-24-cloudflare-radar-osint-tendencias-cortes-internet-contexto.png
---

![Ilustración editorial de una analista OSINT revisando un mapa mundial, series temporales y una caída de conectividad con criterio metodológico](/img/blog/2026-06-24-cloudflare-radar-osint-tendencias-cortes-internet-contexto.png)

**Descargar el podcast!**: <a href="/podcasts/cloudflare-radar-osint-tendencias-cortes-internet-contexto.m4a">Descargar el podcast</a>


Una región deja de responder durante una noche electoral. En redes sociales se habla de censura, el proveedor culpa a una avería y varias gráficas muestran una caída brusca. El problema no es encontrar otra captura: es separar **qué cambió, dónde se observó, durante cuánto tiempo y qué evidencia permitiría explicar la causa**. `Cloudflare Radar` puede aportar señales valiosas para ordenar esa investigación, pero no convierte una curva descendente en una atribución automática.

Radar reúne vistas sobre tráfico de Internet, consultas DNS, rutas BGP, tecnologías, ataques y anomalías. Su utilidad OSINT está en comparar tendencias agregadas y construir una cronología verificable. Su límite también es importante: observa el mundo desde fuentes concretas, normaliza buena parte de los valores y no sustituye los datos del operador, las mediciones independientes ni la documentación local.

<!-- truncate -->

## Qué es Cloudflare Radar y para qué sirve

[Cloudflare Radar](https://radar.cloudflare.com/) es un portal público de tendencias e información sobre Internet. Según su [descripción oficial](https://radar.cloudflare.com/about), combina datos de la red global de Cloudflare con datos agregados y anonimizados del resolvedor DNS público `1.1.1.1`. Algunas secciones incorporan además fuentes externas: por ejemplo, la vista de routing utiliza datos de `RIPE RIS`, mientras que determinados metadatos proceden de `PeeringDB` o `APNIC`.

La distinción entre fuentes no es un detalle menor. Cada panel responde a una pregunta diferente:

- **HTTP** ayuda a observar cambios relativos en tráfico, protocolos, dispositivos o sistemas operativos vistos por Cloudflare;
- **DNS** resume patrones de consultas recibidas por `1.1.1.1`;
- **NetFlows** aporta otra señal sobre cambios de tráfico de red;
- **BGP** permite estudiar anuncios, rutas, fugas o secuestros potenciales desde la visibilidad disponible;
- **anomalías y cortes** organizan descensos de conectividad detectados y revisados;
- **datasets y API** permiten repetir consultas y conservar resultados estructurados.

Esto hace que Radar sea útil en periodismo de datos, respuesta ante incidentes, análisis de políticas públicas, investigación de apagones y verificación de afirmaciones sobre conectividad. No es un medidor universal de “todo Internet” ni una prueba directa de intención.

## Caso de uso legítimo: verificar un corte en una región ficticia

Imagina que una organización de observación electoral estudia una interrupción en `Monteluz`, un país ficticio. Entre las `20:10` y las `23:40` del día de votación, usuarios de dos provincias notifican pérdida de acceso. La hipótesis inicial es abierta: podría tratarse de un apagón eléctrico, una avería de fibra, un problema en un proveedor o una medida deliberada.

El equipo crea una tabla antes de mirar gráficas:

| Pregunta | Señal en Radar | Corroboración necesaria |
| --- | --- | --- |
| ¿Cayó el tráfico agregado? | Serie HTTP o NetFlows por ubicación | Mediciones de otras redes y testimonios fechados |
| ¿Afectó a todo el país? | Comparación nacional, regional y por ASN | Datos de operadores y cobertura local |
| ¿Cambió el routing? | Eventos y rutas BGP | `RIPE RIS`, `RouteViews` y análisis técnico |
| ¿Cuándo empezó y terminó? | Anotación de anomalía y series temporales | Timestamps de sondas, prensa local y avisos oficiales |
| ¿Por qué ocurrió? | Posible causa publicada en el centro de cortes | Fuentes documentales independientes |

Radar puede ayudar a confirmar que hubo una señal temporal y a acotar su alcance. Para atribuir la causa hacen falta capas adicionales. La metodología mejora cuando la conclusión final puede distinguir entre “caída observada”, “alcance corroborado” y “causa documentada”.

## Flujo recomendado paso a paso

### 1. Formula la pregunta y fija el marco temporal

Evita empezar con “demostrar que hubo censura”. Formula una pregunta que pueda fallar: “¿Qué señales abiertas muestran una reducción de conectividad en Monteluz entre las 18:00 y las 02:00 UTC, y qué explicaciones son compatibles con ellas?”.

Registra:

- zona horaria original y conversión a `UTC`;
- ubicación y, si procede, `ASN` bajo estudio;
- periodo principal y periodo de referencia;
- fuentes que podrían refutar la hipótesis;
- y nivel de precisión que permite cada dataset.

Una semana comparable suele ser más útil que una captura aislada. Los ciclos diarios, festivos y cambios de uso pueden parecer anomalías si la línea base está mal elegida.

### 2. Empieza por el centro de cortes, no por la explicación

El [Cloudflare Radar Outage Center](https://radar.cloudflare.com/outage-center) reúne cortes y anomalías de conectividad. Para cada evento pueden aparecer ubicación, `ASN`, tipo, alcance, comienzo, final y una causa probable basada en información pública.

Conserva la URL, la hora de consulta, el identificador del evento y el texto exacto que describe su estado. Una anomalía es una pista priorizada: incluso cuando ha sido revisada por el equipo de Radar, la causa publicada debe contrastarse con comunicados del operador, autoridades, prensa local fiable o mediciones técnicas independientes.

### 3. Compara series dentro de la misma consulta

La [documentación de normalización](https://developers.cloudflare.com/radar/concepts/normalization/) advierte de que Radar normalmente no devuelve valores brutos. Puede expresar datos como porcentajes, cambio porcentual o escalas `min-max`. Si un endpoint normaliza con `min-max`, dos series obtenidas en peticiones separadas pueden no compartir escala.

Por eso, cuando quieras comparar dos ubicaciones, redes o periodos:

1. solicita las series en la misma petición siempre que el endpoint lo permita;
2. revisa `result.meta.normalization`;
3. guarda también `dateRange`, `lastUpdated`, unidades e intervalo de agregación;
4. evita presentar el eje normalizado como volumen absoluto;
5. y documenta cualquier tratamiento posterior.

La [guía oficial de comparaciones](https://developers.cloudflare.com/radar/get-started/making-comparisons/) insiste en este punto: la comparabilidad depende de cómo se solicitaron y normalizaron los datos, no solo de que las líneas aparezcan juntas en un informe.

### 4. Automatiza solo lo necesario y conserva la respuesta

La [API de Radar](https://developers.cloudflare.com/radar/) es gratuita y está disponible para investigar datos globales de Internet mediante un token de Cloudflare. Un ejemplo responsable para recuperar una lista pequeña de cortes recientes sería:

```bash
curl --fail --silent --show-error \
  'https://api.cloudflare.com/client/v4/radar/annotations/outages?limit=5&offset=0&dateRange=7d&format=json' \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -o radar-outages-7d.json
```

No incrustes tokens en scripts, capturas ni repositorios. Guarda junto al JSON la consulta, un timestamp `UTC`, el hash del fichero y una nota sobre el endpoint. Si el análisis se publicará, revisa también la licencia: los datos descargados o servidos por la API se ofrecen, salvo indicación distinta, bajo `CC BY-NC 4.0`.

### 5. Lee la confianza y las anotaciones antes de concluir

Las respuestas pueden incluir `result.meta.confidenceInfo`. La [escala de confianza oficial](https://developers.cloudflare.com/radar/concepts/confidence-levels/) va de niveles con pocos datos o patrones erráticos a un nivel `5`, que indica que no se conocen problemas de calidad. El nivel `4` figura como no asignado.

Esto no es una probabilidad de que tu hipótesis sea cierta. Describe la confianza de Cloudflare en la calidad del dato devuelto. Anota además las incidencias de pipeline, proyecciones parciales y otras anotaciones presentes en los metadatos: una gráfica limpia puede ocultar que parte del intervalo requiere cautela.

### 6. Triangula con señales independientes

Para un corte de conectividad, un mínimo razonable sería cruzar:

- `OONI Explorer` para mediciones de accesibilidad y posibles bloqueos;
- sondas de `RIPE Atlas` para alcance y latencia desde puntos independientes;
- datos de routing de `RIPE RIS` o `RouteViews`;
- avisos públicos del proveedor y del regulador;
- información meteorológica, eléctrica o sobre cables cuando sea pertinente;
- y testimonios locales con hora, lugar y método de conexión claramente documentados.

La convergencia de señales aumenta la confianza. Las discrepancias también informan: una caída visible en tráfico HTTP pero no en BGP podría apuntar a un problema distinto de una retirada masiva de rutas.

## Limitaciones y falsos positivos

### La visibilidad de Cloudflare no es todo Internet

Radar observa una muestra amplia, pero condicionada por la red de Cloudflare, el uso de `1.1.1.1` y las fuentes integradas. Un país, proveedor o protocolo puede estar sobrerrepresentado o infrarrepresentado. “No aparece en Radar” no equivale a “no ocurrió”.

### Una caída no explica su causa

El mismo patrón aparente puede ser compatible con un apagón, mantenimiento, rotura física, fallo de configuración, desastre natural o intervención deliberada. La atribución exige documentos, contexto y, con frecuencia, conocimiento local.

### Porcentajes y valores normalizados se sobreinterpretan

Un descenso del `50 %` puede referirse a un cambio respecto a una línea base, no a la mitad de todos los usuarios del país. Antes de escribir una cifra, identifica qué mide el numerador, qué referencia usa y qué normalización se aplicó.

### Los límites geográficos y temporales importan

Una etiqueta nacional puede ocultar afectación regional o concentrada en un `ASN`. Los intervalos agregados también pueden suavizar un corte breve. Expón la resolución real del dato y no prometas una precisión que el endpoint no ofrece.

### Correlación temporal no implica coordinación

Que una caída coincida con una protesta o una elección justifica investigar la relación, no afirmarla. La cronología es una herramienta para generar y descartar hipótesis, no un sustituto de la causalidad.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con datos agregados y minimiza información personal en notas y capturas.
- No publiques ubicaciones precisas de testigos ni detalles que puedan exponerles.
- Separa datos brutos, transformaciones y conclusiones; conserva siempre la consulta original.
- Usa tokens de solo lectura y alcance mínimo, almacenados fuera del repositorio.
- Respeta licencias, atribución y límites de uso de la API.
- Evita sondear infraestructura ajena para “confirmar” un corte. Prioriza mediciones pasivas, fuentes autorizadas y plataformas diseñadas para investigación abierta.
- Describe hipótesis alternativas y qué evidencia permitiría distinguirlas.

## Checklist para un análisis defendible

- [ ] La pregunta puede confirmarse o refutarse.
- [ ] Todas las horas están normalizadas a `UTC` sin perder la zona original.
- [ ] El periodo principal tiene una línea base comparable.
- [ ] La fuente de cada panel o endpoint está identificada.
- [ ] La normalización, unidades e intervalo de agregación están documentados.
- [ ] El nivel de confianza y las anotaciones de calidad se han revisado.
- [ ] Las series comparadas comparten escala o se solicitaron conjuntamente.
- [ ] Hay al menos dos fuentes independientes de corroboración.
- [ ] “Anomalía”, “corte”, “bloqueo” y “causa” no se usan como sinónimos.
- [ ] El informe conserva consultas, timestamps, ficheros y hashes.

## Alternativas y siguientes pasos

`Cloudflare Radar` encaja bien para una primera vista agregada y para construir cronologías. Según la pregunta, otras fuentes aportan perspectivas distintas:

- `OONI Explorer` se centra en mediciones abiertas de interferencia y accesibilidad;
- `RIPE Atlas` permite analizar mediciones desde sondas distribuidas;
- `RIPE RIS` y `RouteViews` ofrecen datos específicos de routing BGP;
- `IODA` combina señales para estudiar conectividad a escala de país, región y red;
- los comunicados del operador, regulador o proveedor eléctrico pueden sostener la explicación causal.

El takeaway práctico es sencillo: usa Radar para **detectar cambios, acotar tiempo y alcance, y formular mejores preguntas**. Antes de hablar de causa, comprueba la fuente del dato, su normalización y su confianza; después, busca una señal independiente que pueda contradecirte.

Como siguiente tema, merece la pena comparar `Cloudflare Radar`, `OONI Explorer` y `RIPE Atlas` ante un mismo corte ficticio: qué ve cada plataforma, qué no ve y cómo cambia la conclusión cuando sus señales no coinciden.

## Fuentes consultadas

- [Cloudflare Radar: About](https://radar.cloudflare.com/about)
- [Documentación general de Cloudflare Radar](https://developers.cloudflare.com/radar/)
- [Cloudflare Radar: tipos de datos para investigar](https://developers.cloudflare.com/radar/investigate/)
- [Cloudflare Radar: investigación de cortes](https://developers.cloudflare.com/radar/investigate/outages/)
- [Cloudflare Radar: métodos de normalización](https://developers.cloudflare.com/radar/concepts/normalization/)
- [Cloudflare Radar: niveles de confianza](https://developers.cloudflare.com/radar/concepts/confidence-levels/)
- [Cloudflare Radar: comparación de series](https://developers.cloudflare.com/radar/get-started/making-comparisons/)
