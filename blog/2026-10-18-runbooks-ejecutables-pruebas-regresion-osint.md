---
title: "Runbooks ejecutables en OSINT: probar la respuesta sin automatizar el juicio"
slug: /runbooks-ejecutables-pruebas-regresion-osint
authors: [osint-writter]
tags: [osint, methodology, incident-response, testing, automation, privacy]
date: 2026-10-18
image: /img/blog/2026-10-18-runbooks-ejecutables-pruebas-regresion-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una copia pública debería haberse retirado, pero el runbook termina con «comprobar que todo está bien». La persona de guardia mira el origen, recibe un `404` y cierra el incidente. Horas después, una réplica continúa sirviendo el archivo. **La instrucción existía; lo que faltaba era una condición que una máquina o una segunda persona pudieran comprobar.**

![Analista OSINT ante un runbook ejecutable, una batería de pruebas y una barrera previa a la publicación](/img/blog/2026-10-18-runbooks-ejecutables-pruebas-regresion-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Convertir un runbook en algo ejecutable no significa entregar todas las decisiones a un script. Significa expresar precondiciones, observaciones, acciones seguras, límites y pruebas posteriores de forma reproducible. En un flujo OSINT, donde una automatización mal acotada puede volver a publicar información retirada o destruir contexto probatorio, el objetivo es mecanizar lo repetible y reservar el juicio para aquello que cambia el alcance, la atribución o el impacto sobre personas.

Todos los nombres, dominios, identificadores y resultados del ejemplo son ficticios. Este texto se refiere a sistemas propios, fuentes públicas o entornos para los que existe autorización. No propone eludir accesos, vigilar a personas ni automatizar decisiones perjudiciales.

## Qué es un runbook ejecutable (y para qué sirve)

Un runbook tradicional describe cómo responder a una situación: quién interviene, qué debe observar y qué pasos puede dar. Se vuelve **ejecutable** cuando algunas de esas afirmaciones se traducen en comprobaciones o acciones deterministas, versionadas y repetibles. No tiene por qué ser un único programa. Puede combinar:

- documentación legible por personas;
- consultas de solo lectura que recogen el estado;
- tests que comparan ese estado con invariantes;
- acciones con modo simulación y alcance explícito;
- puertas de aprobación antes de efectos irreversibles;
- pruebas posteriores que confirman el resultado desde otra perspectiva.

La clave está en no confundir tres verbos: **observar**, **proponer** y **cambiar**. Un test puede observar que el digest público no coincide con el aprobado. Otro componente puede proponer retirar el artefacto. La retirada real puede seguir necesitando la autorización de una persona distinta, especialmente si afecta a evidencia, comunicación pública o disponibilidad.

[NIST SP 800-61 Rev. 3](https://doi.org/10.6028/NIST.SP.800-61r3) integra preparación, detección, respuesta, recuperación y mejora dentro de la gestión del riesgo, en vez de tratar el incidente como una secuencia aislada. El control IR-3 de [NIST SP 800-53 Rev. 5.1](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) pide probar la eficacia de la capacidad de respuesta y contempla mecanismos automatizados, escenarios realistas y mejora continua basada en datos. Un runbook ejecutable sirve precisamente para convertir una lección en una regresión comprobable, no solo en otro párrafo olvidado.

## Caso legítimo: una retirada que parecía completa

El observatorio ficticio **Vigía Abierta** publica informes agregados sobre licitaciones. Durante un simulacro, el equipo coloca el documento sintético `ensayo-r7.pdf` en un origen de pruebas y en dos réplicas. El ledger conserva el digest aprobado, las ubicaciones esperadas y un identificador opaco de liberación.

La primera versión del runbook decía:

1. detener nuevas publicaciones;
2. guardar una copia para el análisis;
3. retirar el documento;
4. comprobar que ya no está disponible;
5. reabrir el pipeline.

Era comprensible, pero no verificable. No definía qué publicaciones debían detenerse, dónde preservar la copia, qué significaba «retirar», qué rutas había que comprobar ni quién podía reabrir. En el ensayo, el origen dejó de servir el PDF y la caché no. El paso cuatro recibió un visto bueno porque la persona que ejecutó la retirada consultó la misma ruta que acababa de modificar.

Vigía Abierta no responde automatizando un borrado global. Divide el runbook en controles pequeños: inventario independiente de ubicaciones, captura mínima de metadatos, digest de la evidencia preservada, retirada limitada a un `release_id`, sondeo desde las rutas de los destinatarios y una puerta humana antes de restaurar la publicación. El fallo del simulacro se convierte además en un test: el runbook no puede declarar éxito mientras cualquiera de las réplicas conocidas devuelva los bytes retirados.

## Flujo recomendado

### 1. Empieza por el contrato, no por el script

Escribe qué incidente cubre el runbook, qué queda fuera y qué condiciones deben cumplirse antes de ejecutarlo. Identifica sistemas, roles, datos y efectos posibles. Si una acción puede borrar evidencia, ampliar el alcance o afectar a terceros, márcala como punto de decisión humana.

Un contrato conceptual, sin secretos ni datos personales, podría ser:

```yaml
runbook_id: retirada-publicacion-v2
scenario: artefacto_publico_incoherente
scope:
  release_id: ensayo-r7
  destinations: [origen-pruebas, replica-a, replica-b]
preconditions:
  - incidente_declarado
  - evidencia_preservada
safe_default: stop
approval_required_for:
  - retirada
  - reapertura
success:
  - no_ruta_conocida_sirve_digest_retirado
  - ledger_registra_evento_compensatorio
  - publicacion_de_control_supera_pruebas
```

El fichero no es la verdad completa ni una receta universal. Hace visibles supuestos que después deben enlazarse con consultas y pruebas concretas. `safe_default: stop` significa que una observación incompleta no se interpreta como éxito.

### 2. Separa recolectores, evaluadores y actuadores

Un **recolector** consulta inventarios, respuestas HTTP, digests y estados del ledger con permisos de lectura. Un **evaluador** aplica reglas sobre esos datos. Un **actuador** realiza el cambio autorizado. Esta separación facilita probar lógica sin tocar el destino y reduce el riesgo de que una consulta mal formada tenga efectos.

La salida del recolector debe incluir cobertura y errores. No conviertas un timeout en «ausente». Distingue al menos:

- observado y coincide;
- observado y discrepa;
- no observado tras una respuesta concluyente;
- desconocido por timeout, permisos, paginación o fallo del sensor.

Conserva marcas de tiempo, versiones de las herramientas y referencias mínimas a la evidencia. Evita copiar cuerpos completos a logs si bastan un digest, tamaño y estado. Un log lleno de URLs firmadas o selectores personales crea un segundo problema.

### 3. Diseña cada acción para simulación, límite e idempotencia

Antes del modo de cambio, el actuador debe poder producir un plan: qué objeto afectaría, por qué regla y con qué identidad. La simulación no garantiza que la acción real vaya a funcionar, pero permite descubrir un selector vacío, una expansión inesperada o un ámbito excesivo.

Una acción idempotente converge al mismo estado cuando se repite con la misma intención. No basta con añadir `--force` o ignorar errores. La automatización debería exigir un identificador estable, comprobar el estado previo y rechazar una repetición cuyos parámetros no coincidan.

El capítulo sobre [automatización para la fiabilidad de Google SRE](https://sre.google/sre-book/automation-at-google/) documenta tanto el valor de automatizar como el daño que puede multiplicar una interpretación peligrosa del conjunto vacío; entre las correcciones cita comprobaciones de coherencia, limitación de tasa e idempotencia. La lección aplicable es prudente: nunca permitas que «ningún objetivo» signifique «todos» y fija un máximo de objetos modificables por ejecución.

### 4. Convierte el incidente en pruebas de regresión

Una prueba útil reproduce la propiedad rota con datos sintéticos, no el contenido sensible del caso. Para la retirada de Vigía Abierta, la batería podría incluir:

1. una réplica sigue sirviendo el digest antiguo: el resultado debe ser fallo;
2. una ruta agota el tiempo: el resultado debe ser desconocido, nunca éxito;
3. el ledger marca retirado pero el destino conserva bytes: el resultado debe ser fallo;
4. el actuador se ejecuta dos veces con la misma clave: la segunda vez no crea un evento nuevo;
5. la misma clave llega con otro digest: la ejecución debe detenerse;
6. el inventario devuelve cero destinos por un error de permisos: el runbook no puede reabrir;
7. el artefacto de control atraviesa el pipeline tras la recuperación: la prueba posterior debe pasar.

Prueba también el propio test. Introduce deliberadamente una discrepancia conocida y verifica que falla. Un chequeo que siempre queda verde es más peligroso que no tener chequeo, porque fabrica confianza.

NIST SP 800-53 incluye checklists, recorridos, ejercicios de mesa y simulaciones entre las formas de probar la respuesta. La automatización amplía cobertura, pero no sustituye ejercicios organizativos: un test puede validar la purga de una réplica y no saber quién debe aprobar una rectificación pública.

### 5. Ejecuta en CI lo seguro y protege el cambio real

Las validaciones puras —esquema, lint, fixtures, invariantes y simulaciones— pueden ejecutarse con cada cambio. [GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart) permite lanzar tests al actualizar el repositorio y conservar el resultado de cada ejecución. Mantén los fixtures construidos desde cero y evita introducir credenciales o capturas del incidente en el repositorio.

El job que modifica un entorno no debería heredar automáticamente la confianza del job de tests. Los [entornos y reglas de protección de GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) pueden exigir aprobación, restringir ramas y retrasar el acceso a secretos hasta que se cumplan las reglas configuradas. Son un ejemplo de puerta técnica, no una garantía universal: hay que revisar el plan, el alcance y la evidencia, no pulsar «aprobar» por costumbre.

Separa identidades y permisos:

- CI valida sin capacidad de publicación;
- el recolector de producción solo lee;
- el actuador obtiene credenciales de duración y alcance mínimos;
- la persona que inició una acción de alto impacto no debería ser su única aprobadora;
- la verificación posterior usa, cuando sea posible, otra ruta e identidad.

### 6. Define criterios de salida desde la perspectiva del destinatario

«El comando terminó con código cero» es una señal interna. El criterio real debe observar lo que puede obtener un destinatario: origen, CDN, réplicas, índices y enlaces conocidos dentro del alcance. Establece una ventana de propagación basada en el comportamiento medido y diferencia espera prevista de estado desconocido.

La reapertura requiere algo más que ausencia: ledger coherente, evidencia preservada, evento compensatorio, comunicación preparada cuando corresponda y una publicación sintética de control que recorra el flujo completo. El [playbook federal de respuesta de CISA](https://www.cisa.gov/news-events/news/2021/11/16/cisa-releases-cybersecurity-incident-and-vulnerability-response-playbooks) organiza procedimientos y listas de comprobación alrededor de preparación, detección, contención, erradicación, recuperación y actividades posteriores. Úsalo como referencia para no reducir la recuperación a un solo comando.

### 7. Versiona, mide y retira runbooks caducados

El runbook debe vivir junto a sus tests, responsables y dependencias. Registra qué versión se ejecutó, con qué entradas no sensibles, qué aprobaciones recibió y qué comprobaciones pasaron. Mide falsos positivos, estados desconocidos, duración, pasos manuales y hallazgos posteriores; no uses solo el tiempo de cierre como incentivo.

Asigna fecha de revisión y dispara una prueba cuando cambie una API, un destino, un rol o la estructura del ledger. Si dos runbooks se contradicen, falla de forma visible. Un procedimiento antiguo que aún parece oficial puede ser peor que una ausencia reconocida.

## Limitaciones y falsos positivos

Un runbook ejecutable demuestra que ciertas condiciones observables se cumplieron bajo un modelo. No demuestra que el informe fuera verdadero, que el tratamiento fuera lícito ni que nadie guardara una copia. Tampoco conoce automáticamente todas las réplicas o consumidores.

Los falsos positivos pueden surgir por consistencia eventual, relojes desajustados, respuestas intermedias de una CDN, inventarios paginados o transformaciones legítimas de los bytes. Los falsos negativos aparecen cuando el test consulta el mismo plano de control que falló, omite una ruta o interpreta un error como ausencia.

Errores frecuentes:

- convertir una guía ambigua en un script sin aclarar antes el contrato;
- mezclar observación y modificación bajo la misma credencial;
- usar datos reales para que la prueba parezca convincente;
- permitir selectores vacíos, comodines o ámbitos calculados sin límite;
- declarar idempotencia porque el comando no devuelve error;
- aprobar automáticamente cualquier plan que supere tests técnicos;
- guardar secretos, URLs firmadas o contenido retirado en artefactos de CI;
- verificar solo el origen y olvidar réplicas e índices;
- medir rapidez sin medir preservación, cobertura y corrección;
- dejar que un test verde sustituya la revisión de atribución o impacto.

## Buenas prácticas de OPSEC, ética y privacidad

- Ensaya con artefactos y dominios reservados, claramente separados de casos reales.
- Minimiza fixtures, logs y salidas; conserva solo lo necesario durante un plazo definido.
- Aplica mínimo privilegio y credenciales efímeras a cada componente.
- Protege las acciones destructivas con alcance, límite, simulación y aprobación independiente.
- Detén el flujo ante observaciones incompletas o contradictorias.
- Preserva evidencia antes de modificar el destino y documenta la cadena de decisiones.
- No automatices atribuciones, acusaciones ni decisiones que afecten a una persona.
- Incluye una vía de aborto y una reversión comprobada para los ensayos.
- Revisa términos de servicio y autorización antes de consultar sistemas de terceros.
- Declara cobertura, incertidumbre y partes del recorrido que no se probaron.

## Alternativas y siguientes pasos

Si el procedimiento todavía cambia en cada conversación, empieza con un tabletop y una checklist. Si existe una única acción delicada, construye primero una consulta de solo lectura y una prueba posterior. Si el entorno no admite automatización segura, una plantilla estructurada con campos obligatorios puede mejorar mucho la trazabilidad sin ejecutar cambios.

Herramientas de CI, motores de políticas o plataformas de orquestación pueden ayudar, pero la arquitectura importa más que la marca. Busca entradas tipadas, salidas verificables, mínimo privilegio, límites duros, historial versionado y separación entre prueba y efecto.

El takeaway accionable es concreto: elige hoy una frase vaga de tu runbook —«verifica que se retiró», «restaura el servicio» o «notifica a los afectados»— y conviértela en cuatro elementos: observación, criterio de éxito, estado desconocido y autoridad para continuar. Después crea un fixture sintético que obligue al criterio a fallar. Si no puedes expresar qué evidencia cerraría el paso, todavía no está listo para automatizarse.

Como siguiente tema convendría estudiar los **canary runbooks y las pruebas en sombra**: cómo validar una nueva automatización con alcance mínimo, comparar decisiones y detenerla antes de que un error se propague.

## Fuentes consultadas

- [NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations](https://doi.org/10.6028/NIST.SP.800-61r3)
- [NIST SP 800-53 Rev. 5.1: Security and Privacy Controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [CISA: Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/news-events/news/2021/11/16/cisa-releases-cybersecurity-incident-and-vulnerability-response-playbooks)
- [Google SRE: The Evolution of Automation at Google](https://sre.google/sre-book/automation-at-google/)
- [Google SRE Workbook: Incident Response](https://sre.google/workbook/incident-response/)
- [GitHub Actions: Quickstart](https://docs.github.com/en/actions/get-started/quickstart)
- [GitHub Docs: Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
