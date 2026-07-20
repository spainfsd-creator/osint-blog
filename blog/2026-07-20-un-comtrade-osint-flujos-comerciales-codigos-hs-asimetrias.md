---
title: "UN Comtrade en OSINT: flujos comerciales, códigos HS y asimetrías sin falsas certezas"
slug: /un-comtrade-osint-flujos-comerciales-codigos-hs-asimetrias
authors: [osint-writter]
tags: [osint, data, trade, verification, investigation, methodology]
date: 2026-07-20
image: /img/blog/2026-07-20-un-comtrade-osint-flujos-comerciales-codigos-hs-asimetrias.png
---

![Ilustración editorial de una analista OSINT comparando mapas de comercio, códigos de producto, documentos aduaneros y una cronología reproducible](/img/blog/2026-07-20-un-comtrade-osint-flujos-comerciales-codigos-hs-asimetrias.png)

Una gráfica asegura que las exportaciones de un producto se han disparado. Otra, construida con el país socio, cuenta algo distinto. Antes de hablar de evasión, desvíos o una nueva ruta comercial, quedan preguntas bastante menos vistosas: **¿qué país informó el dato, qué código de producto se usó, qué revisión estaba vigente y se están comparando importaciones CIF con exportaciones FOB?** `UN Comtrade` sirve para responderlas con estadísticas oficiales abiertas, siempre que el analista trate cada cifra como una observación documentada y no como una acusación.

<!-- truncate -->

Revisando la documentación oficial el **20 de julio de 2026**, la División de Estadística de Naciones Unidas describe `UN Comtrade` como una plataforma que agrega estadísticas comerciales anuales y mensuales por producto y socio, comunicadas por las autoridades estadísticas de los países y territorios. El portal permite explorar mercancías y servicios, consultar clasificaciones como `HS`, `SITC` y `BEC`, descargar resultados y trabajar mediante API. También advierte que los datos se incorporan y revisan continuamente, y que no existe un calendario fijo para la publicación de cada país.

Eso la convierte en una fuente extraordinaria para investigar tendencias agregadas, dependencias comerciales o aparentes discrepancias. No la convierte en un registro de envíos individuales ni en una prueba directa sobre una empresa o una persona. Este artículo está pensado para periodistas de datos, analistas de riesgo, investigadores académicos y equipos de debida diligencia. No es una guía para perfilar individuos, eludir controles comerciales o señalar conductas ilícitas sin evidencia primaria.

## Qué es UN Comtrade y para qué sirve

`UN Comtrade` reúne estadísticas oficiales de comercio exterior. Su unidad de análisis habitual combina varias dimensiones:

- **reporter**: el país o territorio que comunica el dato;
- **partner**: el socio comercial atribuido;
- **flow**: importación, exportación u otro flujo disponible;
- **period**: año o mes;
- **commodity**: producto clasificado con un código como `HS`;
- **value**, peso y cantidades: medidas cuya disponibilidad y calidad varían;
- metadatos adicionales, cuando el informante los aporta, como modo de transporte o procedimiento aduanero.

La distinción entre *reporter* y *partner* es crucial. Si España declara importaciones procedentes del país ficticio `Litoralia`, observamos la estadística española. Si `Litoralia` declara exportaciones hacia España, observamos otra estadística oficial sobre el flujo espejo. Parecen dos caras de la misma operación agregada, pero rara vez coinciden exactamente.

Para OSINT responsable, Comtrade resulta especialmente útil en cuatro tareas:

1. comprobar si una afirmación pública encaja con la tendencia agregada;
2. comparar productos, socios y periodos con una consulta reproducible;
3. detectar anomalías que merecen una segunda fuente;
4. construir contexto antes de revisar aduanas nacionales, memorias empresariales, sanciones, contratos o registros sectoriales.

No revela por sí sola quién envió una mercancía, qué buque la transportó ni por qué cambió el flujo. Una tabla nacional no debe convertirse mágicamente en una atribución empresarial.

## Caso de uso legítimo: comprobar una narrativa sobre componentes solares

Imagina que una asociación sectorial afirma que `Puerto Claro`, un país ficticio, duplicó en un año sus importaciones de componentes solares desde `Sierra Norte`. El objetivo del analista no es demostrar contrabando ni buscar personas. Es comprobar si la narrativa cuantitativa está bien construida.

La primera tarea consiste en traducir “componentes solares” a una clasificación concreta. Una etiqueta periodística puede abarcar células fotovoltaicas, módulos completos, inversores, conectores y piezas que viven en partidas diferentes. Elegir un único código sin documentarlo puede fabricar el salto que queríamos encontrar.

Un flujo prudente tendría esta forma:

1. identificar la revisión `HS` usada por el informante y leer la descripción oficial del código;
2. consultar a `Puerto Claro` como *reporter*, `Sierra Norte` como *partner* y las importaciones como *flow*;
3. descargar varios años, no solo los dos que producen el titular más llamativo;
4. repetir con el flujo espejo: exportaciones declaradas por `Sierra Norte` hacia `Puerto Claro`;
5. anotar fecha de extracción, parámetros y posibles revisiones;
6. contrastar la anomalía con estadísticas nacionales, cambios arancelarios, capacidad logística y documentación sectorial.

El resultado podría confirmar la dirección del cambio, mostrar que solo afecta a una subpartida o revelar que el supuesto crecimiento aparece porque se compararon revisiones incompatibles. Cualquiera de esos resultados es útil. Ninguno autoriza a atribuir intención ilícita.

## Flujo recomendado paso a paso

### 1. Formula una hipótesis que pueda fallar

Evita empezar con “voy a demostrar un desvío comercial”. Una formulación más sana sería: “quiero comprobar si el valor declarado para este producto, reportero y socio cambia de forma anómala frente a su propia serie y frente al flujo espejo”.

Define antes de consultar:

- producto y nivel de agregación;
- revisión de la clasificación;
- informante y socio;
- importaciones o exportaciones;
- frecuencia y ventana temporal;
- moneda, valor, peso o cantidad que analizarás;
- umbral que justificaría ampliar la investigación.

### 2. Resuelve el código de producto, no solo su nombre

El `Harmonized System` organiza mercancías en una jerarquía de códigos. Las revisiones cambian con el tiempo y una conversión entre versiones puede agrupar, dividir o dejar sin equivalencia exacta determinadas partidas. La documentación histórica de Naciones Unidas recuerda además que no toda conversión es reversible: transformar datos hacia una clasificación anterior no equivale a reconstruir una clasificación posterior con el mismo detalle.

Guarda siempre:

- el código y su descripción;
- la revisión `HS` o la clasificación alternativa;
- el nivel de dígitos consultado;
- cualquier tabla de correspondencia aplicada;
- las partidas incluidas y excluidas por decisión analítica.

Para una primera exploración suele ser sensato empezar con una categoría amplia y bajar de nivel solo cuando la pregunta lo exige. El detalle aparente no compensa una clasificación equivocada.

### 3. Construye una consulta mínima y reproducible

En la interfaz web, fija explícitamente producto, frecuencia, periodo, informante, socio y flujo. Si usas la API, conserva la URL o los parámetros y la respuesta original. Una consulta pública de validación puede seguir esta estructura conceptual:

```text
type=C
freqCode=A
clCode=HS
period=2024
reporterCode=<código del informante>
partnerCode=<código del socio>
cmdCode=<código HS>
flowCode=M
```

Los nombres y límites concretos del servicio deben comprobarse en el portal de desarrolladores antes de automatizar. El acceso gratuito registrado anuncia hasta `100.000` registros por llamada y `500` llamadas diarias, pero esas condiciones pueden cambiar. Diseña caché, consultas acotadas y pausas razonables en vez de depender de cifras permanentes.

Para que otra persona pueda repetir el hallazgo, conserva un pequeño manifiesto junto al fichero descargado:

```yaml
fuente: UN Comtrade
extraido_utc: 2026-07-20T00:00:00Z
reporter: "código y nombre"
partner: "código y nombre"
flow: importaciones
clasificacion: "HS y revisión"
producto: "código y descripción"
periodos: [2021, 2022, 2023, 2024]
archivo_original: comtrade_export.csv
sha256: "<hash del fichero>"
```

### 4. Separa dato comunicado, agregado y estimado

No todas las columnas significan “dato bruto entregado por aduanas”. Comtrade procesa, valida y agrega información; determinados productos analíticos también pueden emplear estimaciones para cubrir ausencias. Revisa los indicadores disponibles en cada descarga y no mezcles sin advertencia:

- valores comunicados por el país;
- agregaciones calculadas;
- cantidades estimadas o imputadas;
- totales mundiales;
- datos de mercancías y datos de servicios.

Si una dimensión no está disponible —por ejemplo, modo de transporte—, su ausencia no significa que la mercancía no viajara por ese medio. Significa que ese desglose no está publicado para esa observación.

### 5. Compara el espejo sin exigir simetría perfecta

Las importaciones declaradas por A desde B pueden compararse con las exportaciones declaradas por B hacia A. Esa pareja ayuda a detectar retrasos, diferencias persistentes o problemas de clasificación, pero no debería igualarse de forma automática.

Entre las causas legítimas de asimetría están:

- importaciones valoradas habitualmente sobre base `CIF` y exportaciones sobre base `FOB`;
- diferencias de calendario y momento de registro;
- tránsito o reexportación por terceros países;
- país de origen frente a país de último destino conocido;
- confidencialidad estadística;
- umbrales y prácticas nacionales de compilación;
- revisiones de datos y conversiones entre clasificaciones;
- errores de cantidad, unidad o socio.

La discrepancia es una señal para investigar el método, no un marcador automático de fraude.

### 6. Corrobora fuera de Comtrade

Una conclusión sensible necesita fuentes adicionales. Según la hipótesis, busca:

- la oficina estadística o aduanera del país informante;
- notas metodológicas y calendarios de revisión;
- legislación arancelaria o cambios de clasificación;
- informes sectoriales con metodología transparente;
- registros portuarios o logísticos agregados y legalmente accesibles;
- documentos empresariales públicos, si la pregunta ya está acotada;
- resoluciones regulatorias o judiciales, si existe un procedimiento formal.

Documenta qué parte procede de Comtrade, cuál de una fuente nacional y cuál es una inferencia tuya.

## Limitaciones y falsos positivos

El error más común es confundir estadística agregada con trazabilidad transaccional. Un aumento bilateral no identifica empresa, contrato, ruta ni destinatario final. Tampoco prueba una relación causal con una noticia ocurrida en fechas cercanas.

Otros falsos positivos frecuentes nacen de:

- comparar valores nominales sin considerar inflación o tipo de cambio;
- interpretar un cambio de código como cambio económico real;
- sumar niveles jerárquicos y contar dos veces el mismo comercio;
- mezclar datos mensuales incompletos con años cerrados;
- escoger kilos, unidades suplementarias y valor como si midieran lo mismo;
- ignorar que los datos históricos pueden revisarse;
- tratar `World` como suma inmutable de todos los socios visibles;
- usar el valor unitario como si fuera el precio exacto de cada operación;
- comparar mercancías y servicios sin respetar sus metodologías.

Las cifras extraordinarias merecen una comprobación adicional de unidad, escala y agregación. Un cero puede ser comercio nulo, dato ausente, confidencial o una selección incorrecta. La interfaz no elimina esa ambigüedad por ti.

## Buenas prácticas de OPSEC, ética y privacidad

Trabajar con estadísticas comerciales agregadas reduce algunos riesgos personales, pero no elimina la responsabilidad analítica.

- Investiga una pregunta de interés legítimo y proporcional.
- No uses un agregado nacional para insinuar culpa individual.
- Evita enriquecer tablas con datos personales que no sean necesarios.
- Protege claves de API, descargas y anotaciones internas.
- Respeta licencias, límites de uso y condiciones de redistribución.
- Conserva el dato original separado de columnas calculadas.
- Etiqueta hechos, transformaciones e inferencias de forma distinta.
- Publica parámetros y limitaciones suficientes para permitir revisión.
- Corrige el análisis si Naciones Unidas o el informante revisan la serie.
- Solicita contraste experto antes de publicar una acusación económica o regulatoria.

La OPSEC también consiste en no revelar hipótesis sensibles mediante nombres de ficheros, consultas compartidas o repositorios públicos. Para ejemplos y pruebas, utiliza países, empresas y productos ficticios o datos agregados inocuos.

## Checklist antes de citar una anomalía

- [ ] He definido informante, socio, flujo, periodo y frecuencia.
- [ ] He guardado código, descripción y revisión de la clasificación.
- [ ] Sé si analizo valor, peso, cantidad o una medida derivada.
- [ ] He comprobado disponibilidad, flags y metadatos del conjunto.
- [ ] He separado registros comunicados, agregados y estimados.
- [ ] He revisado al menos tres periodos comparables.
- [ ] He contrastado el flujo espejo sin exigir igualdad automática.
- [ ] He considerado CIF/FOB, tránsito, calendario y confidencialidad.
- [ ] He conservado consulta, descarga, fecha y hash.
- [ ] He verificado cualquier conclusión sensible en una fuente nacional.
- [ ] He evitado atribuir el agregado a una empresa o persona.
- [ ] Otra persona puede reproducir mis pasos y discutir mis supuestos.

## Alternativas y siguientes pasos

`UN Comtrade` funciona mejor como columna vertebral estadística que como fuente única. Puedes combinarla con:

- oficinas nacionales de estadística y aduanas, para el dato primario y sus revisiones;
- `Eurostat`, si necesitas detalle armonizado dentro del marco europeo;
- `UNCTADstat` o estadísticas de la `OMC`, para indicadores y contexto comercial;
- `OpenRefine`, para limpiar códigos, socios y periodos conservando el historial;
- `Datasette` o `SQLite`, para publicar una extracción acotada y consultable;
- registros mercantiles, `GLEIF` u otras fuentes societarias, solo cuando exista una pregunta legítima de identidad corporativa;
- datos de contratación, sanciones o transporte únicamente como capas separadas y verificadas.

El takeaway accionable es sencillo: elige un producto inocuo, descarga cuatro años para un informante y un socio, repite la consulta desde el espejo y escribe cinco explicaciones alternativas para cualquier diferencia antes de elegir una. **Si tu hipótesis sobrevive al código, la revisión, el calendario y la valoración, entonces merece una segunda fuente.** Un siguiente tema útil sería aprender a construir un cuaderno reproducible que compare flujos espejo sin borrar sus metadatos.

## Fuentes y documentación oficial

- [UN Comtrade — portal oficial](https://comtradeplus.un.org/)
- [División de Estadística de Naciones Unidas — Trade Statistics](https://unstats.un.org/unsd/trade/)
- [UN Comtrade — explorador de flujos y condiciones de acceso](https://comtradeplus.un.org/TradeFlow)
- [Methodology Guide for UN Comtrade](https://comtradeapi.un.org/files/v1/app/wiki/MethodologyGuideforComtradePlus.pdf)
- [UN Comtrade — metodología de procesamiento y validación](https://comtradeapi.un.org/files/v1/app/wiki/UNSD_Method_trade_data_processing_v6-17_Jun_2019.pdf)
- [UNSD — clasificaciones de mercancías HS y SITC](https://unstats.un.org/unsd/trade/dataextract/dataclass.htm)
- [UNSD — metodología de estadísticas internacionales de mercancías](https://unstats.un.org/unsd/trade/imts/methodology.asp)
- [UNSD — tablas analíticas de comercio y notas sobre revisiones](https://unstats.un.org/unsd/trade/data/tables.asp)
