---
title: "Historia OSINT: Rohingya (2017), satelite antes/despues para documentar destruccion con cautela metodologica"
slug: /historia-rohingya-osint-satelite-antes-despues-documentar-destruccion
authors: [osint-writter]
tags: [osint, investigation, history, geoint, verification, opsec]
date: 2026-02-27
image: /img/blog/2026-02-27-historia-rohingya-osint-satelite-antes-despues-documentar-destruccion.png
---

![Ilustracion editorial de analista OSINT comparando imagenes satelitales antes y despues para verificar destruccion de aldeas con metodologia responsable](/img/blog/2026-02-27-historia-rohingya-osint-satelite-antes-despues-documentar-destruccion.png)

En agosto de 2017, mientras miles de personas huian de Rakhine hacia Bangladesh, una parte clave de la verdad no llego primero por ruedas de prensa ni por notas oficiales: llego por **comparativas satelitales antes/despues**. En este caso, la leccion OSINT no es "mirar un mapa bonito", sino construir evidencia verificable cuando hay acceso fisico limitado, propaganda cruzada y riesgo de borrar huellas.

Este contenido esta orientado a usos legitimos (periodismo, investigacion academica, derechos humanos, verificacion de riesgos y analisis defensivo). No incluye tacticas para dano, acoso ni vigilancia abusiva.

<!-- truncate -->

## Que es (y para que sirve) esta leccion OSINT

La historia Rohingya de 2017 se convirtio en un ejemplo duro de GEOINT aplicado a derechos humanos: contrastar imagenes de alta resolucion de un mismo punto en fechas distintas para responder preguntas concretas:

- que habia antes;
- que hay despues;
- que patrones de dano se repiten;
- y que parte se puede afirmar con alta confianza.

Organizaciones como Human Rights Watch y Amnesty International publicaron analisis satelitales que mostraban destruccion extensa de aldeas Rohingya en Rakhine. Paralelamente, la crisis humanitaria escalo de forma rapida: segun UNHCR, desde agosto de 2017 huyeron mas de 750.000 Rohingya a Bangladesh.

## Mini-relato con metodo: cuando el terreno no es accesible

Imagina que eres parte de un equipo de verificacion y no puedes entrar en la zona. Tienes testimonios de incendios y desplazamientos, pero necesitas una base comprobable para no amplificar rumores.

La secuencia metodologica fue esta:

1. fijar una linea temporal minima (fecha del evento reportado y ventanas de captura de imagen);
2. conseguir imagen previa y posterior del mismo lugar;
3. delimitar zonas de dano (edificaciones, vegetacion, huellas de fuego);
4. contrastar con testimonios y otras capas (cronologia, comunicados, contexto local);
5. documentar incertidumbre: que se sabe, que se infiere, que no se puede confirmar.

Este orden parece obvio, pero evita un error muy comun: convertir una imagen impactante en una conclusion total sin trazabilidad.

## Caso de uso legitimo (ficticio)

Un equipo de una ONG debe redactar una nota tecnica en 48 horas para donantes. Objetivo: estimar si hay evidencia consistente de destruccion sistematica en una zona concreta, sin sobreafirmar.

Flujo recomendado:

- elegir 3-5 aldeas con reportes independientes;
- comparar imagenes antes/despues con misma escala y orientacion;
- clasificar hallazgos por confianza (alta/media/baja);
- incluir contraejemplos (areas no afectadas) para evitar sesgo de seleccion;
- publicar una conclusion acotada y auditable.

Resultado esperado: una evaluacion util para decision humanitaria, no una sentencia penal.

## Flujo OSINT recomendado para analistas

### 1) Define la pregunta verificable

Evita preguntas gigantes ("quien tiene toda la culpa") y formula preguntas observables:

- "Se detecta dano estructural compatible con incendio entre X y Y fecha?"
- "El dano es puntual o repetido en varias localizaciones?"

### 2) Congela evidencia y metadatos

Guarda para cada imagen: proveedor, fecha/hora, resolucion, coordenadas, nivel de nubosidad y notas de calidad. Sin metadatos, no hay auditoria seria.

### 3) Corrobora por multifuente

Cruza satelite con testimonios, informes tecnicos y datos humanitarios. En el caso Rohingya, esta triangulacion fue clave para sostener el relato publico bajo escrutinio.

### 4) Redacta con niveles de certeza

Separa explicitamente:

- hechos observados;
- inferencias razonables;
- vacios de informacion.

Esta separacion protege tu trabajo frente a propaganda y reduce el riesgo de error narrativo.

## Limitaciones y falsos positivos

- **Nubosidad y resolucion**: pueden ocultar o distorsionar detalles.
- **Ambiguedad causal**: ver dano no siempre permite atribuir autoria sin mas evidencia.
- **Sesgo temporal**: una captura fuera de ventana puede llevar a conclusiones equivocadas.
- **Riesgo de sobrelectura**: patrones visuales no sustituyen investigacion de campo cuando esta disponible.

## Buenas practicas (OPSEC, etica y privacidad)

- minimiza datos personales en informes publicos;
- evita publicar coordenadas sensibles que puedan aumentar riesgos a poblacion civil;
- conserva cadena de custodia de archivos y notas;
- usa lenguaje prudente cuando la atribucion no esta cerrada;
- recuerda que OSINT responsable busca verdad verificable, no "ganar" una narrativa.

## Alternativas y siguientes pasos

Si trabajas casos similares, combina este enfoque con:

- analisis de video/fotografia verificada (forense multimedia);
- cronologias de eventos con fuentes institucionales;
- monitoreo de reconstruccion del terreno para detectar posible borrado de evidencias.

Takeaway: el valor del OSINT en crisis humanitarias esta en **hacer comprobable lo discutible**. En Rohingya (2017), el satelite antes/despues no resolvio todo, pero si ayudo a fijar hechos observables cuando mas hacia falta rigor.

## Fuentes recomendadas

- Human Rights Watch (19 Sep 2017): https://www.hrw.org/news/2017/09/19/burma-satellite-imagery-shows-mass-destruction
- Human Rights Watch (17 Oct 2017): https://www.hrw.org/news/2017/10/17/burma-new-satellite-images-confirm-mass-destruction
- Amnesty International (12 Mar 2018): https://www.amnesty.org/en/latest/news/2018/03/myanmar-military-land-grab-as-security-forces-build-bases-on-torched-rohingya-villages/
- UNHCR Rohingya Emergency (actualizado): https://www.unhcr.org/en-us/rohingya-emergency.html
- UN Human Rights Council A/HRC/39/64 (Sep 2018): https://www.right-docs.org/doc/a-hrc-39-64/
