---
title: "CISA KEV en OSINT: vulnerabilidades explotadas, prioridad y contexto antes de parchear"
slug: /cisa-kev-osint-vulnerabilidades-explotadas-prioridad-contexto
authors: [osint-writter]
tags: [osint, vulnerability-management, threat-intelligence, cve, defense, verification]
date: 2026-07-02
image: /img/blog/2026-07-02-cisa-kev-osint-vulnerabilidades-explotadas-prioridad-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando un catalogo publico de vulnerabilidades explotadas, tarjetas CVE, fechas de remediacion e inventario de activos](/img/blog/2026-07-02-cisa-kev-osint-vulnerabilidades-explotadas-prioridad-contexto.png)

**Descargar el podcast!**: <a href="/podcasts/cisa-kev-osint-vulnerabilidades-explotadas-prioridad-contexto.m4a">Descargar el podcast</a>


Una lista de vulnerabilidades criticas no te dice por si sola que debes arreglar primero. Algunas tienen `CVSS` alto pero no estan siendo explotadas; otras parecen menos espectaculares y, sin embargo, ya aparecen en campanas reales. El trabajo serio consiste en cruzar la senal publica con tu inventario, tu exposicion y tus ventanas de cambio. Ahi es donde el catalogo `CISA KEV` resulta especialmente util.

Revisando el feed publico el **2 de julio de 2026**, el `CISA Known Exploited Vulnerabilities Catalog` publicaba la version `2026.07.01`, liberada el `2026-07-01T19:00:06.9016Z`, con `1.631` vulnerabilidades. La entrada mas reciente visible en el feed era `CVE-2026-45659`, asociada a `Microsoft SharePoint Server`, anadida el `1 de julio de 2026` y con fecha de accion el `4 de julio de 2026`. Ese dato no es una invitacion a correr detras del ultimo titular: es una forma de ordenar una conversacion defensiva con evidencia de explotacion, fechas y acciones recomendadas.

Este articulo esta escrito para equipos defensivos, responsables de vulnerabilidades, `SOC`, `CERT/CSIRT`, auditoria tecnica y periodistas que necesitan entender como usar una fuente abierta sin convertirla en una lista de sustos. No contiene instrucciones de explotacion, intrusiones, doxxing, acoso ni escaneo contra terceros.

<!-- truncate -->

## Que es CISA KEV y para que sirve

[`CISA KEV`](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) es el catalogo publico de vulnerabilidades conocidas y explotadas que mantiene la Cybersecurity and Infrastructure Security Agency de Estados Unidos. En la practica, es una lista curada de `CVE` para las que CISA ha reunido evidencia de explotacion real y una accion de remediacion clara.

Para un flujo OSINT defensivo, su valor aparece cuando necesitas responder preguntas concretas:

- que `CVE` tienen evidencia publica de explotacion, no solo gravedad teorica;
- que producto y proveedor estan asociados a cada entrada;
- cuando se anadio la vulnerabilidad al catalogo;
- que fecha de accion marca CISA para entornos sujetos a sus directivas;
- si CISA conoce uso en campanas de ransomware;
- que notas enlazan a advisories de proveedor, NVD u otras guias oficiales;
- como priorizar el trabajo sin confundir "nuevo", "critico" y "explotado".

La parte metodologica importa. `KEV` no sustituye un inventario de activos ni una herramienta de gestion de vulnerabilidades. Sirve como senal externa de explotacion observada. Si tu organizacion no tiene el producto afectado, la entrada es contexto. Si lo tiene, pero no esta expuesto y esta segmentado, la prioridad puede ser distinta. Si lo tiene expuesto a internet y sin mitigacion, la conversacion cambia por completo.

Tambien conviene actualizar el contexto normativo. `BOD 22-01` fue la directiva que establecio el catalogo como pieza central de reduccion de riesgo federal, pero CISA la marca ahora como revocada y sustituida por [`BOD 26-04`](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk). La pagina de `BOD 26-04` explica que consolida y aclara las guias de remediacion, y que la urgencia debe leerse combinando exposicion del activo, presencia en `KEV` y otros factores de riesgo. Para analistas fuera del gobierno federal estadounidense, la leccion sigue siendo util: `KEV` es una entrada de priorizacion, no una decision automatica.

## Caso de uso legitimo con ejemplo ficticio

Imagina que `Meridiano Salud`, una organizacion ficticia, recibe un informe mensual de vulnerabilidades con 4.000 hallazgos. El informe esta ordenado por severidad tecnica, asi que los equipos se atascan en una pila enorme de "criticos" y "altos". El responsable de riesgo quiere separar tres cosas:

- que vulnerabilidades estan en productos realmente presentes;
- cuales afectan a activos publicamente expuestos;
- cuales aparecen en `CISA KEV` con evidencia de explotacion.

Un registro inicial podria quedar asi:

| Campo | Ejemplo ficticio | Por que importa |
| --- | --- | --- |
| `cve_id` | `CVE-20XX-12345` | Selector comun para cruzar fuentes |
| Producto afectado | `Servidor documental interno` | Evita trabajar sobre activos inexistentes |
| Exposicion | `VPN / intranet / internet` | Cambia la urgencia operativa |
| `KEV` | `si / no` | Indica explotacion observada por CISA |
| Fecha anadida | `2026-07-01` | Ayuda a construir cronologia |
| Accion recomendada | `Mitigar segun proveedor` | Conecta inteligencia con remediacion |
| Evidencia interna | `scanner, CMDB, ticket` | Evita depender solo de una fuente externa |

La conclusion responsable no seria "todo lo que esta en `KEV` se parchea antes que cualquier otra cosa". Seria mas concreta:

1. Si el `CVE` esta en `KEV`, el producto existe en el inventario y el activo esta expuesto, escalar prioridad.
2. Si el `CVE` esta en `KEV`, pero el producto no existe en el entorno, documentar descarte.
3. Si el producto existe, pero el hallazgo viene de un scanner antiguo, validar version y configuracion antes de abrir una crisis.
4. Si no hay parche inmediato, registrar mitigacion compensatoria, responsable y fecha de revision.
5. Si se detecta exposicion publica, coordinar con respuesta a incidentes antes de publicar ningun detalle.

Ese flujo ensena una idea basica del OSINT serio: la fuente abierta acelera la pregunta, pero la evidencia local decide la accion.

## Flujo recomendado

### 1. Descargar la fuente canónica

CISA publica el catalogo en la web y tambien como feed `JSON`. El repositorio oficial [`cisagov/kev-data`](https://github.com/cisagov/kev-data) actua como espejo de los ficheros de datos y explica que el origen canonico sigue siendo `cisa.gov/kev`. El espejo aporta una ventaja practica: historial de commits para ver cambios con mas transparencia.

Un flujo prudente empieza guardando metadatos de consulta:

- URL consultada;
- fecha y hora en UTC;
- `catalogVersion`;
- `dateReleased`;
- `count`;
- hash del fichero descargado si el caso exige trazabilidad.

No hace falta automatizar nada agresivo. Basta con tratar el feed como una fuente documental que puede cambiar.

### 2. Entender el esquema antes de filtrar

El esquema `JSON` oficial define campos como `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction`, `dueDate`, `knownRansomwareCampaignUse`, `notes` y `cwes`. Esa estructura es mas util que una captura de pantalla porque permite filtrar, auditar y repetir el analisis.

Para una revision defensiva, las preguntas minimas son:

- que entradas nuevas hay desde la ultima revision;
- que entradas tienen fecha de accion cercana;
- que proveedores aparecen en mi inventario;
- que productos son internet-facing o sostienen procesos criticos;
- que notas enlazan a advisories de proveedor que debo leer completos;
- que entradas tienen posible uso en ransomware y requieren coordinacion adicional.

### 3. Cruzar con inventario propio

El error habitual es leer `KEV` como si fuera un ranking universal. No lo es. Una vulnerabilidad explotada contra un producto que no usas no tiene prioridad operativa para ti. Una vulnerabilidad explotada contra un producto que usas en un activo aislado puede requerir accion, pero no necesariamente la misma urgencia que un servicio expuesto.

Un cruce defensivo puede separar tres listas:

- **accion inmediata**: producto presente, version afectada probable, activo expuesto o critico;
- **validacion tecnica**: producto presente, pero version, configuracion o exposicion dudosa;
- **contexto/documentacion**: producto no presente o entrada no aplicable al entorno.

La diferencia entre esas listas reduce ruido y evita dos fallos simetricos: ignorar una senal real o saturar al equipo con falsos positivos.

### 4. Verificar con fuentes primarias

Cuando una entrada importa, no te quedes solo con el resumen. Lee el advisory del proveedor, la entrada de `NVD` si aporta contexto, notas de CISA y documentacion interna. El campo `requiredAction` suele resumir la accion, pero la implementacion real depende del producto, version, arquitectura y dependencias.

En informes, conviene separar:

- dato de `KEV`;
- dato del proveedor;
- dato del scanner;
- dato del inventario;
- inferencia del analista.

Esa separacion protege el informe cuando alguien pregunte "de donde sale esta conclusion".

### 5. Convertirlo en rutina, no en alarma puntual

El catalogo se actualiza cuando CISA incorpora entradas nuevas o modifica datos. El repositorio espejo indica que se sincroniza poco despues del origen canonico, normalmente en dias laborables y horario laboral de la costa este de Estados Unidos cuando hay cambios. Para un equipo defensivo, lo util no es mirar la pagina cuando hay ruido en redes, sino crear una rutina:

- revision diaria o semanal del feed;
- diff contra la version anterior;
- cruce con inventario;
- apertura de tickets solo cuando hay aplicabilidad;
- cierre documentado cuando no aplica;
- metrica de tiempo desde entrada en `KEV` hasta decision interna.

Ese ultimo dato es mas valioso que una presentacion llena de CVEs: mide si la organizacion convierte inteligencia abierta en accion verificable.

## Limitaciones y falsos positivos

`CISA KEV` es una fuente fuerte, pero tiene limites claros:

- no contiene todas las vulnerabilidades explotadas del mundo;
- requiere `CVE` y guia de remediacion clara para incorporar una entrada;
- no prueba que tu organizacion este afectada;
- no sustituye telemetria interna ni respuesta a incidentes;
- no ordena automaticamente por impacto local;
- puede apuntar a productos que aparecen en tu inventario de forma incorrecta o desactualizada;
- la fecha de accion de CISA no siempre coincide con tus ventanas de cambio, contratos o restricciones operativas.

Tambien hay que evitar la lectura inversa: que una vulnerabilidad no este en `KEV` no significa que sea segura, irrelevante o no explotable. Significa que no cumple, o aun no cumple, los criterios de inclusion del catalogo. En gestion de riesgo, ausencia de una senal no equivale a ausencia de riesgo.

## Buenas practicas de OPSEC, etica y privacidad

Usar `KEV` de forma responsable exige disciplina:

- no publiques listas de activos propios afectados sin necesidad;
- no uses el catalogo para buscar victimas ajenas;
- no combines `KEV` con escaneos contra terceros sin autorizacion;
- no conviertas una coincidencia de scanner en acusacion o atribucion;
- limita los detalles tecnicos en informes externos cuando puedan facilitar abuso;
- conserva evidencias de consulta, version del feed y razonamiento;
- prioriza remediacion, mitigacion y comunicacion interna sobre ruido publico.

Para periodistas o investigadores externos, la regla es todavia mas estricta: `KEV` puede explicar por que una vulnerabilidad merece atencion, pero no justifica identificar sistemas vulnerables de terceros ni publicar rutas de explotacion. La historia responsable habla de riesgo, contexto, mitigacion y rendicion de cuentas, no de convertir la fuente publica en municion.

## Alternativas y siguientes pasos

`CISA KEV` funciona mejor como capa de priorizacion junto a otras fuentes:

- `NVD`, para contexto general de `CVE`, `CWE`, referencias y metadatos;
- advisories del proveedor, para versiones afectadas, parches y mitigaciones reales;
- `Vulnrichment`, si necesitas enriquecimiento estructurado del ecosistema CISA;
- inventario interno, para saber si el producto existe y donde;
- scanners de vulnerabilidades, para validar presencia tecnica;
- `OpenCTI` o una plataforma similar, si quieres convertir observables, informes y decisiones en grafo trazable;
- `MISP`, si el equipo comparte inteligencia y necesita taxonomias, distribucion y control de contexto.

El takeaway practico es sencillo: trata `CISA KEV` como una senal OSINT de explotacion real que debe pasar por inventario, exposicion y verificacion. Bien usado, ayuda a priorizar con criterio. Mal usado, solo cambia una lista enorme por otra lista con mas urgencia aparente.

Como siguiente paso editorial, tendria sentido comparar `CISA KEV`, `NVD` y advisories de proveedor sobre un mismo caso ficticio para ver que aporta cada capa y donde empieza el trabajo propio del analista.

## Fuentes consultadas

- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [CISA KEV JSON feed](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- [CISA KEV JSON schema](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json)
- [cisagov/kev-data en GitHub](https://github.com/cisagov/kev-data)
- [BOD 26-04: Prioritizing Security Updates Based on Risk](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk)
- [BOD 22-01 revocada y sustituida por BOD 26-04](https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities-revoked)
- [NVD: Known Exploited Vulnerabilities](https://nvd.nist.gov/general/news/cisa-exploit-catalog)
