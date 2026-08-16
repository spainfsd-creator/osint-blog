---
title: "OpenAIRE en OSINT: seguir proyectos, resultados y repositorios sin confundir enlaces con pruebas"
slug: /openaire-osint-proyectos-resultados-repositorios
authors: [osint-writter]
tags: [osint, investigation, research, verification, data, privacy]
date: 2026-08-16
image: /img/blog/2026-08-16-openaire-osint-proyectos-resultados-repositorios.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT contrastando proyectos, publicaciones, datos, software, repositorios y financiación pública](/img/blog/2026-08-16-openaire-osint-proyectos-resultados-repositorios.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/openaire-osint-proyectos-resultados-repositorios.m4a)


*Imagen generada mediante inteligencia artificial.*

Un consorcio afirma que una subvención pública produjo «una plataforma abierta, tres conjuntos de datos y resultados validados por universidades europeas». La nota de prensa enlaza el proyecto, pero no los resultados; el repositorio muestra varias versiones; y una publicación menciona la ayuda sin explicar qué pagó. **Que proyecto, obra y organización aparezcan conectados en un grafo no demuestra por sí solo autoría, financiación, entrega ni impacto.** OpenAIRE ayuda a encontrar esas relaciones, siempre que volvamos a la procedencia y a los documentos originales.

<!-- truncate -->

[OpenAIRE Explore](https://explore.openaire.eu/) permite buscar producción académica, datos, software, proyectos, organizaciones y fuentes del ecosistema de ciencia abierta. Se apoya en [OpenAIRE Graph](https://graph.openaire.eu/docs/), una colección abierta que agrega metadatos, los limpia, enriquece y enlaza para facilitar descubrimiento, seguimiento y análisis.

En OSINT responsable resulta útil para revisar afirmaciones sobre proyectos financiados, localizar resultados declarados, seguir versiones entre repositorios y editoriales, y construir una lista auditable de pistas. No es un registro contable, una certificación de cumplimiento ni una evaluación humana de la calidad científica. Todos los nombres, códigos, importes y hechos del caso práctico son ficticios.

## Qué es OpenAIRE y para qué sirve

El [modelo de datos oficial](https://graph.openaire.eu/docs/data-model/) distingue varias entidades: productos de investigación, fuentes de datos, organizaciones, proyectos, financiadores, líneas de financiación, comunidades y personas. Los productos pueden ser publicaciones, conjuntos de datos, software u otros resultados. Las fuentes incluyen repositorios, revistas, agregadores y bases de financiadores.

OpenAIRE agrega registros de proveedores como Crossref, DataCite, ORCID, Unpaywall, DOAJ y repositorios registrados en directorios especializados, entre otros. Después aplica procesos de limpieza, deduplicación, enriquecimiento y minería de texto. El resultado es especialmente interesante cuando una pregunta cruza tres capas:

- **financiación:** qué proyecto o ayuda pública aparece declarada;
- **producción:** qué publicación, dato, software u otro resultado se relaciona con ella;
- **procedencia:** qué repositorio, revista o proveedor entregó cada metadato.

Para una investigación legítima puede ayudar a:

- localizar un proyecto por acrónimo, título, identificador o financiador;
- enumerar resultados públicamente relacionados con ese proyecto;
- distinguir publicaciones, datos, software y otros productos;
- encontrar DOI, ORCID, ROR y otros identificadores persistentes;
- comparar repositorios o ubicaciones que ofrecen distintas versiones;
- explorar organizaciones participantes sin inferir relaciones actuales;
- documentar acceso, licencia, fecha y fuente declarados;
- preparar consultas repetibles mediante la API pública.

Su valor está en reunir pistas dispersas con su contexto. El error empieza cuando el analista convierte automáticamente una relación de metadatos en una afirmación jurídica o causal.

## Caso ficticio: auditar los resultados de un proyecto público

La fundación ficticia **Horizonte Claro** revisa el proyecto europeo imaginario `REUSA-DELTA`, ejecutado entre 2021 y 2024. La web del coordinador afirma que recibió 2,4 millones de euros y produjo una plataforma, tres datasets y una metodología «adoptada por cinco ciudades».

La pregunta se formula así:

> ¿Qué proyecto oficial corresponde a `REUSA-DELTA`, qué resultados públicos están enlazados con él, qué fuente sostiene cada relación y cuáles de las afirmaciones requieren corroboración adicional?

Creamos un inventario antes de buscar:

| Afirmación | Identificador o documento deseable | Qué no basta |
|---|---|---|
| existe una ayuda | código de proyecto y resolución oficial | una mención en una publicación |
| hubo 2,4 millones | ficha o contrato del financiador | presupuesto total del consorcio sin desglose |
| se publicó un dataset | DOI de DataCite y repositorio | un título sin archivo accesible |
| se creó software | repositorio, versión y licencia | una URL de organización o una captura |
| participaron cinco ciudades | entregable, convenio o fuente municipal | aparecer citadas en una noticia |
| el resultado fue adoptado | evidencia de uso y fecha | una relación semántica o una cita |

Esta separación evita investigar una conclusión predeterminada.

## Flujo recomendado paso a paso

### 1. Preserva la afirmación y fija alcance

Guarda la URL, el texto exacto, la fecha de consulta en UTC y el periodo investigado. Separa lo que dice la empresa, lo que declara el consorcio y lo que publica el financiador. Define también qué queda fuera: personas sin función pública, cuentas privadas, domicilios o cualquier dato personal irrelevante.

En el caso ficticio, el alcance cubre la existencia del proyecto, su financiación declarada, sus participantes institucionales y sus resultados abiertos hasta el 16 de agosto de 2026. No intenta evaluar la vida privada de investigadores ni atribuir fraude.

### 2. Empieza por el proyecto, no por el acrónimo

Los acrónimos se repiten y cambian de formato. Busca el candidato en Explore, pero no avances hasta confirmar título, identificador, financiador, fechas y organización coordinadora. Contrasta después esos campos con la ficha oficial del programa de financiación.

Registra una tabla mínima:

| Campo | Valor ficticio | Fuente |
|---|---|---|
| Project ID | `101000000` | ficha oficial imaginaria |
| Acrónimo | `REUSA-DELTA` | OpenAIRE y resolución |
| Periodo | 2021–2024 | contrato o portal del financiador |
| Coordinador | Instituto Delta Circular | ficha oficial |
| OpenAIRE ID | identificador interno observado | OpenAIRE Graph |

El OpenAIRE ID facilita repetir consultas; el código de la ayuda permite volver a la autoridad que concedió los fondos. Conserva ambos.

### 3. Explora relaciones y vuelve a cada fuente

Desde la ficha del proyecto, clasifica los resultados por tipo: publicación, dataset, software u otro producto. Para cada uno captura:

- título y tipo declarado;
- identificador persistente, si existe;
- fecha de publicación o depósito;
- proyecto relacionado y procedencia de esa relación;
- fuente que aloja o aportó el registro;
- acceso y licencia declarados;
- autores y organizaciones tal como aparecen en la versión original;
- fecha de recuperación.

No te limites al registro representativo. Abre el DOI, el repositorio y las instancias disponibles. Un mismo resultado puede tener preprint, manuscrito aceptado, versión editorial y copia de repositorio, con fechas y licencias diferentes.

### 4. Repite la consulta con la API

La interfaz es adecuada para explorar; la [API Graph v3](https://graph.openaire.eu/docs/apis/graph-api/overview/) permite dejar una consulta reproducible. La documentación actual recomienda v3 para nuevos flujos y agrupa las entidades bajo rutas consistentes.

Ejemplo ficticio y limitado:

```bash
# Resolver primero el proyecto y revisar sus identificadores.
curl --get 'https://api.openaire.eu/graph/v3/projects' \
  --data-urlencode 'search=REUSA-DELTA' \
  --data-urlencode 'pageSize=10'

# Tras validar el ID o el nombre inequívoco, pedir resultados relacionados.
curl --get 'https://api.openaire.eu/graph/v3/research-products' \
  --data-urlencode 'relProject=REUSA-DELTA' \
  --data-urlencode 'fromPublicationYear=2021' \
  --data-urlencode 'toPublicationYear=2026' \
  --data-urlencode 'pageSize=100'
```

El proyecto no existe y la consulta es ilustrativa. Antes de automatizar, revisa el esquema vigente, las condiciones del servicio y la paginación. Guarda parámetros, instante de consulta, cabeceras relevantes, número de resultados, cursor o página, errores y hash del JSON conservado. No satures el servicio ni recojas campos que no necesitas.

### 5. Entiende la deduplicación antes de contar

La [metodología de deduplicación](https://graph.openaire.eu/docs/graph-production-workflow/deduplication/) explica que el grafo agrupa registros solapados y construye un registro representativo manteniendo información de procedencia e instancias. Usa señales como identificadores, compatibilidad del tipo, títulos y autores. Las fechas no siempre separan productos porque un preprint y la versión publicada pueden pertenecer al mismo resultado.

Esto tiene dos consecuencias prácticas:

1. contar filas de repositorios puede inflar la producción;
2. aceptar sin revisión un grupo deduplicado puede ocultar diferencias entre versiones.

Para cada resultado importante, compara DOI, título, autores, tipo, versión y archivo. Si dos datasets comparten título pero difieren en contenido o DOI, no los fusiones por intuición. Si el grafo los agrupa, documenta la agrupación y verifica las instancias.

### 6. Separa cuatro relaciones que suelen confundirse

- **Producto–proyecto:** el metadato declara una relación con la ayuda.
- **Producto–organización:** una autoría o afiliación vincula una entidad en un momento concreto.
- **Proyecto–organización:** la entidad figura como participante, coordinadora u otro rol declarado.
- **Producto–fuente:** el registro fue recogido o alojado en un repositorio, revista o agregador.

Ninguna equivale automáticamente a propiedad intelectual, subcontratación, pago efectivo o adopción. Para esas afirmaciones necesitas contratos, resoluciones, entregables, cuentas, licencias o fuentes oficiales pertinentes.

### 7. Construye una cronología con distintos relojes

No mezcles:

1. inicio y fin del proyecto;
2. fecha del resultado;
3. fecha de depósito o actualización en el repositorio;
4. fecha de recogida o actualización del metadato;
5. fecha en que el analista consultó el sistema.

Un dataset depositado después del cierre puede ser un resultado tardío legítimo. Una actualización reciente no prueba que el contenido existiera durante la ejecución. Una obra anterior puede haberse enlazado al proyecto posteriormente. Cada conclusión debe indicar qué reloj utiliza.

### 8. Corrobora financiación, entregables y adopción

Para cerrar el caso, compara el grafo con:

- portal y resolución del financiador;
- acuerdo de subvención o ficha pública equivalente;
- repositorio oficial de entregables;
- DOI y landing page del editor o repositorio;
- archivos y versiones del software, junto con su licencia;
- portales de datos de las ciudades que supuestamente adoptaron el resultado;
- respuestas institucionales cuando la decisión lo justifique.

La conclusión puede ser: «resultado enlazado y corroborado», «relación declarada pendiente de confirmar», «versión no identificada», «adopción no demostrada» o «evidencia pública insuficiente». Ausencia en OpenAIRE no demuestra que el resultado no exista.

## Limitaciones y falsos positivos

- **Cobertura desigual:** no todos los repositorios, programas o disciplinas aportan los mismos metadatos.
- **Enlaces inferidos o aportados:** la relación puede proceder de texto minado, proveedor, reclamación o enriquecimiento; revisa la procedencia.
- **Duplicados imperfectos:** versiones distintas pueden fusionarse o quedar separadas.
- **Tipos inconsistentes:** un mismo objeto puede llegar como publicación, dato, software u «otro» según la fuente.
- **Identidad institucional:** nombres históricos, fusiones y filiales exigen ROR y registros oficiales.
- **Afiliación temporal:** participar en una obra no acredita empleo o colaboración actual.
- **Acceso y licencia:** «abierto» en metadatos no sustituye la comprobación del archivo y su licencia.
- **Financiación:** una mención de ayuda no demuestra importe imputado, pago ni cumplimiento.
- **Métricas cambiantes:** recuentos y relaciones varían al actualizarse el grafo.

## Buenas prácticas de OPSEC, ética y privacidad

- Define una finalidad legítima y proporcional antes de descargar datos.
- Minimiza información personal y evita perfiles individuales automatizados.
- Conserva identificadores, consultas, fecha y procedencia, no solo capturas.
- Separa observación, inferencia y contradicción en columnas distintas.
- No publiques claves, notas internas ni ficheros masivos sin necesidad.
- Respeta licencias, condiciones de uso y límites técnicos de cada fuente.
- No conviertas una ausencia o error de metadatos en acusación.
- Solicita segunda revisión antes de una publicación sensible o decisión adversa.
- Ofrece vía de corrección y réplica a las entidades afectadas.

## Alternativas y siguientes pasos

OpenAIRE funciona mejor acompañado:

- **CORDIS** para proyectos y resultados comunicados en programas de la UE;
- **portales nacionales y del financiador** para resoluciones y situación oficial;
- **Crossref y DataCite** para metadatos de DOI;
- **ORCID y ROR** para identidades persistentes de personas y organizaciones;
- **Zenodo y repositorios institucionales** para archivos, versiones y comunidades;
- **Software Heritage y repositorios de código** para preservar y revisar software público;
- **OpenAlex** para una vista bibliográfica complementaria, sin asumir equivalencia de cobertura o deduplicación.

El takeaway accionable es este: elige un proyecto público, exporta sus resultados por tipo y añade a cada fila tres columnas obligatorias —procedencia, identificador y corroboración primaria—. **OpenAIRE descubre conexiones valiosas; una investigación sólida explica quién creó cada enlace, qué significa y qué sigue sin demostrar.**

Un siguiente tema práctico sería estudiar DataCite para seguir versiones, relaciones entre datasets y software, y DOI sin confundir registro con contenido.

## Fuentes consultadas

- [OpenAIRE Graph: visión general](https://graph.openaire.eu/docs/)
- [OpenAIRE Graph: modelo de datos](https://graph.openaire.eu/docs/data-model/)
- [OpenAIRE Graph API v3: visión general](https://graph.openaire.eu/docs/apis/graph-api/overview/)
- [OpenAIRE Graph: deduplicación y procedencia](https://graph.openaire.eu/docs/graph-production-workflow/deduplication/)
- [OpenAIRE Graph API: organizaciones](https://graph.openaire.eu/docs/apis/graph-api/organizations/)
- [OpenAIRE Graph API: fuentes de datos](https://graph.openaire.eu/docs/apis/graph-api/data-sources/)
