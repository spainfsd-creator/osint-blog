---
title: "Historia OSINT: Skripal (2018) y la disciplina de identificar coberturas sin romper la metodologia"
slug: /historia-skripal-osint-identidades-triangulacion
authors: [osint-writter]
tags: [osint, investigation, history, verification, tradecraft, geoint]
date: 2026-02-17
image: /img/blog/2026-02-17-historia-skripal-osint-identidades-triangulacion.png
---

![Mesa de investigacion OSINT con cronologia, mapas y documentos anonimizados](/img/blog/2026-02-17-historia-skripal-osint-identidades-triangulacion.png)

En marzo de 2018, el caso Skripal convirtio Salisbury en un punto de choque entre rumor, propaganda y evidencia publica. Lo dificil no era "encontrar algo" en internet: lo dificil era **demostrar que cada pieza resistia verificacion cruzada** y que una identidad atribuida no era una coincidencia conveniente.

Esta historia no va de vigilancias personales ni de "cazar" individuos. Va de oficio OSINT responsable: como pasar de pistas sueltas a una hipotesis robusta usando solo fuentes abiertas, trazabilidad documental y control de sesgos.

<!-- truncate -->

## Que es (y para que sirve) esta leccion del caso Skripal

El valor OSINT del caso esta en la metodologia, no en el morbo del incidente:

- **Triangulacion de identidad**: unir datos de viaje, registros, imagenes y documentos filtrados/publicos sin depender de una unica fuente.
- **Cronologia auditable**: fijar fechas y horas con evidencia verificable.
- **Corroboracion institucional**: contrastar hallazgos abiertos con comunicados oficiales, informes tecnicos y procesos judiciales/publicos.

Si trabajas en ciberinteligencia, due diligence o verificacion periodistica, este enfoque te sirve para reducir errores de atribucion.

## Caso de uso legitimo (ficticio)

Imagina una investigacion corporativa sobre una red de proveedores pantalla que usa identidades de cobertura para firmar contratos en varios paises.

Flujo inspirado en las lecciones de Skripal:

1. Construyes una cronologia de movimientos con datos abiertos de viajes, registros mercantiles y apariciones publicas.
2. Buscas incoherencias entre identidad declarada y huella documental historica.
3. Exiges doble confirmacion por cada afirmacion critica (documento + fuente independiente).
4. Etiquetas cada dato por nivel de confianza antes de presentarlo a legal/compliance.

El resultado no es "senalar culpables" en redes, sino un informe verificable para toma de decisiones.

## Flujo recomendado (pasos)

### 1. Delimita el alcance y el lenguaje de hipotesis

- Formula hipotesis en condicional: "podria corresponder", "pendiente de corroboracion".
- Separa hechos observados de inferencias.

### 2. Congela una cronologia minima

- Ancla eventos en fechas absolutas (por ejemplo, 4 de marzo de 2018 para el envenenamiento en Salisbury).
- Evita mezclar versiones preliminares con confirmaciones posteriores sin marcar revision.

### 3. Triangula identidades de cobertura

- Compara alias, documentos, patrones de viaje y presencia en distintas bases abiertas.
- No cierres una atribucion por un unico "match"; exige convergencia de senales.

### 4. Corrobora con fuentes tecnicas y oficiales

- Informes forenses/quimicos (cuando existen).
- Comunicados judiciales/policiales con nombres, fechas y cargos.
- Investigacion OSINT independiente para validar o refutar.

### 5. Publica con trazabilidad

- Cada afirmacion relevante debe poder remontarse a una fuente concreta.
- Declara incertidumbres y huecos, en vez de rellenarlos con narrativa.

## Limitaciones y falsos positivos

- **Sesgo de confirmacion**: cuando una teoria "encaja", tendemos a ignorar datos en contra.
- **Reutilizacion de identidad**: perfiles, fotos o registros pueden estar alterados o reciclados.
- **Ruido informativo**: en casos politicamente cargados hay desinformacion deliberada.
- **Deriva temporal**: versiones iniciales pueden quedar obsoletas tras informes oficiales posteriores.

## Buenas practicas (OPSEC, etica, privacidad)

- Trabaja solo con fuentes publicas y legalmente accesibles.
- No publiques datos personales irrelevantes para el interes publico del caso.
- Evita convertir OSINT en acoso digital o doxxing.
- Mantiene un registro de decisiones analiticas: por que descartaste o aceptaste una evidencia.
- Si el riesgo de dano reputacional es alto, aplica umbrales mas estrictos de corroboracion.

## Alternativas y siguientes pasos

Si no dispones de un caso historico de alto perfil, puedes practicar el mismo metodo con escenarios defensivos:

- Auditoria de suplantacion de marca (identidades de dominio y perfiles falsos).
- Verificacion de proveedores internacionales antes de firmar contratos.
- Reconciliacion de cronologias en incidentes de seguridad con evidencia publica.

Siguiente tema recomendado para continuar la serie: **Navalny (2020)**, centrado en patrones de viaje y validacion tecnica multi-fuente.

## Fuentes consultadas

- UK Government, The Dawn Sturgess Inquiry report (2025): https://www.dawnsturgessindependentinquiry.org.uk/report
- Crown Prosecution Service (CPS), charges announcement (5 September 2018): https://www.cps.gov.uk/cps/news/cps-announces-charges-over-nerve-agent-attack-salisbury
- OPCW, report on the Salisbury incident (September 2018): https://www.opcw.org/media-centre/news/2018/09/opcw-report-salisbury-incident
- Bellingcat, identifying "Ruslan Boshirov" as Anatoliy Chepiga (26 September 2018): https://www.bellingcat.com/news/uk-and-europe/2018/09/26/second-salisbury-suspect-colonel-anatoliy-chepiga/
- Bellingcat, identifying "Alexander Petrov" as Alexander Mishkin (8 October 2018): https://www.bellingcat.com/news/uk-and-europe/2018/10/08/identify-salisbury-suspect-petrov-russian-military-doctor/
- Counter Terrorism Policing, update on the Salisbury investigation (5 September 2018): https://www.counterterrorism.police.uk/salisbury-investigation-officers-reveal-key-evidence/
