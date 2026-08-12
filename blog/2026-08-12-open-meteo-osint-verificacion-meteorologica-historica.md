---
title: "Open-Meteo en OSINT: reconstruir el tiempo pasado sin confundir un modelo con una observación"
slug: /open-meteo-osint-verificacion-meteorologica-historica
authors: [osint-writter]
tags: [osint, geoint, verification, weather, investigation, data]
date: 2026-08-12
image: /img/blog/2026-08-12-open-meteo-verificacion-meteorologica-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un análisis OSINT que contrasta una rejilla meteorológica, una estación oficial, gráficas horarias y notas de procedencia](/img/blog/2026-08-12-open-meteo-verificacion-meteorologica-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un vídeo asegura que una concentración pública terminó bajo una tormenta; una fotografía muestra paraguas; y una publicación, subida varias horas después, habla de «viento imposible». Las tres pistas pueden encajar y, aun así, no demostrar qué ocurrió en el lugar y minuto investigados. Antes de tratar el tiempo como un sello de autenticidad, hay que separar **la observación, la estimación de un modelo, la hora de publicación y la hora real del suceso**.

<!-- truncate -->

[Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) facilita esa primera reconstrucción: permite consultar por coordenadas y fechas variables históricas como temperatura, precipitación, nubosidad, visibilidad o viento. Su API es cómoda, reproducible y global. Pero gran parte de su archivo se apoya en **reanálisis meteorológico** y salidas de modelos, no en un sensor colocado exactamente bajo la cámara. En OSINT responsable sirve para formular y contrastar hipótesis; una conclusión sensible debe volver a observaciones oficiales, imágenes, testimonios y otras fuentes independientes.

Todos los lugares secundarios, nombres y afirmaciones del caso práctico son ficticios. La coordenada de ejemplo corresponde aproximadamente al centro de Madrid y se usa solo como referencia pública reproducible.

## Qué es Open-Meteo y para qué sirve

Open-Meteo es un servicio y proyecto de código abierto que normaliza datos procedentes de modelos meteorológicos de distintos proveedores. Su [Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) expone series históricas mediante peticiones HTTP y ofrece, entre otros conjuntos, `ERA5`, `ERA5-Land` y datos de análisis de `ECMWF IFS`.

En una investigación legítima puede ayudar a:

- comprobar si una afirmación sobre lluvia, viento, temperatura o visibilidad es meteorológicamente compatible con un lugar y una franja horaria;
- localizar intervalos que merecen una revisión más precisa en estaciones, radar o imágenes;
- comparar dos fechas o ubicaciones con las mismas variables y unidades;
- detectar errores de zona horaria antes de ordenar una cronología;
- documentar una consulta mediante URL, coordenadas, modelo, variables y fecha de recuperación;
- distinguir el tiempo reconstruido después del suceso de la predicción que estaba disponible antes de él.

No permite concluir por sí solo que una persona estuvo allí, que una imagen se tomó a una hora concreta, que llovió sobre una calle determinada ni que una ráfaga causó un daño. Tampoco convierte un código meteorológico agregado en una descripción exhaustiva del cielo.

## La distinción decisiva: estación, reanálisis y pronóstico archivado

La palabra «histórico» es ambigua. Puede referirse a cosas técnicamente diferentes:

| Fuente | Qué representa | Uso OSINT prudente | Límite principal |
|---|---|---|---|
| Observación de estación | Medición realizada por instrumentos en una ubicación y momento | Corroborar una variable cerca del lugar | La estación puede estar lejos, a otra altitud o tener huecos |
| Reanálisis | Reconstrucción coherente que combina observaciones y un modelo físico | Explorar el contexto y comparar periodos | Es una estimación sobre una rejilla, no una lectura en el punto exacto |
| Pronóstico histórico continuo | Primeras horas de sucesivas ejecuciones operativas enlazadas | Aproximar condiciones recientes con modelos de alta resolución | Los modelos y sus versiones cambian con el tiempo |
| Ejecución individual archivada | Lo que un modelo concreto predijo desde una inicialización determinada | Reconstruir qué pronóstico existía entonces | Una predicción no demuestra lo que finalmente ocurrió |

El [ECMWF explica ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) como un reanálisis global que combina grandes cantidades de observaciones históricas con modelización y asimilación de datos para producir estimaciones horarias. Esa cobertura continua es su fortaleza: rellena zonas y periodos sin una estación próxima. También es la razón por la que no debe citarse como si cada celda fuera un pluviómetro.

Open-Meteo diferencia además cuatro familias históricas en su [documentación de pronósticos archivados](https://open-meteo.com/en/docs/historical-forecast-api): el archivo de reanálisis para series largas; el pronóstico histórico continuo para años recientes; las ejecuciones anteriores a plazos fijos; y las ejecuciones individuales. Elegir mal el conjunto puede cambiar la pregunta sin que el analista se dé cuenta.

## Caso ficticio: ¿la lluvia encaja con la cronología?

Imaginemos que una asociación ficticia, `Foro de la Plaza`, publica un vídeo de un acto celebrado supuestamente el `14 de octubre de 2025` en Madrid. El vídeo muestra suelo seco y sombras definidas. Un mensaje posterior asegura que fue grabado a las `18:00`, «durante un fuerte chaparrón».

La pregunta investigable no es «¿miente la asociación?», sino:

> ¿Qué condiciones meteorológicas estiman las fuentes abiertas para la zona y la franja citadas, y qué evidencia independiente permitiría aceptar o descartar esa hora?

### 1. Fija los cuatro relojes

Registra por separado:

1. la hora afirmada del suceso;
2. la hora visible en cualquier reloj o metadato;
3. la hora de publicación en la plataforma;
4. la zona horaria aplicada a cada dato.

En España, asumir `UTC` o la hora peninsular sin documentarlo puede desplazar toda la comparación. La API acepta nombres de la base de zonas horarias; usar `timezone=Europe/Madrid` hace explícita la conversión y devuelve también el desplazamiento aplicado.

### 2. Conserva la ubicación como una incertidumbre

Una coordenada en una publicación puede señalar el centro de una ciudad, el lugar del acto o simplemente un punto añadido por quien subió el contenido. Anota su procedencia y precisión. Si solo conoces el barrio, prueba varios puntos razonables y no presentes una falsa exactitud decimal.

En el ejemplo utilizamos `40.4168, -3.7038`, una referencia pública aproximada del centro de Madrid. No identifica a una persona ni pretende representar la posición exacta de una cámara.

### 3. Lanza una consulta mínima y reproducible

Para revisar temperatura, precipitación, viento y código meteorológico horario con `ERA5`, una petición de ejemplo es:

```text
https://archive-api.open-meteo.com/v1/archive
  ?latitude=40.4168
  &longitude=-3.7038
  &start_date=2025-10-14
  &end_date=2025-10-14
  &hourly=temperature_2m,precipitation,wind_speed_10m,weather_code
  &timezone=Europe%2FMadrid
  &models=era5
```

Se muestra partida para facilitar la lectura; al ejecutarla debe unirse en una sola URL. La [referencia de parámetros](https://open-meteo.com/en/docs/historical-weather-api#api-documentation) documenta `latitude`, `longitude`, `start_date`, `end_date`, `hourly`, `timezone`, unidades y selección de celda, entre otras opciones.

La respuesta consultada para este artículo devolvió la coordenada de rejilla `40.5, -3.75`, una elevación de `666 m`, zona `Europe/Madrid` y series horarias. En esa estimación `ERA5`, la precipitación fue `0,00 mm` durante las 24 horas y el viento a 10 metros se mantuvo por debajo de `8 km/h`.

Eso **debilita** la afirmación de un fuerte chaparrón en esa zona y franja; no basta para declarar falso el vídeo. Podría haber un error de fecha, lugar u hora, una precipitación muy localizada que la rejilla no represente bien, o una descripción exagerada. El siguiente paso es buscar una estación próxima y datos de radar, no convertir el primer resultado en veredicto.

### 4. Guarda procedencia, no solo una captura bonita

La nota de consulta debería incluir:

- URL completa y fecha/hora de recuperación;
- coordenadas solicitadas y coordenadas devueltas;
- elevación usada por el servicio;
- zona horaria y desplazamiento UTC;
- conjunto o modelo seleccionado;
- variables, unidades y resolución temporal;
- respuesta original en `JSON` o `CSV` y su hash;
- cualquier transformación posterior, como redondeo, agregación o gráfico.

La licencia de Open-Meteo exige [atribución bajo CC BY 4.0](https://open-meteo.com/en/license). Citar el servicio y el conjunto subyacente no es una formalidad: permite que otra persona entienda de dónde salió el dato y reproduzca el análisis.

### 5. Corrobora con observaciones y evidencia visual

Para un caso en España, la fuente primaria natural es AEMET. Sus productos abiertos incluyen observaciones y estadísticas de variables meteorológicas; la [descripción de sus estadísticas meteorofenológicas](https://www.aemet.es/es/datos_abiertos/estadisticas/estadistica_meteorofenologicas) enumera temperatura, precipitación, humedad, viento, presión, visibilidad y otras variables obtenidas de redes de estaciones.

La comparación debe conservar distancia, altitud y tipo de sensor. Una estación a veinte kilómetros no «certifica» una calle; aporta una observación contextual. Combínala, cuando sea legal y pertinente, con:

- radar de precipitación y mapas oficiales del episodio;
- imágenes del mismo lugar y franja;
- sombras y posición solar, con un margen razonable;
- superficies mojadas, paraguas o vegetación en movimiento, sin sobreinterpretarlos;
- avisos meteorológicos archivados;
- testimonios contemporáneos e independientes cuya hora pueda verificarse.

## Qué revisar antes de concluir

### Resolución espacial

Una coordenada de entrada no implica una medición en ese punto. `ERA5` trabaja sobre una rejilla global; Open-Meteo puede seleccionar una celda terrestre y aplicar ajustes relacionados con elevación. La respuesta devuelve coordenadas y altura precisamente porque el punto procesado puede diferir del solicitado.

La [documentación de ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5) describe una rejilla atmosférica de unos `31 km`, mientras que Open-Meteo presenta determinados productos y transformaciones con resoluciones distintas. En costas, montañas, islas o tormentas convectivas, compara modelos y estaciones en lugar de confiar en una única celda.

### Resolución temporal y acumulados

`precipitation=0` en una hora modelada no significa necesariamente que ninguna gota cayera durante cada minuto de esa hora. Revisa si la variable es instantánea, media, máxima o acumulada, y a qué intervalo se atribuye. No mezcles sin explicación acumulados diarios, valores horarios y ráfagas máximas.

### Elevación y microclima

Temperatura, viento y precipitación pueden cambiar mucho con la altitud y el relieve. Comprueba la elevación devuelta por la API frente a la del lugar real. En un puerto de montaña, una ladera o una costa, la discrepancia puede ser material.

### Cambios de modelo

Una serie «seamless» puede combinar modelos o ejecuciones. Open-Meteo advierte que el Historical Forecast API no es idóneo para tendencias largas porque las versiones operativas cambian. Para clima multidecenal recomienda conjuntos consistentes como `ERA5` o `ERA5-Land`; para reproducir una predicción emitida en una fecha concreta, ofrece su [Single Runs API](https://open-meteo.com/en/docs/single-runs-api).

### Incertidumbre y falsa precisión

`12,3 °C` parece exacto, pero la cifra sigue siendo una estimación de modelo si no procede de una estación. Conserva los decimales del dato original para reproducibilidad, pero redacta la conclusión con el nivel de confianza adecuado: «compatible», «incompatible con esta estimación» o «no concluyente» son expresiones más honestas que «demostrado».

## Flujo recomendado para una verificación meteorológica

1. Formula una afirmación falsable sobre lugar, intervalo y variable.
2. Separa hora del suceso, metadato, publicación y zona horaria.
3. Registra la precisión real de la ubicación.
4. Elige conscientemente observación, reanálisis o pronóstico archivado.
5. Consulta pocas variables relevantes antes de ampliar.
6. Guarda petición, respuesta, unidades, modelo, elevación y hash.
7. Compara celdas o modelos si el terreno o el fenómeno lo justifican.
8. Busca observaciones oficiales cercanas y documenta su distancia.
9. Triangula con radar, imágenes, sombras y fuentes contemporáneas.
10. Redacta qué dato contradice, qué sigue abierto y qué haría cambiar la conclusión.

## Falsos positivos y errores comunes

- **Tomar paraguas como lluvia:** también se usan para sol, viento o atrezzo.
- **Confundir suelo mojado con precipitación reciente:** riego, limpieza o agua acumulada producen señales parecidas.
- **Usar la publicación como hora de captura:** una pieza puede subirse horas o días después.
- **Elegir automáticamente la estación más próxima:** otra estación algo más lejana puede compartir mejor altitud y exposición.
- **Comparar una ráfaga con viento medio:** son variables distintas.
- **Forzar la coordenada al relato:** prueba sensibilidad espacial cuando la ubicación sea aproximada.
- **Citar «datos históricos» sin nombrar el producto:** reanálisis, análisis operativo y predicción archivada responden preguntas diferentes.
- **Ignorar resultados negativos:** una discrepancia bien documentada es más útil que ocultarla para conservar una hipótesis atractiva.

## OPSEC, ética y privacidad

La meteorología debe usarse para verificar contenido o hechos de interés legítimo, no para reconstruir rutinas privadas ni localizar a una persona vulnerable. Minimiza coordenadas y datos personales en informes públicos; una precisión innecesaria puede revelar un domicilio, refugio o lugar habitual.

Consulta servicios mediante peticiones acotadas, respeta condiciones y límites de uso, y evita automatizaciones masivas sin necesidad. Los [términos de Open-Meteo](https://open-meteo.com/en/terms) establecen límites para la API gratuita no comercial y advierten que los datos se ofrecen sin garantía de exactitud o disponibilidad. Si el análisis afecta a seguridad, responsabilidad legal, seguros o emergencias, solicita datos certificados y asesoramiento competente.

## Alternativas y siguientes pasos

- `AEMET OpenData` y redes meteorológicas nacionales, para observaciones oficiales y productos del país investigado;
- `ECMWF Climate Data Store`, para trabajar directamente con ERA5 y documentar selecciones avanzadas;
- `Meteostat`, para series de estaciones agregadas, revisando siempre la procedencia;
- archivos de radar y satélite, cuando la distribución espacial de la precipitación o nubosidad sea decisiva;
- `SunCalc` y herramientas solares, para contrastar sombras con una cronología sin convertirlas en reloj perfecto.

La idea accionable es sencilla: **usa Open-Meteo para preguntar mejor, no para cerrar el caso antes de tiempo**. Una consulta reproducible puede descartar errores gruesos y orientar la búsqueda, pero el informe debe distinguir siempre rejilla, estación, pronóstico, hora y grado de incertidumbre. El siguiente tema natural sería cómo archivar y comparar radares meteorológicos sin confundir reflectividad con lluvia observada en superficie.

## Fuentes

- [Open-Meteo: Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [Open-Meteo: Historical Forecast API y elección de conjunto](https://open-meteo.com/en/docs/historical-forecast-api)
- [Open-Meteo: Single Runs API](https://open-meteo.com/en/docs/single-runs-api)
- [Open-Meteo: licencia y atribución](https://open-meteo.com/en/license)
- [ECMWF: ERA5](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5)
- [ECMWF: ERA5-Land](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5-land)
- [AEMET: estadísticas de variables meteorofenológicas](https://www.aemet.es/es/datos_abiertos/estadisticas/estadistica_meteorofenologicas)
