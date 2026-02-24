---
title: "ADS-B Exchange y MarineTraffic en OSINT: seguimiento de activos con contexto, limites y verificacion responsable"
slug: /ads-b-exchange-marinetraffic-osint-seguimiento-activos-contexto-limites
authors: [osint-writter]
tags: [osint, tools, geoint, investigation, verification, opsec]
date: 2026-02-24
image: /img/blog/2026-02-24-ads-b-exchange-marinetraffic-osint-seguimiento-activos-contexto-limites.png
---

![Ilustracion editorial de analista OSINT cruzando trazas de vuelo y trafico maritimo en mapas para verificar contexto operativo](/img/blog/2026-02-24-ads-b-exchange-marinetraffic-osint-seguimiento-activos-contexto-limites.png)

Cuando una investigacion depende de entender **movimientos** (un avion, un buque, una ruta, una ventana temporal), el error mas comun no es "no tener datos": es leer una traza aislada como si ya explicara la historia completa. `ADS-B Exchange` y `MarineTraffic` son dos piezas muy utiles para OSINT, pero solo aportan valor real cuando se usan con contexto, cobertura, tiempos de actualizacion y verificacion cruzada.

Este contenido esta orientado a usos legitimos (periodismo, analisis de riesgos, due diligence, seguridad defensiva, verificacion de incidentes y cadena logistica). No incluye instrucciones para acoso, doxxing ni dano a terceros.

<!-- truncate -->

## Que es (y para que sirve)

### ADS-B Exchange (aviacion)

`ADS-B Exchange` agrega datos de seguimiento de aeronaves a partir de una red de feeders y destaca por su enfoque de datos no filtrados, incluyendo aeronaves que en otros servicios pueden aparecer limitadas o ausentes. Para OSINT, esto es util cuando necesitas:

- Reconstruir una cronologia de movimientos aereos.
- Verificar si una aeronave estuvo realmente en una zona/ventana temporal.
- Contrastar relatos publicos con actividad observable (sin saltar a conclusiones causales).

### MarineTraffic (maritimo/AIS)

`MarineTraffic` se apoya en datos AIS (Automatic Identification System) recibidos por estaciones costeras y, en ciertas zonas, cobertura satelital AIS. En OSINT es especialmente valioso para:

- Seguir rutas y escalas de buques.
- Analizar patrones logísticos y tiempos de transito.
- Corroborar presencia/ausencia de activos cerca de puertos o zonas de interes.

La combinacion de ambas herramientas es potente en investigaciones de cadena de suministro, cumplimiento, incidentes operativos y verificacion de narrativas, siempre con prudencia metodologica.

## Caso de uso legitimo (ejemplo ficticio)

Supongamos una investigacion de cumplimiento interno: una empresa quiere verificar si una carga critica pudo sufrir un retraso por un desvio operativo y no por una supuesta "retencion aduanera" comunicada por un tercero.

Escenario ficticio:

- Un componente urgente vuela a un hub regional.
- Luego se embarca en un buque feeder hacia un puerto final.
- Hay una discrepancia de 36 horas entre la version comercial y la operativa.

Flujo OSINT defensivo:

1. En `ADS-B Exchange`, localizas el vuelo de carga relevante y verificas ventana de aterrizaje aproximada.
2. En `MarineTraffic`, revisas el estado del buque, hora de salida estimada y trayectoria posterior.
3. Cruzas la linea temporal con avisos publicos del puerto, meteorologia y comunicados del operador.
4. Redactas conclusiones separando:
   - hechos observables (trazas/horas/posiciones),
   - inferencias razonables,
   - incertidumbres pendientes.

Resultado esperado: una explicacion mas robusta del retraso sin atribuir intenciones ni acusar a personas.

## Flujo recomendado (pasos)

### 1. Define la pregunta exacta

No empieces por "voy a mirar mapas". Empieza por una pregunta verificable:

- "¿Estuvo el activo X en la zona Y entre T1 y T2?"
- "¿Que tramo explica mejor el retraso?"
- "¿Hay coherencia temporal entre el movimiento observado y el relato publico?"

### 2. Identifica el activo con trazabilidad

Evita homonimos y coincidencias superficiales.

- Aviacion: matricula, hex/ICAO, callsign y tipo de aeronave.
- Maritimo: MMSI, IMO, nombre del buque (los nombres cambian o se repiten).

Documenta desde el inicio el identificador principal y los alias secundarios.

### 3. Captura evidencia temporal (no solo capturas de pantalla)

Registra:

- Fecha y hora (con zona horaria clara).
- Fuente exacta (URL/pantalla/consulta).
- Estado de cobertura ("en rango", "sin refresco", "dato historico", etc.).
- Limitaciones observadas (saltos, downsampling, huecos).

Una captura bonita sin metadatos de contexto vale poco para revisiones posteriores.

### 4. Verifica cobertura y frecuencia de actualizacion

Este paso evita la mayoria de errores de interpretacion:

- En `MarineTraffic`, la frecuencia visible depende del tipo de transpondedor, estado del buque y cobertura (costera vs satelital).
- En zonas remotas, la latencia puede crecer mucho y no debes interpretar huecos como "apagado" o "maniobra oculta" sin mas evidencias.
- En aviacion, la cobertura tambien depende de la red de receptores y del tipo/calidad de senal disponible en esa zona.

### 5. Cruza con una segunda fuente

Nunca cierres una conclusion solo con una traza.

- NOTAM/avisos operativos (si aplican)
- METAR/meteorologia
- comunicados de puertos/aeropuertos
- imagenes satelitales, prensa local o redes institucionales
- documentos corporativos/publicos con horarios o escalas

### 6. Separa observacion de interpretacion

Ejemplo de redaccion correcta:

- Observacion: "El buque aparece en posicion A a las 10:12 UTC y en posicion B a las 11:14 UTC (fuente: MarineTraffic)."
- Inferencia: "Es compatible con una espera o baja velocidad en aproximacion."
- No demostrado: "No se puede afirmar causa sin datos operativos del armador/puerto."

## Limitaciones y falsos positivos

### 1. Cobertura incompleta no equivale a ocultacion

Un hueco en la traza puede deberse a:

- falta de cobertura terrestre,
- latencia satelital,
- downsampling en la plataforma,
- problemas de recepcion locales,
- cambios de visualizacion historica.

### 2. Identidad mal resuelta del activo

Errores tipicos:

- confundir aeronaves por callsign similar,
- confundir buques por nombre comercial repetido,
- mezclar historial de un activo con otro tras cambios de identificador.

### 3. Sobrelectura causal

Ver una ruta no demuestra automaticamente:

- motivo del vuelo/escala,
- carga concreta,
- decision interna de una organizacion,
- intencionalidad.

Las trazas muestran movimiento; la explicacion causal exige mas capas.

## Buenas practicas (OPSEC, etica y privacidad)

- Define un objetivo legitimo antes de abrir herramientas (cumplimiento, seguridad, verificacion, periodismo).
- Minimiza datos personales en notas y capturas si no son necesarios para la hipotesis.
- Evita compartir en tiempo real movimientos sensibles de personas fisicas.
- Conserva un registro de fuentes para auditoria interna y correccion de errores.
- Usa lenguaje de certeza graduada ("compatible con", "sugiere", "no concluyente").

La disciplina de escritura es una medida de seguridad metodologica.

## Alternativas y siguientes pasos

Segun el caso, estas herramientas pueden combinarse con:

- `OpenSky Network` (aviacion, segun disponibilidad del caso y acceso)
- avisos portuarios/aeronauticos oficiales
- datos meteorologicos historicos
- `Sentinel Hub` u otras fuentes GEOINT para corroboracion visual
- hojas de tiempo (timeline) en `SQLite`/`Datasette` para trazabilidad

Si vas a trabajar este tipo de casos de forma recurrente, el siguiente salto de calidad no es "otra app": es crear una plantilla de cronologia con campos de evidencia, cobertura y grado de confianza.

## Referencias (consulta y metodologia)

- ADS-B Exchange: que es la plataforma y como funciona la red de feeders (sitio oficial).
- ADS-B Exchange: acceso a datos, terminos de uso y caracteristicas de feeds/historico (sitio oficial).
- MarineTraffic Help Center: protocolo AIS, recoleccion de datos y uso de estaciones receptoras.
- MarineTraffic Help Center: frecuencias de actualizacion, cobertura costera/satelital y downsampling.

## Cierre

`ADS-B Exchange` y `MarineTraffic` son excelentes herramientas OSINT cuando la pregunta es temporal y espacial. El valor no esta en "ver puntitos moviendose", sino en construir una **cronologia verificable** con limites explicitados y corroboracion multifuente.

Siguiente tema sugerido (para seguir alternando sin repetir enfoque): `ExifTool & InVID` para verificacion multimedia con metodologia de falsos positivos.
