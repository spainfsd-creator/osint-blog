---
title: "OpenAQ en OSINT: calidad del aire, sensores y contexto antes de atribuir causas"
slug: /openaq-osint-calidad-aire-datos-abiertos-contexto
authors: [osint-writter]
tags: [osint, geoint, data, verification, methodology, tools]
date: 2026-07-13
image: /img/blog/2026-07-13-openaq-osint-calidad-aire-datos-abiertos-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando datos abiertos de calidad del aire, sensores, series temporales, mapas y notas de verificacion](/img/blog/2026-07-13-openaq-osint-calidad-aire-datos-abiertos-contexto.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/openaq-osint-calidad-aire-datos-abiertos-contexto.m4a)


Un pico de contaminacion en una grafica puede parecer una acusacion lista para publicar: una fabrica cercana, una carretera saturada, una columna de humo y una hora concreta. En OSINT ambiental responsable, sin embargo, el primer deber no es senalar un culpable, sino preguntar **que midio realmente el sensor, de donde procede el dato, que licencia lo cubre y que explicaciones alternativas siguen abiertas**.

[`OpenAQ`](https://openaq.org/) ayuda en esa fase de contexto. Agrega y armoniza datos abiertos de calidad del aire de muchas fuentes, los expone mediante una plataforma web y una API, y permite trabajar con mediciones historicas o recientes sin depender solo de una captura aislada. Revisando su documentacion oficial el **13 de julio de 2026**, la API publica recursos para ubicaciones, sensores, mediciones, ultimos valores, parametros, proveedores, propietarios y licencias; usa `X-API-Key` para autenticar peticiones; y documenta limites generales de `60` solicitudes por minuto y `2.000` por hora para uso gratuito.

Este articulo esta escrito para periodistas de datos, analistas OSINT, equipos ambientales, investigadores academicos y organizaciones que necesitan contrastar informacion publica sobre calidad del aire. No es una guia para acosar instalaciones, exponer domicilios, fabricar alarmas sanitarias ni convertir una correlacion temporal en atribucion causal.

<!-- truncate -->

## Que es OpenAQ y para que sirve

`OpenAQ` es una plataforma abierta de datos de calidad del aire. Su objetivo practico es reunir datos de distintas fuentes, armonizarlos y hacerlos consultables con una estructura comun. Para una investigacion OSINT, eso permite pasar de "he visto una grafica" a preguntas mas defendibles:

- que sensores existen cerca de una zona;
- que parametros mide cada sensor;
- quien es el proveedor y, cuando consta, quien gestiona la estacion;
- que unidades y contaminantes se estan observando;
- que mediciones recientes o historicas hay para un periodo;
- que licencia y condiciones de atribucion afectan al uso del dato;
- si una senal aparece en un sensor aislado o se repite en estaciones cercanas.

La documentacion de la API describe un enfoque `REST` con respuestas `JSON` y recursos orientados a entidades. Tambien acota el tipo de datos que conviene esperar: OpenAQ se centra sobre todo en contaminantes criterio como `PM2.5`, `PM10`, `SO2`, `NO2`, `CO`, `O3`, carbono negro, humedad relativa y temperatura, con cobertura limitada para otros parametros como `PM1`, `PM4`, `CO2`, `NO`, `NOx`, `CH4` y particulas ultrafinas.

Ese matiz importa. OpenAQ no es un laboratorio forense, no reemplaza a las autoridades ambientales y no observa causas. Es una capa de datos para formular mejores hipotesis, detectar huecos y decidir que corroboracion hace falta.

## Caso de uso legitimo con ejemplo ficticio

Imagina que una redaccion local recibe quejas por olor y particulas en el barrio ficticio de `Ribera Norte`. En redes circula una captura que acusa directamente a una planta industrial. La redaccion quiere comprobar si hubo una anomalia ambiental real sin amplificar una acusacion que todavia no esta probada.

Un flujo prudente podria empezar asi:

1. delimitar la zona y la ventana temporal de la queja;
2. buscar ubicaciones de OpenAQ dentro de un radio razonable;
3. identificar que sensores miden `PM2.5`, `PM10`, `NO2` u otros parametros relevantes;
4. anotar proveedor, propietario, zona horaria, licencia y estado activo de cada ubicacion;
5. comparar la serie del sensor cercano con estaciones de referencia y estaciones de fondo;
6. contrastar meteorologia, direccion del viento, trafico, obras, incendios, avisos oficiales y comunicados;
7. escribir una conclusion limitada a lo observado.

El resultado responsable no seria "OpenAQ demuestra que la planta X contamino". Seria algo mas estrecho:

> En la tarde del 12 de julio se observa un aumento de PM2.5 en dos sensores cercanos a Ribera Norte. La senal coincide con viento del oeste y no basta para atribuir causa. Hemos pedido datos oficiales, revisado estaciones de referencia y conservado el rango horario para contraste.

La diferencia es clave: el dato abre una investigacion, no condena a nadie.

## Flujo recomendado

### 1. Empezar por ubicaciones, no por conclusiones

Antes de buscar mediciones, localiza las estaciones o sensores que cubren la zona. El recurso de `locations` documenta nombres, coordenadas, zona horaria, proveedor, propietario cuando existe, sensores asociados y detalles como si una estacion es movil o fija.

En un cuaderno de investigacion, conviene registrar:

```text
Zona ficticia: Ribera Norte
Pregunta: hubo una anomalia de PM2.5 o PM10 durante la tarde del 12 de julio?
Fuente base: OpenAQ locations y measurements
Radio inicial: 5 km, ampliable si hay pocos sensores
Unidad temporal: hora local documentada y UTC cuando se exporte
Decision: detectar senal ambiental que merezca contraste, no atribuir causa
```

Una ausencia de sensores cercanos no significa ausencia de contaminacion. Significa ausencia de observacion en esa capa.

### 2. Separar parametro, sensor y proveedor

No mezcles todo bajo la etiqueta "contaminacion". `PM2.5`, `PM10`, `NO2` y `O3` cuentan historias diferentes. Tambien cambia mucho si el dato procede de una estacion regulatoria, una red universitaria, un sensor comunitario o un proveedor privado.

OpenAQ ayuda a separar esas piezas con recursos como:

| Recurso | Utilidad OSINT | Riesgo si lo ignoras |
| --- | --- | --- |
| `parameters` | Entender contaminante, unidad y descripcion | Comparar cosas que no son equivalentes |
| `locations` | Situar estaciones, zona horaria y sensores | Creer que un punto cubre toda una ciudad |
| `sensors` | Ver que mide cada instrumento | Tratar un valor como si viniera de cualquier sensor |
| `providers` | Saber quien suministra el dato | Perder trazabilidad de origen |
| `owners` | Identificar quien gestiona la estacion cuando consta | Atribuir mal la responsabilidad del dato |
| `licenses` | Comprobar permisos y atribucion | Reutilizar datos incumpliendo condiciones |

La trazabilidad no es burocracia. Es lo que permite que otro analista revise tu lectura.

### 3. Usar `latest` solo para triage rapido

El recurso `latest` sirve para ver mediciones recientes y ubicacion geografica. Es util para una primera orientacion, pero no deberia cerrar una historia sensible. Un valor reciente puede estar afectado por latencia, calibracion, mantenimiento, condiciones meteorologicas o ruido local.

Para una pieza publicable, pasa cuanto antes a mediciones por sensor y a agregaciones adecuadas. La propia documentacion de `measurements` distingue valores originales y distintos niveles de agregacion. Decide si necesitas dato puntual, media horaria, comparacion diaria o contexto historico.

### 4. Documentar la API y sus limites

La API requiere clave en la cabecera `X-API-Key`. Los ejemplos oficiales usan un placeholder que no funciona por si solo, y la documentacion indica que hay que registrarse en OpenAQ Explorer para obtener una clave propia.

Un ejemplo responsable, con coordenadas ficticias, seria:

```bash
curl --request GET \
  --url "https://api.openaq.org/v3/locations?coordinates=-3.7038,40.4168&radius=5000&limit=100" \
  --header "X-API-Key: TU_CLAVE_OPENAQ"
```

No automatices a ciegas. Si tu flujo necesita volumen, respeta los limites, pagina resultados, cachea respuestas y registra que endpoints consultaste. En julio de 2026, la documentacion de rate limits indica `60` peticiones por minuto y `2.000` por hora para el uso gratuito general.

### 5. Corroborar fuera de OpenAQ

Una serie ambiental nunca deberia interpretarse sola. Como minimo, contrasta:

- estaciones oficiales cercanas y de fondo urbano;
- meteorologia, especialmente viento, lluvia e inversiones termicas;
- mapas de trafico, obras y actividad portuaria o industrial cuando sea pertinente;
- avisos de autoridades ambientales;
- imagenes satelitales o datos de incendios si el caso apunta a humo;
- cronologia de quejas, comunicados y observaciones sobre el terreno autorizadas.

Si la senal solo aparece en un sensor y no en otros, no la descartes ni la conviertas en titular. Tratarla como pista aislada suele ser mas honesto.

## Limitaciones y falsos positivos

OpenAQ es valioso precisamente porque reduce friccion, pero tiene limites que deben aparecer en cualquier analisis serio:

- la cobertura geografica es desigual;
- no todos los sensores miden todos los parametros;
- los sensores de bajo coste pueden necesitar calibracion y contexto;
- una estacion puede estar fuera de servicio, moverse o cambiar de proveedor;
- los datos pueden llegar con retraso o correcciones posteriores;
- las unidades y agregaciones deben leerse con cuidado;
- una correlacion temporal no prueba fuente, intencion ni responsabilidad;
- la licencia puede exigir atribucion o limitar ciertos usos;
- el dato ambiental puede afectar a comunidades reales, por lo que el lenguaje importa.

El falso positivo clasico es confundir proximidad con causalidad: "el sensor esta cerca de una instalacion, luego la instalacion causo el pico". En realidad pueden intervenir viento, trafico, obras, polvo sahariano, incendios, calefaccion residencial, mantenimiento del sensor o un error de lectura.

## Buenas practicas de OPSEC, etica y privacidad

Aunque la calidad del aire parezca un tema menos sensible que personas o infraestructura critica, el dano por mala atribucion puede ser real. Un informe precipitado puede alarmar a vecinos, perjudicar a trabajadores, estigmatizar una zona o acusar a una organizacion sin base suficiente.

Buenas practicas:

- trabaja con datos agregados cuando no necesites granularidad extrema;
- evita publicar coordenadas de sensores privados o comunitarios si pueden identificar domicilios;
- no presentes sensores ciudadanos como equivalentes automaticos a estaciones regulatorias;
- conserva consultas, fechas, zona horaria, endpoint, parametros y version de salida;
- cita proveedor, propietario y licencia cuando el dataset lo indique;
- separa observacion, hipotesis y conclusion;
- ofrece derecho de respuesta cuando una pieza mencione a una entidad concreta;
- deja claro que OpenAQ aporta mediciones, no atribucion causal.

En OSINT responsable, la prudencia no rebaja el trabajo: lo hace mas util.

## Alternativas y siguientes pasos

OpenAQ encaja bien cuando necesitas datos abiertos de calidad del aire con API y trazabilidad. Segun la pregunta, puede combinarse con:

- portales oficiales de calidad del aire de administraciones nacionales, regionales o municipales;
- `NASA FIRMS`, si el contexto apunta a incendios o anomalias termicas;
- meteorologia oficial y reanalisis atmosfericos para viento y dispersion;
- `Overpass Turbo` u `OpenStreetMap` para contexto territorial;
- `GDELT` o hemerotecas si quieres mapear cobertura mediatica de un episodio;
- `Datasette`, `SQLite` u `OpenRefine` para limpiar y auditar series descargadas.

La takeaway accionable es simple: usa `OpenAQ` para **convertir una sospecha ambiental en una pregunta verificable**, no para saltar de una grafica a una acusacion. Si detectas una senal, guarda la consulta, compara sensores, revisa licencias y busca corroboracion independiente antes de publicar.

## Fuentes consultadas

- [OpenAQ](https://openaq.org/)
- [OpenAQ Docs: About the API](https://docs.openaq.org/about/about)
- [OpenAQ Docs: API overview](https://docs.openaq.org/api)
- [OpenAQ Docs: Locations](https://docs.openaq.org/resources/locations)
- [OpenAQ Docs: Measurements](https://docs.openaq.org/resources/measurements)
- [OpenAQ Docs: Latest](https://docs.openaq.org/resources/latest)
- [OpenAQ Docs: API key](https://docs.openaq.org/using-the-api/api-key)
- [OpenAQ Docs: Rate limits](https://docs.openaq.org/using-the-api/rate-limits)
- [OpenAQ Docs: Licenses](https://docs.openaq.org/resources/licenses)
