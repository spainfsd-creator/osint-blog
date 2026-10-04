---
title: "Simulacros de incidentes en OSINT: ensayar la rectificación antes de improvisarla"
slug: /simulacros-incidentes-equipos-osint
authors: [osint-writter]
tags: [osint, methodology, incident-response, verification, automation, privacy]
date: 2026-10-04
image: /img/blog/2026-10-04-simulacros-incidentes-equipos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un equipo OSINT realizando un simulacro seguro de respuesta a incidentes](/img/blog/2026-10-04-simulacros-incidentes-equipos-osint.png)

*Imagen generada mediante inteligencia artificial.*

A las 10:07, una analista recibe un aviso: el informe publicado esa mañana podría haberse construido con una descarga incompleta. A las 10:09, alguien pregunta si debe retirar la página; otra persona quiere corregir la gráfica; nadie sabe quién conserva el original ni quién avisará a la audiencia. Esta vez no hay víctimas ni datos reales. **El reloj, el informe y el error forman parte de un simulacro diseñado para descubrir esas dudas antes de que importen.**

Un simulacro de incidentes permite ensayar cómo detectar, contener, preservar, rectificar y comunicar un fallo OSINT en un entorno seguro. No busca sorprender ni puntuar a individuos. Busca comprobar si el equipo puede convertir una señal ambigua en decisiones trazables, sin destruir evidencia, amplificar una acusación o exponer datos personales.

<!-- truncate -->

## Qué es un simulacro y para qué sirve

Un ejercicio de mesa o *tabletop* es una conversación guiada alrededor de un escenario. Las personas explican qué harían, con qué información, bajo qué autoridad y usando qué procedimiento. La [definición de NIST](https://csrc.nist.gov/glossary/term/tabletop_exercise) destaca precisamente su carácter basado en discusión: un facilitador presenta una situación y formula preguntas para validar un plan y las responsabilidades descritas en él.

No es lo mismo que una prueba funcional. En esta última, el equipo ejecuta tareas en un entorno simulado: abre un ticket de ensayo, preserva un fixture, genera una página no pública o redacta una rectificación marcada como ficticia. La [guía NIST SP 800-84](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-84.pdf) distingue ejercicios de mesa, ejercicios funcionales y pruebas, y propone diseñarlos a partir de objetivos, alcance, participantes y criterios de evaluación.

En un equipo OSINT, un simulacro puede revelar preguntas que el documento de respuesta daba por resueltas:

- ¿quién puede declarar un incidente y detener una publicación programada?;
- ¿cómo retiramos un derivado sin borrar el original adquirido ni su registro de procedencia?;
- ¿qué afirmaciones, gráficos y entregables dependen del lote sospechoso?;
- ¿quién redacta una advertencia provisional y quién aprueba la rectificación?;
- ¿cómo se registran decisiones, hipótesis descartadas y horas en una cronología común?;
- ¿qué hacemos si el supuesto fallo resulta ser un cambio legítimo de la fuente?

El ejercicio no verifica que una fuente sea verdadera ni garantiza que el equipo reaccionará igual bajo presión real. Sí permite observar si el plan es comprensible, si sus dependencias existen y si una decisión crítica tiene propietario.

## Caso de uso legítimo: una segunda página que nadie vio

Imaginemos **Observatorio Río Claro**, un proyecto ficticio que publica agregados semanales de contratos administrativos. El equipo trabaja con documentos públicos y minimiza los campos personales. Para el ejercicio, todo se recrea con dominios `.example`, nombres inventados, importes sintéticos y copias aisladas de producción.

El objetivo no es «resolver el incidente». Es más preciso:

> Comprobar si el equipo puede decidir en quince minutos qué salida debe detener, preservar el original y los derivados afectados, y publicar una advertencia interna trazable sin usar producción.

El facilitador prepara un lote ficticio de 47 registros, una segunda página con otros 31 y una gráfica que anuncia una caída del 38 %. También prepara cinco *injects*: fragmentos de información que entregará a horas concretas o cuando el grupo tome una decisión.

1. **10:07 — aviso inicial:** una lectora ficticia señala dos expedientes ausentes.
2. **10:10 — señal técnica:** el job terminó con código `0`, pero el HTML contiene un enlace `next` no recorrido.
3. **10:15 — presión editorial:** un mensaje simulado pregunta si puede enviarse el boletín en cinco minutos.
4. **10:20 — alcance:** otros tres gráficos consumieron el mismo lote normalizado.
5. **10:25 — giro:** la segunda página incluye un registro duplicado y una corrección retrospectiva.

El último giro es importante: evita que el ejercicio premie una respuesta automática. Descargar más filas no convierte el resultado en verdad. El equipo todavía debe deduplicar, interpretar la corrección, documentar cobertura y comprobar qué afirmaciones siguen siendo defendibles.

## Diseñar el ejercicio sin convertirlo en una trampa

### 1. Escribe un objetivo observable

«Mejorar la preparación» no se puede evaluar. Formula una capacidad, una condición y un criterio:

- localizar todos los derivados del lote antes de quince minutos;
- asignar coordinación, operaciones, documentación y comunicación sin dejar funciones implícitas;
- conservar original, hash, hora de adquisición y versión del parser antes de transformar nada;
- decidir entre mantener, etiquetar, retirar o corregir aplicando la política vigente;
- producir una acción de mejora con responsable, fecha y prueba de cierre.

Un ejercicio corto con un objetivo suele enseñar más que una catástrofe barroca con diez fallos simultáneos. NIST advierte que los escenarios excesivamente detallados pueden desviar la conversación desde los objetivos hacia la discusión del relato.

### 2. Separa diseño, facilitación, juego y observación

Una persona puede cubrir varias funciones en un equipo pequeño, pero conviene nombrarlas:

- **dirección del ejercicio:** define alcance, permisos y condiciones de parada;
- **facilitación:** presenta el escenario, entrega *injects* y devuelve la discusión al objetivo;
- **participantes:** responden con los procedimientos y herramientas que usarían;
- **observación:** registra hechos y tiempos contra criterios acordados, sin interpretar intenciones;
- **control de seguridad:** puede pausar el ejercicio si una acción amenaza producción, privacidad o bienestar.

Los [paquetes CTEP de CISA](https://www.cisa.gov/resources-tools/resources/ctep-package-documents) separan materiales para planificación, facilitación, participantes, comentarios e informe posterior. No hace falta copiar su escala, pero sí su idea central: quien evalúa debe saber antes qué evidencia observará.

### 3. Define límites antes del primer minuto

Un simulacro responsable no autoriza acciones que serían inadecuadas fuera de él. Deja por escrito:

- ningún mensaje sale a audiencias reales;
- no se modifican el sitio público, el repositorio de producción ni las alertas operativas;
- no se consultan personas, cuentas, teléfonos o correos reales;
- los documentos sintéticos llevan una marca inequívoca de ejercicio;
- no se simulan acusaciones contra personas u organizaciones identificables;
- las credenciales, canales y destinatarios de prueba están aislados;
- cualquier participante puede pedir una pausa sin penalización;
- una palabra de seguridad detiene inmediatamente la ejecución funcional.

El [NCSC británico](https://www.ncsc.gov.uk/section/advice-guidance/all-topics/exercising) resume el valor de estos ejercicios como práctica de la respuesta en un entorno seguro. Para OSINT, «seguro» incluye seguridad técnica, protección de datos y prevención del daño reputacional.

## Flujo recomendado: de la preparación al cierre

### Antes: alcance, fixtures y línea de base

1. Elige una sola capacidad surgida de un riesgo o postmortem reciente.
2. Decide si será conversación de mesa o ejecución funcional aislada.
3. Crea originales, derivados, capturas y mensajes completamente ficticios.
4. Anota la respuesta esperada del sistema, no una única secuencia «correcta» de decisiones.
5. Define criterios observables y recoge la versión vigente del procedimiento.
6. Confirma participantes, canales de prueba, duración y criterios de parada.
7. Comprueba que todos distinguen `EJERCICIO` de `INCIDENTE REAL`.

Haz una prueba en seco de los *injects*. Un PDF deliberadamente paginado debe abrirse; una URL `.example` no debe activar un recolector real; una captura no puede contener datos arrastrados de otro caso. Si la ficción técnica no es coherente, terminarás evaluando la capacidad de adivinar qué quiso decir el facilitador.

### Durante: declarar, contener, preservar y comunicar

El facilitador presenta solo la información disponible en ese momento. Los participantes pueden pedir comprobaciones y reciben la respuesta preparada. El observador registra:

| Momento | Evidencia observable | Pregunta de control |
|---|---|---|
| Declaración | responsable, alcance inicial y canal | ¿Todos saben que es un ejercicio? |
| Contención | publicación o cola ficticia identificada | ¿Se evitó alterar originales? |
| Preservación | URL, UTC, hash, fichero y versión | ¿Puede reconstruirse el estado? |
| Análisis | hipótesis y hechos separados | ¿Se documentó qué falta por saber? |
| Decisión | opción, autoridad y justificación | ¿La política sostiene la medida? |
| Comunicación | borrador, audiencia y próxima actualización | ¿Describe incertidumbre sin acusar? |

No conviertas la facilitación en un concurso de secretos. Si el equipo se bloquea por una ambigüedad artificial, aporta contexto. Si resuelve el caso antes de tiempo, introduce una dependencia afectada o una información contradictoria que esté dentro del objetivo, no una sorpresa imposible.

Google SRE recomienda practicar la respuesta periódicamente, usar escenarios inventados o derivados de postmortems y revisar después qué funcionó y qué debe cambiar. Su [capítulo sobre respuesta a incidentes](https://sre.google/workbook/incident-response/) también subraya que la práctica desarrolla coordinación y comunicación; no basta con memorizar una lista.

### Después: *hotwash*, informe y mejora verificable

Reserva los últimos quince minutos para una revisión inmediata o *hotwash*. Pregunta:

1. ¿Qué información permitió avanzar?
2. ¿Dónde dudamos sobre autoridad, canal o procedimiento?
3. ¿Qué barrera limitó el impacto simulado?
4. ¿Qué observó el evaluador que el grupo no vio?
5. ¿Qué debe cambiar antes del siguiente ejercicio?

El informe posterior debe separar observación de recomendación. «La advertencia se redactó a los 19 minutos; el objetivo era 15» es una observación. «Añadir una plantilla enlazada desde el runbook» es una recomendación. La acción útil añade propietario, fecha y comprobación: «ejecutar un ensayo con la plantilla y demostrar que contiene alcance, incertidumbre y hora de próxima actualización».

No cierres el ejercicio al enviar el acta. Ciérralo cuando se hayan verificado las acciones o se haya aceptado explícitamente el riesgo residual.

## Limitaciones y falsos positivos del propio ejercicio

Un simulacro produce señales, no una certificación. Sus límites más habituales son:

- **efecto guion:** quien conoce el escenario puede conducir al equipo hacia la respuesta prevista;
- **presión irreal:** una sala tranquila no reproduce cansancio, exposición pública ni información fragmentaria;
- **éxito teatral:** completar el ejercicio puede ocultar que los accesos o dependencias reales no funcionarían;
- **medición pobre:** un tiempo rápido no compensa haber destruido procedencia o comunicado una certeza falsa;
- **sobreajuste:** repetir siempre la misma paginación entrena el libreto, no la capacidad de razonar;
- **daño accidental:** un mensaje ficticio mal etiquetado puede llegar a una persona real;
- **silencio confundido con acuerdo:** participantes con menor rango pueden detectar un riesgo y no expresarlo.

Alterna ejercicios de mesa con pruebas funcionales en entornos aislados. Cambia una variable cada vez y conserva una línea de base. Si un control no puede probarse sin tocar producción, registra esa limitación en lugar de fingir que quedó validado.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa entidades, dominios, cuentas, hashes e importes sintéticos.
- Elimina capturas reales de los fixtures, incluidos nombres, avatares y metadatos invisibles.
- No uses el ejercicio para evaluar públicamente a una persona ni para justificar vigilancia laboral.
- Evalúa funciones y barreras: «faltó autoridad documentada», no «alguien fue lento».
- Mantén la lista de *injects* separada de los materiales de participantes.
- Protege las notas: pueden describir debilidades internas, contactos y procedimientos de emergencia.
- Fija retención y acceso para grabaciones, chats y documentos colaborativos.
- Incluye una vía para declarar un incidente real si aparece durante el ejercicio.
- Marca todos los artefactos con `EJERCICIO — NO PUBLICAR` y retíralos de canales de prueba al cerrar.
- Si el escenario incluye contenido sensible, avisa de su naturaleza y ofrece alternativas de participación.

## Plantilla mínima reutilizable

```text
Nombre: SIM-OSINT-01 — publicación incompleta
Tipo: ejercicio de mesa / funcional aislado
Objetivo observable:
Fuera de alcance:
Responsable de seguridad y palabra de parada:
Participantes y funciones:
Fixture sintético:
Duración:
Injects y condiciones de entrega:
Criterios de evaluación:
Canales y destinatarios de prueba:
Evidencias que conservará el observador:
Hotwash:
Acciones, responsables, fechas y prueba de cierre:
```

## Checklist

- [ ] El objetivo mide una capacidad, no la obediencia al guion.
- [ ] Los materiales son sintéticos y están marcados como ejercicio.
- [ ] Producción, cuentas reales y audiencias públicas quedan fuera.
- [ ] Existe una persona con autoridad para detener la prueba.
- [ ] Los roles de facilitación, participación y observación están claros.
- [ ] Cada *inject* sirve al objetivo y tiene una respuesta preparada.
- [ ] Los criterios se definieron antes de empezar.
- [ ] Se observan procedencia, privacidad y calidad de decisión, no solo velocidad.
- [ ] El cierre incluye *hotwash* e informe posterior.
- [ ] Cada mejora tiene responsable, fecha y comprobación.
- [ ] Se distingue una limitación del ejercicio de un control validado.
- [ ] Nadie presenta el resultado como garantía de verdad factual.

## Alternativas y siguientes pasos

Si primero necesitas reconstruir un fallo real, empieza por [postmortems sin culpa](/postmortems-sin-culpa-incidentes-osint). Para decidir cuándo detener una salida, revisa [presupuestos de error](/presupuestos-error-pipelines-osint); para detectar degradaciones, [observabilidad de datos](/observabilidad-datos-osint); y para recorrer los derivados afectados, [OpenLineage](/openlineage-linaje-datos-osint).

El takeaway accionable es sencillo: toma una rectificación reciente, sustituye todos sus datos por fixtures sintéticos y organiza un ejercicio de mesa de 45 minutos con un solo objetivo. Mide cuándo se declara, qué se preserva y quién decide. Si la mejora final dice «comunicar mejor», todavía no está cerrada: conviértela en una acción observable.

Como próximo tema, merece la pena estudiar **la comunicación pública de correcciones OSINT**: cómo mantener una nota visible, enlazar versiones y explicar el cambio sin borrar el historial ni amplificar el dato equivocado.

## Fuentes consultadas

- [NIST SP 800-84: Guide to Test, Training, and Exercise Programs for IT Plans and Capabilities](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-84.pdf)
- [NIST CSRC: definición de Tabletop Exercise](https://csrc.nist.gov/glossary/term/tabletop_exercise)
- [CISA: Cybersecurity Tabletop Exercise Package Documents](https://www.cisa.gov/resources-tools/resources/ctep-package-documents)
- [NCSC: Exercising](https://www.ncsc.gov.uk/section/advice-guidance/all-topics/exercising)
- [Google SRE Workbook: Incident Response](https://sre.google/workbook/incident-response/)
- [Google SRE: Anatomy of an Incident](https://sre.google/resources/practices-and-processes/anatomy-of-an-incident/)
