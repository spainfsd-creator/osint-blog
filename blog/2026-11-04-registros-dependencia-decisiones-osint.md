---
title: "Registros de dependencia de decisiones en OSINT: retirar excepciones sin reconstruir el caso"
slug: /registros-dependencia-decisiones-osint
authors: [osint-writter]
tags: [osint, methodology, data, verification, investigation, privacy]
date: 2026-11-04
image: /img/blog/2026-11-04-registros-dependencia-decisiones-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una fuente provisional permitió entregar un informe a tiempo. Días después, la fuente oficial la contradice y el equipo corrige el documento original. Parece resuelto, hasta que alguien pregunta qué ocurrió con el panel, la alerta y las dos decisiones que reutilizaron aquella conclusión. **Si una excepción puede propagarse pero su retirada no, el problema no es solo la calidad de la evidencia: es que nadie registró qué dependía de qué.**

![Analista siguiendo las dependencias entre evidencias, informes y decisiones para retirar una excepción vencida](/img/blog/2026-11-04-registros-dependencia-decisiones-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Un registro de dependencia de decisiones sirve para contestar una pregunta operativa: cuando cambia, caduca o se invalida una pieza de evidencia, ¿qué productos y actuaciones necesitan revisión? No promete demostrar causalidad ni decidir automáticamente. Conserva una ruta comprobable desde las fuentes hasta los usos autorizados para que corregir no exija reconstruir el expediente desde cero.

## Qué es y para qué sirve

Un registro de decisiones tradicional conserva qué se decidió, por qué, con qué alternativas y quién asumió la decisión. La guía del [Government Digital Service sobre decisiones de arquitectura](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html) recomienda preservar el contexto y mantener el registro bajo control de versiones. En una investigación, el [Health and Safety Executive](https://www.hse.gov.uk/foi/internalops/og/ogprocedures/investigation/decisionlog.htm) describe el *Key Decision Log* como un registro contemporáneo de las decisiones que afectan al curso de la investigación y de sus razones.

Para OSINT falta una capa adicional: representar las dependencias entre la evidencia, las afirmaciones, los productos y sus usos. El registro no debería ser una narración lineal, sino un pequeño grafo dirigido y versionado.

Sus nodos pueden ser:

- **fuentes y capturas:** una página pública, una descarga, una consulta o una respuesta oficial;
- **artefactos:** una extracción, tabla, transcripción, imagen, cálculo o conjunto de datos;
- **afirmaciones:** proposiciones concretas, no temas vagos;
- **decisiones de evidencia:** aceptar, rechazar, mantener inconcluso o permitir un uso provisional;
- **productos:** informes, paneles, alertas, fichas y exportaciones;
- **acciones:** publicar, escalar, revisar o retirar, sin almacenar detalles personales innecesarios.

Las aristas expresan relaciones limitadas y verificables: `deriva_de`, `usa`, `corrobora`, `contradice`, `autoriza`, `incluye` o `activa`. El modelo [W3C PROV-O](https://www.w3.org/TR/prov-o/) ofrece una base útil con entidades, actividades y agentes, además de relaciones de uso, generación, derivación, atribución e invalidación. No obliga a desplegar RDF: una tabla o un fichero JSON puede adoptar esas ideas sin convertir el registro en un proyecto semántico.

### Lo que el registro no demuestra

Una flecha no prueba que una fuente sea verdadera, que dos entidades sean idénticas ni que una decisión haya sido correcta. Solo declara una dependencia registrada. Tampoco sustituye las notas analíticas, la conservación de evidencias, el control de acceso ni la revisión humana.

Esta distinción evita un error frecuente: confundir **linaje** con **validez**. Saber que un panel deriva de una tabla ayuda a localizar el impacto de una corrección; no certifica que la tabla interprete bien el mundo.

## Caso de uso legítimo con un ejemplo ficticio

La organización ficticia `Faro Norte` realiza debida diligencia sobre proveedores para decidir qué expedientes requieren una revisión documental más profunda. No perfila a particulares ni toma decisiones automatizadas.

Una nota pública de una asociación sectorial afirma que `Puerto Claro SL` ha cambiado de administrador. El registro mercantil accesible al equipo aún no refleja el cambio. Como la conclusión solo se usará para priorizar una comprobación interna y reversible, una responsable autoriza durante 48 horas la afirmación provisional `A-104`.

El equipo registra estas dependencias:

```text
F-31 nota sectorial (captura y hash)
  -> E-18 extracción del nombre y fecha
  -> A-104 "existe un cambio de administrador pendiente de confirmar"
  -> X-07 excepción: solo priorización interna, vence 2026-11-06T10:00Z
  -> I-22 ficha de investigación v3
  -> P-09 cola privada de revisión
```

La afirmación no dice «el nuevo administrador es X» porque la fuente disponible no basta para sostenerlo. El alcance permitido también queda explícito: priorizar una revisión, no publicar, atribuir conducta ni contactar con terceros.

Al día siguiente llega una certificación oficial que descarta el cambio. El equipo invalida `A-104`, cierra `X-07` y consulta el grafo hacia delante. Descubre dos descendientes: la ficha `I-22` y la cola `P-09`. Retira la prioridad, crea `I-23` con la corrección y conserva la versión anterior como historial restringido. No necesita buscar el nombre por carpetas, chats y hojas de cálculo para adivinar dónde viajó la afirmación.

## Diseña el registro desde las preguntas de retirada

Antes de elegir una base de datos, formula las consultas que el equipo deberá responder bajo presión:

1. ¿Qué productos contienen o resumen esta afirmación?
2. ¿Qué decisiones siguen abiertas y dependen de ella?
3. ¿Qué versión estaba vigente cuando se autorizó cada uso?
4. ¿Qué excepciones han vencido sin cerrar sus descendientes?
5. ¿Existe algún derivado público o difícil de revertir?
6. ¿Quién debe revisar cada elemento y en qué plazo?

Si el esquema no responde a esas preguntas, añadir más campos no arreglará el diseño. La unidad básica debe ser una afirmación identificable y versionada, no «el caso completo». Un informe puede contener veinte afirmaciones y solo una depender de una excepción.

### Un esquema mínimo

Una implementación inicial puede separar nodos y relaciones:

```yaml
node:
  id: A-104
  type: claim
  version: 2
  status: invalidated
  created_at: 2026-11-04T09:20:00Z
  invalidated_at: 2026-11-05T14:10:00Z
  owner_role: case_reviewer
  sensitivity: restricted
  retention_class: investigation_record

edge:
  from: I-22
  relation: includes
  to: A-104@2
  recorded_at: 2026-11-04T11:05:00Z
  recorded_by_role: analyst
```

La versión forma parte de la referencia. Si `A-104@3` corrige la afirmación, no debe parecer que `I-22` utilizó retroactivamente la versión nueva. W3C PROV distingue revisión, derivación e invalidación; esa separación resulta más informativa que sobrescribir una fila.

Para linaje automatizado, [OpenLineage](https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md) organiza eventos alrededor de ejecuciones, trabajos y conjuntos de datos, con *facets* para metadatos estándar o personalizados. Su [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) puede describir de qué conjuntos, trabajos y campos deriva un dato. Es una referencia útil para pipelines, pero no modela por sí sola el razonamiento ni la autorización humana: conviene enlazar el evento técnico con el registro de decisión, no fingir que son lo mismo.

## Flujo recomendado

### 1. Identifica la afirmación antes de registrar dependencias

Redáctala de manera falsable y con alcance. «Problemas societarios» no sirve; «la fuente F-31 afirma que existe un cambio de administrador aún no confirmado en el registro oficial» sí permite decidir qué evidencia la sostiene y cuándo deja de ser válida.

Asigna un identificador estable. No uses nombres personales, correos o teléfonos como claves. Además de proteger privacidad, una clave opaca evita que un cambio ortográfico fragmente el grafo.

### 2. Fija la evidencia y su procedencia

Registra URL o localizador, hora de consulta, método, versión y una referencia al artefacto conservado. Cuando sea apropiado, añade hash, cabeceras o metadatos suficientes para detectar cambios. El [Research Data Framework de NIST](https://www.nist.gov/publications/nist-research-data-framework-rdaf-version-15) relaciona la procedencia con la trazabilidad, el seguimiento de ediciones y la posibilidad de volver a revisiones anteriores.

No copies todo el contenido al registro. Guarda la evidencia en un repositorio con controles adecuados y conserva aquí un puntero estable. El grafo necesita saber que un artefacto existe y qué versión se usó; no necesita convertirse en un segundo archivo de datos sensibles.

### 3. Registra la decisión contemporáneamente

Anota estado, razón, alternativas, responsable por rol, fecha, alcance permitido y condición de revisión. Si existe una excepción, enlaza su vencimiento, barreras duras y comprobaciones compensatorias.

Evita justificar después de conocer el resultado. Un registro retrospectivo tiende a limpiar dudas y presentar como inevitable lo que fue provisional. La marca temporal y el historial de cambios son evidencia del proceso, no adornos administrativos.

### 4. Captura dependencias al producir, no al retirar

Cuando un informe incorpora una afirmación, crea la arista en ese momento. Intentar reconstruir todas las relaciones durante un incidente reproduce el problema que el registro pretende resolver.

En procesos manuales puede bastar una plantilla que obligue a citar identificadores. En pipelines, instrumenta la transformación para emitir entradas y salidas. No aceptes una relación automática sin contexto: un fichero leído por un proceso no implica que cada campo haya influido en cada conclusión.

### 5. Propaga estado sin reescribir la historia

Cuando una fuente cambia o una excepción vence:

1. añade un evento de cambio o invalidación;
2. no borres el nodo ni sus relaciones históricas;
3. recorre descendientes hasta los límites definidos;
4. clasifica impacto y reversibilidad;
5. asigna revisión, bloqueo o retirada;
6. registra la resolución de cada descendiente.

Un descendiente no siempre queda invalidado. Puede contener otras evidencias independientes que sostengan la misma conclusión. El cambio debe abrir una revisión proporcionada, no ejecutar un borrado ciego.

### 6. Ensaya la retirada

Selecciona una afirmación sintética, márcala como vencida y mide si el equipo encuentra todos sus derivados. Comprueba también el camino inverso: desde una decisión, ¿puede reconstruirse qué versiones de evidencia se usaron?

Mide tiempo hasta identificar impacto, descendientes sin responsable, aristas creadas tarde y productos que no admiten retirada. Un grafo lleno pero no ejercitado es documentación decorativa.

## Prioridad de revisión sin automatizar la verdad

Al invalidar un nodo, no todos los descendientes merecen la misma respuesta. Una cola interna reversible no equivale a una publicación o a una decisión que afecte a derechos. Puede utilizarse una matriz cualitativa:

| Factor | Menor urgencia | Mayor urgencia |
|---|---|---|
| Exposición | interno y restringido | público o compartido externamente |
| Reversibilidad | recalculable | acción difícil de deshacer |
| Dependencia | evidencia redundante | única base registrada |
| Sensibilidad | datos no personales | datos personales o fuente sensible |
| Vigencia | producto ya retirado | producto activo |

La matriz ordena trabajo; no decide si la afirmación es cierta. La revisión debe comprobar qué papel tuvo el nodo afectado, si existe corroboración realmente independiente y si el producto conserva advertencias visibles.

## Limitaciones y falsos positivos

### Dependencia registrada no es dependencia real

Un informe puede citar una fuente por contexto sin apoyarse en ella, o apoyarse en una hoja auxiliar que nadie enlazó. El registro tendrá falsos positivos y falsos negativos. Conviene distinguir `cita`, `usa_como_evidencia` y `deriva_de`, auditar muestras y permitir que el revisor documente por qué un descendiente no resulta afectado.

### El linaje de datos no captura el razonamiento

Un sistema puede saber que una tabla alimentó un panel, pero no qué juicio transformó un dato ambiguo en una afirmación. La nota de decisión debe conservar alternativas, incertidumbre y alcance. Automatizar el transporte no automatiza la interpretación.

### Los grafos crecen deprisa

Registrar cada consulta, celda y vista genera ruido y desalienta el uso. Define fronteras: afirmaciones materiales, artefactos versionados, productos consumidos y decisiones con consecuencias. Agrega dependencias técnicas de bajo riesgo cuando no se pierda capacidad de retirada.

### La retirada puede amplificar daño

Una notificación demasiado detallada puede redistribuir datos personales o revelar una fuente sensible. El aviso debe identificar el nodo y la acción necesaria sin repetir el contenido. Separa el registro operativo del almacén de evidencias y aplica control de acceso en ambos.

### Un estado inválido no siempre implica borrar

Las obligaciones de archivo, transparencia o defensa jurídica pueden exigir conservar versiones. La respuesta puede ser retirar de circulación, marcar, sustituir o restringir, manteniendo un historial autorizado. Consulta las reglas aplicables; el registro no decide plazos legales.

## Buenas prácticas de OPSEC, ética y privacidad

- Registra identificadores opacos y roles; evita nombres personales en nodos y etiquetas.
- Aplica mínimo privilegio: quien consulta impacto no siempre necesita abrir la evidencia.
- Separa procedencia de contenido y cifra los almacenes sensibles.
- No conviertas el grafo en un mapa de relaciones personales que amplíe el objetivo de la investigación.
- Define retención y borrado por clase de nodo; «por si acaso» no es una política.
- Evita URLs con tokens, consultas privadas o credenciales incrustadas.
- Conserva contradicciones y estados inconclusos; no los aplanes para obtener un grafo limpio.
- Requiere revisión humana antes de publicar, atribuir o ejecutar acciones difíciles de revertir.
- Registra también las exportaciones y copias autorizadas que queden fuera del sistema principal.
- Limita las alertas a quienes puedan actuar y audita accesos al registro.

## Alternativas y siguientes pasos

Para un equipo pequeño, una tabla versionada con `origen`, `destino`, `relación`, `versión`, `estado` y `responsable` puede ser suficiente. Un repositorio Git aporta historial, pero no sustituye controles de acceso ni es apropiado para contenido sensible. Una base relacional permite recorridos con consultas recursivas; una base de grafos ayuda cuando las dependencias son numerosas y cambiantes. OpenLineage encaja mejor cuando el reto principal es observar pipelines de datos.

La elección tecnológica viene después del contrato operativo: qué se registra, cuándo, quién corrige y cómo se ensaya la retirada. Empieza con un solo producto y una sola clase de excepción. Si el equipo no mantiene diez relaciones con disciplina, tampoco mantendrá diez mil por comprar una plataforma.

El takeaway accionable es elegir una excepción abierta y dibujar, en quince minutos, sus descendientes conocidos: afirmaciones, informes, paneles, exportaciones y acciones. Después intenta responder quién retiraría cada uno si la evidencia cambiara hoy. **Cada casilla sin propietario o sin versión es una dependencia real que el sistema todavía trata como memoria informal.**

Como siguiente tema convendría estudiar las **pruebas de retirada y simulacros de revocación**: cómo introducir una invalidación sintética, medir propagación y descubrir copias huérfanas sin tocar expedientes reales.

## Fuentes consultadas

Fuentes primarias consultadas el 4 de noviembre de 2026:

- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [OpenLineage: especificación](https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md)
- [OpenLineage: Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/)
- [GDS Way: Documenting architecture decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- [HSE: Key Decision Log](https://www.hse.gov.uk/foi/internalops/og/ogprocedures/investigation/decisionlog.htm)
- [NIST Research Data Framework, versión 1.5](https://www.nist.gov/publications/nist-research-data-framework-rdaf-version-15)
