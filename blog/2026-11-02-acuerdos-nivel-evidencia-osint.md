---
title: "Acuerdos de nivel de evidencia en OSINT: decidir antes de que llegue la presión"
slug: /acuerdos-nivel-evidencia-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, investigation, privacy]
date: 2026-11-02
image: /img/blog/2026-11-02-acuerdos-nivel-evidencia-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una captura de una web corporativa parece confirmar un cambio de administrador. El dato encaja con un agregador, circula por dos redes sociales y el informe debe salir en una hora. Solo hay un problema: **nadie acordó qué evidencia bastaba para afirmar el cambio, cuánto podía envejecer ni qué hacer si el registro oficial todavía no lo reflejaba**. Bajo presión, el umbral deja de ser una regla y se convierte en una negociación con el resultado ya sobre la mesa.

![Analista comparando procedencia, frescura y umbrales de evidencia en una investigación OSINT](/img/blog/2026-11-02-acuerdos-nivel-evidencia-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un patrón de trabajo: el **acuerdo de nivel de evidencia** (ANE). No es un estándar reconocido ni una fórmula universal. Es un contrato operativo, escrito antes de investigar, que vincula cada tipo de decisión con la procedencia, frescura, independencia, integridad y revisión mínimas que necesita. La inspiración de nombre procede de los objetivos de nivel de servicio de la ingeniería de fiabilidad, pero aquí el objeto no es la disponibilidad de un sistema: es la suficiencia de un expediente para una decisión concreta.

## Qué es y para qué sirve

Un ANE responde de antemano a seis preguntas:

1. **¿Qué afirmación exacta se quiere sostener?** No «la empresa ha cambiado», sino «el registro consultado muestra a la persona ficticia B como administradora a fecha T».
2. **¿Para qué decisión se usará?** Una pista de triage, una nota interna y una publicación requieren umbrales distintos.
3. **¿Qué procedencia mínima se acepta?** Fuente primaria, copia verificable, transformación documentada y responsable de cada paso.
4. **¿Qué frescura necesita?** Una matrícula mercantil, una ruta de red y una imagen histórica envejecen a velocidades diferentes.
5. **¿Qué corroboración o revisión exige?** Dos páginas que replican la misma base no son dos fuentes independientes.
6. **¿Qué ocurre si falta una condición?** El resultado debe poder ser `inconcluso`, `solo pista` o `requiere revisión`, no pasar automáticamente a verdadero o falso.

W3C PROV ofrece un vocabulario útil para describir entidades, actividades, agentes y derivaciones. Su valor práctico es obligarnos a registrar de qué artefacto procede otro y quién o qué proceso intervino. NIST, desde la preservación de evidencia digital, insiste en documentar el origen y proteger la integridad de objetos fáciles de modificar. Ninguno de esos marcos decide por nosotros si una afirmación es cierta: hacen visible el camino que permite evaluarla.

## Caso de uso legítimo: verificar un cambio societario ficticio

Imaginemos una due diligence autorizada sobre **Litoral Ejemplo, S. L.**, nombre inventado. El equipo necesita saber si consta un cambio de administrador antes de actualizar una ficha interna. No busca domicilios personales, familiares ni perfiles privados; el alcance se limita al hecho societario pertinente.

Antes de consultar fuentes, define tres niveles:

| Uso permitido | Evidencia mínima | Frescura | Salida si no cumple |
| --- | --- | --- | --- |
| abrir una pista | índice público con URL y fecha de consulta | 30 días | descartar o volver a consultar |
| actualizar la ficha interna | documento o asiento oficial identificable, copia preservada y contraste con una segunda vista | 7 días | mantener dato anterior y marcar revisión |
| publicar una afirmación | fuente oficial vigente, contexto de fecha y jurisdicción, revisión independiente y contradicciones resueltas o expuestas | 24 horas | no publicar como hecho |

La tabla no afirma que «dos fuentes siempre bastan». Define qué función cumple cada una. Un agregador puede servir para descubrir el expediente; no sustituye al registro en una afirmación pública. Una copia archivada demuestra qué se observó en un momento, pero no necesariamente el estado vigente. Y un hash prueba que el archivo conservado no ha cambiado desde que se calculó; no certifica que su contenido sea verdadero.

## Flujo recomendado

### 1. Escribe la decisión antes de buscar

Formula una proposición que pueda refutarse y añade el uso previsto. Separa hechos observados de inferencias:

```text
Observación: el documento R, consultado a T, identifica a B en el cargo C.
Inferencia: B ejercía efectivamente ese cargo durante el periodo P.
Decisión: actualizar una ficha interna, sin publicación automática.
```

La inferencia suele necesitar más contexto que la observación. Si ambas comparten umbral, el equipo tenderá a convertir una lectura puntual en una conclusión más amplia.

### 2. Define dimensiones observables

Evita adjetivos como «fuente buena» o «dato fiable» sin criterio. Usa campos comprobables:

- **procedencia:** URL, organismo o editor, fecha, versión y relación con el original;
- **integridad:** archivo preservado, hash, firma o mecanismo equivalente cuando proceda;
- **frescura:** hora de observación y ventana máxima compatible con la decisión;
- **independencia:** origen de los datos, no solo dominio o interfaz distintos;
- **cobertura:** qué parte de la afirmación observa realmente la fuente;
- **reproducibilidad:** consulta, parámetros y transformaciones suficientes para repetir el recorrido;
- **revisión:** quién puede aprobar, impugnar o ampliar el alcance.

El modelo C2PA ilustra bien una cautela: una credencial puede aportar procedencia y señales resistentes a manipulación, pero su propia especificación no convierte esas señales en un juicio de valor sobre el contenido. Procedencia comprobable y veracidad no son sinónimos.

### 3. Asigna umbrales por consecuencia

No clasifiques primero la fuente y luego permitas cualquier uso. Empieza por el daño de equivocarse. Una pista reversible tolera más incertidumbre que acusar públicamente, bloquear una cuenta o señalar a una persona.

Una matriz sencilla puede usar cuatro estados:

- `P0 — pista`: orienta una búsqueda, pero no sostiene una afirmación;
- `P1 — uso interno`: permite una acción reversible y documentada;
- `P2 — publicación`: exige fuente primaria o justificación explícita, corroboración pertinente y revisión;
- `P3 — alto impacto`: requiere autoridad competente, asesoramiento aplicable y un proceso específico fuera del flujo editorial ordinario.

Los nombres importan menos que las consecuencias. Un número alto no debe parecer una probabilidad ni una garantía.

### 4. Registra dependencias y transformaciones

Dos medios pueden citar el mismo teletipo; tres buscadores pueden indexar la misma página; un gráfico y una tabla pueden proceder del mismo CSV. Dibuja la cadena mínima:

```text
registro oficial -> copia descargada -> extracción tabular -> ficha interna
                         |                     |
                      hash + T            script + versión
```

Así se ve qué observaciones son independientes y dónde una transformación puede haber introducido un error. PROV-O permite formalizar estas relaciones, pero una tabla clara suele bastar para empezar.

### 5. Evalúa cláusulas, no una nota total

Una media oculta fallos críticos. Una fuente muy fresca no compensa una procedencia desconocida; tres réplicas no compensan la ausencia del original. Usa condiciones necesarias:

```yaml
decision: publicar_cambio_societario
requiere:
  - fuente_oficial_identificable
  - observacion_menor_de_24h
  - copia_preservada_con_hash
  - contradicciones_documentadas
  - revision_independiente
si_falta: inconcluso_no_publicar
```

Este ejemplo es deliberadamente local y ficticio. No es una recomendación jurídica ni sustituye las reglas de cada registro, organización o jurisdicción.

### 6. Conserva el disenso y la caducidad

El expediente debe indicar qué condición falló, quién autorizó una excepción, cuándo caduca la observación y qué hecho obligaría a reabrirla. Si una fuente oficial se actualiza mañana, la decisión de hoy no debe seguir circulando sin contexto temporal.

La analogía con los SLO resulta útil aquí: un objetivo solo ayuda si expresa lo que importa al usuario y se define antes de interpretar la métrica. Trasladado con prudencia a OSINT, el umbral debe reflejar el riesgo de la decisión, no aquello que casualmente podemos medir.

## Checklist operativo

Antes de cerrar una investigación, comprueba:

- [ ] la afirmación y el uso permitido están escritos;
- [ ] cada fuente tiene URL, responsable, fecha y versión cuando existe;
- [ ] se distingue original, copia, cita y transformación;
- [ ] la ventana de frescura está justificada por el dominio;
- [ ] las corroboraciones no comparten silenciosamente el mismo origen;
- [ ] integridad, autenticidad y veracidad no se usan como sinónimos;
- [ ] existe una salida `inconcluso` y una regla de escalado;
- [ ] las excepciones tienen responsable, motivo y caducidad;
- [ ] se han minimizado datos personales y material sensible;
- [ ] una persona distinta puede reconstruir el razonamiento.

## Limitaciones y falsos positivos

Un ANE puede crear una peligrosa sensación de rigor si se aplica mecánicamente. Sus fallos habituales son:

- **umbrales arbitrarios:** exigir «dos fuentes» sin explicar qué observa cada una;
- **teatro de procedencia:** conservar metadatos impecables de una fuente que nunca pudo conocer el hecho;
- **frescura uniforme:** imponer 24 horas a datos estables o aceptar meses para señales volátiles;
- **independencia aparente:** contar sindicaciones, espejos o interfaces como confirmaciones separadas;
- **puntuación sustitutiva:** sumar casillas y ocultar una condición crítica incumplida;
- **excepción permanente:** aprobar una urgencia y reutilizarla como precedente sin revisión;
- **coste desproporcionado:** exigir preservación forense para una pista efímera de bajo riesgo;
- **sesgo institucional:** tratar «oficial» como infalible cuando puede haber retrasos, errores o límites de cobertura.

Tampoco toda evidencia pública puede preservarse del mismo modo. Hay contenido dinámico, restricciones de acceso, derechos de autor, términos de uso y obligaciones de protección de datos. El acuerdo debe indicar qué no se recogerá y por qué.

## Buenas prácticas de OPSEC, ética y privacidad

- Limita la recolección al hecho necesario para una finalidad legítima.
- No uses el nivel de evidencia para justificar vigilancia de personas ni ampliar el alcance por curiosidad.
- Prefiere identificadores de expediente y datos corporativos pertinentes frente a atributos personales.
- Conserva hashes y metadatos en lugar de copias completas cuando sean suficientes.
- Separa material sensible, credenciales y notas operativas del expediente compartido.
- Define retención, acceso y borrado antes de recopilar.
- No publiques inferencias personales solo porque una tabla alcance el umbral técnico.
- Documenta incertidumbre, contradicciones y ausencia de cobertura.
- Exige revisión humana para decisiones irreversibles o de alto impacto.
- Respeta legislación, condiciones de uso y autorización aplicables.

## Alternativas y siguientes pasos

Una política de fuentes indica qué repositorios se prefieren; una cadena de custodia registra manipulación y transferencias; un modelo de procedencia describe derivaciones; un protocolo de arbitraje resuelve señales contradictorias. El ANE conecta esas piezas con la decisión: especifica qué combinación es suficiente **antes** de conocer el resultado.

El takeaway accionable es elegir una decisión recurrente y crear una ficha de una página con `afirmación`, `uso`, `procedencia`, `frescura`, `independencia`, `integridad`, `revisión`, `caducidad` y `salida si falta`. Después pruébala con un expediente antiguo. **Si solo funciona cuando todas las fuentes coinciden, todavía no es un acuerdo: falta diseñar el estado inconcluso y gobernar las excepciones.**

Como siguiente tema convendría estudiar los **presupuestos de excepción de evidencia**: cómo limitar, revisar y retirar excepciones urgentes sin convertirlas en el nuevo umbral por defecto.

## Fuentes consultadas

- [W3C: PROV-O, The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [W3C: PROV Overview](https://www.w3.org/TR/prov-overview/)
- [NIST IR 8387: Digital Evidence Preservation — Considerations for Evidence Handlers](https://www.nist.gov/publications/digital-evidence-preservation-considerations-evidence-handlers)
- [NIST CSRC: Chain of Custody](https://csrc.nist.gov/glossary/term/chain_of_CUSTODY)
- [C2PA: Content Credentials Technical Specification](https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html)
- [Google SRE: Service Level Objectives](https://sre.google/resources/book-update/slos/)
