---
title: "Codificación manual en OSINT: comparar marcos narrativos sin convertir interpretación en etiqueta"
slug: /codificacion-manual-marcos-narrativos-osint
authors: [osint-writter]
tags: [osint, methodology, media, verification, research, privacy]
date: 2026-11-19
image: /img/blog/2026-11-19-codificacion-manual-marcos-narrativos-osint.png
aiDisclosure: generated
humanReviewed: false
---

Dos medios describen la misma protesta. Uno abre con los cortes de tráfico; el otro, con las reivindicaciones. Contar palabras permite ver diferencias de vocabulario, pero no demuestra por sí solo que exista un encuadre estable. **Para comparar marcos narrativos hay que convertir una interpretación discutible en decisiones observables, repetibles y abiertas al desacuerdo.**

![Dos analistas codifican por separado noticias públicas y comparan su acuerdo mediante un libro de códigos](/img/blog/2026-11-19-codificacion-manual-marcos-narrativos-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un protocolo de codificación manual para analizar noticias públicas en una investigación OSINT legítima. El caso es ficticio; no pretende clasificar la ideología de periodistas ni inferir intenciones personales. La meta es más modesta y comprobable: describir qué aspectos aparecen, con qué evidencia textual y con qué grado de acuerdo entre analistas.

## Qué es codificar un marco narrativo y para qué sirve

Codificar consiste en aplicar reglas explícitas a unidades previamente definidas —una pieza completa, un titular, un párrafo o una intervención— y registrar categorías de forma estructurada. El resultado no es «la verdad» sobre el texto, sino un conjunto de observaciones creado mediante un protocolo que otras personas pueden inspeccionar.

Un **marco narrativo** tampoco es una palabra llamativa ni un sinónimo de tono. El trabajo clásico de [Robert Entman sobre framing](https://doi.org/10.1111/j.1460-2466.1993.tb01304.x) propone observar qué aspectos se seleccionan y resaltan para definir un problema, atribuir causas, evaluar y sugerir respuestas. Esa idea ofrece dimensiones útiles, pero no convierte automáticamente cada artículo en una de cuatro casillas. El libro de códigos debe traducir la pregunta concreta a señales visibles.

En OSINT, este método puede servir para:

- comparar cómo distintas colecciones cubren un mismo acontecimiento;
- comprobar si una impresión obtenida al leer unos pocos titulares se sostiene en una muestra;
- localizar piezas representativas y casos que contradicen la hipótesis;
- distinguir presencia de un elemento, prominencia y valoración;
- documentar incertidumbre antes de publicar una conclusión sobre cobertura.

No sirve para leer la mente del autor, demostrar coordinación editorial ni decidir si una afirmación es verdadera. Para eso hacen falta otras evidencias.

## Caso de uso legítimo con un ejemplo ficticio

El observatorio ficticio **Río Abierto** quiere comparar la cobertura de una consulta municipal sobre movilidad. Ha reunido 240 piezas publicadas durante cuatro semanas por ocho medios locales. Su pregunta no es «¿qué medio está a favor?», demasiado amplia y cargada, sino esta:

> ¿Con qué frecuencia y prominencia aparecen consecuencias sobre tráfico, comercio, salud y participación vecinal en las piezas informativas de la muestra?

La unidad principal será la **pieza**, pero cada decisión llevará un fragmento justificativo. Se excluirán editoriales, duplicados de agencia, galerías sin texto y contenidos fuera del periodo. La comparación se hará con proporciones dentro de cada medio y semana, no con recuentos brutos que premien a quien publica más.

Antes de ver resultados agregados, el equipo registra una hipótesis, el criterio de inclusión y un plan de análisis. Así evita cambiar categorías después de descubrir qué clasificación produce el gráfico más atractivo.

## Flujo recomendado paso a paso

### 1. Congela la pregunta, el corpus y la unidad

Guarda para cada pieza un identificador, URL, medio, fecha publicada, fecha de captura y estado de acceso. Conserva también una copia permitida o un hash cuando proceda. Separa tres decisiones que suelen mezclarse:

1. **Universo:** qué población de contenidos pretende describir el estudio.
2. **Muestra:** qué piezas del universo entran realmente y cómo se eligieron.
3. **Unidad:** qué objeto recibe cada código.

Si el corpus viene de un buscador o archivo, documenta sus lagunas. La entrada anterior sobre [Media Cloud](/media-cloud-osint-cobertura-mediatica) explica por qué el índice observado no equivale a toda la prensa. Una codificación impecable no corrige una muestra sesgada o incompleta.

### 2. Diseña un libro de códigos ejecutable

Cada variable necesita algo más que un nombre. Una ficha mínima debería contener:

| Campo | Ejemplo operativo |
| --- | --- |
| variable | `consecuencia_trafico` |
| valores | presente / ausente / no se puede determinar |
| unidad | pieza completa, incluido titular y entradilla |
| inclusión | atasco, desvío, tiempo de viaje o acceso de vehículos |
| exclusión | uso metafórico de «tráfico» o mención en un enlace relacionado |
| prioridad | codificar presente aunque la fuente rechace esa consecuencia |
| evidencia | fragmento breve y ubicación dentro de la pieza |
| ejemplo positivo | «el desvío añade diez minutos al recorrido» |
| contraejemplo | «la propuesta ha generado mucho tráfico en redes» |
| caso límite | foto con vehículos sin referencia textual: indeterminado |

Incluye un valor para la incertidumbre. Obligar a elegir «sí» o «no» cuando falta texto, hay un paywall o la pieza es ambigua oculta problemas del material bajo una precisión ficticia.

### 3. Separa presencia, prominencia y valoración

Que una pieza mencione el comercio no significa que lo presente como perjudicado. Para evitar esa inferencia, registra variables distintas:

- **presencia:** aparece o no un elemento definido;
- **prominencia:** titular, entradilla, cuerpo o mención incidental;
- **actor que lo expresa:** periodista, fuente oficial, asociación, ciudadano u otro;
- **valoración explícita:** favorable, desfavorable, mixta o indeterminada, solo si la regla identifica evidencia;
- **fragmento justificativo:** texto exacto o referencia temporal si es audio o vídeo.

Esta separación permite volver a la fuente cuando una cifra sorprende. También evita atribuir al medio una frase citada para cuestionarla.

### 4. Construye un conjunto piloto difícil

Elige una muestra piloto que contenga formatos, medios y fechas distintos, incluidos casos limítrofes. No uses solo piezas fáciles. Dos analistas deben codificarla **de forma independiente**, sin comentar sus decisiones mientras trabajan.

Después comparan resultados variable por variable. Cada desacuerdo debe producir una de estas salidas:

- aclarar una definición;
- añadir un ejemplo o contraejemplo;
- dividir una variable que mezclaba dos conceptos;
- retirar una categoría que no puede observarse con fiabilidad;
- mantener el desacuerdo como dato si ambas lecturas son defendibles.

Las metodologías publicadas por [Pew Research Center](https://www.pewresearch.org/journalism/2020/09/28/youtube-news-methodology/) muestran este patrón de entrenamiento, pruebas de acuerdo y control durante la codificación. No existe, sin embargo, un número universal de rondas o piezas que vuelva válido cualquier proyecto: debe justificarse según la complejidad, prevalencia de categorías, número de codificadores y uso previsto.

### 5. Mide acuerdo antes de adjudicar

Calcula la fiabilidad con las decisiones independientes, **antes** de que el equipo se reúna para resolver diferencias. El porcentaje de acuerdo es intuitivo, pero puede parecer alto cuando una categoría es muy rara. El artículo de [Lombard, Snyder-Duch y Bracken](https://doi.org/10.1111/j.1468-2958.2002.tb00826.x) advierte de los problemas de depender únicamente de ese porcentaje.

Según el diseño pueden utilizarse Cohen kappa, Fleiss kappa o alfa de Krippendorff. Este último admite distintos números de codificadores, datos ausentes y niveles de medida; la [Universidad de Pensilvania mantiene recursos del propio Krippendorff](https://www.asc.upenn.edu/krippendorffs-alpha-reliability) para entender y calcular la familia de coeficientes.

No conviertas un umbral memorizado en certificado automático. Publica, al menos:

- métrica y versión o implementación utilizada;
- variable evaluada y nivel de medida;
- número de unidades y codificadores;
- distribución de categorías y datos ausentes;
- resultado antes de adjudicar;
- cambios hechos al libro de códigos tras el piloto.

Un coeficiente bajo puede revelar una definición confusa; uno alto no demuestra que la categoría mida el concepto correcto. **Fiabilidad y validez son preguntas diferentes.**

### 6. Adjudica sin borrar el desacuerdo

Terminada la prueba, conserva dos capas: códigos originales independientes y valor adjudicado. Registra quién resolvió el caso, qué regla aplicó y si el libro de códigos cambió. No sobrescribas las columnas iniciales: son necesarias para auditar el acuerdo y detectar sesgos sistemáticos.

Cuando cambie una regla sustancial, vuelve a codificar las unidades afectadas. Si la categoría evoluciona a mitad del trabajo sin revisar lo anterior, la primera mitad y la segunda ya no representan la misma medición.

### 7. Codifica la muestra completa con controles

Asigna piezas aleatoriamente o mediante bloques equilibrados. Inserta una proporción oculta de unidades duplicadas para comprobar deriva y programa revisiones periódicas sin convertirlas en sesiones de consenso sobre cada pieza. Si solo hay una persona, repite una muestra tras un intervalo y presenta el resultado como estabilidad intracodificador, no como acuerdo entre observadores independientes.

Mantén un registro de incidencias: páginas inaccesibles, cambios de contenido, idioma, transcripción dudosa y casos excluidos. Las ausencias también afectan al denominador.

### 8. Analiza sin inflar la inferencia

Compara proporciones con denominadores visibles y presenta intervalos o incertidumbre cuando el diseño los permita. Examina también:

- resultados por semana y fuente, no solo un total;
- sensibilidad al excluir casos indeterminados;
- categorías muy raras o concentradas en un único medio;
- ejemplos concordantes y contraejemplos;
- diferencia entre pieza informativa, análisis y opinión;
- influencia de sindicación o duplicados.

El trabajo de [Matthes y Kohring sobre análisis de marcos](https://doi.org/10.1111/j.1460-2466.2008.00384.x) recuerda que los marcos pueden entenderse como patrones de varios elementos, no como una etiqueta intuitiva aplicada de una vez. Para una investigación pequeña, eso aconseja publicar primero las dimensiones observadas y explicar después, con cautela, cualquier agrupación interpretativa.

## Limitaciones y falsos positivos

### Un código reproducible todavía puede estar mal planteado

Dos analistas pueden aplicar con gran acuerdo una categoría que no responde a la pregunta. Si «conflicto» significa simplemente que aparecen dos voces, el código será fácil de repetir, pero quizá no mida un encuadre conflictivo. Revisa la validez conceptual con teoría, expertos y casos negativos.

### La unidad cambia el resultado

Un titular puede enfatizar el tráfico mientras el cuerpo dedica casi todo el espacio a salud. Codificar la pieza completa, el párrafo o cada afirmación produce datos distintos. No mezcles niveles sin declararlo.

### La rareza distorsiona métricas y lecturas

Cuando casi todo es «ausente», un acuerdo aparente elevado puede ocultar que los codificadores discrepan justo en los pocos positivos. Publica la tabla de coincidencias y revisa manualmente esos casos.

### Traducción, ironía y material multimodal añaden capas

Un pie de foto, un gráfico o una cita irónica puede cambiar la lectura. Si el protocolo solo observa texto extraído, delimita esa limitación. Si se traducen piezas, conserva idioma original, traducción, responsable y criterios para expresiones ambiguas.

### El corpus puede cambiar mientras se codifica

Titulares corregidos, URL redirigidas o vídeos editados afectan a la reproducibilidad. Registra la representación realmente observada, su fecha y, cuando sea proporcionado y legal, una copia o huella verificable.

## Buenas prácticas de OPSEC, ética y privacidad

- Codifica contenido de interés legítimo; no uses el protocolo para perfilar a periodistas o ciudadanos.
- Minimiza nombres y datos personales incidentales en hojas, ejemplos y exportaciones.
- No publiques fragmentos que faciliten localizar a una persona vulnerable si el texto no es necesario para sostener el análisis.
- Separa identidad del codificador y decisión analítica cuando exista riesgo de represalias.
- Protege credenciales, copias con copyright y transcripciones no públicas; no las subas al repositorio del proyecto.
- Define acceso, retención y borrado antes de recoger material.
- Documenta conflictos de interés y posibles sesgos lingüísticos o culturales del equipo.
- Mantén un canal de corrección y una versión fechada del libro de códigos.
- No presentes categorías inferidas como rasgos personales ni un marco textual como intención del autor.
- Publica suficientes reglas y agregados para auditar el método, no un corpus innecesario.

## Checklist operativo

- [ ] La pregunta puede responderse mediante señales observables.
- [ ] Universo, muestra, periodo, exclusiones y unidad están definidos.
- [ ] Cada variable incluye valores, reglas, ejemplos y contraejemplos.
- [ ] Presencia, prominencia, fuente y valoración están separadas.
- [ ] Existe un valor para ausencia de información o ambigüedad.
- [ ] El piloto incluye formatos y casos difíciles.
- [ ] Al menos dos personas codificaron el piloto de forma independiente.
- [ ] El acuerdo se calculó antes de adjudicar discrepancias.
- [ ] Se conservan códigos originales, decisión final y motivo del cambio.
- [ ] Los denominadores y datos ausentes aparecen en el informe.
- [ ] Se probaron sensibilidad, prevalencia y posibles duplicados.
- [ ] Los ejemplos publicados están minimizados y tienen trazabilidad.

## Alternativas y siguientes pasos

Una lectura cualitativa profunda puede ser mejor para un corpus pequeño y exploratorio; un análisis asistido por ordenador puede localizar patrones en miles de piezas, pero necesita validación humana y una pregunta bien definida; los diccionarios de términos son transparentes, aunque pierden negación, ironía y contexto; las entrevistas a redacciones estudian procesos, no solo productos. Estas vías se complementan.

El takeaway práctico es este: **no empieces asignando etiquetas a medios; empieza escribiendo reglas que permitan a dos personas independientes encontrar la misma evidencia y explicar sus desacuerdos**. Pilota con casos difíciles, mide antes de consensuar y conserva la trazabilidad desde cada resultado hasta el fragmento que lo sostiene. Como siguiente tema, tendría sentido construir una hoja reproducible para calcular acuerdo, explorar errores por categoría y publicar solo agregados minimizados.

## Fuentes y documentación

- [Entman: *Framing: Toward Clarification of a Fractured Paradigm*](https://doi.org/10.1111/j.1460-2466.1993.tb01304.x)
- [Matthes y Kohring: *The Content Analysis of Media Frames*](https://doi.org/10.1111/j.1460-2466.2008.00384.x)
- [Lombard, Snyder-Duch y Bracken: fiabilidad entre codificadores](https://doi.org/10.1111/j.1468-2958.2002.tb00826.x)
- [Krippendorff: recursos sobre alfa y fiabilidad, Annenberg School](https://www.asc.upenn.edu/krippendorffs-alpha-reliability)
- [Pew Research Center: metodología de codificación de noticias en YouTube](https://www.pewresearch.org/journalism/2020/09/28/youtube-news-methodology/)
- [Pew Research Center: ejemplo de codificación y alfa de Krippendorff](https://www.pewresearch.org/journalism/2020/06/24/covid-facebook-methodology/)
