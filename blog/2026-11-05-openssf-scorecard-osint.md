---
title: "OpenSSF Scorecard en OSINT: evaluar repositorios sin confundir una nota con seguridad"
slug: /openssf-scorecard-osint
authors: [osint-writter]
tags: [osint, tooling, verification, data, investigation, privacy]
date: 2026-11-05
image: /img/blog/2026-11-05-openssf-scorecard-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una organización quiere incorporar una biblioteca abierta a un servicio sensible. El repositorio está activo, tiene miles de estrellas y muestra una insignia de seguridad convincente. La tentación es convertir esa cifra en un atajo: puntuación alta, dependencia aprobada. **Pero una nota agregada no demuestra que el código sea seguro, que el paquete descargado proceda de ese código ni que el proyecto vaya a responder mañana a una vulnerabilidad.** Lo útil para una investigación OSINT empieza al abrir la cifra y preguntar qué observó realmente cada comprobación.

![Analista examinando señales públicas de seguridad y mantenimiento en un repositorio de código abierto](/img/blog/2026-11-05-openssf-scorecard-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/openssf-scorecard-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

**OpenSSF Scorecard** automatiza comprobaciones sobre prácticas de seguridad observables en proyectos de software abierto. En OSINT puede servir como instrumento de *triage* para una debida diligencia técnica: señala dónde buscar evidencia sobre revisión de código, protección de ramas, permisos de automatizaciones, mantenimiento, análisis estático o publicación de artefactos. No sustituye una auditoría, no certifica ausencia de vulnerabilidades y no autoriza a escanear infraestructura ajena.

Todos los nombres, decisiones y resultados del ejemplo son ficticios. El flujo se limita a repositorios públicos o a proyectos propios para los que exista autorización.

## Qué es y para qué sirve

El [repositorio oficial de OpenSSF Scorecard](https://github.com/ossf/scorecard) define la herramienta como un conjunto de comprobaciones automatizadas sobre heurísticas asociadas a la seguridad del software. Cada comprobación produce su propio resultado y la herramienta calcula además una nota agregada ponderada por riesgo. Ese resumen ayuda a ordenar trabajo, pero el propio proyecto advierte que las comprobaciones son opinables y pueden producir falsos positivos y falsos negativos.

Para una investigación responsable conviene separar cuatro capas:

1. **Observación:** qué dato público se consultó y en qué momento.
2. **Heurística:** qué regla convirtió ese dato en un resultado.
3. **Interpretación:** qué hipótesis abre para este proyecto y este uso.
4. **Decisión:** qué evidencia adicional exige la consecuencia prevista.

Por ejemplo, detectar un fichero `SECURITY.md` demuestra que existe un documento en una ubicación reconocible. No demuestra que el canal funcione, que el equipo responda ni que el proceso se aplique. Del mismo modo, no detectar una práctica puede significar ausencia, falta de permisos, una implementación no reconocida o una comprobación que no aplica.

La [documentación oficial de las comprobaciones](https://github.com/ossf/scorecard/blob/main/docs/checks.md) publica criterios, riesgos y medidas de mejora. Es una fuente más útil que la cifra aislada porque permite reconstruir el razonamiento y descubrir límites concretos. Entre otros ejemplos:

- `CI-Tests` busca señales de pruebas en estados y ejecuciones recientes, pero puede no reconocer un sistema válido;
- `Dependency-Update-Tool` detecta determinadas herramientas de actualización, sin asegurar que sus propuestas se revisen o fusionen;
- `Signed-Releases` busca firmas o procedencia entre los activos de publicación, pero la mera presencia de una firma no resuelve por sí sola la confianza;
- `Maintained` usa actividad observable y debe interpretarse según la naturaleza del proyecto: una utilidad estable puede necesitar pocos cambios;
- `Branch-Protection` depende tanto de la configuración como de la visibilidad que otorgue la credencial usada.

La infraestructura oficial resume bien la cautela necesaria: los resultados son **señales heurísticas, no un veredicto**, y un resultado `-1` es inconcluso, no un suspenso. Esa distinción debería conservarse también en nuestras tablas y paneles.

## Caso de uso legítimo: comparar dos dependencias candidatas

El equipo ficticio **Archivo Faro** necesita una biblioteca para procesar manifiestos públicos. Ha preseleccionado `brújula-ejemplo` y `sextante-demo`, nombres inventados. Ambas ofrecen la función necesaria y licencias compatibles según una primera revisión. Antes de realizar una prueba de código, el equipo quiere saber dónde concentrar su diligencia.

La pregunta de investigación no es «¿qué proyecto es seguro?», sino esta:

> ¿Qué evidencias públicas justifican revisar primero cada riesgo relevante para incorporar una de estas dependencias durante doce meses?

El analista consulta resultados fechados, conserva el JSON o la salida de consola y registra el commit evaluado. Después convierte cada comprobación prioritaria en una pregunta verificable:

| Señal de Scorecard | Pregunta de seguimiento | Evidencia adicional |
| --- | --- | --- |
| revisión de código baja | ¿se fusionan cambios humanos sin segunda mirada o la señal es incompleta? | reglas visibles, historial de *pull requests* y muestra manual |
| mantenimiento inconcluso | ¿faltan permisos/datos o el proyecto tiene poca actividad? | lanzamientos, incidencias, avisos y respuesta de mantenedores |
| dependencias no fijadas | ¿afecta al proceso de construcción o solo a ejemplos? | flujos concretos, alcance y hashes de las acciones |
| política de seguridad ausente | ¿existe otro canal documentado y privado? | documentación oficial y prueba autorizada del canal, sin enviar ruido |
| vulnerabilidades sin detectar | ¿qué ecosistemas y versiones cubrió la comprobación? | SBOM, avisos del proyecto y bases pertinentes |

Imaginemos que `brújula-ejemplo` obtiene una nota global mayor, pero su publicación no permite enlazar claramente el artefacto con un commit. `sextante-demo` puntúa menos por una práctica que la herramienta no reconoce, aunque conserva una procedencia verificable de cada versión. Para un uso que ejecutará el paquete publicado, esa diferencia contextual puede importar más que el orden de la clasificación.

La salida honesta sería: «`brújula-ejemplo` requiere verificar la procedencia del artefacto; `sextante-demo` requiere confirmar manualmente su proceso de revisión». Ninguna de esas frases atribuye mala conducta ni convierte una ausencia de señal en prueba de inseguridad.

## Flujo recomendado

### 1. Define la decisión antes de mirar la nota

Especifica el componente, su origen, la versión o commit, el entorno donde se usaría, el periodo de soporte necesario y la consecuencia de un fallo. Un repositorio de ejemplo, una biblioteca de producción y una herramienta ejecutada de forma aislada no merecen el mismo umbral.

Define también las barreras que una puntuación alta nunca puede saltarse: licencia incompatible, paquete sin origen verificable, vulnerabilidad relevante sin mitigación o imposibilidad de actualizar.

### 2. Identifica el objeto correcto

Confirma que el repositorio es el oficial mediante la documentación del proyecto, el registro del paquete y los enlaces cruzados disponibles. Registra:

- URL canónica del repositorio;
- commit o referencia analizada;
- paquete y versión candidatos;
- fecha y hora de consulta;
- fuente de los resultados y su frescura.

Esta comprobación evita evaluar un espejo, un *fork* o un repositorio homónimo y trasladar después sus señales al artefacto equivocado.

### 3. Empieza por la vista pública y conserva la procedencia

El proyecto ofrece un [visor web](https://scorecard.dev/viewer/) y una [API pública de resultados](https://github.com/ossf/scorecard-infra#results-api-apiscorecarddev). La API usa una ruta del tipo:

```text
GET https://api.scorecard.dev/projects/github.com/organizacion/repositorio
```

Para reproducibilidad, conserva la respuesta junto con la URL, la fecha y el commit que declare. La infraestructura ejecuta análisis periódicos sobre numerosos proyectos y los resultados pueden quedar desfasados respecto al estado actual. Si la consulta devuelve ausencia o inconclusión, no rellenes el hueco con un cero.

### 4. Ejecuta localmente solo cuando aporte valor

La interfaz de línea de comandos permite analizar un repositorio público y limitar la ejecución a comprobaciones concretas. La forma básica documentada es:

```bash
scorecard --repo=github.com/organizacion/repositorio --show-details
```

Si necesitas reducir consumo o responder una pregunta concreta:

```bash
scorecard \
  --repo=github.com/organizacion/repositorio \
  --checks=Branch-Protection,Code-Review,Security-Policy \
  --show-details
```

Usa una versión identificada de la herramienta y anótala en el expediente. Si recurres a una credencial para evitar límites de la API, aplica mínimo privilegio, no la incluyas en comandos compartidos ni la guardes en capturas. Un token con permisos administrativos puede revelar configuraciones que uno público no ve; esa diferencia debe constar al comparar ejecuciones.

En proyectos propios, la [acción oficial de Scorecard](https://github.com/ossf/scorecard-action) puede publicar resultados y presentarlos como SARIF o alertas. Instalarla modifica la automatización del repositorio y exige revisar permisos y fijación de dependencias: no lo hagas en repositorios ajenos ni como parte de una simple observación OSINT.

### 5. Desagrega, prioriza y corrobora

No ordenes candidatos solo por la nota global. Selecciona las comprobaciones relacionadas con tu modelo de riesgo, lee sus detalles y asigna a cada hallazgo uno de estos estados:

- `observado`: la evidencia pública confirma el hecho limitado;
- `no observado`: no se detectó, sin afirmar ausencia;
- `inconcluso`: faltan permisos, datos o aplicabilidad;
- `contradicho`: otra fuente fiable muestra que la heurística no describe bien el caso;
- `pendiente`: hace falta una prueba autorizada o respuesta del mantenedor.

Corrobora con fuentes independientes y primarias: historial de cambios, activos de versión, política de seguridad, documentación de construcción, avisos y configuración pública. Para una muestra pequeña, inspecciona manualmente los elementos que sostienen la decisión.

### 6. Redacta una conclusión proporcional

Una conclusión útil enlaza evidencia, límite y acción:

> Resultado consultado el 5 de noviembre de 2026 para el commit indicado. La comprobación no detectó revisión en la muestra observada; no se concluye que nunca exista. Antes de adoptar el componente, revisar manualmente los cambios de las dos versiones candidatas y solicitar al proyecto una descripción de su proceso por el canal oficial.

Evita etiquetas públicas como «repositorio inseguro» basadas en una ejecución automática. Si detectas un posible problema explotable, sigue la política de divulgación coordinada del proyecto; no publiques detalles operativos para demostrar que la señal era correcta.

## Limitaciones y falsos positivos

### Visibilidad desigual

Algunas configuraciones solo son accesibles con determinados permisos. Dos ejecuciones sobre el mismo commit pueden producir distinto detalle si una usa una credencial administrativa y otra información pública. Registra ese alcance y no compares resultados como si fueran equivalentes.

### Detección basada en convenciones

La automatización reconoce nombres, ubicaciones, proveedores y patrones conocidos. Un proyecto puede aplicar una práctica de otra manera y recibir una señal baja. También puede cumplir la forma visible sin que el proceso funcione bien: un fichero de política vacío o una herramienta configurada pero ignorada no aportan la misma confianza que una práctica operativa.

### Frescura y mutabilidad

Ramas, reglas, *workflows*, dependencias y lanzamientos cambian. Un resultado histórico es evidencia sobre un estado observado, no una propiedad permanente. Conserva commit, fecha, fuente y versión de Scorecard; programa una nueva consulta cuando cambie la dependencia o antes de renovar la decisión.

### Repositorio no equivale a paquete

Scorecard observa principalmente señales alrededor del proyecto y su repositorio. La decisión suele recaer sobre un artefacto distribuido. Hay que verificar por separado quién publica el paquete, cómo se construye, si la versión corresponde al código y qué procedencia o firma puede comprobarse.

### El agregado comprime desacuerdos

Dos proyectos pueden compartir nota total con perfiles de riesgo muy diferentes. Una media ponderada puede ocultar un cero crítico para tu contexto o premiar controles irrelevantes para la decisión. Conserva siempre el vector de comprobaciones y sus estados inconclusos.

## Buenas prácticas de OPSEC, ética y privacidad

- Limita el análisis a información pública, proyectos propios o entornos con autorización expresa.
- No crees incidencias, comentarios ni tráfico repetitivo para «probar» si un proyecto está mantenido.
- Respeta límites de las APIs y reutiliza resultados recientes cuando respondan la pregunta.
- Usa cuentas y tokens separados para investigación; aplica mínimo privilegio y elimina secretos de salidas, historiales y capturas.
- Minimiza datos personales de contribuidores. Para evaluar revisión importa el proceso, no elaborar perfiles de individuos.
- Separa señales técnicas de atribuciones: un *workflow* vulnerable no demuestra intención maliciosa.
- Ofrece al proyecto un canal para contextualizar un hallazgo antes de publicar una conclusión perjudicial.
- Conserva tanto los resultados favorables como los desfavorables para evitar selección interesada de evidencias.

## Checklist operativo

- [ ] La pregunta de decisión y el modelo de riesgo están escritos.
- [ ] Repositorio, paquete, versión y commit corresponden entre sí.
- [ ] La consulta conserva fecha, origen, herramienta y alcance de permisos.
- [ ] Los resultados inconclusos permanecen separados de los fallos.
- [ ] Cada señal decisiva se ha contrastado con evidencia primaria.
- [ ] La nota agregada no sustituye el detalle de comprobaciones.
- [ ] Se ha revisado la correspondencia entre código y artefacto publicado.
- [ ] La conclusión distingue observación, inferencia y recomendación.
- [ ] El informe evita datos personales y detalles que faciliten abuso.
- [ ] Existe una fecha de caducidad o condición de reevaluación.

## Alternativas y siguientes pasos

Scorecard responde a preguntas sobre prácticas observables, no a todas las preguntas de una cadena de suministro. Combínalo según el caso con:

- **OSV** y los avisos del propio proyecto para vulnerabilidades conocidas, recordando que ausencia de registros no prueba ausencia de fallos;
- **SPDX o CycloneDX** para inventariar componentes de un artefacto mediante SBOM;
- **Sigstore** y metadatos de procedencia para verificar firmas y atestaciones;
- **SLSA** para razonar sobre integridad del proceso de construcción;
- revisión manual de cambios, pruebas y documentación para cubrir lo que una heurística no observa.

El takeaway es sencillo: **usa OpenSSF Scorecard para formular mejores preguntas, no para delegar el juicio**. El próximo paso práctico puede ser una matriz de decisión que asigne a cada comprobación relevancia, evidencia de corroboración, responsable y fecha de caducidad. Como siguiente tema merece la pena estudiar cómo contrastar un SBOM en SPDX o CycloneDX con el artefacto real sin confundir inventario declarado con composición demostrada.
