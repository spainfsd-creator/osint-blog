---
title: "Maltego en OSINT: analisis de enlaces y grafos para investigar con metodo"
slug: /maltego-osint-analisis-enlaces-grafos
authors: [osint-writter]
tags: [osint, tools, investigation, tradecraft, privacy, link-analysis]
date: 2026-02-13
image: /img/blog/2026-02-13-maltego-osint-grafos.png
---

![Ilustracion sobre analisis de enlaces (grafos) en una investigacion OSINT con Maltego](/img/blog/2026-02-13-maltego-osint-grafos.png)

Cuando una investigacion OSINT crece, el problema deja de ser "encontrar algo" y pasa a ser **no perderse**: demasiados dominios, correos, organizaciones, infraestructuras, aliases y fuentes abiertas inconexas. En ese punto, herramientas de **analisis de enlaces** (link analysis) como Maltego ayudan a convertir una lista caotica de hallazgos en una estructura que se puede revisar, auditar y explicar.

En esta guia vas a ver un enfoque **practico y responsable**: metodologia, buen uso de transformaciones, y como evitar falsos positivos, sesgos y recogida innecesaria de datos personales.

<!-- truncate -->

## Que es Maltego (y por que encaja en OSINT)

Maltego es una herramienta de investigacion basada en **entidades** y **relaciones**.

- Una entidad es un "tipo de cosa": dominio, IP, organizacion, correo, persona, documento, etc.
- Una relacion es un vinculo: resuelve a, pertenece a, aparece en, comparte infraestructura con, etc.

La idea clave: en lugar de trabajar con notas sueltas, construyes un **grafo** donde cada nodo tiene procedencia y cada enlace se puede justificar.

Usos legitimos tipicos en OSINT:

- Due diligence (relaciones entre empresas, marcas, dominios, presencia publica).
- Ciberinteligencia defensiva (mapear infraestructura expuesta propia o autorizada).
- Respuesta a incidentes (correlacionar dominios, certificados, rangos e indicadores publicos).
- Investigacion periodistica (organizar fuentes abiertas y lineas de relacion verificables).

## Caso de uso (ficticio): due diligence de proveedor

Contexto: una empresa va a contratar a un proveedor de servicios digitales. El proveedor presenta tres dominios y un conjunto de marcas. El objetivo es **reducir riesgo** (no "cazar" a nadie).

Preguntas razonables:

1. Que dominios y subdominios publicos se asocian a esa marca/proveedor.
2. Si hay infraestructura compartida con servicios que no encajan (p. ej. paneles publicos no esperados).
3. Si hay indicios publicos de suplantaciones o typosquatting alrededor de su marca.

Resultado deseado: un mapa claro de activos publicos relacionados (y su nivel de confianza) para informar al equipo de compras/seguridad.

## Flujo recomendado (paso a paso, con criterio)

### 1) Define alcance, permisos y limite de datos

Antes de abrir la herramienta:

- Define el objetivo: "inventario publico" y "coherencia de marca/infra".
- Documenta el alcance (dominios proporcionados, marcas, paises, ventana temporal).
- Minimiza PII: si una relacion no aporta a la hipotesis, no la persigas ni la conserves.

Regla de oro: **OSINT responsable no es acumular, es justificar**.

### 2) Prepara semillas (inputs) de calidad

En Maltego, una buena investigacion empieza con pocas semillas, pero buenas:

- Dominios oficiales: `proveedor-ejemplo.com`, `proveedor-ejemplo.net`
- Marca/razon social: "Proveedor Ejemplo, S.L."
- Correo generico de contacto (si es publico y relevante): `contacto@proveedor-ejemplo.com`

Evita empezar con datos personales (nombres, handles) salvo que sea imprescindible y este justificado.

### 3) Ejecuta transformaciones en capas, no en cascada sin control

Una trampa comun es lanzar "todo" y producir un grafo enorme, imposible de revisar.

En su lugar, trabaja por capas:

1. Resolucion basica: dominio -> DNS -> IPs (y a la inversa, cuando aplique).
2. Contexto tecnico: certificados TLS (cuando la fuente lo permita), hosting, ASNs.
3. Contexto de marca: presencia en fuentes abiertas (webs oficiales, perfiles verificados, repositorios, etc.).

Despues de cada capa:

- Revisa que cada salto tenga sentido.
- Elimina ruido.
- Anota "por que" lo mantienes.

### 4) Registra procedencia y nivel de confianza

No todos los enlaces valen lo mismo.

- Una relacion basada en una fuente oficial (web corporativa, repositorio oficial, documento firmado) tiene mas peso.
- Una relacion inferida por coincidencias tecnicas (hosting compartido, CDN, etc.) es util, pero puede ser circunstancial.

Practica recomendable:

- Marca en tus notas si una relacion es: confirmada, probable, debil.
- Guarda evidencia reproducible (URL, fecha/hora, captura si procede).

### 5) Cierra el ciclo con verificacion cruzada

Maltego te ayuda a **formular hipotesis**; la verificacion la haces con triangulacion:

- Contrasta con otras fuentes abiertas.
- Repite una consulta con otra herramienta cuando el hallazgo sea critico.
- Si el trabajo es para una organizacion: contrasta con inventario interno/autorizado.

## Limitaciones (y donde aparecen los falsos positivos)

- **Fuentes heterogeneas**: las transformaciones dependen de proveedores/fuentes con coberturas y politicas distintas.
- **Cambios en la web**: una relacion valida hoy puede no existir manana (y al reves).
- **Infraestructura compartida**: hosting, CDNs y servicios gestionados pueden generar relaciones engañosas.
- **Sesgos de entrada**: si empiezas con una semilla equivocada, todo el grafo se contamina.

Mitigacion practica: cuanto mas "sorprendente" sea una conclusion, mas evidencia cruzada necesita.

## Buenas practicas de OPSEC, etica y privacidad

- Trabaja con finalidad legitima y con permiso cuando corresponda.
- Evita automatizar recogida masiva de datos personales.
- No publiques PII en el blog ni en informes; redacta o agrega.
- Respeta terminos de servicio de las fuentes y licencias de datos.
- Documenta tus pasos: una investigacion profesional es reproducible.

## Alternativas (segun tu caso)

- Si buscas automatizacion "one-click" orientada a reconocimiento: herramientas de OSINT automatizado pueden encajar mejor en fases iniciales.
- Si tu problema es analisis avanzado de grafos a gran escala: bases de datos de grafos (y pipelines propios) pueden ser mas adecuadas, a costa de mas ingenieria.
- Si necesitas solo un mapa visual sencillo: incluso una tabla bien mantenida puede ser mejor que un grafo gigante.

## Fuentes y lecturas recomendadas

- Sitio oficial de Maltego: https://www.maltego.com/
- Documentacion oficial: https://docs.maltego.com/
- Transform Hub (integraciones y transformaciones): https://www.maltego.com/transform-hub/
- Metodologias OSINT y verificacion (enfoque responsable): https://www.bellingcat.com/resources/how-tos/

Si quieres, en un proximo post puedo cubrir un flujo complementario: como usar una herramienta de automatizacion OSINT para generar semillas y luego pasar a Maltego para el analisis de enlaces.
