---
title: "Correcciones públicas en OSINT: rectificar sin borrar el rastro ni amplificar el daño"
slug: /comunicacion-publica-correcciones-osint
authors: [osint-writter]
tags: [osint, methodology, verification, tradecraft, investigation, privacy]
date: 2026-10-05
image: /img/blog/2026-10-05-comunicacion-correcciones-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando versiones y preparando una corrección pública trazable](/img/blog/2026-10-05-comunicacion-correcciones-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/comunicacion-publica-correcciones-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El mapa llevaba nueve horas publicado cuando una lectora señaló que dos puntos pertenecían a sedes con nombres parecidos, pero no a la misma organización. El equipo corrigió el CSV y volvió a generar la imagen. A primera vista, problema resuelto. Sin embargo, la captura equivocada seguía circulando, el texto no decía qué había cambiado y quienes descargaron el fichero original no tenían forma de saber que ya no era válido. **Cambiar el dato fue la mitad técnica de la rectificación; comunicarla era la mitad que protegía a la audiencia.**

Una corrección pública OSINT debe permitir responder, sin reconstruir el repositorio a ciegas, a cinco preguntas: qué estaba mal, qué es correcto ahora, qué conclusiones quedan afectadas, cuándo cambió y dónde están las versiones o derivados que deben dejar de usarse. Hacerlo bien no exige publicar detalles dañinos ni conservar en abierto datos personales inexactos. Exige diseñar una señal visible, proporcional y trazable.

<!-- truncate -->

## Qué es una corrección pública (y para qué sirve)

Una corrección pública es un aviso unido al artefacto corregido que reconoce un error factual o material, delimita su alcance y dirige a una versión utilizable. No es un historial de cada coma ni un postmortem completo. Tampoco es una fórmula defensiva como «se ha actualizado el contenido» cuando lo que ocurrió fue un error.

La [Associated Press](https://www.ap.org/about/news-values-and-principles/telling-the-story/) exige etiquetar las correcciones como tales, hacerlas visibles para consumidores y distribuidores y evitar eufemismos. [Reuters](https://reutersagency.com/about/standards-values/) resume un principio compatible: rectificar los errores con rapidez, claridad y amplitud suficiente en texto, gráficos, pies o guiones. Trasladado a OSINT, esto implica corregir tanto la afirmación como los objetos que la transportan: página, imagen, conjunto de datos, PDF, repositorio, boletín o publicación social.

Conviene separar cuatro operaciones que a menudo se mezclan:

| Operación | Cuándo usarla | Señal pública mínima |
| --- | --- | --- |
| Corrección | Un hecho, cifra, enlace o atribución era incorrecto | qué decía, qué debe decir y alcance |
| Aclaración | El texto era defendible, pero podía inducir a una lectura materialmente distinta | ambigüedad resuelta y motivo |
| Actualización | Apareció información posterior que no vuelve falso el contenido original | fecha y dato nuevo |
| Retirada | El artefacto causa daño, contiene datos que no deben seguir expuestos o falla en su base | aviso sustitutivo, motivo general y vía de contacto |

Nombrar bien la operación importa. Si un análisis identificó erróneamente a una entidad, «actualización» oculta que hubo un error. Si una cifra era correcta al publicarse y luego cambió, llamarla «corrección» reescribe injustamente la cronología.

## Caso de uso legítimo: dos sedes y un nombre casi idéntico

Imaginemos **Observatorio Río Claro**, un proyecto ficticio que analiza subvenciones públicas agregadas. Solo utiliza portales abiertos y evita publicar datos personales que no sean necesarios.

El equipo descarga un directorio oficial en el que aparecen `Fundación Horizonte Norte` y `Fundación Horizonte del Norte`. Una normalización demasiado agresiva elimina la preposición y agrupa ambas entidades. El informe resultante asigna dos sedes y 180.000 euros a una sola organización. El error pasa la revisión porque el total general sigue cuadrando.

A las 16:20 UTC, una lectora aporta los identificadores registrales de ambas entidades. El equipo preserva la entrada recibida, comprueba el directorio original, reproduce la transformación y confirma el fallo. La respuesta no consiste en borrar discretamente una fila. Debe abarcar:

- la tabla HTML que fusionó las entidades;
- el CSV descargable;
- un gráfico con el importe agregado;
- dos párrafos cuya comparación dependía de esa suma;
- el boletín que enlazó la versión inicial;
- las copias internas usadas para generar esos derivados.

### Antes de publicar: una ficha de impacto

La persona coordinadora registra primero hechos y decisiones:

```text
Incidente: COR-2026-017
Detectado: 2026-10-05T16:20:00Z
Confirmado: 2026-10-05T16:47:00Z
Error: fusión de dos entidades jurídicas distintas
Origen: regla de normalización de nombres
Artefactos afectados: HTML, CSV, PNG, dos párrafos y boletín
Conclusiones afectadas: ranking e importe atribuido; total global no cambia
Riesgo: atribución financiera incorrecta a una organización
Estado: publicación pausada; derivados corregidos en preparación
```

La ficha interna puede contener rutas, hashes y responsables. La nota pública no necesita revelar nombres personales, mensajes privados ni una receta explotable del sistema. Su función es describir el cambio con precisión suficiente para quien usó el material.

### Una nota pública útil

En este caso ficticio, una corrección visible podría decir:

> **Corrección — 5 de octubre de 2026, 18:05 CEST.** La versión publicada a las 11:00 agrupaba por error dos entidades con nombres similares. Hemos separado sus registros y sustituido la tabla, el CSV y el gráfico. Cambian el importe atribuido y la posición de ambas entidades; el total general no cambia. La versión anterior no debe utilizarse. Conservamos su hash y el registro de cambios en el expediente interno.

La nota reconoce el error, fija tiempos, delimita impacto y da una instrucción. No reproduce el dato incorrecto más veces de las necesarias ni culpa a quien avisó.

## Flujo recomendado: de la señal a la versión corregida

### 1. Recibe el aviso por un canal verificable

Publica una vía sencilla para comunicar errores. Registra la hora, el artefacto señalado y la evidencia aportada; minimiza los datos de contacto y limita el acceso. Una solicitud no convierte automáticamente la afirmación en falsa, pero sí activa una revisión proporcionada.

Si el aviso afecta a datos personales, aumenta la prioridad y consulta el procedimiento jurídico aplicable. El [RGPD, en su artículo 5](https://eur-lex.europa.eu/legal-content/ES/ALL/?uri=CELEX%3A32016R0679), exige exactitud y medidas razonables para suprimir o rectificar sin dilación datos inexactos respecto a la finalidad del tratamiento. La [AEPD](https://www.aepd.es/derechos-y-deberes/conoce-tus-derechos/derecho-de-rectificacion) explica además el derecho a completar datos incompletos mediante una declaración adicional. Esta entrada no sustituye asesoramiento legal.

### 2. Separa señal, contención y veredicto

No anuncies una conclusión antes de verificarla. Si el daño potencial es alto, puedes pausar descargas, añadir un aviso provisional o retirar temporalmente un derivado mientras compruebas el fondo. Escribe el estado con lenguaje inequívoco: «en revisión» no significa «confirmado como falso».

Preserva antes de editar:

- el original adquirido y su URL;
- la versión publicada y sus hashes;
- los parámetros o revisión de código que generaron los derivados;
- la hora en UTC y la zona mostrada al público;
- las decisiones de contener, mantener o retirar.

La preservación no obliga a mantener accesible un dato dañino. Puedes restringir el original y conservar solo su identificador o hash en la nota pública.

### 3. Clasifica severidad por impacto, no por tamaño del cambio

Cambiar una letra puede corregir la identidad de una persona; sustituir una gráfica entera puede no alterar la conclusión. Usa una matriz sencilla:

| Nivel | Ejemplo | Respuesta orientativa |
| --- | --- | --- |
| Bajo | enlace roto o errata sin cambio de significado | corregir; registrar internamente |
| Medio | cifra secundaria o explicación ambigua | nota visible y actualización de derivados |
| Alto | atribución, identidad, ubicación sensible o conclusión principal | aviso destacado, pausa o retirada, notificación a canales de distribución |
| Crítico | riesgo inmediato para una persona, exposición ilícita o artefacto imposible de sanear | retirar acceso, escalar y comunicar sin repetir el dato |

La tabla orienta; no reemplaza el juicio. Define antes quién puede declarar cada nivel y quién autoriza la republicación.

### 4. Corrige desde la fuente hacia todos los derivados

No empieces retocando la captura. Corrige la transformación o interpretación que produjo el error, vuelve a generar las salidas y comprueba las dependencias. Para cada artefacto registra:

1. identificador o ruta de la versión anterior;
2. hash anterior y nuevo cuando proceda;
3. cambio factual;
4. conclusiones alteradas y no alteradas;
5. hora de sustitución;
6. canal al que se distribuyó.

El vocabulario [W3C PROV-O](https://www.w3.org/TR/prov-o/) ofrece relaciones como `prov:wasRevisionOf`, además de tiempos de generación e invalidación, para modelar versiones sin fingir que son el mismo estado. No necesitas desplegar una ontología para aplicar la idea: cada revisión debe poder apuntar a la anterior y a la actividad que la generó.

### 5. Escribe una nota con seis campos

Una corrección práctica responde a:

- **etiqueta:** «Corrección», no «ajuste» si hubo un error factual;
- **tiempo:** cuándo se publicó el aviso, con zona horaria;
- **error:** qué clase de dato o afirmación era incorrecta;
- **cambio:** qué muestra ahora la versión válida;
- **alcance:** qué conclusiones y derivados cambian o permanecen;
- **acción:** qué debe hacer quien descargó o citó la versión anterior.

Evita convertir la nota en una segunda difusión del error. Si una URL, imagen o identificador expone a una persona, describe la categoría del cambio sin repetir el valor retirado.

### 6. Mantén enlaces de ida y vuelta cuando haya dos recursos

Si la corrección vive en una página distinta, enlaza desde el artefacto incorrecto hacia la corrección y desde la corrección hacia el original o su registro sanitizado. Las [guías de confianza de IPTC](https://www.iptc.org/std/guidelines/trust-and-credibility/) contemplan precisamente vínculos bidireccionales entre el trabajo incorrecto y el que lo corrige.

En una página actualizada sobre la misma URL, coloca la nota cerca del inicio o del punto afectado y conserva un registro de cambios accesible. Para facilitar la lectura automática, [Schema.org](https://schema.org/CreativeWork) incluye la propiedad `correction`; y Google recomienda que `dateModified` coincida entre el dato estructurado y la fecha visible de actualización. Ese marcado ayuda a expresar el cambio, pero no sustituye la nota legible ni garantiza cómo aparecerá en un buscador.

### 7. Notifica por los mismos caminos de distribución

Corregir la web no alcanza a quien recibió un PDF, un CSV o una imagen. Recorre los canales utilizados:

- boletín y feed;
- repositorio y release;
- publicaciones sociales;
- personas u organizaciones a las que se envió directamente;
- APIs, espejos o conjuntos descargables bajo tu control.

No puedes garantizar que desaparezcan todas las copias. Sí puedes emitir una señal clara, mantener una URL canónica y pedir a los receptores conocidos que sustituyan o etiqueten su copia.

### 8. Verifica la rectificación como una publicación nueva

Antes de cerrar:

- abre la URL sin sesión y comprueba que la nota es visible;
- descarga cada derivado y compara hash, fecha y contenido;
- prueba enlaces entre versiones;
- confirma que cachés y miniaturas no muestran el material retirado bajo tu control;
- revisa que el aviso no contenga el mismo dato personal que pretendías eliminar;
- registra quién verificó cada salida y cuándo;
- abre una acción separada para prevenir la repetición.

La corrección restaura una versión utilizable. El postmortem explica por qué falló el sistema; no bloquees la primera esperando a terminar el segundo.

## Limitaciones y falsos positivos

### Una discrepancia no demuestra un error

Dos fuentes pueden medir periodos, jurisdicciones o entidades diferentes. Preserva la discrepancia, compara definiciones y etiqueta la incertidumbre. Corregir hacia la fuente más reciente solo porque parece más oficial puede destruir una observación histórica válida.

### El historial no debe convertirse en amplificador

La transparencia no exige publicar un diff con nombres, direcciones o acusaciones equivocadas. Mantén la evidencia bajo acceso proporcional y publica metadatos suficientes para auditar la decisión. Un hash demuestra que conservas un objeto concreto; no demuestra que su contenido era cierto.

### La fecha de modificación no explica el cambio

Un sello «actualizado» puede corresponder a formato, enlaces o una corrección sustantiva. Acompáñalo de una nota humana. Tampoco cambies la fecha de publicación original por la fecha de corrección: conserva ambas funciones temporales.

### Una corrección no recupera todas las copias

Capturas, cachés y exportaciones pueden persistir. Prioriza avisar a quienes recibieron el artefacto, ofrece una versión canónica y evita prometer borrado universal. Cuando exista riesgo para una persona, escala la retirada y las solicitudes a plataformas según el procedimiento aplicable.

### Demasiadas notas pueden ocultar lo importante

No conviertas cada mejora tipográfica en una alerta. Define un umbral basado en significado e impacto y conserva los cambios menores en el control de versiones. La audiencia debe distinguir una corrección material de mantenimiento rutinario.

## Buenas prácticas de OPSEC, ética y privacidad

- Corrige con la misma visibilidad con la que difundiste el error.
- No identifiques a quien avisó sin permiso ni publiques su mensaje completo.
- Minimiza nombres, ubicaciones, cuentas y datos de contacto en tickets y notas.
- Preserva originales en almacenamiento restringido; trabaja sobre copias.
- Separa hechos confirmados, alegaciones, opiniones e inferencias.
- Evita repetir la afirmación dañina en título, redes o metadatos.
- No culpes a una fuente por un error de interpretación propio.
- Registra UTC y muestra también una zona comprensible para la audiencia.
- Mantén el enlace canónico; no fuerces a descubrir la corrección por una URL nueva.
- Avisa a quienes recibieron directamente el material incorrecto.
- Documenta por qué retienes o suprimes una versión con datos personales.
- No presentes el historial de Git, una firma o un hash como validación factual.

## Plantilla mínima reutilizable

```text
CORRECCIÓN — <fecha, hora y zona>

Qué estaba mal:
Qué muestra ahora la versión válida:
Artefactos sustituidos o retirados:
Conclusiones que cambian:
Conclusiones que no cambian:
Acción para quien descargó o citó la versión anterior:
Enlace a la versión válida:
Canal para comunicar otra inexactitud:
```

## Checklist de cierre

- [ ] La nota usa la palabra «corrección» cuando hubo un error factual.
- [ ] Indica fecha, hora y zona sin sustituir la fecha original.
- [ ] Explica qué cambió y qué impacto tiene en las conclusiones.
- [ ] HTML, datos, imágenes, PDF y boletines están inventariados.
- [ ] La versión anterior está marcada, retirada o restringida según el riesgo.
- [ ] Los enlaces entre original, revisión y nota funcionan.
- [ ] Los destinatarios conocidos han recibido el aviso.
- [ ] La nota no vuelve a exponer el dato que debía minimizarse.
- [ ] La versión corregida se ha probado sin sesión y desde cero.
- [ ] Hay una acción preventiva separada, con responsable y prueba de cierre.

## Alternativas y siguientes pasos

Si aún no sabes qué salidas dependen del dato erróneo, empieza por [OpenLineage](/openlineage-linaje-datos-osint). Para reconstruir decisiones y factores contribuyentes, usa [postmortems sin culpa](/postmortems-sin-culpa-incidentes-osint); para ensayar la respuesta con material ficticio, revisa [simulacros de incidentes](/simulacros-incidentes-equipos-osint); y para conservar un paquete de evidencia con contexto, consulta [RO-Crate](/ro-crate-osint-paquete-evidencia) y [BagIt](/bagit-osint-transferencia-evidencia).

El takeaway accionable es concreto: toma una corrección reciente y comprueba si alguien que solo conserva el CSV o la captura equivocada podría descubrir el cambio, entender su alcance y localizar la versión válida. Si la respuesta es no, la edición está hecha, pero la rectificación todavía no.

Como próximo tema, merece la pena estudiar **registros públicos de cambios para investigaciones OSINT**: cómo definir un esquema mínimo, enlazar hashes y automatizar avisos sin convertir el historial en un repositorio de datos sensibles.

## Fuentes consultadas

- [Associated Press: News Values and Principles — Corrections](https://www.ap.org/about/news-values-and-principles/telling-the-story/)
- [Reuters: Journalistic Standards — Corrections](https://reutersagency.com/about/standards-values/)
- [W3C PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/)
- [IPTC: Expressing Trust and Credibility Information](https://www.iptc.org/std/guidelines/trust-and-credibility/)
- [Schema.org: CreativeWork](https://schema.org/CreativeWork)
- [Google Search Central: publicación y modificación de artículos](https://developers.google.com/search/docs/appearance/publication-dates?hl=es)
- [Reglamento (UE) 2016/679](https://eur-lex.europa.eu/legal-content/ES/ALL/?uri=CELEX%3A32016R0679)
- [AEPD: derecho de rectificación](https://www.aepd.es/derechos-y-deberes/conoce-tus-derechos/derecho-de-rectificacion)
