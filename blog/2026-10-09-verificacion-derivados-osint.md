---
title: "Verificación de derivados en OSINT: corregir el dato sin dejar gráficos huérfanos"
slug: /verificacion-derivados-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, automation, privacy]
date: 2026-10-09
image: /img/blog/2026-10-09-verificacion-derivados-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando el grafo de impacto de una corrección OSINT](/img/blog/2026-10-09-verificacion-derivados-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un equipo corrige una fila de su dataset maestro y vuelve a publicar el CSV. La tabla ya contiene el valor bueno, pero la portada conserva el gráfico anterior, el informe mensual repite la cifra equivocada y una alerta programada sigue citando el resultado antiguo. **Corregir la fuente no corrige automáticamente todo lo que aprendió, calculó o publicó a partir de ella.**

La verificación de derivados sirve para responder una pregunta operativa: cuando cambia o se invalida una evidencia, ¿qué artefactos quedan potencialmente afectados, cuáles deben regenerarse y cómo demostramos que ya no transportan el dato erróneo? La respuesta no es «reconstruirlo todo», sino mantener un grafo de impacto suficientemente preciso y cerrar cada corrección con pruebas observables.

<!-- truncate -->

Todas las entidades, cifras, rutas, hashes e identificadores del caso práctico son ficticios. El método se aplica a materiales propios, públicos o adquiridos con autorización; no justifica recuperar información retirada por privacidad, conservar copias innecesarias ni ampliar la exposición de personas.

## Qué es un derivado (y por qué se queda atrás)

Un **derivado** es un artefacto producido total o parcialmente a partir de otro: una tabla limpia desde un CSV, un gráfico desde esa tabla, un PDF desde el gráfico o una alerta desde una métrica calculada. También puede ser menos obvio: una frase copiada a una cronología, una miniatura almacenada en caché o una conclusión incorporada a una presentación.

El [modelo PROV-O del W3C](https://www.w3.org/TR/prov-o/) distingue entidades, actividades y relaciones como derivación, revisión e invalidación. Esa separación ayuda a no confundir tres hechos diferentes:

- la fuente `dataset:v3` fue sustituida por `dataset:v4`;
- el gráfico `incidentes-por-mes:v2` se generó usando `dataset:v3`;
- una ejecución posterior produjo `incidentes-por-mes:v3` usando la versión corregida.

Un nombre de archivo no expresa por sí solo esas relaciones. Tampoco basta el momento de modificación: un informe puede haberse abierto ayer sin haber sido regenerado, y una salida reproducida hoy puede seguir leyendo una caché antigua.

El objetivo práctico es conservar **identidad, versión y dependencia**. Cada nodo representa una versión concreta de una fuente o salida; cada arista explica qué entrada utilizó una transformación para producir otra versión. Así puede recorrerse el grafo desde el objeto corregido hacia sus descendientes sin atribuir dependencias por simple proximidad.

## Caso ficticio: una cifra corregida y cuatro destinos

El Observatorio Delta publica un fichero abierto sobre incidencias marítimas. A las 09:10 corrige el recuento de la región ficticia Norte: no eran 148 casos, sino 84. El repositorio contiene estos artefactos:

| ID estable | Versión | Tipo | Dependencia relevante |
| --- | --- | --- | --- |
| `fuente-incidencias` | `v17` | CSV sustituido | — |
| `fuente-incidencias` | `v18` | CSV vigente | revisión de `v17` |
| `tabla-mensual` | `v31` | dataset limpio | usó `fuente-incidencias:v17` |
| `grafico-regiones` | `v12` | PNG | usó `tabla-mensual:v31` |
| `informe-octubre` | `v4` | PDF | incluye `grafico-regiones:v12` y una cifra escrita |
| `alerta-variacion` | `v8` | JSON | usó `tabla-mensual:v31` |
| `mapa-puertos` | `v6` | GeoJSON | usó otras columnas de `v17` |

El error no afecta necesariamente a todos los descendientes por igual. El gráfico, la alerta y dos fragmentos del informe dependen del recuento corregido. El mapa leyó el mismo CSV, pero solo columnas de ubicación que no cambiaron. Marcarlo como **potencialmente afectado** es prudente; regenerarlo sin mirar puede ser innecesario.

El equipo necesita distinguir cuatro estados:

1. **Candidato:** existe un camino desde la versión corregida hasta el artefacto.
2. **Afectado:** la transformación consumió el campo, fila o fragmento modificado.
3. **Regenerado:** existe una nueva versión construida desde entradas vigentes.
4. **Verificado:** las comprobaciones de contenido, procedencia y publicación han pasado.

«La tarea terminó» no equivale a «la corrección llegó a todos los destinos».

## Diseñar un grafo de impacto mínimo

### Nodos con identidad verificable

Cada versión debería registrar, como mínimo:

- `artifact_id`: identidad estable de la obra o salida;
- `version_id`: identidad inmutable de esa versión;
- tipo y ubicación controlada;
- instante de adquisición o generación;
- resumen criptográfico del contenido cuando proceda;
- estado: vigente, sustituido, retirado o en cuarentena;
- clasificación de sensibilidad y política de conservación.

Los campos de resumen `Content-Digest` normalizados por el [RFC 9530](https://www.rfc-editor.org/rfc/rfc9530.html) permiten verificar que se recuperaron los mismos bytes, pero no demuestran que esos bytes sean correctos. El hash identifica contenido; la corrección editorial explica por qué dejó de ser utilizable.

### Aristas que expliquen la transformación

Una arista útil no dice solo «A está relacionado con B». Debe indicar:

- qué versión de entrada se usó;
- qué ejecución realizó la transformación;
- qué campos, particiones o fragmentos consumió, si se conocen;
- código, consulta o configuración aplicados;
- instante y resultado de la ejecución;
- si la dependencia fue directa, agregada, manual o inferida.

[OpenLineage](https://openlineage.io/docs/spec/object-model/) modela trabajos, ejecuciones y datasets de entrada y salida. Su [faceta de linaje](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) permite describir dependencias a nivel de dataset y de campo. No hace falta implantar la especificación completa para aprender de ella: evitar el producto cartesiano «toda entrada alimenta toda salida» reduce falsos impactos.

### Relaciones editoriales, no solo técnicas

Un pipeline no ve que una analista copió una cifra a un párrafo. Por eso el inventario debe admitir aristas manuales como `cita`, `resume`, `incluye` o `visualiza`. Los tipos de relación de [DataCite](https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/) —por ejemplo, versión, derivación o suplemento— ofrecen un vocabulario de referencia, aunque un equipo pequeño puede usar un conjunto más corto y documentado.

Registrar una dependencia manual lleva segundos en el momento de publicar. Reconstruirla durante una rectificación puede llevar horas y, aun así, omitir una diapositiva enviada a terceros.

## Flujo recomendado para cerrar una corrección

### 1. Congelar la propagación

Pausa las publicaciones y alertas que dependan de la rama afectada. No borres la evidencia adquirida ni sobrescribas silenciosamente la versión anterior. Márcala como sustituida o inválida, limita su acceso según el riesgo y conserva solo lo necesario para trazabilidad.

La congelación debe tener ámbito: parar la alerta regional no obliga a detener un producto independiente que no consume esos datos.

### 2. Registrar el evento de corrección

Asigna al evento una identidad estable y enlaza:

- versión sustituida y versión vigente;
- alcance conocido del cambio;
- campos o fragmentos afectados;
- motivo comunicable sin repetir información sensible;
- persona o rol responsable de cerrar la revisión.

Si aún no se conoce el alcance, dilo. Un estado `investigando` es más honesto que declarar una reparación completa por haber actualizado el CSV.

### 3. Recorrer descendientes

Parte de la versión corregida y recorre las aristas de salida. Mantén un conjunto de visitados para evitar ciclos y registra por qué cada nodo entró en la cola. El resultado inicial es una lista de candidatos, no una sentencia sobre su contenido.

Prioriza por impacto público y capacidad de seguir propagando el error:

1. APIs, feeds, alertas y datasets reutilizables;
2. conclusiones, cifras destacadas y gráficos públicos;
3. informes, anexos y presentaciones descargables;
4. cachés, miniaturas e índices de búsqueda;
5. copias internas sin distribución.

Una salida retirada por razones legítimas no debe reaparecer para facilitar el análisis. El nodo puede conservar metadatos mínimos de identidad y estado sin retener ni rehidratar el contenido.

### 4. Confirmar el impacto real

Compara el cambio con la dependencia registrada. Si se modificó `conteo_total` y el mapa solo consumió `latitud` y `longitud`, documenta por qué queda fuera. Cuando falte linaje fino, adopta la decisión conservadora: revisa o regenera y marca la incertidumbre.

La granularidad tiene un coste. El linaje de campo es valioso para productos importantes o pipelines estables; para una investigación puntual puede bastar con dependencias de archivo y una nota de alcance. Lo peligroso es presentar un grafo incompleto como inventario exhaustivo.

### 5. Regenerar desde entradas vigentes

No edites el PNG, el PDF o el JSON final para que «parezca correcto». Ejecuta de nuevo la transformación desde la versión vigente, con cachés invalidadas y parámetros registrados. La nueva salida debe recibir otra identidad de versión y conservar el vínculo con la sustituida.

Una ejecución segura comprueba antes de publicar:

- que ninguna entrada está marcada como sustituida, retirada o en cuarentena;
- que los hashes coinciden con el manifiesto de la ejecución;
- que código y configuración son los esperados;
- que el destino no mezcla ficheros nuevos con restos de la ejecución anterior.

### 6. Verificar contenido, procedencia y distribución

Las [aserciones de calidad de OpenLineage](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions/) ilustran cómo asociar resultados de pruebas a un dataset o a sus campos. En OSINT conviene combinar tres familias:

- **Contenido:** la cifra corregida aparece donde debe y el valor antiguo no aparece en campos afectados.
- **Procedencia:** todos los caminos de entrada terminan en versiones vigentes y la ejecución queda identificada.
- **Distribución:** la URL pública, el feed, el archivo descargable y las cachés controladas sirven la versión nueva.

Evita una búsqueda ciega del valor antiguo. El número `148` podría aparecer legítimamente en otra región, una cita histórica o el registro de la corrección. Las pruebas deben estar vinculadas al campo y al contexto, no a una cadena aislada.

### 7. Publicar y cerrar con evidencia

Publica las nuevas versiones, añade una nota visible y avisa a los consumidores conocidos de forma proporcional. Cierra el incidente solo cuando cada candidato tenga una resolución: verificado, no afectado con justificación, retirado o pendiente con responsable y plazo.

Un cierre útil conserva un manifiesto como este:

```yaml
correction_id: corr-2026-10-09-01
replaced: fuente-incidencias:v17
current: fuente-incidencias:v18
resolved:
  - artifact: grafico-regiones:v13
    previous: grafico-regiones:v12
    status: verified
    checks: [content, provenance, public-url]
  - artifact: mapa-puertos:v6
    status: not-affected
    reason: "solo consumió columnas de ubicación sin cambios"
pending: []
```

Es un ejemplo ficticio de estructura, no un estándar. Lo importante es que el cierre pueda auditarse sin depender de la memoria de quien ejecutó la reparación.

## Limitaciones y falsos positivos

### El linaje observado nunca es todo el linaje

Una captura pegada en un chat, un fichero descargado por un tercero o una cifra copiada a mano pueden quedar fuera. El grafo describe lo que el equipo registró y controla. La comunicación pública de la corrección sigue siendo necesaria para consumidores desconocidos.

### Una dependencia no implica impacto semántico

Que dos nodos estén conectados no demuestra que el cambio altere la salida. Regenerar todo puede desperdiciar tiempo y provocar nuevas diferencias irrelevantes; excluir demasiado pronto puede dejar errores vivos. La solución es guardar la razón de inclusión o exclusión.

### Reproducible no significa verdadero

Un pipeline puede reproducir perfectamente una conclusión equivocada. Los hashes, manifiestos y ejecuciones repetibles demuestran continuidad técnica. La verdad factual exige contrastar fuentes, contexto y razonamiento.

### Las cachés crean versiones invisibles

CDN, navegadores, miniaturas sociales, buscadores y consumidores externos pueden servir copias antiguas. Documenta qué capas controlas, purga solo las necesarias y verifica desde fuera. No prometas una desaparición global que no puedes observar.

### La precisión excesiva también filtra

Un grafo de procedencia puede revelar rutas internas, fuentes sensibles, nombres de personas o ubicaciones de almacenamiento. Separa el registro operativo detallado del resumen público, aplica control de acceso y minimiza logs. La trazabilidad no exige publicar todo el mapa.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja con identificadores de artefactos, no con perfiles personales, salvo necesidad legítima y documentada.
- Conserva la versión errónea solo durante el plazo requerido para auditoría, litigio o reproducción controlada.
- No incluyas el dato sensible retirado dentro de la nota que pretende retirarlo.
- Usa ejemplos y pruebas sintéticas para ensayar recorridos, ciclos y regeneraciones.
- Separa quién corrige, quién verifica y quién autoriza la republicación cuando el impacto sea alto.
- Registra incertidumbre, límites de cobertura y decisiones de exclusión.
- No uses el grafo para ampliar el alcance de una investigación sobre personas ni para descubrir copias que no necesitas tratar.

## Alternativas y siguientes pasos

Un equipo pequeño puede empezar con un manifiesto por publicación y una tabla de dependencias en Git. Un pipeline más estable puede emitir eventos de linaje y cargar el grafo en un catálogo. Si el trabajo es principalmente documental, una matriz «fuente × entregable» suele ser más útil que desplegar una plataforma.

La herramienta importa menos que tres propiedades:

1. cada salida apunta a entradas versionadas;
2. una corrección permite enumerar descendientes;
3. el cierre exige verificar contenido, procedencia y distribución.

No conviertas el catálogo en otra fuente de verdad abandonada. Contrástalo periódicamente con ejecuciones reales, enlaces públicos y artefactos almacenados.

## Checklist de cierre

- [ ] La corrección tiene identidad, alcance y responsable.
- [ ] La versión sustituida no se usa en nuevas ejecuciones.
- [ ] Se recorrieron todos los descendientes registrados.
- [ ] Cada candidato tiene resolución y justificación.
- [ ] Las cachés se invalidaron donde correspondía.
- [ ] Los derivados afectados se regeneraron desde entradas vigentes.
- [ ] Las pruebas verifican campos y contexto, no cadenas aisladas.
- [ ] URLs, feeds y descargas sirven las versiones nuevas.
- [ ] Los consumidores conocidos recibieron un aviso proporcional.
- [ ] El registro no expone datos personales ni rutas sensibles.
- [ ] Los límites de cobertura están declarados.
- [ ] La corrección técnica no se presenta como garantía de verdad factual.

El takeaway accionable es concreto: elige una cifra de prueba, cámbiala en una copia sintética de la fuente y recorre el grafo hasta cada salida pública. Debes poder explicar **por qué cada artefacto fue regenerado o descartado, con qué entradas se construyó y qué comprobación cerró la tarea**. Si solo puedes señalar el CSV corregido, aún has reparado un nodo, no el impacto.

Como siguiente tema, sería útil estudiar las **pruebas de no regresión para correcciones OSINT**: cómo convertir un error real en una propiedad o fixture sintético que impida reintroducirlo sin conservar datos sensibles.

## Fuentes consultadas

- [W3C: PROV-O, The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [OpenLineage: Object Model](https://openlineage.io/docs/spec/object-model/)
- [OpenLineage: Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/)
- [OpenLineage: Data Quality Assertions Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/data_quality_assertions/)
- [DataCite Metadata Schema: relationType](https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/)
- [RFC 9530: Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html)
