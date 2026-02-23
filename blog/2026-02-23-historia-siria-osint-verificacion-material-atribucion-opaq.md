---
title: "Historia OSINT: Siria (2013-2020), de la verificacion de material a la atribucion formal (OPAQ)"
slug: /historia-siria-osint-verificacion-material-atribucion-opaq
authors: [osint-writter]
tags: [osint, investigation, history, verification, geoint, opsec]
date: 2026-02-23
image: /img/blog/2026-02-23-historia-siria-osint-verificacion-material-atribucion-opaq.png
---

![Ilustracion editorial de analista OSINT verificando videos, mapas y cronologia para documentar un caso en Siria con metodologia responsable](/img/blog/2026-02-23-historia-siria-osint-verificacion-material-atribucion-opaq.png)

Cuando circulan videos de un ataque en tiempo real, el error mas caro no suele ser "no encontrar suficiente material": es **confundir volumen con prueba**. El caso de Siria (2013-2020), especialmente en torno a denuncias de uso de armas quimicas, ensena una leccion central para cualquier analista OSINT: la verificacion abierta puede fijar hechos y reducir incertidumbre, pero la **atribucion formal** exige un marco institucional, cadena metodologica y lenguaje de certeza disciplinado.

Este contenido se centra en metodologia de verificacion responsable y analisis historico. No incluye instrucciones para dano, acoso, doxxing ni fabricacion de pruebas.

<!-- truncate -->

## Que es (y para que sirve) esta leccion metodologica

Este no es un post para "resolver Siria" en una sola pieza. Es una guia de oficio sobre **como separar capas** en una investigacion compleja:

- capa 1: recopilacion y preservacion de material abierto (videos, fotos, publicaciones, mapas);
- capa 2: verificacion tecnica (tiempo, lugar, consistencia visual, metadatos cuando existen);
- capa 3: corroboracion multifuente (testimonios, informes, satelite, contexto operacional);
- capa 4: atribucion formal (cuando una autoridad competente publica conclusiones con mandato).

En OSINT profesional (periodismo, DD, ciberinteligencia defensiva, compliance), esta separacion evita dos errores frecuentes:

- presentar una hipotesis fuerte como hecho cerrado;
- despreciar hallazgos OSINT validos porque "aun no hay sentencia final".

## Caso de uso legitimo (ficticio): verificar un clip viral sin sobreactuar

Imagina que trabajas en una redaccion o en un equipo de riesgo y aparece un video viral que afirma mostrar un ataque en una localidad siria. Tu objetivo **no** es dictar culpables en una hora, sino producir una nota interna fiable:

1. Confirmar si el material es reciente o reciclado.
2. Geolocalizar el lugar con elementos visibles (calles, edificios, relieve, minaretes, cruces, naves).
3. Estimar una ventana temporal razonable (luz, sombras, secuencia de publicaciones, contexto meteorologico si aplica).
4. Comparar con otros clips/fotos del mismo evento.
5. Registrar que parte es observacion directa y que parte es inferencia.
6. Señalar si existe o no una investigacion institucional posterior (OPAQ/ONU u otras).

Ese flujo ya aporta valor real aunque la atribucion formal llegue meses o anos despues.

## Flujo recomendado (pasos) para casos complejos como Siria

## 1) Preservar primero, interpretar despues

En eventos de alto impacto, enlaces y publicaciones desaparecen rapido. Antes de debatir conclusiones:

- guarda URL original;
- registra fecha/hora de captura;
- exporta capturas con contexto (nombre de cuenta, texto, respuestas);
- conserva versiones del archivo si cambia o se re-suben copias.

La preservacion temprana reduce discusiones posteriores sobre "eso nunca estuvo publicado".

## 2) Verificar lugar y cronologia con evidencia observable

La verificacion OSINT fuerte suele apoyarse en piezas humildes pero acumulativas:

- arquitectura y patrones urbanos;
- topografia y linea de horizonte;
- daños visibles y su continuidad entre clips;
- secuencia de humo/plumas/nubes;
- audio ambiente (llamadas a oracion, sirenas, trafico, acentos; siempre como apoyo, no prueba unica).

Punto clave: si una pieza no encaja, no la fuerces. En Siria circularon muchisimos contenidos legitimos, reciclados y descontextualizados al mismo tiempo.

## 3) Cruzar fuentes sin confundir independencia

En investigaciones sirias, varias cuentas pueden publicar el mismo video en cadena. Eso **no** equivale a validacion independiente.

Trabaja una matriz simple:

- fuente original o mas temprana localizada;
- republicadores;
- medios/investigadores que verifican;
- informes tecnicos posteriores;
- conclusiones institucionales (si existen).

La pregunta correcta no es "cuantas veces se compartio", sino "cuantas confirmaciones independientes tengo y de que tipo son".

## 4) Diferenciar verificacion OSINT de atribucion formal

Esta es la leccion mas util del periodo 2013-2020.

- La verificacion OSINT puede documentar que un evento ocurrio, donde, cuando y con que consistencia visual/contextual.
- La atribucion formal requiere mandato, procedimientos y estandar de reporte institucional.

En el ecosistema OPAQ/ONU, esto se vio claramente:

- la **Fact-Finding Mission (FFM)** de la OPAQ se centra en determinar si hubo uso de armas quimicas, no en asignar autores;
- en 2015 el Consejo de Seguridad creo el **Joint Investigative Mechanism (JIM)** para identificar responsables cuando correspondia;
- tras el final del JIM, en 2018 los Estados parte de la OPAQ aprobaron que la Secretaria Tecnica dispusiera arreglos para identificar a los perpetradores en Siria en casos donde la FFM concluyera uso o probable uso;
- en 2020 el **Investigation and Identification Team (IIT)** emitio su primer informe, marcando un hito de atribucion formal dentro del marco OPAQ.

Para un analista OSINT, el aprendizaje es practico: puedes aportar evidencia robusta antes de la atribucion oficial, pero debes etiquetar correctamente el nivel de certeza.

## Mini-cronologia util (2013-2020) para no mezclar capas

## 2013: shock global y marco politico-institucional

Tras el ataque de Ghouta en agosto de 2013, el debate internacional acelero un marco diplomático y tecnico. La Resolucion 2118 del Consejo de Seguridad (27 de septiembre de 2013) se convirtio en una referencia central para la respuesta internacional y el rol de la OPAQ.

Metodologicamente, esta fase deja una leccion: cuando el volumen de material abierto es enorme, la utilidad del analista depende de construir **cronologias auditables**, no de emitir veredictos inmediatos.

## 2014-2017: verificar hechos, documentar patrones, gestionar limites de mandato

La OPAQ establecio en abril de 2014 la Fact-Finding Mission para establecer los hechos en torno a alegaciones de uso de sustancias quimicas toxicas como armas en Siria. Esa separacion de funciones es clave para leer bien los informes: una cosa es concluir "hubo uso", otra muy distinta es "quien lo hizo".

En 2015, la Resolucion 2235 creo el mecanismo conjunto ONU-OPAQ (JIM) para identificar individuos, entidades, grupos o gobiernos responsables en ciertos casos. Durante esos anos, el trabajo OSINT (periodismo, grupos de verificacion, archivo de evidencia) convivio con investigaciones institucionales y con fuertes disputas politicas.

## 2018-2020: de la verificacion a la atribucion OPAQ (IIT)

Tras la expiracion/no renovacion del JIM en 2017, quedo una laguna de atribucion que afectaba la lectura publica de muchos casos. En junio de 2018, una sesion especial de la Conferencia de los Estados Partes de la OPAQ encargo nuevos arreglos para identificar perpetradores en Siria en el marco definido por la decision adoptada.

El salto metodologico importante llega con el primer informe del IIT (publicado el 8 de abril de 2020), que atribuye ataques en Ltamenah (marzo de 2017) a la Fuerza Aerea Arabe Siria. Independientemente de debates politicos, para el oficio OSINT esto fija una distincion muy valiosa:

- evidencia abierta y verificacion tecnica pueden preparar el terreno;
- la atribucion formal requiere otra capa de procedimiento, custodia y mandato.

## Limitaciones y falsos positivos tipicos en material de conflicto

- Reciclaje de videos: material antiguo recirculado con fecha/lugar nuevos.
- Compresion y re-subidas: destruyen metadatos y degradan detalles visuales.
- Narrativas adelantadas: interpretar primero y buscar despues.
- Dependencia excesiva de una sola tecnica (solo geolocalizacion, solo audio, solo metadatos).
- Confundir "consenso en redes" con corroboracion independiente.

## Buenas practicas (OPSEC, etica y calidad analitica)

- Minimiza la exposicion de datos personales de testigos o civiles.
- Evita compartir material sensible o grafico cuando no sea necesario para el analisis.
- Documenta siempre el nivel de confianza de cada afirmacion.
- Conserva trazabilidad de capturas, hashes/archivos y URLs cuando proceda.
- Separa claramente observacion, inferencia y conclusion institucional.

## Herramientas y recursos utiles para este tipo de trabajo (sin fetichizar la herramienta)

- Verificacion multimedia: InVID/WeVerify (como apoyo a inspeccion manual).
- Archivo y preservacion: Wayback Machine + repositorios internos de evidencias.
- Cartografia/geolocalizacion: mapas, imagen satelital y comparacion visual manual.
- Gestion analitica: cronologias, tablas de corroboracion y notas de confianza.

La herramienta ayuda; el resultado lo determina la disciplina metodologica.

## Alternativas y siguientes pasos

Si quieres adaptar esta leccion a tu flujo diario de OSINT defensivo:

1. Crea una plantilla de verificacion con columnas `hecho observado / evidencia / fuente / confianza`.
2. Exige al menos dos corroboraciones independientes antes de elevar una afirmacion sensible.
3. Añade una seccion fija de "limites y dudas" en cada informe.
4. Distingue siempre entre verificacion tecnica y atribucion formal.

El siguiente paso natural en el blog seria una entrada practica sobre `ExifTool & InVID` aplicada a verificacion multimedia responsable.

## Fuentes consultadas

- OPCW, Fact-Finding Mission (Syria): https://www.opcw.org/fact-finding-mission-ffm
- UN Security Council press release sobre Resolucion 2118 (27-09-2013): https://press.un.org/en/2013/sc11135.doc.htm
- UN Security Council press release sobre Resolucion 2235 (07-08-2015): https://press.un.org/en/2015/sc12001.doc.htm
- UN Security Council press release (16-11-2017) sobre no renovacion del JIM: https://press.un.org/en/2017/sc13040.doc.htm
- OPCW, decision de la sesion especial (27-06-2018) para identificar perpetradores en Siria: https://www.opcw.org/media-centre/news/2018/06/opcw-conference-states-parties-adopts-decision-address-threat-use-chemical
- OPCW, primer informe del IIT (08-04-2020): https://www.opcw.org/media-centre/news/2020/04/opcw-investigation-and-identification-team-concludes-reasonable-grounds
- Bellingcat Online Investigation Toolkit (referencia metodologica): https://bellingcat.gitbook.io/toolkit
