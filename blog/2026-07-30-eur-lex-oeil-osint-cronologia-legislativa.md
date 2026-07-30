---
title: "EUR-Lex y OEIL en OSINT: reconstruir una ley europea sin inventar quién cambió qué"
slug: /eur-lex-oeil-osint-cronologia-legislativa
authors: [osint-writter]
tags: [osint, investigation, verification, due-diligence, methodology, data]
date: 2026-07-30
image: /img/blog/2026-07-30-eur-lex-oeil-osint-cronologia-legislativa.png
---

![Ilustración editorial de una analista OSINT comparando versiones de una propuesta europea dentro de una cronología documental](/img/blog/2026-07-30-eur-lex-oeil-osint-cronologia-legislativa.png)

Una asociación publica una propuesta técnica. Meses después, una frase muy parecida aparece en una ley europea. La captura de pantalla parece perfecta para denunciar que «Bruselas copió el texto», pero faltan casi todas las piezas importantes: qué versión se está comparando, quién presentó la enmienda, cuándo entró en el expediente, qué otras fuentes usaron la misma fórmula y cuál fue el texto finalmente aprobado. `EUR-Lex` y el Observatorio Legislativo del Parlamento Europeo (`OEIL`) permiten reconstruir esa historia documental; no convierten una semejanza verbal en prueba de autoría o influencia.

<!-- truncate -->

Este artículo propone un método responsable para periodismo, debida diligencia, investigación académica y seguimiento regulatorio. El expediente y las organizaciones del ejemplo son ficticios. El objetivo es documentar **estados, fechas, actores institucionales y cambios de redacción** sin atribuir intenciones que las fuentes no sostienen.

## Qué son EUR-Lex y OEIL

[EUR-Lex](https://eur-lex.europa.eu/homepage.html?locale=es) es el portal de acceso al Derecho de la Unión Europea. Reúne, entre otros materiales, tratados, actos jurídicos, documentos preparatorios, jurisprudencia y ediciones del Diario Oficial de la Unión Europea. Sus fichas permiten pasar del texto a metadatos, relaciones documentales y, según el tipo de acto, vistas de procedimiento, medidas nacionales de transposición o versiones consolidadas.

El [Observatorio Legislativo del Parlamento Europeo](https://oeil.europarl.europa.eu/oeil/en/find-out-more) permite seguir procedimientos legislativos y no legislativos que pasan por el Parlamento. Cada ficha de procedimiento utiliza una referencia única y reúne:

- información básica y estado del expediente;
- comisión parlamentaria competente, ponentes y otros actores;
- acontecimientos ordenados cronológicamente;
- base jurídica y tipo de procedimiento;
- documentos del Parlamento, la Comisión, el Consejo y otras instituciones;
- resúmenes factuales de los hitos principales;
- enlace al acto final publicado, cuando existe.

Las dos fuentes se complementan. `OEIL` funciona bien como **mapa del expediente**; `EUR-Lex`, como **repositorio jurídico y documental**. Ninguna sustituye la lectura de los documentos originales.

### Cuatro identificadores que evitan mezclar expedientes

Antes de descargar nada, registra los identificadores observados en la ficha:

| Identificador | Ejemplo de formato | Para qué sirve |
|---|---|---|
| Referencia del procedimiento | `AAAA/NNNN(COD)` | Seguir el expediente interinstitucional |
| Documento de la Comisión | `COM(AAAA) NNN final` | Identificar una propuesta o comunicación concreta |
| Documento del Consejo | `ST NNNNN AAAA INIT`, `REV` o `ADD` | Distinguir documento, revisión y anexo |
| CELEX | Cadena estructurada propia de EUR-Lex | Localizar y enlazar de forma persistente un documento |

Los ejemplos son formatos, no expedientes reales. Copia siempre el valor desde la fuente: un dígito, un sufijo o un año equivocado puede llevarte a otro texto. EUR-Lex explica cómo crear [enlaces permanentes mediante CELEX, ELI y otros identificadores](https://eur-lex.europa.eu/content/help/data-reuse/linking.html?locale=es).

## Caso legítimo: la enmienda ficticia sobre baterías

Imaginemos una propuesta europea para facilitar la reparación de baterías. La empresa ficticia `Acumuladores Boreal` publica el 3 de febrero una posición que pide conservar datos técnicos durante diez años. Un texto parlamentario fechado el 20 de mayo contiene una obligación aparentemente similar. En redes se afirma que Boreal «escribió la ley».

Para evaluar la afirmación habría que separar al menos estas proposiciones:

1. Boreal publicó esa redacción antes de la enmienda.
2. La aportación llegó a una institución o actor del expediente.
3. Un documento oficial incorporó una fórmula sustancialmente coincidente.
4. Puede identificarse quién presentó o negoció el cambio.
5. La propuesta de Boreal explica el cambio mejor que otras fuentes posibles.
6. La redacción sobrevivió hasta el acto adoptado y publicado.

Las fechas y versiones pueden sostener las proposiciones primera y tercera. Una lista de enmiendas quizá ayude con la cuarta. Las proposiciones segunda y quinta requieren evidencia adicional: registro de consulta, carta, reunión, acta, justificación, declaración o testimonio verificable. La sexta exige llegar al Diario Oficial. No saltes de la coincidencia textual a la causalidad.

Un resultado proporcionado podría decir:

> La posición de Boreal, fechada el 3 de febrero, precede al documento parlamentario del 20 de mayo y ambos contienen una fórmula semejante sobre conservación durante diez años. La enmienda aparece atribuida en el documento a estos miembros, pero las fuentes consultadas no demuestran que proceda de Boreal ni descartan que derive del informe técnico publicado en enero. El acto final reduce el plazo a siete años.

## Flujo recomendado

### 1. Define la afirmación y el punto final

Escribe una pregunta comprobable:

- ¿cuándo apareció por primera vez esta frase en el expediente?;
- ¿qué institución produjo cada versión?;
- ¿qué enmiendas llegaron al texto aprobado?;
- ¿qué documentos preparatorios citan la evidencia técnica?;
- ¿la norma está propuesta, acordada, adoptada, publicada o ya es aplicable?

Fija también el periodo y el tipo de procedimiento. Una propuesta, una posición de negociación, un acuerdo provisional y un reglamento publicado no son estados intercambiables.

### 2. Usa OEIL para construir el esqueleto cronológico

Busca por referencia, título o materia y abre la ficha del procedimiento. Registra:

```text
Referencia:
Título:
Tipo de procedimiento:
Estado observado:
Comisión parlamentaria y ponencia:
Fecha de consulta:
URL permanente o ficha:
```

Después recorre los acontecimientos y la pasarela documental. No empieces comparando PDF al azar: primero sitúa cada documento en su fase y en su institución. Ten en cuenta que las fichas y resúmenes de OEIL están en inglés y francés, aunque muchos documentos enlazados ofrecen otras lenguas.

La cronología de OEIL es un índice editorial actualizado, no una transcripción completa de cada negociación. Conserva el documento fuente enlazado y anota cuándo consultaste la ficha.

### 3. Baja a EUR-Lex y conserva la identidad documental

En EUR-Lex, revisa la vista de información del documento:

- título oficial y tipo de acto;
- autor e institución;
- fecha del documento y de publicación;
- referencia, CELEX y, cuando exista, ELI;
- Diario Oficial, serie y número;
- documentos relacionados y actos que modifica o que lo modifican;
- lenguas y formatos disponibles.

Guarda el PDF o HTML junto con un pequeño registro:

```text
Fuente: EUR-Lex
Identificador:
Versión o estado:
Fecha del documento:
Fecha de descarga:
URL:
SHA-256 del fichero:
```

No uses el nombre descargado como único identificador. Dos archivos llamados `proposal_es.pdf` pueden corresponder a fases distintas.

### 4. Completa el carril del Consejo

El [registro público del Consejo](https://www.consilium.europa.eu/es/documents/public-register/) contiene documentos legislativos preparatorios y documentación de reuniones desde 1999. Los documentos vinculados a una propuesta comparten un código de expediente interinstitucional, útil para recuperar el conjunto sin depender de palabras clave.

Clasifica por separado:

- propuesta recibida;
- documentos de grupos de trabajo;
- compromisos de la Presidencia;
- orientación general o mandato negociador;
- revisiones (`REV`) y adiciones (`ADD`);
- resultados de reuniones y votaciones.

Que una referencia aparezca en el registro no garantiza que el contenido esté inmediatamente disponible. Algunos documentos requieren una solicitud de acceso y pueden publicarse total o parcialmente. Registra la ausencia; no reconstruyas el texto perdido mediante rumores o versiones de terceros.

### 5. Separa los carriles institucionales

Una tabla sencilla evita fabricar una única «versión de Bruselas»:

| Fecha | Carril | Documento | Estado | Qué permite afirmar |
|---|---|---|---|---|
| 03-02 | Actor externo | Posición de Boreal | Publicada | Qué pidió públicamente |
| 15-03 | Comisión | Propuesta | Presentada | Punto de partida formal |
| 20-05 | Parlamento | Enmiendas de comisión | Presentadas | Cambios propuestos y autoría formal visible |
| 18-06 | Consejo | Compromiso de Presidencia | Borrador | Estado de negociación documentado |
| 12-09 | Interinstitucional | Acuerdo provisional | Pendiente de aprobación | Compromiso político, aún no acto final |
| 30-11 | Diario Oficial | Reglamento | Publicado | Texto adoptado y publicación oficial |

En el procedimiento legislativo ordinario, Parlamento y Consejo actúan como colegisladores. Los trílogos pueden acercar posiciones, pero un acuerdo informal debe ser aprobado formalmente por las instituciones. La [explicación oficial del Consejo](https://www.consilium.europa.eu/es/council-eu/decision-making/ordinary-legislative-procedure/) ayuda a no confundir negociación con adopción.

### 6. Compara texto, no maquetación

Descarga versiones en la misma lengua cuando sea posible. Conserva los originales y trabaja sobre copias:

```bash
pdftotext -layout propuesta.pdf propuesta.txt
pdftotext -layout posicion-parlamento.pdf parlamento.txt
diff -u propuesta.txt parlamento.txt > cambios.diff
```

La extracción automática puede romper columnas, notas, guiones y numeración. Verifica cada cambio importante contra el PDF o HTML oficial. Para artículos complejos resulta más fiable construir una matriz:

| Unidad | Comisión | Parlamento | Consejo | Texto final | Nota |
|---|---|---|---|---|---|
| Art. 8.2 | 10 años | 10 años | 5 años | 7 años | Cambia plazo |
| Art. 8.3 | No existe | Nueva excepción | Excepción distinta | Suprimido | No llega al acto |

Compara unidades jurídicas completas —considerando, artículo, apartado, anexo— y no frases aisladas. Una traducción puede variar sin que cambie el efecto normativo; ante una duda sustantiva, revisa más de una versión lingüística y la formulación aprobada.

### 7. Busca la vía plausible de transmisión

Una coincidencia gana valor cuando aparece acompañada de:

- contribución publicada en una consulta;
- carta o documento entregado con fecha verificable;
- enmienda que identifica proponente;
- acta o agenda que sitúa a los actores;
- informe que cita expresamente la fuente;
- secuencia de borradores que conserva una formulación distintiva.

También debes buscar explicaciones alternativas: estándares técnicos, legislación previa, documentos de otra jurisdicción, informes científicos o aportaciones coincidentes. Las fórmulas jurídicas comunes tienen poco poder atributivo.

### 8. Llega al Diario Oficial y comprueba aplicabilidad

El punto final no es «se alcanzó un acuerdo». Comprueba el acto publicado en el Diario Oficial, su fecha de entrada en vigor y, si procede, fechas de aplicación escalonadas. Solo los actos publicados oficialmente son vinculantes en los términos que correspondan.

EUR-Lex ofrece textos consolidados que integran el acto inicial con modificaciones y correcciones para mostrar las reglas aplicables en una fecha. Son muy útiles para orientarse y comparar estados, pero [los textos consolidados no tienen efecto jurídico propio](https://eur-lex.europa.eu/collection/eu-law/consleg.html?locale=es). Para una cita jurídica sensible, vuelve al acto publicado y a sus modificaciones.

## Limitaciones y falsos positivos

### Una fecha visible puede no ser la fecha de circulación

Fecha del documento, registro, publicación, votación y aplicación responden a hechos distintos. Un PDF subido hoy puede reproducir un texto acordado antes. Conserva todas las fechas con su etiqueta.

### El estado del procedimiento puede tener latencia

OEIL se actualiza de forma continuada, pero ninguna ficha elimina el desfase entre un acontecimiento y su registro. Escribe «la ficha consultada el día X muestra…», especialmente en expedientes abiertos.

### `INIT`, `REV`, `ADD` y `COR` no son adornos

Una revisión puede sustituir contenido; una adición puede contener un anexo esencial; una corrección puede afectar solo a metadatos o a texto sustantivo. No ordenes versiones únicamente por el número principal.

### Consolidación no equivale a texto original

El consolidado facilita leer el estado de una norma en una fecha, pero mezcla el acto base con cambios posteriores y no es el documento jurídicamente vinculante. Tampoco aparecerá un consolidado si el acto nunca fue modificado o corregido.

### Ausencia de documento no demuestra negociación secreta

Puede haber retrasos, excepciones de acceso, documentos no producidos, referencias distintas o búsquedas mal formuladas. Describe repositorios, identificadores, lenguas y fechas consultadas antes de concluir que falta transparencia.

### Similitud no equivale a autoría

Dos textos pueden compartir vocabulario porque resuelven el mismo problema técnico, copian una norma anterior o siguen una plantilla. Atribuir autoría exige una vía de transmisión y evidencia adicional. La proximidad temporal solo establece orden.

## Buenas prácticas de OPSEC, ética y privacidad

- Investiga expedientes, organizaciones y cargos con función pública relevante; no acumules datos personales de personal técnico sin necesidad.
- Separa autoría formal de una enmienda, participación en una reunión e influencia causal.
- Conserva originales, hashes, notas de extracción y reglas de normalización.
- Enlaza documentos permanentes y registra la fecha de consulta de las fichas dinámicas.
- No presentes una solicitud de acceso como acusación ni publiques datos personales incidentales obtenidos en anexos.
- Ofrece derecho de respuesta cuando una conclusión pueda afectar a una organización o persona.
- Expresa incertidumbre con precisión: «no localizado», «precede», «coincide», «es consistente con» y «no permite atribuir».

Este método ayuda a investigar, pero no sustituye asesoramiento jurídico. Si la conclusión depende de vigencia, interpretación o efectos legales, contrástala con una persona cualificada y con la versión oficial aplicable.

## Checklist antes de publicar

- [ ] El expediente está identificado con una referencia copiada de la fuente.
- [ ] Cada documento conserva institución, estado, fecha, identificador y URL.
- [ ] Las versiones comparadas pertenecen al mismo expediente y unidad jurídica.
- [ ] Los cambios automáticos se verificaron contra el original.
- [ ] Propuesta, posición, acuerdo, adopción, publicación y aplicación están separados.
- [ ] Se buscaron explicaciones alternativas para las coincidencias textuales.
- [ ] La conclusión no atribuye autoría o influencia sin una vía de transmisión.
- [ ] El texto final se comprobó en el Diario Oficial.

## Alternativas y siguientes pasos

Amplía el expediente con:

- [Have Your Say](https://commission.europa.eu/law/law-making-process/planning-and-proposing-law_es), para convocatorias, consultas, propuestas y evaluaciones de impacto;
- el registro documental del Consejo, para documentos preparatorios y de reuniones;
- webs de comisiones y plenos del Parlamento, para enmiendas, informes y votaciones;
- `IPEX`, para actividad de parlamentos nacionales;
- registros de transparencia y agendas institucionales, sin confundir reunión con resultado;
- archivos web, cuando necesites demostrar cómo se presentó públicamente una posición en una fecha.

La regla práctica es: **OEIL para orientarte, identificadores para no mezclar, documentos originales para demostrar y Diario Oficial para cerrar**. Si todavía no puedes decir qué versión, qué institución y qué fecha sostienen una frase, aún no tienes una cronología: tienes una impresión.

El siguiente paso natural sería aplicar esta matriz a un expediente europeo ya cerrado y publicar, junto al análisis, un paquete reproducible de identificadores, hashes y diferencias verificadas.
