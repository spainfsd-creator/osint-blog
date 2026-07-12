---
title: "Global Fishing Watch en OSINT: actividad marítima, AIS y SAR con contexto"
slug: /global-fishing-watch-osint-actividad-maritima-ais-sar-contexto
authors: [osint-writter]
tags: [osint, geoint, maritime, verification, data, investigation]
date: 2026-07-12
image: /img/blog/2026-07-12-global-fishing-watch-osint-actividad-maritima-ais-sar-contexto.png
---

![Ilustración editorial de una analista OSINT revisando actividad marítima abierta, trazas AIS, detecciones SAR, notas de verificación y un mapa oceánico sin embarcaciones identificables](/img/blog/2026-07-12-global-fishing-watch-osint-actividad-maritima-ais-sar-contexto.png)

Una mancha de calor sobre el océano puede parecer una historia cerrada: barcos, ruta, zona protegida y una hora aproximada. En investigación marítima responsable, sin embargo, esa imagen solo abre una pregunta: **qué actividad pública se observa, con qué datos, con qué retraso y con qué nivel de incertidumbre**. `Global Fishing Watch` ayuda justo ahí, no como radar infalible, sino como una capa abierta para estudiar actividad humana en el mar con método.

Revisando su documentación oficial el **12 de julio de 2026**, la plataforma combina datos de seguimiento de embarcaciones, modelos de aprendizaje automático, capas ambientales, detecciones satelitales y APIs para explorar actividad pesquera aparente, presencia de buques, encuentros, eventos AIS apagado y detecciones SAR. La palabra clave es "aparente": el dato puede orientar una investigación, pero no sustituye la corroboración con registros, autorizaciones, imágenes, contexto local y fuentes primarias.

Este artículo está escrito para analistas OSINT, periodistas, equipos ambientales, investigadores académicos y organizaciones que trabajan con fuentes abiertas de forma proporcionada. No es una guía para perseguir tripulaciones, acosar armadores, exponer rutas sensibles ni convertir una coincidencia algorítmica en acusación.

<!-- truncate -->

## Qué es Global Fishing Watch y para qué sirve

[`Global Fishing Watch`](https://globalfishingwatch.org/) es una organización y plataforma de datos orientada a hacer más transparente la actividad humana en el océano. Su mapa público permite visualizar capas como esfuerzo pesquero aparente, presencia de embarcaciones, encuentros, eventos de apagado AIS, detecciones nocturnas, capas de referencia y zonas marítimas.

Su valor OSINT no está en "verlo todo". Está en formular preguntas mejores:

- dónde se concentra actividad pesquera aparente en una zona y periodo;
- qué diferencias hay entre presencia de buques y actividad clasificada como pesca;
- si una zona protegida, EEZ o área de gestión merece una revisión temporal;
- qué eventos podrían requerir contraste documental, como encuentros o apagados AIS;
- qué parte del análisis procede de AIS, VMS, SAR, VIIRS, modelos o capas de referencia;
- qué límites de cobertura, latencia, identidad y clasificación afectan a la lectura.

La guía de usuario explica que el esfuerzo pesquero aparente se calcula analizando datos AIS de buques conocidos o posibles pesqueros y aplicando un algoritmo basado en cambios de velocidad y dirección. Esa distinción importa: el sistema clasifica puntos de transmisión como aparentemente pescando o no pescando, pero no observa directamente una red, una captura ni una infracción.

La documentación de APIs, por su parte, muestra una plataforma más amplia que el mapa. En la versión 3 aparecen endpoints y datasets para visualización, presencia AIS, esfuerzo pesquero aparente, detecciones SAR, eventos, buques, insights, datasets y descargas masivas. Para un analista, esto permite pasar de una exploración manual a un flujo reproducible, siempre que se respeten licencias, límites y finalidad.

## Caso de uso legítimo con ejemplo ficticio

Imagina una ONG ficticia, `Costa Clara`, que prepara un informe sobre presión pesquera alrededor de una reserva marina. El objetivo no es identificar personas ni señalar a una embarcación concreta en redes sociales. El objetivo es construir una pregunta verificable:

```text
Pregunta: ¿hubo concentración anómala de actividad pesquera aparente cerca del límite exterior de la reserva?
Zona: polígono público de la reserva y franja de 20 millas náuticas alrededor
Periodo: enero a marzo de 2026
Unidad de análisis: celdas/agregados y eventos para revisión, no acusaciones individuales
Fuentes auxiliares: normativa de la reserva, autorizaciones públicas, comunicados, imágenes satelitales y entrevistas autorizadas
```

Un primer mapa puede revelar horas de actividad aparente cerca del límite. Eso no prueba pesca ilegal. Puede tratarse de tránsito, actividad permitida, errores de clasificación, desfases temporales, cobertura desigual o límites geográficos mal entendidos. La utilidad real consiste en ordenar qué merece revisión:

| Señal | Lectura prudente | Siguiente comprobación |
| --- | --- | --- |
| Alta actividad aparente en una celda | Posible concentración de esfuerzo | Comparar fechas, artes, bandera y límites oficiales |
| Presencia sin pesca aparente | Tránsito, espera u otra actividad | Contrastar con rutas, puertos y condiciones |
| Encuentros entre buques | Indicador para revisar, no prueba de transbordo | Mirar duración, distancia a puerto, tipo de buque y contexto |
| AIS apagado | Hueco de señal, intencional o técnico | Corroborar con SAR, historial y explicación plausible |
| Detección SAR no emparejada | Posible buque sin AIS visible | Revisar resolución, confianza, climatología y fuentes externas |

El resultado defendible no sería "estos barcos cometieron una infracción". Sería algo más estrecho:

> Entre enero y marzo se observa actividad pesquera aparente agregada en varias celdas próximas al límite de la reserva. Recomendamos contrastar esas fechas con autorizaciones, normativa aplicable y observaciones independientes antes de atribuir conducta irregular.

Ese matiz protege la investigación y a las personas afectadas.

## Flujo recomendado

### 1. Empezar por una pregunta geográfica y temporal

No abras el mapa para "buscar cosas raras". Define zona, periodo y decisión analítica:

- zona exacta: EEZ, área marina protegida, puerto, corredor o polígono propio;
- periodo: fechas cerradas y zona horaria documentada;
- métrica: horas de esfuerzo aparente, presencia, eventos, detecciones o comparación entre capas;
- hipótesis: qué esperas comprobar y qué dato la refutaría.

En OSINT marítimo, una mala geometría contamina todo. Si el polígono de una reserva, una frontera marítima o un buffer no corresponde a la fuente oficial adecuada, el análisis puede parecer preciso y estar desplazado desde el primer paso.

### 2. Separar presencia, pesca aparente y detección

`Global Fishing Watch` distingue capas con significados diferentes. Conviene escribirlos en tus notas:

- `AIS vessel presence`: presencia derivada de posiciones AIS, no limitada a pesca;
- `AIS apparent fishing effort`: clasificación de posible actividad pesquera por patrones de movimiento;
- `SAR vessel detections`: detecciones en imágenes radar, útiles también cuando no hay AIS visible;
- `VMS`: datos de sistemas de seguimiento pesquero cuando están disponibles para países o acuerdos concretos;
- eventos: encuentros, loitering, visitas a puerto, actividad pesquera aparente o apagados AIS, según cobertura.

Mezclar esas capas en una sola frase suele producir conclusiones exageradas. "Había presencia de buques" no es lo mismo que "había pesca aparente", y "SAR detectó un objeto compatible" no es lo mismo que "identificamos un buque concreto".

### 3. Trabajar primero en agregado

Para un informe responsable, empieza por patrones:

1. selecciona el área y el rango temporal;
2. compara actividad antes, durante y después del periodo de interés;
3. revisa si el patrón se concentra en el borde de una zona, en rutas conocidas o en puntos aislados;
4. documenta capas activas, filtros y fecha de consulta;
5. exporta solo lo necesario para replicar el análisis;
6. pasa a eventos o buques concretos solo cuando exista una razón legítima y proporcionada.

La propia disponibilidad de datos indica que muchos productos son dinámicos y de "near real time" con retrasos como 72 horas, mientras otros son datasets estables actualizados diaria, mensual o históricamente. Esa mezcla obliga a anotar qué versión o estado se consultó.

### 4. Tratar eventos como indicadores de revisión

Los eventos son atractivos porque parecen narrativos: dos buques se encuentran, una señal desaparece, una embarcación entra o sale de puerto. Pero son salidas de modelos o reglas aplicadas a datos imperfectos.

Por ejemplo, la FAQ de encuentros explica que un evento se clasifica cuando dos embarcaciones aparecen dentro de 500 metros durante al menos dos horas, a baja velocidad y lejos de un fondeadero costero. La misma página advierte que los encuentros pueden deberse a transbordo, suministros, cambios de tripulación, seguridad u otros motivos, y que la proximidad se calcula con posiciones estimadas en una malla temporal.

La forma sana de escribirlo es:

```text
Correcto: "El sistema marca un evento de encuentro que requiere revisión."
Incorrecto: "El mapa demuestra un transbordo ilegal."
```

### 5. Corroborar antes de atribuir

Una línea de evidencia no basta. Según el caso, combina:

- normativa y límites oficiales de la zona;
- registros de autorizaciones, licencias o listas RFMO;
- información de puertos y escalas;
- imágenes SAR o ópticas cuando sean pertinentes;
- meteorología, estado de mar y visibilidad;
- registros corporativos o de propiedad cuando el análisis sea societario;
- respuesta de las partes afectadas si se va a publicar una conclusión sensible.

La pregunta no es "qué puedo inferir". La pregunta es "qué inferencia sobreviviría a una revisión técnica y legal".

## Limitaciones y falsos positivos

`Global Fishing Watch` es potente precisamente porque hace visibles patrones que antes estaban dispersos. Pero sus límites son parte del dato:

- `AIS` nació como sistema de seguridad y evitación de colisiones, no como registro forense universal;
- no todos los buques están obligados a emitir AIS en todos los contextos;
- las señales pueden faltar, ser irregulares, estar mal configuradas o cambiar de identidad aparente;
- la clasificación de pesca depende de modelos que interpretan movimiento, no capturas reales;
- la cobertura SAR ayuda a detectar buques sin AIS visible, pero también requiere lectura de confianza, fecha, resolución y contexto;
- los límites marítimos, áreas protegidas y autorizaciones pueden variar por fuente;
- el dato bruto AIS usado por la plataforma no está disponible libremente, aunque existan datasets derivados y muestras anonimizadas;
- una ausencia en el mapa no demuestra ausencia de actividad en el mar.

La documentación técnica también recuerda problemas de identidad: una búsqueda de buque puede devolver varios identificadores porque las transmisiones AIS y los registros no siempre encajan limpiamente. Un cambio real de bandera, nombre o puerto puede parecerse a una transmisión incompleta; una transmisión incompleta puede crear registros separados para el mismo buque.

## Buenas prácticas de OPSEC, ética y privacidad

El OSINT marítimo toca actividades económicas, tripulaciones, comunidades costeras, investigación ambiental, cumplimiento regulatorio y, a veces, conflictos. Esa combinación exige prudencia:

- evita publicar rutas operativas recientes si no hay interés público claro;
- trabaja con agregados cuando baste para responder la pregunta;
- no conviertas nombres de buques, banderas o empresas en acusaciones sin contraste;
- separa dato observado, salida de modelo, inferencia y conclusión;
- respeta términos de uso, límites de API y licencias de datos;
- documenta capturas, consultas, fechas y filtros;
- minimiza datos personales y evita señalar tripulantes;
- si el caso puede tener consecuencias legales, pide revisión especializada antes de publicar.

La transparencia no consiste en exponerlo todo. Consiste en que el análisis sea verificable, proporcional y honesto sobre sus incertidumbres.

## Alternativas y siguientes pasos

`Global Fishing Watch` encaja especialmente bien cuando la pregunta es marítima, espacial y temporal. Según el caso, puede complementarse con:

- registros oficiales de buques y autorizaciones pesqueras;
- `MarineTraffic`, `VesselFinder` u otros servicios AIS comerciales, teniendo en cuenta licencias y cobertura;
- `Sentinel Hub EO Browser` o `Copernicus Browser` para imágenes satelitales;
- `NASA FIRMS` si la investigación toca incendios, anomalías térmicas o actividad costera;
- `OpenStreetMap` y cartas náuticas para contexto geográfico;
- registros societarios y sanciones cuando el análisis se mueva de actividad marítima a propiedad, control o cumplimiento.

La takeaway accionable es simple: usa `Global Fishing Watch` para **convertir actividad marítima visible en preguntas reproducibles**, no para cerrar casos por intuición. Si una señal parece importante, el siguiente paso no es endurecer el titular, sino comprobar fuente, modelo, zona, fecha, autorización y explicación alternativa.

## Fuentes consultadas

- [`Global Fishing Watch`, mapa y guía de usuario](https://globalfishingwatch.org/user-guide/), consultado el `12 de julio de 2026`.
- [`Global Fishing Watch API Documentation`](https://globalfishingwatch.org/our-apis/documentation), consultado el `12 de julio de 2026`.
- [`Global Fishing Watch Data Availability`](https://globalfishingwatch.org/global-fishing-watch-data-availability/), consultado el `12 de julio de 2026`.
- [`Can I download raw AIS data?`](https://globalfishingwatch.org/faqs/can-i-download-raw-ais-data/), consultado el `12 de julio de 2026`.
- [`What is a vessel encounter?`](https://globalfishingwatch.org/faqs/what-is-a-vessel-encounter/), consultado el `12 de julio de 2026`.
- [`Journal article clarifies how Global Fishing Watch fishing data is generated`](https://globalfishingwatch.org/article/journal-article-clarifies-how-global-fishing-watch-fishing-data-is-generated/), consultado el `12 de julio de 2026`.
