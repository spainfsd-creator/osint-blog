---
title: "Caducidad de fixtures OSINT: conservar la prueba sin acumular el caso real"
slug: /caducidad-fixtures-osint
authors: [osint-writter]
tags: [osint, methodology, testing, data, automation, privacy]
date: 2026-10-11
image: /img/blog/2026-10-11-caducidad-fixtures-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial del ciclo de vida de fixtures sintéticos en un pipeline OSINT](/img/blog/2026-10-11-caducidad-fixtures-osint.png)

*Imagen generada mediante inteligencia artificial.*

Una prueba creada después de un incidente lleva cuatro años en verde. Nadie recuerda qué defecto protege, el formato de entrada ya cambió y el fichero conserva nombres que pertenecían a un caso real. Borrarla a ciegas puede reabrir el fallo; mantenerla «por si acaso» prolonga un riesgo que el equipo dejó de evaluar. **Un fixture útil no es un fósil: necesita propósito, propietario y una fecha de revisión.**

Gestionar la caducidad de fixtures OSINT consiste en conservar la propiedad que hizo valiosa una prueba mientras se reduce el dato, el acoplamiento y el coste que ya no aportan cobertura. El objetivo no es que cada caso de prueba viva para siempre, sino que cada uno pueda responder por qué existe, qué comportamiento vigila y bajo qué condiciones debe renovarse, sintetizarse o retirarse.

<!-- truncate -->

Todos los nombres, rutas, fechas, registros y organizaciones de este artículo son ficticios. El método se aplica a datos públicos o autorizados dentro de entornos de prueba; no justifica copiar expedientes reales a un repositorio, conservar información retirada ni ampliar la observación de personas.

## Qué caduca realmente

En este artículo, un **fixture** es una entrada controlada que prepara el estado necesario para ejecutar una prueba: puede ser una fila CSV, una respuesta HTTP grabada, un documento mínimo, una secuencia de eventos o un pequeño conjunto de entidades relacionadas. No debe confundirse con la evidencia original ni con una copia de seguridad del caso.

La documentación de [pytest sobre fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) explica cómo su ámbito determina cuándo se crea y destruye el estado de prueba. Aquí añadimos otra dimensión: el ciclo de vida editorial y de privacidad del contenido almacenado. Un archivo puede seguir cargando correctamente y estar, sin embargo, conceptualmente caducado.

Conviene separar cinco fechas:

1. **Creación:** cuándo se incorporó el fixture.
2. **Última ejecución:** cuándo participó por última vez en una suite.
3. **Último fallo útil:** cuándo detectó una regresión real.
4. **Última revisión:** cuándo alguien comprobó propósito, datos y vigencia.
5. **Próxima revisión:** cuándo debe volver a decidirse su destino.

La última ejecución no sustituye a la revisión. Un test puede pasar a diario mientras valida una ruta muerta, compara una salida obsoleta o conserva información innecesaria.

### Caducar no significa borrar automáticamente

La fecha de revisión es un disparador de decisión, no una orden de eliminación. Al llegar, el fixture puede:

- mantenerse sin cambios, si sigue siendo mínimo, válido y necesario;
- regenerarse para un esquema o contrato nuevo;
- sustituirse por un ejemplo sintético más pequeño;
- dividirse, si mezcla varios comportamientos;
- archivarse fuera de la suite activa, con acceso y plazo justificados;
- retirarse, conservando solo la explicación del defecto y del control sustituto.

El [artículo 5 del RGPD](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679) recoge los principios de minimización y limitación del plazo de conservación. No fija un número mágico de días: exige que el dato sea adecuado, pertinente y limitado a lo necesario, y que no permita identificar a personas durante más tiempo del necesario para la finalidad. Que algo esté en una carpeta llamada `tests` no lo excluye de ese razonamiento.

## Caso legítimo: el parser que ya no recibe aquel documento

El observatorio ficticio **Faro Abierto** transforma boletines públicos en estadísticas agregadas. En 2024, un salto de línea dentro de una celda desplazó una columna y atribuyó una cantidad a la región equivocada. El equipo corrigió el parser y guardó el boletín completo como fixture de no regresión.

En 2026 revisa la suite:

- la fuente ya publica JSON con un esquema versionado;
- el importador del formato antiguo se conserva solo para reproducibilidad;
- el fixture contiene nombres y notas libres irrelevantes para el defecto;
- la aserción únicamente necesita tres columnas, dos filas y el salto de línea;
- existe un registro del incidente, pero no enlaza con la prueba.

La respuesta responsable no es borrar el test porque sea antiguo ni conservar íntegro el boletín porque una vez fue público. Faro Abierto crea un contraejemplo sintético de dos filas, verifica que hace fallar la versión defectuosa y pasar la corregida, enlaza el nuevo fixture con el registro del incidente y retira la copia real conforme a su política.

Lo que sobrevive es la **forma mínima del fallo**. Lo que desaparece es el contenido que no participa en la propiedad comprobada.

## Flujo recomendado

### 1. Inventariar antes de tocar

Empieza por cada fixture, no por cada carpeta. Un inventario mínimo puede vivir junto al test en YAML:

```yaml
id: fx-csv-salto-linea-001
owner: equipo-ingesta
purpose: "Impide desplazar la columna region cuando una nota contiene un salto de linea"
origin: synthetic-from-incident
contains_personal_data: false
created: 2024-06-18
last_reviewed: 2026-10-11
review_after: 2027-04-11
schema: bulletin-v1
tests:
  - test_multiline_note_keeps_region
supersedes: fx-boletin-completo-2024
```

No conviertas este manifiesto en otra colección de datos sensibles. Registra categorías y decisiones, no nombres, URLs privadas ni fragmentos del expediente. Si no puedes identificar qué prueba consume un archivo, trátalo como deuda pendiente de aclaración, no como basura confirmada.

### 2. Clasificar el riesgo y el valor

Evalúa dos ejes por separado:

| Pregunta | Señal de conservar o renovar | Señal de retirar o sustituir |
|---|---|---|
| ¿Qué defecto detecta? | Propiedad concreta y aún relevante | «Siempre ha estado ahí» |
| ¿Lo cubre otro control? | Cobertura única demostrable | Control equivalente más pequeño |
| ¿Representa una interfaz vigente? | Formato activo o compatibilidad mantenida | Ruta retirada sin obligación de reproducirla |
| ¿Qué datos contiene? | Sintéticos y mínimos | Identificadores, texto libre o metadatos reales innecesarios |
| ¿Es estable? | Resultado determinista | Depende de red, fecha o servicio vivo |
| ¿Tiene responsable? | Equipo y revisión asignados | Archivo huérfano |

Una antigüedad alta puede aumentar la prioridad de revisión, pero no prueba inutilidad. Del mismo modo, que un fixture sea reciente no garantiza que esté minimizado.

### 3. Demostrar la cobertura antes de sustituir

Antes de retirar el archivo original, ejecuta una prueba de equivalencia práctica:

1. la versión anterior del código debe fallar con el fixture nuevo;
2. la versión corregida debe pasar;
3. la aserción debe vigilar la misma propiedad;
4. el caso sintético no debe introducir otra causa de fallo;
5. la suite completa debe seguir detectando conflictos con otras etapas.

En transformaciones de datos, [dbt permite entradas estáticas](https://docs.getdbt.com/docs/build/unit-tests) en formatos `dict`, CSV o SQL y recomienda limitar los datos simulados a las columnas relevantes. Esa idea es trasladable: si el error depende de tres campos, copiar treinta columnas «para que parezca real» suele aumentar el riesgo y el mantenimiento, no la fidelidad de la prueba.

### 4. Sintetizar por propiedad, no por maquillaje

Cambiar `Ana` por `Persona 1` no basta si permanecen combinaciones de edad, ubicación, empleo o cronología que permiten reconocer a alguien. [NIST SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) advierte que quitar identificadores directos no elimina necesariamente el riesgo de reidentificación y contempla, entre otras opciones, publicar datos sintéticos.

Para un fixture de regresión, la síntesis más segura suele ser manual y pequeña:

- conserva tipos, cardinalidades y relación causal;
- reemplaza valores con ejemplos ficticios diseñados para la prueba;
- elimina campos que la transformación no lee;
- rompe combinaciones singulares heredadas del caso;
- vuelve a comprobar el directorio completo, no solo las columnas evidentes;
- documenta qué propiedad conserva y qué realismo sacrifica.

Un fixture sintético no demuestra que la fuente real sea correcta. Demuestra que el software responde como se espera ante una forma de entrada controlada.

### 5. Registrar sustitución e invalidación

No borres el vínculo histórico al cambiar de fixture. Conserva un registro pequeño como este:

```text
incidente INC-042
  -> motivó el control TEST-017
  -> usó inicialmente FX-REAL-009
  -> fue sustituido por FX-SYN-014 el 2026-10-11
  -> FX-REAL-009 quedó invalidado y se eliminó según RET-02
```

[PROV-O del W3C](https://www.w3.org/TR/prov-o/) ofrece relaciones para expresar derivación, generación, atribución e invalidación. No hace falta desplegar una ontología completa: basta con conservar identidades estables y relaciones explícitas para evitar que un borrado rompa la memoria del control.

El hash del fichero retirado puede ayudar a verificar una referencia interna, pero no es una copia inocua del contenido ni prueba por sí solo qué contenía. Si el propio hash puede actuar como identificador o permitir confirmar la presencia de un archivo sensible, evalúa también si necesitas conservarlo y quién puede verlo.

### 6. Automatizar avisos, no decisiones irreversibles

La CI puede detectar fixtures sin manifiesto, propietarios vacíos, fechas vencidas, archivos demasiado grandes o patrones de datos personales. También puede abrir una incidencia o bloquear nuevas incorporaciones que incumplan la política.

La eliminación automática al vencer una fecha es más arriesgada. Antes hay que comprobar dependencias, obligaciones, copias, artefactos de CI y controles sustitutos. Una regla prudente es:

```text
vigente -> revision_pendiente -> sustituido_o_renovado -> retirado_verificado
```

Cada transición debe producir evidencia observable. «Retirado verificado» significa que el fixture ya no está en la suite, artefactos publicados, cachés de CI ni ubicaciones bajo control del equipo; no significa afirmar que ninguna copia pueda existir fuera de ese ámbito.

## Cómo fijar el periodo de revisión

No existe una frecuencia universal. Define el intervalo según riesgo y cambio:

- **Revisión corta:** fixtures derivados de incidentes, texto libre, multimedia o fuentes con personas identificables.
- **Revisión media:** respuestas de API reducidas, formatos que cambian con frecuencia o pruebas ligadas a contratos externos.
- **Revisión larga:** generadores puramente sintéticos, esquemas estables y casos matemáticos sin datos personales.
- **Revisión por evento:** retirada de la fuente, cambio de finalidad, nueva versión de esquema, solicitud de supresión, incidente de privacidad o cierre del componente.

La fecha debe tener una justificación legible. «Seis meses porque sí» solo sustituye una retención indefinida por una cifra arbitraria.

## Limitaciones y falsos positivos

### Un test que nunca falla no está necesariamente muerto

Puede proteger una frontera estable y valiosa. Compruébalo mutando temporalmente la condición que vigila o ejecutándolo contra la versión defectuosa conocida. Si deja de distinguir el comportamiento correcto del incorrecto, entonces sí hay una señal fuerte de obsolescencia.

### La cobertura no justifica cualquier retención

Un fixture puede detectar un fallo importante y seguir siendo desproporcionado. La solución suele ser reducirlo o sintetizarlo, no aceptar el fichero completo como coste inevitable.

### El esquema nuevo puede ocultar una compatibilidad antigua

Antes de retirar ejemplos de un formato legado, confirma si aún existen archivos históricos que deban reprocesarse legítimamente. Si se mantiene esa capacidad, conserva un caso mínimo representativo y separa su suite de la ruta principal.

### «Anónimo» no equivale a irreconocible

Los identificadores indirectos, la rareza de una combinación y el texto libre pueden reconstruir contexto. Evalúa el conjunto, incluidos nombres de archivo, metadatos, snapshots, logs y mensajes de error.

### La procedencia no certifica la verdad

Saber de qué incidente nació un fixture mejora la trazabilidad. No demuestra que la fuente original fuera exacta, que la atribución fuese correcta ni que el test cubra todos los casos.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa ejemplos sintéticos por defecto y datos reales solo con finalidad, base y controles documentados.
- No descargues de nuevo una fuente retirada para «refrescar» un fixture.
- Mantén secretos, tokens, cookies y cabeceras de autenticación fuera de capturas y grabaciones HTTP.
- Revisa contenido incrustado: EXIF, propiedades de documentos, comentarios, rutas locales y texto OCR.
- Limita acceso, copias y duración incluso cuando el repositorio sea privado.
- Separa el registro del incidente de los datos necesarios para reproducir el defecto.
- Haz que las solicitudes de borrado o rectificación activen una revisión de fixtures y derivados.
- Evita que los fallos de CI vuelquen el contenido completo del ejemplo en logs.
- Documenta el ámbito de la eliminación y cualquier copia que no controles.
- Escala a revisión jurídica o de protección de datos cuando la finalidad o la base de conservación no estén claras.

## Alternativas y siguientes pasos

Si un fixture estático se degrada con rapidez, considera un generador determinista con semilla fija. Si necesitas muchas combinaciones, usa property-based testing y conserva solo los contraejemplos minimizados que aporten una regresión distinta. Si el problema está en el contrato de una API, una especificación de esquema más unos pocos ejemplos de frontera puede ser mejor que una respuesta real completa.

Para casos visuales o documentales, separa estructura y contenido: una plantilla construida desde cero puede reproducir páginas, bloques o metadatos relevantes sin copiar el expediente. Si el formato propietario impide hacerlo, reduce el acceso, define una retención explícita y registra por qué no existe aún un sustituto seguro.

## Checklist de cierre

- [ ] Cada fixture tiene propósito, propietario y prueba consumidora.
- [ ] La próxima revisión responde a riesgo o cambio, no a una cifra arbitraria.
- [ ] Se conoce si contiene datos reales, sintéticos, seudonimizados o personales.
- [ ] Los campos y registros son los mínimos necesarios para la propiedad probada.
- [ ] El sustituto hace fallar la versión defectuosa y pasar la corregida.
- [ ] La aserción sigue vigilando el mismo comportamiento.
- [ ] La sustitución mantiene el vínculo con el incidente sin conservar su contenido.
- [ ] La retirada contempla repositorio, artefactos, cachés y copias bajo control.
- [ ] Los logs no imprimen el fixture completo.
- [ ] La revisión humana es proporcional al posible impacto sobre personas.
- [ ] La trazabilidad no se presenta como garantía de verdad factual.

El takeaway accionable es simple: elige hoy el fixture real más antiguo de tu suite, escribe en una frase la propiedad que protege y trata de reproducirla con el conjunto sintético más pequeño posible. No retires el original hasta demostrar equivalencia; cuando lo hagas, conserva la decisión y el control, no el expediente.

Como siguiente tema, convendría estudiar los **generadores deterministas de datos sintéticos para OSINT**: cómo producir casos variados y reproducibles sin convertir las semillas, plantillas o logs en otra vía de exposición.

## Fuentes consultadas

- [Reglamento (UE) 2016/679, artículo 5: principios relativos al tratamiento](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32016R0679)
- [NIST SP 800-188: De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final)
- [pytest: How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [dbt Developer Hub: Unit tests](https://docs.getdbt.com/docs/build/unit-tests)
- [W3C: PROV-O, The PROV Ontology](https://www.w3.org/TR/prov-o/)
