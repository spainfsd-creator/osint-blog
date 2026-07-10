---
title: "ICIJ Offshore Leaks Database en OSINT: grafos societarios, contexto y cautela antes de atribuir"
slug: /icij-offshore-leaks-osint-grafos-societarios-contexto
authors: [osint-writter]
tags: [osint, due-diligence, data, verification, investigation, privacy]
date: 2026-07-10
image: /img/blog/2026-07-10-icij-offshore-leaks-osint-grafos-societarios-contexto.png
---

![Ilustración editorial de una mesa de investigación OSINT con un grafo abstracto de entidades offshore, documentos redactados, mapa de jurisdicciones y notas de verificación](/img/blog/2026-07-10-icij-offshore-leaks-osint-grafos-societarios-contexto.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/icij-offshore-leaks-osint-grafos-societarios-contexto.m4a)


Una coincidencia en una base offshore puede parecer una revelación inmediata: un nombre, una sociedad, una dirección, una jurisdicción y una línea que une dos nodos. El problema es que en investigación societaria **una coincidencia no es una atribución**. Puede ser una pista excelente, pero también un homónimo, un dato viejo, una relación administrativa o una estructura legítima que exige contexto antes de escribir una sola frase contundente.

La [`ICIJ Offshore Leaks Database`](https://offshoreleaks.icij.org/) sirve justo para ese primer mapa prudente. Reúne información publicada por el Consorcio Internacional de Periodistas de Investigación a partir de investigaciones como `Offshore Leaks`, `Panama Papers`, `Bahamas Leaks`, `Paradise Papers` y `Pandora Papers`. Revisando su documentación el **10 de julio de 2026**, la base afirma cubrir más de `810.000` entidades offshore, con registros que abarcan más de `80` años hasta `2020` y vínculos con personas y compañías en más de `200` países y territorios.

Este artículo está escrito para periodistas, analistas de cumplimiento, investigadores corporativos, equipos anticorrupción y personas que necesitan trabajar con indicios societarios de forma proporcionada. No es una guía para señalar personas por homonimia, acosar, doxxear ni convertir filtraciones en acusaciones automáticas.

<!-- truncate -->

## Qué es ICIJ Offshore Leaks Database y para qué sirve

`Offshore Leaks Database` es una base consultable y descargable de entidades, intermediarios, oficiales, direcciones y relaciones extraídas de varias investigaciones periodísticas de ICIJ. Su valor OSINT no está en “encontrar culpables”, sino en abrir preguntas verificables:

- qué entidades aparecen asociadas a un nombre o dirección;
- qué jurisdicción y fuente de filtración aporta cada registro;
- qué intermediarios o direcciones conectan sociedades aparentemente separadas;
- qué relaciones merecen contraste en registros mercantiles, sanciones, prensa, tribunales o documentos corporativos;
- qué parte del grafo es dato publicado y qué parte es inferencia del analista.

La propia página de ICIJ incluye una advertencia metodológica esencial: hay usos legítimos para sociedades y trusts offshore, y aparecer en la base no implica por sí mismo conducta ilegal o impropia. También recuerda que muchas personas y entidades comparten nombres similares, por lo que la identidad debe confirmarse con direcciones u otros datos distinguibles.

La base puede usarse de tres formas principales:

- interfaz web, para búsquedas puntuales y exploración visual;
- descarga en `CSV`, con archivos por tipo de nodo y relaciones;
- trabajo en grafo, con guías y paquetes para `Neo4j`;
- `Reconciliation API`, para comparar datasets propios contra entidades de la base.

Esta variedad importa porque no todas las investigaciones necesitan el mismo nivel técnico. Un caso pequeño puede resolverse con lectura manual y buenas notas. Un proyecto de datos, en cambio, puede necesitar limpieza, reconciliación, grafo y revisión por pares.

## Caso de uso legítimo con un ejemplo ficticio

Imagina que una redacción investiga contratos públicos adjudicados a varias empresas de consultoría en distintos países. En una memoria anual aparece una sociedad llamada `Blue Harbor Advisory Ltd.` y una dirección postal en una jurisdicción offshore. El nombre no prueba nada, pero el equipo quiere saber si existe una pista documental que merezca atención.

Un flujo responsable empezaría así:

1. anotar la fuente original donde aparece `Blue Harbor Advisory Ltd.`;
2. buscar el nombre exacto y variantes razonables en Offshore Leaks;
3. separar coincidencias por jurisdicción, dirección, intermediario y fuente de filtración;
4. descartar homónimos obvios;
5. contrastar la entidad candidata en registros oficiales y documentos públicos;
6. revisar si la relación está vigente, histórica, administrativa o ambigua;
7. formular una hipótesis limitada, no una acusación.

La conclusión provisional no debería ser “esta empresa está en los papeles offshore”. Una redacción rigurosa escribiría algo más estrecho:

> Hemos localizado una entidad con nombre coincidente y dirección compatible en la base de ICIJ. La relación procede de una filtración concreta y debe contrastarse con el registro mercantil, documentos societarios y respuesta de las partes antes de extraer conclusiones.

Ese matiz cambia todo. Convierte una coincidencia llamativa en una pista verificable.

## Flujo recomendado

### 1. Definir el sujeto exacto

Antes de buscar, escribe qué entidad estás investigando y de dónde sale:

```text
Sujeto ficticio: Blue Harbor Advisory Ltd.
Fuente inicial: memoria anual 2025 de una empresa contratista
Dato distinguible: dirección postal parcial y país de incorporación declarado
Pregunta: ¿hay registros offshore publicados que apunten a una entidad compatible?
```

La base contiene nombres repetidos, transliteraciones, abreviaturas y direcciones incompletas. Si no defines el sujeto, acabarás adaptando la hipótesis al resultado más interesante.

### 2. Buscar por capas, no por ansiedad

Empieza por el nombre exacto. Luego prueba variantes razonables:

```text
Blue Harbor Advisory Ltd
Blue Harbor Advisory Limited
"Blue Harbor" offshore
```

Después usa atributos secundarios: dirección, jurisdicción, intermediario o nombre de oficial. No mezcles todo desde el principio. Cada capa debe responder una pregunta concreta.

### 3. Leer el nodo y la relación

En un grafo societario, el error común es mirar solo el nodo más visible. La relación importa igual o más:

- `officer_of` no significa necesariamente propietario real;
- `registered_address` puede ser un proveedor compartido;
- un `intermediary` puede actuar para miles de sociedades;
- una dirección puede representar despacho, agente registrado o buzón;
- una fecha histórica puede no describir el estado actual.

El dato debe conservar su etiqueta original. Si la base dice “oficial”, no lo conviertas en “dueño” salvo que otra fuente lo demuestre.

### 4. Volver a fuentes primarias

ICIJ recomienda verificar la información contra otras fuentes. En un caso societario, eso suele significar:

- registro mercantil de la jurisdicción;
- documentos de incorporación, disolución, cambios de dirección o cargos;
- litigios y expedientes administrativos;
- sanciones, PEP y listas de cumplimiento cuando sean relevantes;
- hemeroteca y comunicados oficiales;
- sitios corporativos archivados;
- documentos de contratación o subvenciones;
- respuesta de la entidad investigada si el hallazgo va a publicarse.

La base sirve para encontrar rutas. La evidencia publicable suele estar en la corroboración.

### 5. Registrar incertidumbre

Una tabla pequeña ayuda más que un grafo bonito:

| Elemento | Resultado | Riesgo |
| --- | --- | --- |
| Nombre | Coincidencia exacta | Puede haber homónimos |
| Dirección | Compatible, no idéntica | Puede ser agente registrado |
| Jurisdicción | Coincide con otra fuente | No prueba control |
| Relación | Oficial de entidad | No equivale a beneficiario real |
| Fecha | Registro histórico | Puede estar desactualizado |

Si una pieza es débil, márcala como débil. La trazabilidad no consiste en llenar una tabla; consiste en no esconder dónde el caso todavía se mueve.

## Descarga, CSV, Neo4j y reconciliación

La página de descarga de ICIJ explica que la base funciona sobre `Neo4j`, pero que el equipo convirtió los datos en varios `CSV`: uno por tipo de nodo y uno para relaciones. Eso permite trabajar con herramientas más sencillas antes de saltar a un grafo completo.

Un flujo técnico prudente sería:

```text
CSV de ICIJ -> OpenRefine o SQLite -> normalización mínima
             -> revisión de coincidencias -> grafo solo para relaciones relevantes
             -> fuentes primarias -> informe con límites
```

No hace falta cargar todo en `Neo4j` para cada caso. El grafo es útil cuando hay muchas relaciones, pero puede crear una falsa sensación de patrón si los datos no están limpios.

La documentación de la `Reconciliation API` añade otra capa: permite comparar nombres, direcciones, entidades, intermediarios, oficiales y otros tipos contra la base. ICIJ la presentó en enero de 2025 como una forma de ayudar a usuarios a cruzar sus propios datos con más de `810.000` entidades offshore. La API puede acelerar proyectos grandes, pero no elimina revisión humana. Un “match” es candidato, no conclusión.

Buenas prácticas para reconciliación:

- normaliza mayúsculas, sufijos societarios y espacios, pero conserva el valor original;
- separa coincidencias exactas de aproximadas;
- no fusiones personas solo por nombre;
- usa dirección, jurisdicción y fuente como desempate;
- conserva el identificador del nodo y la URL consultada;
- revisa manualmente los casos que vayan a aparecer en un informe.

## Limitaciones y falsos positivos

### La base no es un registro universal

Offshore Leaks contiene datos publicados a partir de investigaciones concretas. No cubre todas las jurisdicciones, todas las entidades offshore ni todos los periodos. La ausencia de resultado no demuestra ausencia de estructura.

### Los datos pueden estar desactualizados

ICIJ indica que los registros cubren periodos definidos y que parte de la información puede haber cambiado. Una entidad activa en una filtración histórica puede estar disuelta, renombrada o transferida.

### Una dirección compartida no prueba coordinación

Agentes registrados, despachos y proveedores fiduciarios pueden aparecer en miles de entidades. Esa relación abre una vía, pero no prueba control común.

### Offshore no equivale automáticamente a ilegal

Existen usos legítimos para estructuras offshore. El análisis debe distinguir entre secreto, planificación fiscal, cumplimiento, conflicto de interés, sanciones, fraude y simple formalidad societaria.

### No todo el material original es público

La base pública no es una entrega masiva de documentos originales. ICIJ ha explicado históricamente que publica información corporativa limitada de interés público, no todos los correos, pasaportes, cuentas bancarias o archivos internos.

### La coincidencia de nombres es peligrosa

En bases internacionales, los homónimos son inevitables. Si no hay fecha, dirección, documento o identificador robusto, la atribución debe quedarse en hipótesis o descartarse.

## Buenas prácticas de OPSEC, ética y privacidad

- Investiga entidades y hechos de interés público, no la vida privada por curiosidad.
- Minimiza datos personales en notas, capturas y exports.
- No publiques direcciones personales si no son indispensables y ya están justificadas por interés público.
- No confundas un intermediario administrativo con una red criminal.
- Conserva fecha de consulta, URL, nodo, relación y fuente de filtración.
- Distingue dato, inferencia y valoración editorial.
- Busca derecho de respuesta cuando el hallazgo pueda afectar reputaciones.
- No automatices acusaciones a partir de la `Reconciliation API`.
- Documenta qué evidencia podría refutar tu hipótesis.

La ética en OSINT societario no consiste en evitar hallazgos incómodos. Consiste en no dañar a alguien por una lectura perezosa de un grafo.

## Alternativas y siguientes pasos

Offshore Leaks encaja mejor como una capa dentro de un flujo más amplio:

- `OpenCorporates`, para descubrir entidades y llegar a registros primarios;
- `Companies House`, cuando el caso toca sociedades británicas;
- `OpenOwnership`, para modelos y datos de beneficiario real cuando existan;
- `OpenSanctions`, para revisar coincidencias de sanciones y PEP con cautela;
- `EDGAR`, si hay compañías cotizadas o filings estadounidenses;
- `OpenRefine`, para limpiar nombres y reconciliar datasets;
- `Datasette` o `SQLite`, para hacer consultas reproducibles;
- `Maltego` o `Neo4j`, cuando el grafo aporte claridad real y no decoración.

El takeaway práctico es sencillo: usa `ICIJ Offshore Leaks Database` como **motor de hipótesis verificables**, no como veredicto. Primero identifica el nodo correcto, después entiende la relación, luego contrasta en fuentes primarias y solo al final decide qué puede afirmarse. En investigación offshore, el hallazgo más valioso suele ser una frase con límites bien escritos.

## Fuentes consultadas

- [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org/)
- [ICIJ Offshore Leaks Database: How to download this database](https://offshoreleaks.icij.org/pages/database)
- [ICIJ Offshore Leaks Database: Reconciliation API](https://offshoreleaks.icij.org/docs/reconciliation)
- [ICIJ: Explore the latest tool to power up investigations via the Offshore Leaks database](https://www.icij.org/inside-icij/2025/01/explore-the-latest-tool-to-power-up-investigations-via-the-offshore-leaks-database/)
- [ICIJ/offshoreleaks-data-packages](https://github.com/ICIJ/offshoreleaks-data-packages)
- [ICIJ Offshore Leaks Database FAQs](https://www.icij.org/inside-icij/2013/06/offshore-leaks-database-faqs/)
- [Center for Public Integrity: ICIJ to release Panama Papers offshore companies data](https://publicintegrity.org/accountability/coming-soon-icij-to-release-panama-papers-data/)
