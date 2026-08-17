---
title: "DataCite en OSINT: seguir DOI, versiones y relaciones sin confundir metadatos con pruebas"
slug: /datacite-osint-doi-versiones-relaciones
authors: [osint-writter]
tags: [osint, investigation, research, data, verification]
date: 2026-08-17
image: /img/blog/2026-08-17-datacite-osint-doi-versiones-relaciones.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT siguiendo DOI, versiones, datasets, software y relaciones de procedencia](/img/blog/2026-08-17-datacite-osint-doi-versiones-relaciones.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/datacite-osint-doi-versiones-relaciones.m4a)


*Imagen generada mediante inteligencia artificial.*

Una empresa asegura que su producto procede de «años de investigación abierta» y enlaza un dataset con DOI. La ficha parece impecable: autores, institución, licencia y trabajos relacionados. Sin embargo, el fichero descargable no coincide con la versión citada y la relación con el software fue declarada por el repositorio, no demostrada por una auditoría independiente. **Un DOI hace un objeto citable y localizable; no certifica por sí solo su contenido, calidad, autoría material ni las conclusiones que alguien extrae de él.**

<!-- truncate -->

Consultada el **17 de agosto de 2026**, la documentación oficial presenta [DataCite Commons](https://support.datacite.org/docs/datacite-commons) como una herramienta para descubrir obras con DOI, personas con ORCID, organizaciones con ROR y repositorios mediante las conexiones depositadas en los metadatos. Para OSINT responsable, su valor está en ordenar identificadores, versiones y relaciones antes de volver al archivo, al repositorio y a las fuentes primarias.

## Qué es DataCite y para qué sirve

DataCite es una infraestructura de identificadores persistentes y metadatos, muy utilizada para conjuntos de datos, software, informes, imágenes, colecciones y otros resultados de investigación. Su buscador público, [DataCite Commons](https://commons.datacite.org/), permite explorar ese catálogo; la [REST API](https://support.datacite.org/reference/introduction) devuelve metadatos en JSON siguiendo la especificación JSON:API.

En una investigación legítima puede ayudar a:

- localizar un objeto aunque cambie la URL de su repositorio;
- distinguir una versión concreta de un DOI que agrupa varias versiones;
- identificar relaciones declaradas entre dataset, software, artículo, informe o colección;
- recuperar autores, colaboradores, ORCID, afiliaciones y financiadores consignados;
- revisar licencia, fechas, tipo de recurso y repositorio responsable;
- documentar cuándo cambió el **registro de metadatos**;
- preparar consultas repetibles sin depender solo de capturas de pantalla.

Conviene fijar desde el principio tres capas que no son equivalentes:

| Capa | Qué observamos | Qué no demuestra por sí sola |
|---|---|---|
| DOI | identificador que resuelve a una página | que el archivo siga accesible o sea correcto |
| metadatos | descripción depositada por una cuenta responsable | que cada afirmación haya sido verificada externamente |
| contenido | ficheros y documentación del repositorio | que las conclusiones del productor sean ciertas |

## Caso de uso legítimo: comprobar la genealogía de un dataset

Imaginemos una *startup* ficticia, **Nimbo Delta Labs**, que atribuye su modelo de previsión agrícola a un proyecto universitario. Publica tres referencias:

1. un DOI «general» para el dataset;
2. un DOI para la versión 2.0 empleada en una demostración;
3. un DOI para el software que, según la empresa, produjo los resultados.

La pregunta OSINT no es «¿cómo desenmascaramos a la empresa?», sino una mucho más comprobable:

> ¿Qué objetos públicos existen, cómo están relacionados, qué versión estaba disponible en la fecha relevante y qué parte de la historia requiere corroboración independiente?

Antes de buscar, crea una tabla de hipótesis:

| Afirmación | Evidencia esperada | Fuente primaria |
|---|---|---|
| existía una versión 2.0 | DOI específico, campo `version`, fecha y archivos | registro DataCite y repositorio |
| el software generó el dataset | relación con semántica adecuada y documentación técnica | metadatos de ambos objetos y README |
| hubo financiación pública | identificador de ayuda y resolución | organismo financiador |
| la universidad participó | afiliación con fecha o documento del proyecto | universidad y memoria del proyecto |
| los resultados son reproducibles | datos, código, entorno y método suficientes | archivos de la versión citada |

Esta tabla impide que un grafo atractivo sustituya la verificación.

## Flujo recomendado

### 1. Parte del DOI exacto y conserva la resolución

Normaliza el identificador como `https://doi.org/<doi>` y registra:

- DOI literal, sin corregirlo silenciosamente;
- URL de destino y cadena de redirecciones;
- fecha y hora UTC de consulta;
- título, creador, editor o repositorio;
- versión y tipo de recurso declarados;
- licencia y disponibilidad real de los archivos.

El DOI suele llevar a una página de aterrizaje, no directamente al fichero. Guarda ambas URL. Si la página no carga, no concluyas que el objeto nunca existió: documenta el error y busca el registro por DOI en Commons o por API.

### 2. Explora el registro en DataCite Commons

La guía oficial de [obras en Commons](https://support.datacite.org/docs/works-in-datacite-commons) explica que la búsqueda general consulta campos como DOI, título, creador, editor, descripción, materia e identificadores relacionados. Después permite filtrar por año, tipo de obra, licencia, repositorio y otros campos.

En la ficha anota, por separado:

- **identidad:** título, creadores, ORCID y afiliaciones;
- **objeto:** `resourceTypeGeneral`, versión, formatos y tamaños;
- **custodia:** editor, repositorio y URL;
- **derechos:** licencia y URI de derechos;
- **contexto:** descripciones, materias y financiación;
- **relaciones:** cada identificador relacionado y su `relationType`.

Commons puede mostrar un grafo de conexiones. Ese grafo se construye con relaciones de los metadatos del DOI principal y de los objetos enlazados; **una arista representa una declaración estructurada, no una conclusión probatoria**.

### 3. Lee la dirección y el significado de cada relación

No reduzcas `relatedIdentifiers` a una lista de enlaces. La dirección cambia el sentido:

| Relación observada en A | Lectura prudente |
|---|---|
| `IsVersionOf B` | A se declara versión de B |
| `HasVersion B` | A se declara recurso que agrupa o tiene la versión B |
| `IsNewVersionOf B` | A se declara edición nueva de B |
| `IsPreviousVersionOf B` | A se declara edición anterior a B |
| `IsSupplementTo B` | A se declara suplemento de B |
| `IsDerivedFrom B` | A declara derivación desde B; falta valorar método y alcance |
| `IsSourceOf B` | A se declara fuente de B |
| `References B` | A referencia B; no implica uso material ni validación |
| `IsDocumentedBy B` | B se declara documentación de A |

Comprueba la relación desde los dos extremos. Puede existir solo en uno, estar mal orientada o utilizar una categoría demasiado genérica. Después abre la documentación del repositorio: el README, el historial de versiones, el artículo metodológico o el fichero de citas puede precisar lo que el metadato resume.

### 4. Separa DOI canónico, versión y secuencia

La guía oficial de [versionado](https://support.datacite.org/docs/versioning) recomienda que los cambios menores puedan reflejarse actualizando metadatos y el campo de versión, mientras que para cambios mayores se registre un DOI nuevo y se conecte con identificadores relacionados. La decisión de qué es «mayor» o «menor» corresponde a quien custodia el recurso.

En la práctica, pregunta:

1. ¿El DOI representa una versión concreta o todas las versiones?
2. ¿Existe un DOI canónico con relaciones `HasVersion`?
3. ¿Las versiones específicas apuntan al canónico con `IsVersionOf`?
4. ¿La secuencia enlaza edición anterior y nueva?
5. ¿La página ofrece exactamente los ficheros de la versión citada?
6. ¿Cambió el contenido bajo el mismo DOI o solo su descripción?

No ordenes versiones únicamente por `publicationYear`. Usa el campo de versión, las relaciones, las fechas relevantes y el historial del repositorio. Un año igual puede contener varias entregas; una fecha posterior puede corresponder solo a la corrección de metadatos.

### 5. Consulta la API para dejar una pista reproducible

La [sintaxis de búsqueda oficial](https://support.datacite.org/docs/queries) usa consultas de OpenSearch tanto en Commons como en el parámetro `query` de la API. Por ejemplo, para buscar objetos de software cuyo título contenga dos términos ficticios:

```bash
curl --get 'https://api.datacite.org/dois' \
  --data-urlencode 'query=titles.title:("Nimbo" AND "Delta") AND types.resourceTypeGeneral:Software' \
  --data-urlencode 'page[size]=10'
```

Para recuperar un DOI que ya conoces, codifica correctamente la barra en la URL o pásalo a una herramienta que lo haga. Del JSON conserva solo lo necesario para el caso:

```text
doi
titles[].title
creators[]
publisher
publicationYear
types.resourceTypeGeneral
version
relatedIdentifiers[]
rightsList[]
dates[]
fundingReferences[]
url
updated
```

Registra también la consulta exacta, la hora, el número de resultados y cualquier paginación. Si repites el trabajo más tarde, compara los registros por DOI; no confíes en la posición del resultado.

### 6. Recupera metadatos sin raspar la página

La [negociación de contenido de DataCite](https://support.datacite.org/docs/datacite-content-resolver) permite pedir representaciones de metadatos mediante la cabecera HTTP `Accept`. Para una ficha individual:

```bash
curl -L -H 'Accept: application/vnd.datacite.datacite+json' \
  'https://doi.org/DOI-DE-EJEMPLO'
```

`DOI-DE-EJEMPLO` es deliberadamente ficticio: sustitúyelo solo por un DOI público pertinente para tu investigación. Según la documentación, una petición HTML normalmente resuelve a la página del recurso; otros tipos admitidos pueden devolver DataCite JSON, XML, JSON-LD, BibTeX, RIS o una cita formateada.

Esto mejora la reproducibilidad, pero sigue recuperando **metadatos**. Para verificar el contenido debes descargar el fichero legítimamente accesible, anotar su versión y calcular una huella local si la finalidad y las condiciones lo permiten.

### 7. Revisa la procedencia de los cambios

DataCite documenta un endpoint de [procedencia de metadatos](https://support.datacite.org/docs/tracking-provenance):

```text
https://api.datacite.org/dois/<doi>/activities
```

Para registros desde el 10 de marzo de 2019 puede mostrar actividades de creación, actualización o eliminación, marcas temporales, cuenta de repositorio o miembro atribuida y campos cambiados. Es útil para responder «¿cuándo cambió este metadato?».

No responde automáticamente «¿cuándo cambió el fichero?», «¿quién hizo personalmente el cambio?» ni «¿por qué se corrigió?». La cuenta atribuida puede ser institucional y el contenido vivir en otro sistema con su propio historial.

### 8. Corrobora fuera de DataCite y redacta por niveles

Vuelve a las fuentes primarias:

- repositorio y archivos de la versión concreta;
- control de versiones o registro de *releases* del software;
- documentación metodológica y ficheros de entorno;
- resolución del financiador y número de ayuda;
- perfiles ORCID con su procedencia, no como certificación universal;
- registro ROR y web institucional para identidad organizativa;
- artículo, preprint o informe que explique la relación con los datos.

Redacta cada resultado como uno de estos estados:

- **observado:** el registro declara una relación o versión;
- **corroborado:** otra fuente primaria independiente coincide;
- **contradicho:** las fuentes discrepan de forma documentada;
- **no verificable:** faltan archivos, fechas o contexto;
- **inferido:** conclusión analítica explícitamente separada de los hechos.

## Checklist de validación

- [ ] He guardado el DOI exacto, la URL resuelta y la hora UTC.
- [ ] Sé si cito un DOI canónico o una versión específica.
- [ ] He leído la dirección de cada `relationType`.
- [ ] He comprobado ambos extremos de las relaciones importantes.
- [ ] He separado fecha de publicación, actualización del registro y versión.
- [ ] He abierto los archivos y la documentación, no solo el metadato.
- [ ] He registrado consulta, filtros, paginación y campos exportados.
- [ ] He corroborado autoría, afiliación y financiación en fuentes primarias.
- [ ] He distinguido ausencia de datos de evidencia negativa.
- [ ] He minimizado datos personales y documentado incertidumbre.

## Limitaciones y falsos positivos

- **Metadatos depositados:** la calidad depende de quien registra y mantiene el DOI.
- **Cobertura parcial:** Commons incluye los DOI de DataCite en estado *Findable*; otros DOI pueden aparecer solo bajo determinadas conexiones o importaciones.
- **Relaciones incompletas:** un enlace puede faltar en uno de los extremos o tardar en indexarse.
- **Semántica desigual:** dos repositorios pueden describir una relación similar con tipos distintos.
- **Versionado local:** cada custodio decide qué cambio merece DOI nuevo.
- **DOI canónico ambiguo:** citar el agregador cuando necesitabas una versión puede impedir reproducir el análisis.
- **Afiliación no temporal:** una institución declarada no demuestra empleo actual ni participación durante todo el proyecto.
- **Licencia descriptiva:** un valor en metadatos no sustituye leer la licencia del archivo y sus restricciones.
- **Métricas aportadas:** vistas y descargas dependen de informes enviados por repositorios; no equivalen a impacto o calidad.
- **Actualización de metadatos:** un cambio registrado en `/activities` no acredita modificación del contenido.
- **Ausencia:** no encontrar un DOI o una relación no prueba que el objeto o vínculo no existan.

## Buenas prácticas de OPSEC, ética y privacidad

- Define una finalidad legítima y proporcional antes de recopilar datos.
- Trabaja con objetos públicos necesarios para la pregunta; evita perfilar personas por curiosidad.
- No automatices decisiones adversas a partir de afiliaciones o grafos.
- Respeta condiciones de uso, límites técnicos y licencias de cada repositorio.
- Conserva originales y deriva copias de trabajo; no sobrescribas evidencia.
- Separa identificadores de notas sensibles y protege el expediente.
- No publiques correos, nombres u otros datos personales que no aporten valor probatorio.
- Describe errores de metadatos como errores, no como engaño, salvo evidencia adicional.
- Solicita segunda revisión para afirmaciones sensibles y ofrece vía de corrección.

## Alternativas y siguientes pasos

DataCite funciona mejor como una pieza de un flujo más amplio:

- **Crossref** para DOI y metadatos centrados especialmente en literatura académica;
- **OpenAIRE** para explorar proyectos, productos, repositorios y procedencia agregada;
- **OpenAlex** para redes bibliográficas de obras, autores e instituciones;
- **ORCID y ROR** para identificadores de personas y organizaciones, atendiendo a quién aportó cada dato;
- **Zenodo u otros repositorios** para archivos, comunidades, versiones y documentación;
- **Software Heritage** y el repositorio de origen para preservar y revisar código público;
- **portales del financiador** para resoluciones, importes y estado oficial.

El takeaway accionable es sencillo: toma un DOI público de un dataset, decide si identifica una versión o una familia, exporta sus `relatedIdentifiers` y añade cuatro columnas: **dirección, significado, procedencia y corroboración**. Si no puedes completar las cuatro, la arista sigue siendo una pista.

Como siguiente tema, sería útil estudiar **Software Heritage** para distinguir repositorio, *release*, artefacto y captura preservada cuando una investigación necesita citar código que cambia.

## Fuentes consultadas

- [DataCite Commons: introducción](https://support.datacite.org/docs/datacite-commons)
- [Obras y conexiones en DataCite Commons](https://support.datacite.org/docs/works-in-datacite-commons)
- [Consultas sobre metadatos DOI](https://support.datacite.org/docs/queries)
- [DataCite REST API](https://support.datacite.org/reference/introduction)
- [Versionado y relaciones entre versiones](https://support.datacite.org/docs/versioning)
- [Procedencia de los cambios de metadatos](https://support.datacite.org/docs/tracking-provenance)
- [Negociación de contenido para DOI](https://support.datacite.org/docs/datacite-content-resolver)
