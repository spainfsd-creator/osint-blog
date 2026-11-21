---
title: "Hypothesis en OSINT: anotar la web sin confundir una nota con evidencia"
slug: /hypothesis-anotacion-web-osint
authors: [osint-writter]
tags: [osint, tooling, research, verification, methodology, privacy]
date: 2026-11-21
image: /img/blog/2026-11-21-hypothesis-anotacion-web-osint.png
aiDisclosure: generated
humanReviewed: false
---

Una frase decisiva aparece en la página de una licitación. Dos horas después, el organismo corrige el texto, el enlace redirige y el equipo solo conserva una nota que dice «esto demuestra el cambio». **Anotar una fuente ayuda a pensar en común; no preserva por sí solo lo que se observó ni convierte una interpretación en prueba.**

![Equipo OSINT revisando páginas públicas, anotaciones y un registro separado de evidencias](/img/blog/2026-11-21-hypothesis-anotacion-web-osint.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un uso responsable de [Hypothesis](https://web.hypothes.is/) para leer, comentar y revisar fuentes web dentro de una investigación OSINT legítima. El caso, las entidades y los datos son ficticios. La finalidad no es vigilar a personas ni organizar información privada, sino reducir malentendidos entre analistas y conservar la distancia entre **texto observado, nota analítica, verificación y conclusión**.

## Qué es Hypothesis y para qué sirve en OSINT

Hypothesis es un sistema de anotación web. Su cliente se superpone a una página o a un PDF y permite vincular una nota a un fragmento seleccionado, crear notas sobre el documento completo, añadir etiquetas y responder en hilos. Según la [descripción oficial de su arquitectura](https://web.hypothes.is/help/overview-of-the-hypothesis-system/), el servicio almacena y busca anotaciones, gestiona usuarios y grupos y ofrece una API; el cliente puede llegar mediante extensión, integración en la página, proxy o aplicaciones educativas.

En un flujo OSINT, esa capa puede servir para:

- señalar el pasaje exacto que motiva una pregunta;
- separar una cita literal de la interpretación del analista;
- pedir una segunda lectura sin copiar el documento entero a un chat;
- etiquetar estados como `por-verificar`, `corroborado` o `contradicho`;
- discutir una traducción, una fecha o el alcance de una afirmación;
- reunir notas accesibles para un equipo con permisos definidos;
- exportar el trabajo para revisarlo fuera de la plataforma.

No es un capturador forense, una hemeroteca ni un sistema de gestión de expedientes. Una anotación puede mantener el texto seleccionado y un enlace, pero la página de destino puede cambiar, desaparecer o presentar otra versión. Tampoco garantiza que quien anotó interpretara correctamente el fragmento, que la cuenta represente a quien dice representar ni que una etiqueta haya pasado un control de calidad.

### Cuatro objetos que conviene no mezclar

La [guía básica de Hypothesis](https://web.hypothes.is/help/annotation-basics/) distingue anotaciones ligadas a una selección, resaltados, notas de página y respuestas. Para investigar con rigor conviene añadir una distinción operativa propia:

| Objeto | Qué registra | Qué no demuestra |
| --- | --- | --- |
| resaltado | un pasaje que llamó la atención | que sea verdadero o relevante |
| anotación | comentario y etiquetas sobre una selección | que la interpretación esté verificada |
| nota de página | contexto sobre el documento completo | que describa todas sus versiones |
| respuesta | discusión o revisión de una nota | que exista consenso válido |
| ficha de evidencia | fuente, captura, huella, localizador y estado | que la conclusión final sea correcta |

La última fila no la aporta automáticamente la herramienta. Es una pieza del método del equipo.

## Caso de uso legítimo: seguimiento de una convocatoria pública

La asociación ficticia **Observatorio Costa Clara** revisa una convocatoria municipal de subvenciones ambientales. Quiere comprobar cómo cambian los criterios y plazos publicados durante tres semanas, no perfilar a solicitantes ni buscar información sobre empleados públicos.

El equipo trabaja con la página oficial, dos PDF enlazados y el boletín administrativo. Antes de anotar, crea un registro con un identificador por representación:

| ID | Tipo | URL de origen | Observado en | Huella o captura | Estado |
| --- | --- | --- | --- | --- | --- |
| `CC-001` | página HTML | URL oficial ficticia | 2026-11-21 09:15 CET | WARC + SHA-256 | capturado |
| `CC-002` | bases PDF | URL oficial ficticia | 2026-11-21 09:18 CET | PDF + SHA-256 | capturado |
| `CC-003` | boletín | URL oficial ficticia | 2026-11-21 09:27 CET | referencia oficial | corroborado |

Las anotaciones usan esos identificadores. Una nota no dice «han ampliado el plazo», sino algo más comprobable:

> `CC-001`, apartado «Presentación»: la representación observada a las 09:15 muestra «30 de noviembre». Comparar con `CC-002`, página 7, y con la edición vigente del boletín. Estado: `por-verificar`.

Si después aparece una corrección, el equipo no sobrescribe la primera observación. Crea una nueva ficha, relaciona ambas representaciones y documenta qué fuente tiene autoridad normativa.

## Flujo recomendado paso a paso

### 1. Define la pregunta y el límite de recogida

Empieza con una pregunta verificable: «¿qué fechas y requisitos aparecen en cada representación oficial durante el periodo?» es mejor que «encuentra irregularidades». Define dominios, tipos documentales, fechas, criterios de exclusión y datos que no deben recogerse.

Una página pública puede incluir nombres, firmas, teléfonos o comentarios incidentales. Que el navegador permita seleccionarlos no significa que deban entrar en el cuaderno compartido. Aplica minimización desde el principio.

### 2. Decide visibilidad antes de escribir

La configuración de privacidad es parte del diseño, no un detalle para el final. La [ayuda oficial sobre visibilidad](https://web.hypothes.is/help/who-can-see-my-annotations-in-the-web-app/) indica que las anotaciones de la capa pública son públicas por defecto y pueden verse mediante la interfaz y la API. Los resaltados simples son privados; los grupos privados limitan la lectura a sus miembros, aunque un miembro pueda compartir enlaces que seguirán requiriendo pertenecer al grupo.

Para un equipo de investigación:

1. crea un grupo privado específico para el caso;
2. revisa quién puede entrar y quién modera;
3. prueba la visibilidad con una nota ficticia;
4. evita nombres reales y secretos en títulos, etiquetas y comentarios;
5. fija una fecha para revisar miembros, retención y exportaciones.

«Solo yo» puede servir para una lectura inicial, pero no sustituye una política de acceso. Una nota que fue pública pudo ser leída o copiada antes de volverse privada.

### 3. Captura la representación antes de interpretarla

Antes de crear una anotación decisiva, registra la URL canónica y la URL final tras redirecciones, la fecha y zona horaria, el título visible y el identificador de la ficha. Cuando sea legal y proporcionado, conserva una captura reproducible —por ejemplo, WARC, PDF original o respuesta descargada— y calcula una huella.

No afirmes que Hypothesis preserva la página porque conserve el fragmento citado. El anclaje puede quedar huérfano si cambia el texto o el documento. La anotación ayuda a volver al contexto; el artefacto capturado permite explicar qué representación se observó.

### 4. Usa una plantilla de anotación

Una nota libre suele mezclar cita, intuición y conclusión. Una plantilla corta obliga a mostrar el salto lógico:

```text
Fuente: CC-002
Localizador: página 7, apartado 4.2
Observación: el PDF indica «30 de noviembre»
Interpretación: posible plazo aplicable
Comprobación pendiente: contrastar boletín y correcciones
Estado: por-verificar
Responsable / fecha de revisión: equipo documental / 2026-11-22
```

La selección visible no necesita copiarse de nuevo entera. Incluye solo el fragmento mínimo que permita reconocer el punto y evita reproducir material personal o protegido sin necesidad.

### 5. Diseña un vocabulario pequeño y controlado

Las etiquetas facilitan la búsqueda, pero se degradan si cada persona inventa variantes. Empieza con pocas dimensiones:

- estado: `por-verificar`, `corroborado`, `contradicho`, `inconcluso`;
- acción: `revisar-fecha`, `buscar-fuente-primaria`, `validar-traduccion`;
- objeto: `plazo`, `importe`, `requisito`, `correccion`;
- sensibilidad: `minimizar`, `no-exportar`.

No uses etiquetas como `fraude`, `culpable` o `mentira` para sustituir una conclusión argumentada. Si una afirmación queda corroborada, especifica por qué fuente independiente y bajo qué criterio.

### 6. Revisa en dos pasadas

La primera persona anota; la segunda comprueba el fragmento en su contexto y examina la ficha de evidencia. Puede aceptar, discutir o dejar el estado en `inconcluso`. La respuesta debe identificar el motivo: versión distinta, traducción ambigua, documento sin autoridad, fecha incompatible o simple error de lectura.

El número de respuestas no mide fiabilidad. Tres comentarios derivados de la misma página siguen siendo una sola procedencia. Cuenta fuentes independientes, no participantes en el hilo.

### 7. Exporta y reconcilia fuera de la interfaz

La [función oficial de exportación](https://web.hypothes.is/help/exporting-and-importing-annotations/) permite sacar notas accesibles como JSON, texto, CSV o HTML. JSON sirve también para importar anotaciones, mientras que CSV facilita una revisión tabular.

Una exportación periódica puede conservar:

- identificador de anotación;
- autor y fechas de creación y actualización;
- URL y fragmento objetivo;
- cuerpo, etiquetas, grupo y relaciones de respuesta;
- identificador de evidencia enlazado;
- hash y fecha del archivo exportado.

Haz un recuento antes y después. La guía advierte de límites de la importación: las notas importadas aparecen como creadas por quien importa y las respuestas exportadas no se importan como tal. Por eso una exportación es un respaldo analítico, no una migración perfecta de identidad y conversación.

### 8. Automatiza solo lo que puedas auditar

La [API v1 de Hypothesis](https://h.readthedocs.io/en/latest/api-reference/v1/) permite buscar anotaciones por URL, usuario, grupo, etiqueta, texto o cita. La lectura de datos públicos no requiere autorización; el acceso a contenido restringido y las operaciones de escritura sí exigen credenciales adecuadas.

Un uso razonable es generar un inventario de notas `por-verificar` o comprobar que todas enlazan a una ficha existente. No conviene publicar tokens en scripts, descargar anotaciones públicas para perfilar autores ni inferir coordinación a partir de etiquetas coincidentes. Respeta límites, condiciones de uso y finalidad.

## Limitaciones y falsos positivos

### El anclaje puede romperse

Una edición, redirección, cambio de PDF o modificación de la estructura puede impedir que la nota vuelva al pasaje exacto. El fragmento guardado ayuda a diagnosticar el problema, pero no identifica necesariamente qué versión estuvo disponible en cada instante.

### Una URL no siempre identifica el mismo objeto

El contenido tras una URL puede cambiar. A la inversa, parámetros, copias, URL móviles o redirecciones pueden representar el mismo documento. Normaliza para buscar, pero conserva siempre la URL observada y la final; no fusiones registros sin justificar la equivalencia.

### La selección elimina contexto

Una frase puede depender de un encabezado, una nota al pie, una negación anterior o una tabla. Revisa alrededor del fragmento y anota página, sección o estructura. En PDF con OCR, compara además con la imagen de la página: el texto seleccionable puede contener errores u orden de lectura incorrecto.

### La actividad no equivale a acuerdo

Muchos comentarios pueden reflejar controversia, formación o duplicación. Un grupo silencioso puede haber revisado fuera de la herramienta. No conviertas recuentos de notas, autores o etiquetas en una métrica de verdad o importancia sin un diseño explícito.

### Privado no significa secreto ni eterno

Un grupo privado restringe acceso dentro del servicio, pero sus miembros pueden copiar contenido. La [política de privacidad](https://web.hypothes.is/privacy/) también recuerda que una anotación que fue pública pudo haber sido recogida mediante la API antes de editarse o borrarse. No introduzcas material cuya exposición resulte inaceptable.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa una finalidad legítima y documenta por qué cada fuente entra en el caso.
- No anotes para hostigar, perfilar o coordinar vigilancia sobre personas.
- Separa cuenta personal y cuenta de trabajo cuando el modelo de riesgo lo requiera.
- No pongas datos sensibles, hipótesis acusatorias ni secretos en etiquetas visibles.
- Revisa visibilidad y grupo antes de publicar cada nota.
- Almacena tokens de API fuera del repositorio y rótalos si se exponen.
- Mantén originales y capturas fuera de Hypothesis con controles de acceso adecuados.
- Conserva texto observado, interpretación, verificación y conclusión en campos distintos.
- Documenta correcciones sin borrar el rastro de la decisión anterior.
- Minimiza citas, exportaciones y datos personales; fija retención y borrado.
- Ofrece un canal de rectificación cuando una publicación afecte a terceros.
- Expresa estados inconclusos: una buena investigación también registra lo que no pudo confirmar.

## Checklist operativo

- [ ] La pregunta, el periodo y las exclusiones están definidos.
- [ ] Se eligió y probó la visibilidad antes de anotar fuentes reales.
- [ ] Miembros, moderación, retención y exportaciones tienen responsables.
- [ ] Cada fuente tiene identificador, URL observada, fecha y representación capturada.
- [ ] Las anotaciones separan observación, interpretación y comprobación pendiente.
- [ ] Las etiquetas proceden de un vocabulario corto y documentado.
- [ ] Los datos personales incidentales se han minimizado.
- [ ] Una segunda persona revisa los hallazgos de mayor consecuencia.
- [ ] La corroboración cuenta procedencias independientes, no respuestas.
- [ ] Los anclajes rotos se tratan como incidencia, no como ausencia de evidencia.
- [ ] Las exportaciones tienen recuento, fecha y huella.
- [ ] Tokens, capturas y documentos sensibles están fuera del repositorio público.

## Alternativas y siguientes pasos

Zotero es más apropiado para gestionar referencias, archivos y notas bibliográficas; Google Pinpoint ayuda a buscar dentro de colecciones documentales; un repositorio de casos o una herramienta de tickets ofrece estados, responsables y auditoría más explícitos; WARC y los servicios de archivo web preservan representaciones con otra finalidad. Una hoja estructurada puede ser suficiente para un equipo pequeño.

Hypothesis encaja cuando la conversación necesita permanecer cerca del pasaje. No tiene por qué convertirse en el sistema central del expediente: puede actuar como una capa de lectura que enlaza con capturas, fichas y decisiones conservadas en herramientas bajo mayor control.

El takeaway práctico es este: **anota para mostrar dónde empezó una pregunta, captura para demostrar qué observaste y verifica antes de convertir la nota en conclusión**. Prueba el método con tres páginas ficticias, rompe deliberadamente un anclaje y exporta el resultado. Si el equipo puede reconstruir qué vio, qué pensó y qué confirmó, la herramienta está ayudando. Como siguiente tema, merecería la pena comparar anotación, archivo y gestión de casos sobre una misma página que cambia con el tiempo.

## Fuentes y documentación

- [Hypothesis: fundamentos de la anotación](https://web.hypothes.is/help/annotation-basics/)
- [Hypothesis: tipos de anotaciones y resaltados](https://web.hypothes.is/help/whats-the-difference-between-an-annotation-and-a-highlight/)
- [Hypothesis: visibilidad de las anotaciones](https://web.hypothes.is/help/who-can-see-my-annotations-in-the-web-app/)
- [Hypothesis: anotación mediante grupos](https://web.hypothes.is/help/annotating-with-groups/)
- [Hypothesis: exportación e importación](https://web.hypothes.is/help/exporting-and-importing-annotations/)
- [Hypothesis: descripción general del sistema](https://web.hypothes.is/help/overview-of-the-hypothesis-system/)
- [Hypothesis API v1](https://h.readthedocs.io/en/latest/api-reference/v1/)
- [Hypothesis: política de privacidad](https://web.hypothes.is/privacy/)
