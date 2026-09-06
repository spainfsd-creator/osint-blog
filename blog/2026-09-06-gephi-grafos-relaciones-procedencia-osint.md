---
title: "Gephi en OSINT: explorar grafos sin convertir proximidad visual en evidencia"
slug: /gephi-grafos-relaciones-procedencia-osint
authors: [osint-writter]
tags: [osint, investigation, verification, link-analysis, tooling, privacy]
date: 2026-09-06
image: /img/blog/2026-09-06-gephi-grafos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista examinando un grafo de entidades, contratos y documentos públicos con marcas de procedencia e incertidumbre](/img/blog/2026-09-06-gephi-grafos-osint.png)

*Imagen generada mediante inteligencia artificial.*

Tres sociedades concurren a varias licitaciones públicas. Comparten apoderados, direcciones antiguas y proveedores, pero esos datos proceden de años distintos y no todos significan lo mismo. Al dibujarlos, el grafo produce un centro brillante y aparentemente sospechoso. El peligro está servido: **una visualización puede hacer que una coincidencia parezca una trama antes de que hayamos demostrado siquiera que las entidades son las mismas**.

[Gephi](https://gephi.org/desktop/) es una aplicación abierta para explorar y visualizar redes. En OSINT ayuda a revisar conjuntos de relaciones que ya hemos obtenido de fuentes legítimas: sociedades y contratos, organizaciones y documentos, dominios y certificados o publicaciones y referencias. No descubre por arte de magia quién controla qué. Su verdadero valor consiste en hacer visibles preguntas, errores de modelado y zonas que requieren corroboración.

<!-- truncate -->

Este artículo propone un flujo responsable y reproducible. Las fuentes oficiales se consultaron el **6 de septiembre de 2026**. Todas las entidades, expedientes, identificadores y relaciones del ejemplo son ficticios. El objetivo es analizar datos públicos con una finalidad legítima, no perfilar personas ni ampliar información sensible.

## Qué es Gephi y qué representa un grafo

Un grafo contiene **nodos** y **aristas**. Los nodos representan entidades definidas por el investigador —por ejemplo, una organización, un contrato o un documento— y las aristas expresan una relación concreta entre dos nodos. Tanto unos como otras pueden llevar atributos: tipo, fecha, jurisdicción, fuente, confianza o estado de verificación.

La [guía rápida oficial](https://gephi.org/quickstart/) muestra que una tabla con columnas `Source` y `Target` basta para importar relaciones. La [documentación del importador CSV](https://docs.gephi.org/desktop/User_Manual/Import/CSV_Format/) añade matices importantes: ambas columnas son obligatorias para aristas, se puede decidir el tipo de cada campo y un valor que no encaje puede terminar como nulo. Importar no equivale, por tanto, a validar.

Conviene separar estas capas:

| Capa | Pregunta | Lo que no demuestra |
| --- | --- | --- |
| fuente | ¿Qué documento o registro contiene el dato? | que el dato siga vigente o sea correcto |
| entidad | ¿Qué objeto estable hemos definido? | que dos nombres parecidos sean la misma entidad |
| relación | ¿Qué vínculo exacto declara la fuente? | control, intención o causalidad |
| grafo | ¿Cómo conectan las relaciones modeladas? | que lo no incluido no exista |
| visualización | ¿Cómo coloca y estiliza el algoritmo los elementos? | distancia real, culpabilidad o importancia factual |

Gephi ofrece laboratorio de datos, filtros, algoritmos de disposición, métricas y exportación. Es una mesa de exploración visual. La evidencia continúa en las fuentes y en las decisiones documentadas que transformaron esas fuentes en nodos y aristas.

## Caso de uso legítimo: las compras de Puerto Niebla

El municipio ficticio de **Puerto Niebla** publica contratos, adjudicatarios y resoluciones en su portal de transparencia. Una asociación quiere comprobar si varios proveedores aparecen repetidamente en expedientes relacionados y preparar preguntas para el ayuntamiento. No busca atribuir delitos ni investigar la vida privada de administradores.

La pregunta se formula así:

> ¿Qué relaciones declaradas existen entre expedientes, organizaciones y documentos públicos durante 2024-2026, de qué fuente procede cada una y qué patrones merecen una comprobación independiente?

El equipo adopta tres tipos de nodo:

- `organizacion`, identificada por jurisdicción y número registral;
- `contrato`, identificado por el código oficial del expediente;
- `documento`, identificado por URL canónica y huella del fichero adquirido.

Y limita las aristas a verbos observables: `ADJUDICADO_A`, `MENCIONA_A`, `SUSTITUYE_A` y `PUBLICADO_EN`. No usa una arista genérica llamada `RELACIONADO_CON`, porque borraría la diferencia entre adjudicar, mencionar y reemplazar.

El resultado esperado no es «encontrar el nodo culpable», sino un inventario auditable de vínculos, una lista de ambigüedades y varias hipótesis verificables en fuentes primarias.

## Flujo recomendado paso a paso

### 1. Define la unidad de análisis antes de recolectar

Escribe qué representa cada nodo, qué significa cada arista y qué periodo cubre el trabajo. Decide si la red es dirigida: `contrato ADJUDICADO_A organizacion` tiene sentido y dirección; «dos documentos comparten categoría» quizá sea simétrica.

Aclara también si permites varias aristas entre el mismo par. Dos contratos diferentes no deberían colapsarse en una sola relación solo porque conectan las mismas entidades. Una decisión estructural cambia las métricas posteriores.

### 2. Conserva una tabla de entidades separada

Asigna identificadores estables y evita usar el nombre visible como clave. Una tabla mínima de nodos podría contener:

```csv
Id,Label,Type,Jurisdiction,SourceUrl,ObservedAt,Verification
org_es_b12345678,Brisa Norte SL,organizacion,ES-FICTICIA,https://datos.example/org/17,2026-09-01,corroborado
exp_2025_0042,EXP-2025-0042,contrato,Puerto Niebla,https://datos.example/exp/42,2026-09-01,corroborado
doc_sha256_ab12,Resolucion 42,documento,Puerto Niebla,https://datos.example/doc/42,2026-09-01,adquirido
```

Los dominios y valores son ficticios. En un caso real, conserva además la fecha de consulta, el hash del documento cuando proceda y una nota sobre las reglas de normalización. Si dos registros pueden referirse a la misma sociedad pero falta un identificador común, mantenlos separados y registra la posible equivalencia como hipótesis, no como fusión silenciosa.

### 3. Construye aristas que puedan citarse

Cada fila debe responder «quién afirma esta relación, cuándo y con qué alcance». Por ejemplo:

```csv
Source,Target,Type,ValidFrom,ValidTo,EvidenceUrl,EvidencePage,Confidence
exp_2025_0042,org_es_b12345678,ADJUDICADO_A,2025-06-14,,https://datos.example/doc/42,7,alta
doc_sha256_ab12,org_es_b12345678,MENCIONA_A,2025-06-14,,https://datos.example/doc/42,7,alta
```

No uses `Weight` como cajón de sastre. Puede representar número de contratos, importe agregado, frecuencia de coaparición o una puntuación propia; cada interpretación produce una lectura distinta. Si necesitas varias magnitudes, guárdalas en columnas separadas con unidad y método.

### 4. Valida el CSV antes de abrir Gephi

Comprueba identificadores duplicados, aristas sin extremos, fechas imposibles, campos nulos y tipos inconsistentes. La documentación del importador advierte de que Gephi puede asignar identificadores automáticamente cuando faltan y convertir en nulo lo que no puede interpretar. Eso ayuda a cargar datos, pero puede ocultar un fallo de preparación.

Guarda el CSV original, el CSV normalizado y un registro de transformaciones. Calcula hashes y no sobrescribas el material adquirido. El proyecto `.gephi` es un artefacto de análisis; no reemplaza las tablas ni las fuentes.

### 5. Importa y revisa el informe, no solo el dibujo

Importa primero los nodos y después las aristas. Confirma delimitador, codificación, columnas, tipos y carácter dirigido o no dirigido. Revisa cuántos registros entraron, cuántos quedaron fuera y qué valores pasaron a nulo. Luego abre el laboratorio de datos y contrasta una muestra con los CSV.

Para una primera prueba, trabaja sobre una copia pequeña y conocida. Si esperabas 18 organizaciones, 30 expedientes y 30 adjudicaciones, el lienzo no es suficiente: verifica los recuentos por tipo y relación.

### 6. Usa la disposición como interfaz, no como medición

Los algoritmos de *layout* asignan coordenadas para hacer el grafo legible. Cambiar parámetros, semilla o algoritmo puede acercar o separar nodos sin que cambie una sola arista. Color, tamaño y posición deben tener una leyenda explícita.

Una regla útil es ejecutar más de una disposición y comprobar si la pregunta sobrevive. Si una conclusión depende de que dos círculos «parezcan cerca», no es una conclusión sobre los datos. Inspecciona la arista y vuelve a su fuente.

### 7. Calcula métricas con una hipótesis concreta

El grado cuenta conexiones según la definición del grafo. La intermediación estima cuántos caminos mínimos atraviesan un nodo. La modularidad propone grupos según una función y unos parámetros. Ninguna de ellas mide automáticamente influencia, propiedad o conducta indebida.

Antes de ejecutar una métrica, registra:

- grafo completo o subconjunto filtrado;
- dirigido o no dirigido;
- tratamiento de pesos y aristas múltiples;
- intervalo temporal;
- parámetros utilizados;
- pregunta que la métrica pretende explorar.

Un portal de contratación puede convertirse en el nodo con mayor grado porque todos los expedientes enlazan a él. Eso describe el modelo, no una posición de poder. Un documento puente puede tener intermediación alta por cómo descompusimos la información, no por su importancia real.

### 8. Filtra sin borrar el universo de referencia

Los filtros facilitan examinar un periodo, un tipo de entidad o un umbral. La [documentación de filtros](https://docs.gephi.org/desktop/Plugins/Filter/) explica que operan sobre vistas del grafo y que pueden encadenarse. Conserva la consulta exacta y el recuento antes y después.

Publicar solo el subgrafo atractivo puede ocultar cientos de nodos aislados o relaciones que contradicen la narrativa. Exporta una tabla de exclusiones y explica por qué se aplicó el filtro. Ausencia en una vista filtrada no significa ausencia en los datos originales.

### 9. Trata el tiempo como parte del vínculo

Una dirección compartida en 2019 y un contrato de 2026 no son simultáneos por aparecer en el mismo lienzo. Gephi admite redes dinámicas con marcas o intervalos; su [documentación sobre datos temporales](https://docs.gephi.org/desktop/User_Manual/Import_Dynamic_Data/) señala que ambos modelos no deben mezclarse dentro del mismo grafo.

Separa al menos `observed_at`, fecha del documento y periodo de vigencia declarado. Usa un valor abierto cuando se desconozca el final, sin inventarlo. Repite el análisis por cortes temporales para distinguir continuidad, sucesión y simple solapamiento visual.

### 10. Verifica fuera del grafo y documenta la salida

Selecciona los patrones candidatos y vuelve a los registros oficiales, documentos completos y contexto temporal. Busca explicaciones ordinarias: homónimos, proveedores comunes, cambios de razón social, lotes de una misma licitación o relaciones exigidas por el procedimiento.

El informe final debe incluir el diccionario del grafo, fuentes, fecha de adquisición, reglas de resolución de entidades, filtros, parámetros y limitaciones. Exporta una tabla de aristas que permita revisar cada afirmación. La imagen es un índice navegable, no la prueba principal.

## Limitaciones y falsos positivos

El sesgo más grande suele entrar antes de Gephi. Un registro incompleto produce una red incompleta; una API con paginación mal resuelta borra relaciones; una fuente que solo conserva cargos actuales destruye la cronología. Los nodos sin aristas pueden desaparecer del análisis aunque su ausencia sea relevante.

La resolución de entidades añade errores de fusión y división. Dos «Servicios del Norte» pueden ser organizaciones distintas; una entidad puede cambiar de denominación sin dejar de ser la misma. Dominios, direcciones y teléfonos también se reutilizan. Necesitas identificadores fuertes, jurisdicción, fechas y corroboración.

Las métricas dependen del muestreo. Un nodo central en un conjunto pequeño puede volverse periférico al añadir otra fuente. Los algoritmos de comunidades siempre pueden ofrecer una partición visualmente persuasiva, pero el grupo resultante no equivale a una organización coordinada.

Por último, el gráfico comunica con enorme eficacia. Una etiqueta grande, un color rojo o una línea gruesa pueden insinuar peligro sin base metodológica. Diseña estilos descriptivos, publica leyendas y distingue observado, inferido y no verificado.

## OPSEC, ética y privacidad

Un grafo puede amplificar daño porque reúne datos dispersos y facilita inferencias nuevas. Aplica minimización desde el esquema:

1. Incluye solo entidades necesarias para una pregunta legítima.
2. Prefiere identificadores organizativos y expedientes frente a datos personales.
3. Seudonimiza los nodos de trabajo cuando el nombre no aporta valor analítico.
4. No publiques domicilios, teléfonos, rutinas ni relaciones familiares innecesarias.
5. Protege tablas, proyectos, exportaciones y copias de seguridad según su sensibilidad.
6. Revisa complementos antes de instalarlos y evita servicios de publicación para redes confidenciales.
7. Introduce un paso de réplica y derecho de respuesta antes de formular acusaciones.

La página oficial de un complemento para publicar grafos en la web [advierte expresamente](https://gephi.org/desktop/plugins/web-publish-plugin/) que no se deben publicar redes con información confidencial. Incluso si cada dato era público por separado, la agregación puede elevar el riesgo. Accesible no significa inocuo.

## Checklist de control antes de publicar

- [ ] La pregunta y el periodo están definidos.
- [ ] Cada tipo de nodo y arista tiene una semántica inequívoca.
- [ ] Las entidades se resuelven con identificadores y fechas, no solo por nombre.
- [ ] Cada arista conserva fuente y referencia verificable.
- [ ] Se documentan nulos, exclusiones, filtros y transformaciones.
- [ ] El carácter dirigido, los pesos y las métricas tienen justificación.
- [ ] La conclusión no depende de la posición visual de los nodos.
- [ ] Los patrones importantes se corroboraron fuera del grafo.
- [ ] La publicación minimiza datos personales y explica incertidumbres.

## Alternativas y siguientes pasos

Gephi destaca en exploración visual interactiva y preparación de gráficos. Si necesitas un flujo programable y repetible, [NetworkX](https://networkx.org/documentation/stable/reference/introduction.html) ofrece estructuras, algoritmos y lectura/escritura de grafos en Python; su propia documentación recomienda herramientas especializadas como Gephi para visualización avanzada. [Cytoscape](https://manual.cytoscape.org/en/latest/Node_and_Edge_Column_Data.html) es otra opción para redes con atributos y tablas asociadas. Una base SQL también puede ser suficiente cuando la pregunta se responde mejor con uniones auditables que con centralidades.

Elige por necesidad: hoja de cálculo para inspección pequeña, SQL para transformaciones trazables, NetworkX para automatización y pruebas, y Gephi para exploración visual. Puedes combinarlos si conservas formatos intermedios y controles de recuento.

El takeaway accionable es este: **antes de interpretar un grafo, audita el diccionario que convirtió documentos en nodos y relaciones**. Después prueba filtros y métricas; al final, regresa a las fuentes. El siguiente tema natural será estudiar cómo validar resolución de entidades con reglas, muestras y estados de incertidumbre sin fusionar homónimos por comodidad.
