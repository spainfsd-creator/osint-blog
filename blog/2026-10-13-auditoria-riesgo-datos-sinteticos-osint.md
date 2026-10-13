---
title: "Auditar datos sintéticos en OSINT: medir similitud y riesgo de divulgación antes de publicar"
slug: /auditoria-riesgo-datos-sinteticos-osint
authors: [osint-writter]
tags: [osint, methodology, privacy, data, verification, testing]
date: 2026-10-13
image: /img/blog/2026-10-13-auditoria-riesgo-datos-sinteticos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista que compara datos reales y sintéticos tras una barrera de privacidad](/img/blog/2026-10-13-auditoria-riesgo-datos-sinteticos-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/auditoria-riesgo-datos-sinteticos-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Un equipo sustituye un expediente sensible por mil filas «sintéticas», abre el repositorio y respira tranquilo. Horas después descubre que siete filas reproducen registros de entrenamiento y que una combinación rara de localidad, fecha y categoría señala a la misma persona aunque su nombre haya desaparecido. **Inventar filas no basta: antes de publicar hay que intentar demostrar que el conjunto no recuerda demasiado bien a su origen.**

Auditar datos sintéticos consiste en comprobar por separado su utilidad, su parecido con los datos de partida y el riesgo de que permitan inferir pertenencia, atributos o registros reales. No produce un sello universal de anonimato. Produce evidencia documentada para decidir si publicar, restringir, regenerar o no compartir.

<!-- truncate -->

Todos los nombres, cifras, rutas y organizaciones de este artículo son ficticios. El método se aplica a datos propios, públicos o tratados con autorización y dentro de un entorno controlado; no justifica recolectar información personal adicional ni probar ataques sobre conjuntos ajenos.

## Qué se audita y para qué sirve

Los datos sintéticos son registros generados para conservar determinadas propiedades de un conjunto de referencia sin entregar, en principio, sus filas originales. Ese «en principio» importa. Un generador puede memorizar casos, recrear combinaciones singulares o preservar relaciones que faciliten un enlace con información externa.

La auditoría debe responder cuatro preguntas distintas:

1. **Validez:** ¿los registros cumplen el esquema y las reglas del dominio?
2. **Utilidad:** ¿sirven para la tarea declarada, como probar un parser o estimar agregados?
3. **Similitud peligrosa:** ¿hay copias exactas o vecinos anormalmente próximos a registros reales?
4. **Divulgación:** ¿un adversario razonable podría inferir que alguien estaba en el conjunto de entrenamiento o descubrir un atributo reservado?

La [política de datos sintéticos de la Office for National Statistics](https://www.ons.gov.uk/aboutus/transparencyandgovernance/datastrategy/datapolicies/syntheticdatapolicy) exige comprobar problemas de divulgación cuando el conjunto vaya a salir de un entorno seguro o a compartirse más ampliamente que el original. También advierte de que el riesgo no puede eliminarse por completo.

No confundas el objetivo con una competición por obtener la mayor semejanza. La guía del [Information Commissioner's Office sobre datos sintéticos](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/) señala precisamente la tensión: cuanto más imita el conjunto al real, más útil puede resultar, pero también aumenta la posibilidad de revelar información personal.

## Caso legítimo: un dataset para probar un pipeline de ayudas

El observatorio ficticio **Norte Abierto** procesa resoluciones públicas de ayudas y quiere entregar a un proveedor un conjunto de prueba. El original contiene expedientes, fechas, municipios, importes y una categoría administrativa poco frecuente. El proveedor solo necesita comprobar importación, normalización y agregados mensuales.

El equipo genera 20.000 filas artificiales y reserva los datos reales en un entorno aislado. Antes de compartir descubre tres señales:

- dos filas sintéticas coinciden exactamente con registros de entrenamiento tras normalizar espacios y fechas;
- varios vecinos muy próximos pertenecen a una categoría con solo cuatro casos reales;
- los totales globales se parecen, pero un municipio pequeño aparece con una frecuencia cinco veces mayor.

La respuesta correcta no es borrar las dos copias y publicar el resto automáticamente. Las coincidencias pueden ser el síntoma visible de una memorization más amplia; la categoría rara puede permitir divulgación por atributos; y la distorsión del municipio invalida el uso prometido. El equipo regenera con menos detalle, agrupa fechas, elimina la categoría innecesaria y repite toda la evaluación.

## Flujo recomendado

### 1. Escribe la finalidad y el adversario antes de medir

Define qué debe permitir el conjunto y qué no necesita conservar. «Que parezca real» no es una finalidad comprobable. Sí lo son:

- validar tipos, nulos y errores de un importador;
- probar tiempos de ejecución con un volumen determinado;
- conservar tres agregados mensuales dentro de una tolerancia acordada;
- enseñar una consulta sin representar casos ni personas reales.

Después formula un modelo de amenaza proporcionado. ¿El receptor dispone de la misma fuente pública? ¿Conoce que una persona concreta aparece en ella? ¿Puede enlazar localidad, fecha y una categoría rara? ¿La descarga será pública e irreversible o quedará en un entorno de investigación controlado?

El contexto cambia el umbral de decisión. Una muestra para pruebas internas y una descarga anónima mundial no tienen la misma superficie de ataque.

### 2. Separa entrenamiento, control y datos sintéticos

Antes de entrenar o ajustar el generador, aparta un conjunto de control real que el modelo no verá. Mantén tres particiones accesibles solo dentro del entorno autorizado:

| Partición | Uso en la auditoría |
| --- | --- |
| Entrenamiento | Datos reales que sí influyeron en el generador |
| Control | Datos reales comparables que no influyeron en él |
| Sintético | Candidato que se pretende compartir |

Esta separación permite una pregunta útil: ¿las filas sintéticas están sistemáticamente más cerca del entrenamiento que del control? Si solo comparas contra el entrenamiento, una distancia pequeña carece de referencia. Si preparas el control después de mirar resultados, contaminas la evaluación.

Documenta la unidad protegida. En una tabla de eventos, varias filas pueden pertenecer a una misma persona u organización; dividir al azar por fila podría dejar la misma entidad en entrenamiento y control.

### 3. Busca copias exactas después de normalizar

Compara primero representaciones canónicas: codificación uniforme, fechas equivalentes, espacios normalizados y orden de campos fijo. Hazlo tanto con la fila completa como con subconjuntos sensibles previamente definidos.

Un manifiesto de prueba puede registrar el control sin incluir los valores:

```yaml
release_candidate: ayudas-sinteticas-v3
protected_unit: expediente
exact_full_row_matches: 0
sensitive_projection_matches: 0
train_control_split: by_entity
decision: continue_review
```

El cero es una condición útil, no una demostración de privacidad. Una fila puede diferir en un campo irrelevante y seguir revelando la misma combinación singular. Tampoco conviertas hashes de combinaciones predecibles en una lista pública: un tercero podría reconstruirlos por diccionario.

### 4. Mide vecinos con una distancia que respete el dominio

La distancia debe reflejar significado, no comodidad matemática. Estandariza variables numéricas, trata categorías con una regla explícita y evita asignar códigos enteros que inventen proximidades —por ejemplo, que la categoría 2 esté «más cerca» de la 3 que de la 8—.

Calcula, dentro del entorno seguro, la distancia de cada fila sintética a su vecino real más próximo. Compara después las distribuciones frente a entrenamiento y control:

- percentiles de distancia, no solo la media;
- proporción de coincidencias o casi coincidencias;
- resultados por subgrupos y categorías raras;
- sensibilidad a varias definiciones razonables de distancia.

No existe un corte universal como «0,1 es seguro». Depende de la escala, las variables, la rareza, el conocimiento auxiliar y las consecuencias. Un umbral debe vincularse al modelo de amenaza y probarse con controles, no importarse de otro dataset.

El [piloto metodológico de ONS sobre datos sintéticos](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot) propone evaluar el parecido según finalidad y riesgo. Su espectro recuerda que conservar relaciones multivariantes finas eleva el riesgo y que las propiedades importantes deben elegirse con los usuarios, no preservarse indiscriminadamente.

### 5. Ensaya divulgación, no solo parecido

Una auditoría práctica incorpora ataques controlados con información que el adversario definido podría poseer:

- **inferencia de pertenencia:** estimar si un registro concreto formó parte del entrenamiento;
- **divulgación de atributos:** inferir un campo reservado a partir de los campos conocidos y del conjunto sintético;
- **enlace:** combinar cuasi-identificadores con una fuente auxiliar permitida;
- **riesgo de singulares:** revisar extremos, categorías pequeñas y secuencias inusuales.

Compara el éxito del ataque con una línea base y con el conjunto de control. Un clasificador con un 70 % de acierto no significa lo mismo si la regla trivial ya consigue un 69 %. Registra además intervalos o variación entre repeticiones: una sola ejecución puede ocultar inestabilidad.

El ICO identifica expresamente los riesgos de inversión de modelo, inferencia de pertenencia y divulgación de atributos. Su mitigación puede exigir suprimir extremos, aplicar privacidad diferencial, reducir detalle o restringir el entorno de uso.

### 6. Evalúa utilidad por tarea y por subgrupo

La pregunta no es si dos histogramas «se ven parecidos», sino si el candidato sirve para el propósito escrito en el paso 1. Para un pipeline OSINT podrías comprobar:

- esquema, tipos y reglas de edición;
- tasas de nulos, duplicados y errores intencionados;
- agregados y correlaciones estrictamente necesarios;
- resultado de consultas o modelos concretos;
- error desglosado por categorías minoritarias;
- estabilidad entre varias generaciones.

NIST advierte en sus [Guidelines for Evaluating Differential Privacy Guarantees, SP 800-226](https://doi.org/10.6028/NIST.SP.800-226) de que los datos sintéticos pueden reducir precisión en subpoblaciones y añadir incertidumbre y sesgo que se propagan a usos posteriores. Un promedio global aceptable puede esconder un conjunto inútil o perjudicial para el grupo más pequeño.

### 7. Decide con una matriz, no con una nota mágica

Reúne utilidad y riesgo en una decisión explícita:

| Resultado | Acción razonable |
| --- | --- |
| Baja utilidad, bajo riesgo observado | Simplificar o usar solo para pruebas estructurales |
| Alta utilidad, riesgo elevado | No publicar; reducir detalle, cambiar método o limitar acceso |
| Utilidad suficiente, riesgo residual acotado | Compartir bajo las condiciones documentadas |
| Evidencia inconclusa | Mantener en entorno seguro y pedir revisión especializada |

Registra versión del original, código, parámetros, semilla, partición, métricas, modelo de amenaza, responsable de la decisión, condiciones de uso y fecha de reevaluación. Si cambia el generador, el dataset o el público receptor, la decisión anterior no se hereda automáticamente.

La herramienta oficial [SDNist](https://github.com/usnistgov/SDNist) ilustra la evaluación conjunta de utilidad y privacidad para sus datasets de referencia. No es un botón genérico de certificación: su documentación limita el soporte a benchmarks concretos, por lo que sirve como ejemplo de informe y métricas, no como aval automático de cualquier conjunto OSINT.

## Privacidad diferencial: una garantía distinta

Las pruebas empíricas buscan fallos conocidos bajo un modelo de amenaza. Que no encuentren uno no garantiza resistencia frente a ataques nuevos. NIST SP 800-226 subraya que los generadores sin privacidad diferencial ofrecen, por lo general, garantías informales; un conjunto sintético con privacidad diferencial añade una garantía matemática parametrizada sobre la influencia de las unidades protegidas.

Eso tampoco elimina el trabajo:

- hay que definir correctamente la unidad de privacidad;
- contabilizar el presupuesto y todas las ejecuciones que lo consumen;
- validar la implementación y sus supuestos;
- medir utilidad, sesgo y error por subgrupos;
- proteger los datos durante entrenamiento;
- controlar artefactos, logs y modelos intermedios.

No describas un dataset como «diferencialmente privado» porque se añadió ruido después o porque el resultado parece distinto. La propiedad corresponde a un mecanismo definido y a sus parámetros, no a una impresión visual.

## Limitaciones y falsos positivos

### Una coincidencia puede ser inevitable

En dominios pequeños —por ejemplo, booleanos y unas pocas categorías— dos filas pueden coincidir por azar. La frecuencia esperada y el contexto importan. Aun así, una combinación rara merece revisión antes de concluir que es inocua.

### Una gran distancia puede engañar

Cambiar una fecha un día o añadir ruido a un importe puede aumentar la distancia y conservar una historia fácilmente enlazable. Las métricas deben representar la semántica y el conocimiento auxiliar plausible.

### Los ataques probados nunca son exhaustivos

Una tasa baja de inferencia de pertenencia para un atacante concreto no cubre otros auxiliares, algoritmos o poblaciones. Documenta el alcance como evidencia limitada, no como ausencia de riesgo.

### El conjunto de control puede no ser comparable

Si pertenece a otro periodo o población, una diferencia entre entrenamiento y control puede medir deriva, no memorization. Diseña la partición antes de generar y comprueba su comparabilidad.

### El propio informe puede divulgar

Listar los diez registros más próximos, categorías raras o hashes fáciles de adivinar puede filtrar lo que la auditoría intentaba proteger. Publica metodología y resultados agregados; guarda detalles sensibles en el entorno controlado.

## Buenas prácticas de OPSEC, ética y privacidad

- Minimiza variables antes de entrenar; no esperes que el generador arregle una recolección excesiva.
- Mantén originales, modelos, controles y reportes detallados fuera del repositorio público.
- Divide por la unidad protegida, no por filas cuando varias pertenezcan a la misma entidad.
- Usa identificadores inequívocamente ficticios y recursos reservados en ejemplos.
- Trata extremos y categorías raras como señales de revisión, no como curiosidades.
- Separa quien genera de quien aprueba cuando el impacto o la exposición sean altos.
- Limita consultas y ejecuciones; los intentos repetidos también pueden filtrar información.
- Declara finalidad, limitaciones, procedencia y usos prohibidos junto a la descarga.
- Reevalúa tras cambios de datos, código, parámetros, público o fuentes auxiliares.
- Si el equilibrio no es aceptable, no publiques microdatos: entrega agregados, una interfaz limitada o un entorno seguro.

## Alternativas y siguientes pasos

Si el objetivo es probar formato y volumen, genera desde un esquema y distribuciones inventadas sin entrenar con microdatos reales. Si basta con estadísticas, publica tablas agregadas sujetas a control de divulgación. Para consultas acotadas, una API con límites puede exponer menos que una descarga completa. Para investigación sensible, usa un entorno de acceso controlado.

Cuando necesites una garantía formal, estudia un mecanismo de privacidad diferencial con asesoramiento competente. Cuando solo quieras reproducir un defecto técnico, vuelve al patrón más estrecho: un contraejemplo mínimo construido desde cero suele ser más seguro y comprensible que un dataset realista.

## Checklist antes de compartir

- [ ] La finalidad y los usuarios autorizados están definidos.
- [ ] El modelo de amenaza incluye información auxiliar plausible.
- [ ] Entrenamiento y control se separaron por la unidad protegida.
- [ ] No hay copias exactas tras una canonicalización documentada.
- [ ] Las distancias a vecinos se compararon contra el control y por subgrupos.
- [ ] Se ensayaron pertenencia, atributos o enlaces relevantes.
- [ ] La utilidad se midió sobre tareas declaradas, no por apariencia.
- [ ] Se revisaron extremos, categorías pequeñas y texto libre.
- [ ] El informe público no expone vecinos ni combinaciones sensibles.
- [ ] La decisión, condiciones y fecha de reevaluación quedaron registradas.

El takeaway accionable es concreto: antes de subir tu próximo fixture sintético, separa un control que el generador no vea, cuenta coincidencias canónicas y compara la distancia al vecino más próximo frente a entrenamiento y control. Si no puedes explicar qué protege esa comparación, qué atacante representa y qué decisión cambia, aún no tienes una auditoría; solo tienes una métrica.

Como siguiente tema, convendría estudiar la **gestión del presupuesto de privacidad en pipelines OSINT**: cómo contabilizar consultas y regeneraciones sin presentar `epsilon` como una nota de calidad aislada.

## Fuentes consultadas

- [NIST SP 800-226: Guidelines for Evaluating Differential Privacy Guarantees](https://doi.org/10.6028/NIST.SP.800-226)
- [NIST: SDNist Deidentified Data Report Tool](https://github.com/usnistgov/SDNist)
- [Office for National Statistics: Synthetic data policy](https://www.ons.gov.uk/aboutus/transparencyandgovernance/datastrategy/datapolicies/syntheticdatapolicy)
- [Office for National Statistics: Synthetic data pilot](https://www.ons.gov.uk/methodology/methodologicalpublications/generalmethodology/onsworkingpaperseries/onsmethodologyworkingpaperseriesnumber16syntheticdatapilot)
- [Information Commissioner's Office: Synthetic data](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/)
