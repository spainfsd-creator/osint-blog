---
title: "RiskIQ PassiveTotal en OSINT: passive DNS, WHOIS y TLS para correlacionar infraestructura con contexto"
slug: /riskiq-passivetotal-osint-passive-dns-whois-tls-contexto
authors: [osint-writter]
tags: [osint, infrastructure, dns, investigation, tooling, verification]
date: 2026-05-03
image: /img/blog/2026-05-03-riskiq-passivetotal-osint-passive-dns-whois-tls-contexto.png
---

![Ilustracion editorial de una analista OSINT correlacionando passive DNS, WHOIS, certificados TLS y relaciones de infraestructura publica en varias pantallas](/img/blog/2026-05-03-riskiq-passivetotal-osint-passive-dns-whois-tls-contexto.png)

Cuando una investigacion tecnica se atasca, suele pasar por lo mismo: tienes un dominio, una IP o un host, pero te faltan puentes. Sabes que algo esta relacionado, pero no puedes explicarlo todavia con trazabilidad suficiente. `RiskIQ PassiveTotal`, hoy integrado en la experiencia de `Microsoft Defender Threat Intelligence`, resulta util justo en ese hueco: **no porque "resuelva" una atribucion, sino porque te deja enlazar tiempos, resoluciones, WHOIS, certificados y artefactos web para decidir que merece verificacion adicional**.

El matiz importa aun mas en 2026. La documentacion oficial de Microsoft indica que `Defender TI` se retirara como experiencia independiente el `1 de agosto de 2026` para quedar absorbido dentro de `Microsoft Defender`. Traducido al lenguaje de analista: el nombre comercial cambia, pero el valor OSINT sigue siendo el mismo si tu pregunta es sensata y tu metodo tambien. Lo que interesa no es la marca, sino la capacidad de **pivotar con criterio sobre infraestructura publica**.

<!-- truncate -->

## Que es y para que sirve

En su forma historica, `PassiveTotal` se hizo conocido por reunir varias piezas que los analistas solian consultar por separado: `passive DNS`, `WHOIS`, certificados `TLS/SSL`, subdominios, resoluciones y relacion entre artefactos tecnicos. La documentacion actual de `Microsoft Defender Threat Intelligence` conserva esa idea central y explica que la plataforma agrega conjuntos de datos de internet para apoyar analisis de infraestructura, triage, hunting e investigacion.

Segun `Microsoft Learn`, entre los datasets soportados estan:

- `Resolutions`
- `WHOIS`
- `SSL certificates`
- `Subdomains`
- `DNS`
- `Reverse DNS`
- `Detonation analysis`
- datasets derivados del `DOM`, como `trackers`, `components`, `host pairs` y `cookies`

Eso convierte a `PassiveTotal` en una buena respuesta para preguntas como estas:

- que otros hosts han resuelto historicamente hacia una IP concreta;
- que infraestructura comparte un certificado visto en varios activos;
- que subdominios o relaciones DNS merecen revisarse manualmente;
- y si una huella web concreta apunta a reutilizacion tecnica o solo a un proveedor compartido.

## Caso de uso legitimo: due diligence tecnica sobre un proveedor

Imagina un caso ficticio. Una empresa va a integrar a un proveedor externo para alojar formularios, paneles y micrositios. Antes de firmar, el equipo de seguridad quiere entender **que infraestructura publica esta asociada realmente al proveedor y que partes parecen simplemente herencia de terceros o servicios comunes**.

Ese es un uso OSINT legitimo para `PassiveTotal`:

1. partir de un dominio principal confirmado;
2. revisar resoluciones historicas y subdominios observados;
3. pivotar a certificados `TLS` para ver reuso entre hosts;
4. abrir `WHOIS` y fechas con cautela, sabiendo que puede haber privacidad o datos obsoletos;
5. y cerrar con una nota clara sobre que es hallazgo, que es inferencia y que sigue pendiente.

El objetivo no es "descubrirlo todo". Es reducir ambiguedad antes de tomar una decision tecnica o escalar un riesgo.

## Flujo recomendado

### 1. Empezar por un artefacto estable

Si puedes elegir, mejor empezar por un dominio o `host` ya confirmado que por una IP suelta. La propia documentacion de `Defender TI` organiza buena parte del trabajo alrededor de artefactos como `hosts`, `domains` e `IPs`, y eso ayuda a no mezclar demasiado pronto hosting compartido, CDN o rotaciones temporales.

En esta fase la pregunta correcta no es "que mas hay". Es "que otras piezas publicas aparecen conectadas a este indicador y desde cuando".

### 2. Leer `passive DNS` y resoluciones como cronologia, no como propiedad

El valor de `passive DNS` no esta solo en listar nombres. Esta en ordenar observaciones en el tiempo. Fechas como `first seen` y `last seen` sirven para distinguir entre una relacion vigente, una relacion historica o una coincidencia ya caducada.

Ese detalle evita muchos errores:

- un subdominio visto hace meses no implica que siga activo hoy;
- una IP compartida no demuestra propiedad exclusiva;
- y una resolucion breve puede ser una prueba tecnica o una migracion, no una infraestructura estable.

### 3. Usar `WHOIS` para contexto, no como verdad final

La documentacion oficial de datasets recuerda algo importante: muchos actores usan servicios de privacidad y, en esos casos, `WHOIS` deja de ser una fuente fuerte para enlazar dominios por contacto directo. Aun asi, sigue aportando mucho contexto operativo:

- fechas de creacion, actualizacion y expiracion;
- registrador;
- estados del dominio;
- y, cuando existe, organizacion o correos asociados.

La lectura responsable aqui es sencilla: `WHOIS` suma pistas, pero rara vez cierra el caso por si solo.

### 4. Pivotar por certificados `TLS` para encontrar relaciones menos obvias

Uno de los puntos mas utiles de la documentacion de `Defender TI` es que explica por que los certificados valen mas de lo que parece. Microsoft mantiene un repositorio historico de asociaciones entre certificados e infraestructura observada, y eso permite responder preguntas como:

- en que otros hosts o IPs se ha visto este certificado;
- si el certificado es `self-signed`;
- que `Subject Alternative Names` incluye;
- y que relaciones sobreviven aunque un actor mueva contenido de un servidor a otro.

Para OSINT defensivo, esta es una idea potente: **el certificado puede unir piezas que ni `passive DNS` ni `WHOIS` conectan con claridad**.

### 5. Tratar reputacion e `analyst insights` como triage

La experiencia moderna de `Defender TI` anade `reputation scoring` e `analyst insights`. Microsoft explica que la reputacion puntua hosts, dominios e IPs entre `0` y `100`, y que esa puntuacion se apoya en reglas y asociaciones detectadas por su infraestructura.

Eso es util para priorizar, pero no para dictar sentencia. En una investigacion seria, una etiqueta de `suspicious` o `malicious` sirve para decidir por donde mirar primero, no para redactar una conclusion automatica sin contraste.

### 6. Documentar el caso en `Projects`

Otra pieza util de la plataforma son los `Projects`, pensados para organizar `IOCs`, artefactos y colaboracion entre analistas. Para un flujo OSINT responsable, esto encaja muy bien con una disciplina sencilla:

- guardar el indicador de partida;
- anotar por que hiciste cada pivote;
- exportar resultados relevantes;
- y dejar claro que evidencia era directa y cual era contexto.

Cuando una investigacion crece, esa trazabilidad vale mas que cualquier captura espectacular.

## Limitaciones y falsos positivos

`PassiveTotal` es potente, pero castiga al analista que sobrerreacciona:

- `CDN`, proveedores cloud y hosting compartido pueden crear relaciones tecnicas sin valor atributivo.
- Un certificado reutilizado puede apuntar a continuidad operativa, pero tambien a clonado legitimo o infraestructura comun.
- `WHOIS` privado, redacciones y datos viejos reducen mucho la fuerza de algunos pivotes.
- Los datasets web derivados del `DOM` (`trackers`, `components`, `cookies`, `host pairs`) son utiles para contexto, pero no prueban por si solos control o intencion.
- Y, a fecha de `3 de mayo de 2026`, el producto esta en transicion hacia `Microsoft Defender`, asi que conviene describir bien la funcion analitica y no depender solo del nombre comercial.

## Buenas practicas de OPSEC, etica y privacidad

- Trabaja solo sobre fines legitimos: defensa, verificacion, due diligence o investigacion autorizada.
- Minimiza datos personales si el caso es de infraestructura y no de individuos.
- Separa siempre observacion, inferencia y conclusion.
- Guarda fechas de consulta y exportaciones para poder reproducir el analisis.
- Si una relacion tecnica puede explicarse por un tercero compartido, redacta esa incertidumbre en vez de esconderla.

## Alternativas y siguientes pasos

Si lo que necesitas es mas contexto historico de DNS, `SecurityTrails` sigue siendo un buen complemento. Si tu prioridad es busqueda de infraestructura por banners y servicios, `Censys`, `Netlas`, `FOFA` o `ZoomEye` encajan mejor segun cobertura y presupuesto. Y si quieres validar una relacion web concreta, `urlscan.io`, `CT logs` y `RDAP/WHOIS` continuan siendo pivotes muy utiles.

`PassiveTotal` destaca cuando la pregunta principal mezcla **tiempo, infraestructura y relacion entre artefactos**, no solo busqueda puntual.

## Fuentes recomendadas

- `Microsoft Learn`, What is Microsoft Defender Threat Intelligence?: https://learn.microsoft.com/en-us/defender/threat-intelligence/what-is-microsoft-defender-threat-intelligence-defender-ti
- `Microsoft Learn`, Defender TI data sets: https://learn.microsoft.com/en-us/defender/threat-intelligence/data-sets
- `Microsoft Learn`, Using Projects in Defender TI: https://learn.microsoft.com/en-us/defender/threat-intelligence/using-projects
- `Microsoft Learn`, Defender TI reputation scoring: https://learn.microsoft.com/en-us/defender/threat-intelligence/reputation-scoring
- `Microsoft Learn`, Quickstart and retirement notice for Defender TI: https://learn.microsoft.com/en-us/defender/threat-intelligence/learn-how-to-access-microsoft-defender-threat-intelligence-and-make-customizations-in-your-portal
- `Microsoft Learn`, RiskIQ Illuminate connector reference: https://learn.microsoft.com/en-us/connectors/riskiqpassivetotal/

Takeaway final: `RiskIQ PassiveTotal` no vale por darte "mas datos". Vale por ayudarte a **ordenar relaciones publicas de infraestructura sin perder el contexto temporal ni el sentido comun**. Si quieres seguir por esta linea, el siguiente puente natural seria un post practico sobre como combinar `Passive DNS`, `CT logs` y `urlscan.io` para revisar superficie web externa sin confundir coincidencia tecnica con propiedad real.
