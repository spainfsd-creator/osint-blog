---
title: "Browsertrix y WACZ en OSINT: preservar webs dinámicas sin confundir una captura con la verdad"
slug: /browsertrix-wacz-osint-preservacion-web
authors: [osint-writter]
tags: [osint, archiving, verification, methodology, tooling, privacy]
date: 2026-09-12
image: /img/blog/2026-09-12-browsertrix-wacz-osint-preservacion-web.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista comparando una web pública en directo con su reproducción archivada y controles de integridad](/img/blog/2026-09-12-browsertrix-wacz-osint-preservacion-web.png)

*Imagen generada mediante inteligencia artificial.*

Una web pública anuncia una adjudicación y, horas después, cambia un anexo cargado mediante JavaScript. Guardar una captura de pantalla conserva el aspecto; descargar el HTML puede conservar un esqueleto vacío; anotar la URL solo promete que quizá mañana siga allí. Para que otra persona pueda revisar qué observamos necesitamos **captura, alcance, contexto, reproducción y control de calidad**, no una fotografía huérfana.

[Browsertrix](https://docs.browsertrix.com/user-guide/crawl-workflows/) automatiza capturas con un navegador y permite empaquetarlas como archivos web reproducibles. El formato [WACZ](https://specs.webrecorder.net/wacz/latest/) reúne datos WARC, índices, páginas y metadatos en un paquete transportable que herramientas como [ReplayWeb.page](https://replayweb.page/) pueden abrir en el navegador. Juntos ofrecen una base sólida para preservar fuentes web dinámicas, pero no certifican por sí solos que lo publicado fuese verdadero ni que la captura sea completa.

<!-- truncate -->

> **Transparencia editorial:** esta entrada ha sido generada mediante inteligencia artificial y se publica sin revisión humana ni *fact-checking* humano. Las fuentes técnicas se consultaron el 12 de septiembre de 2026.

## Qué son Browsertrix y WACZ, y para qué sirven

Browsertrix es un sistema de archivo web basado en navegador. Un flujo de captura define las URL iniciales, el alcance, los límites y el comportamiento que se aplicará al recorrer un sitio. Al terminar produce un elemento archivado que puede descargarse, revisarse y agruparse en colecciones.

WACZ —*Web Archive Collection Zipped*— no sustituye a WARC. La [especificación oficial](https://specs.webrecorder.net/wacz/1.2.0/) lo plantea como una convención para empaquetar el contenido archivado y los datos necesarios para localizarlo y reproducirlo con eficiencia. El paquete puede incluir:

- registros WARC con las respuestas capturadas;
- índices para buscar URL y posiciones dentro del archivo;
- `pages.jsonl` con puntos de entrada navegables;
- `datapackage.json` con metadatos técnicos y descriptivos;
- datos de integridad definidos por el formato.

ReplayWeb.page abre estos archivos directamente en el navegador y solicita solo las partes necesarias cuando el servidor admite peticiones por rangos. Esa portabilidad resulta valiosa en OSINT: el material, su índice y su contexto básico viajan juntos.

| Pieza | Pregunta que ayuda a responder | Lo que no demuestra |
| --- | --- | --- |
| configuración del rastreo | «¿qué intentamos capturar?» | que todo lo previsto se guardase |
| WARC dentro del WACZ | «¿qué respuestas recibió el navegador?» | que el servidor mostrase lo mismo a todos |
| índice y lista de páginas | «¿qué podemos localizar y reproducir?» | exhaustividad del sitio |
| metadatos y hashes | «¿ha cambiado el paquete comprobado?» | autoría o veracidad del contenido |
| reproducción | «¿cómo se comporta la copia archivada?» | equivalencia perfecta con la web viva |

La distinción decisiva es esta: **capturar conserva una observación; autenticar una afirmación exige corroboración externa**.

## Caso de uso legítimo: documentar una convocatoria pública ficticia

Imaginemos que la Agencia Regional de Innovación de **Puerto Claro**, entidad ficticia, publica una convocatoria con una página principal, un calendario interactivo y varios anexos PDF. Nuestro encargo legítimo es documentar sus cambios durante el plazo de alegaciones.

La pregunta no es «¿podemos copiar toda la sede?», sino «¿qué conjunto mínimo permite verificar requisitos, plazos y anexos sin recoger datos personales innecesarios?». Definimos como semillas la página de la convocatoria y el índice público de anexos. Excluimos buscadores internos, áreas de identificación, formularios, calendarios infinitos y rutas ajenas al expediente. Fijamos límites de páginas, tiempo y tamaño.

Tras cada captura conservamos:

1. el WACZ original sin editar;
2. la configuración exacta del flujo;
3. hora de inicio y fin, zona horaria y operador;
4. informe de errores y URL fallidas;
5. notas de revisión de las páginas relevantes;
6. hash del paquete en un registro separado;
7. referencias a la publicación oficial y al boletín que corroboran el contenido.

Si el anexo cambia, dos capturas fechadas permiten comparar observaciones. No permiten afirmar, sin más, la hora exacta de modificación ni quién la ordenó: el intervalo solo queda acotado entre la última captura anterior y la primera posterior.

## Flujo recomendado: de la pregunta a un archivo revisable

### 1. Define propósito, autoridad y alcance

Escribe una frase que pueda auditarse: «preservar las páginas y anexos públicos de la convocatoria X entre el 12 y el 30 de septiembre». Enumera semillas, dominios permitidos, exclusiones, profundidad y límites. La [documentación de alcance](https://crawler.docs.browsertrix.com/user-guide/crawl-scope/) distingue capturas de una página, prefijo, host, dominio o reglas personalizadas; ampliar de `page` a `domain` puede multiplicar el volumen y el riesgo de recolectar datos irrelevantes.

Respeta `robots.txt`, condiciones de uso, límites de tasa y normativa aplicable cuando correspondan. La accesibilidad técnica no elimina las obligaciones legales ni éticas.

### 2. Haz una captura piloto pequeña

Empieza por las URL esenciales y un límite bajo. Observa redirecciones, bucles de calendario, parámetros de sesión, contenido cargado al desplazarse y recursos de terceros. Ajusta las exclusiones antes de escalar.

Los comportamientos de navegador pueden hacer *scroll*, reproducir elementos o activar contenido dinámico. Son útiles, pero también alteran lo que el sitio carga y pueden disparar solicitudes no deseadas. Documenta qué comportamiento empleaste y evita acciones que envíen formularios, publiquen contenido o accedan a zonas no autorizadas.

### 3. Captura con una identidad operativa mínima

Para páginas realmente públicas, evita sesiones autenticadas. Si una fuente legítima exige cuenta, usa un perfil dedicado y autorización expresa. La [guía oficial de perfiles](https://docs.browsertrix.com/user-guide/browser-profiles/browser-profiles-overview/) advierte de que cookies, preferencias, información personalizada y tokens pueden terminar en el archivo. Un WACZ con sesión no debe tratarse como un adjunto inocuo.

Registra también versión del flujo, idioma, zona, agente de usuario, proxy si existe y hora del sistema. Esos factores pueden cambiar el contenido devuelto.

### 4. Conserva original y registro de adquisición

Al finalizar, mueve el WACZ a almacenamiento controlado, calcula un hash y registra quién lo adquirió, desde dónde y con qué configuración. No «limpies» el original. Si necesitas retirar material sensible para compartir, crea un derivado identificado y conserva por separado la relación con el original bajo controles adecuados.

Un hash detecta cambios en los bytes comparados; no prueba que la captura sea verdadera, completa ni anterior a una fecha. Incluso la firma de un paquete necesita una cadena de confianza externa para vincular una clave con una identidad.

### 5. Reproduce y revisa lo importante

Abre el archivo en ReplayWeb.page desde un entorno de confianza. Comprueba cada página crítica, sus anexos, navegación, imágenes y texto. La [función de análisis de calidad](https://docs.browsertrix.com/user-guide/qa-review/) compara lo observado durante la captura con su reproducción mediante capturas visuales, texto extraído y recursos. Esa comparación evalúa la fidelidad de reproducción, no la verdad de la página viva.

Mantén una tabla de control:

| URL esperada | Capturada | Reproduce | Recurso crítico | Acción |
| --- | --- | --- | --- | --- |
| página principal | sí | sí | texto y fecha | aceptar |
| calendario | sí | parcial | eventos dinámicos | captura manual complementaria |
| anexo PDF | sí | sí | bytes y firma oficial | verificar en boletín |
| formulario | excluido | no aplica | fuera de propósito | documentar exclusión |

### 6. Corrobora y publica con contexto

Compara fechas, anexos y referencias con fuentes primarias independientes: boletines oficiales, registros administrativos o documentos firmados. Al compartir el WACZ incluye alcance, limitaciones, hash, instrucciones de reproducción y una lista de elementos revisados. Si se aloja en web, la [guía de ReplayWeb.page](https://replayweb.page/docs/embedding/) explica los requisitos de alojamiento y reproducción, pero la exposición pública debe decidirse según sensibilidad y derechos.

## Limitaciones y falsos positivos

- **Contenido no capturado:** vídeos segmentados, peticiones tardías, marcos, recursos protegidos y rutas descubiertas solo tras interacción pueden faltar.
- **Sesiones y personalización:** región, idioma, cookies, autenticación, pruebas A/B y consentimiento pueden producir una versión distinta.
- **Normalización de URL:** dos variantes pueden tratarse como equivalentes para el rastreo aunque tengan significado operativo diferente.
- **Redirecciones:** una semilla puede terminar fuera del alcance previsto; registra destino, cadena y regla aplicada.
- **Reproducción imperfecta:** que una página «se vea bien» no garantiza que estén todos los recursos; que se vea mal tampoco implica que los datos centrales falten.
- **Tiempos de observación:** el reloj de la captura no equivale necesariamente a la fecha de publicación del contenido.
- **Integridad mal interpretada:** un hash consistente protege contra alteraciones posteriores del paquete comprobado, no contra una adquisición defectuosa.
- **Falsa exhaustividad:** un rastreo terminado no significa «sitio completo». Solo significa que terminó según unas semillas, reglas y límites concretos.

Una ausencia dentro del archivo debe formularse con precisión: «la URL o el recurso no aparece en esta captura bajo esta configuración», no «nunca existió».

## Buenas prácticas de OPSEC, ética y privacidad

- Crea una identidad operativa separada solo cuando sea necesaria y esté autorizada; nunca reutilices una cuenta personal.
- No incluyas contraseñas, tokens, bandejas privadas, borradores ni datos de terceros en perfiles de captura.
- Mantén el alcance mínimo y excluye formularios, paneles, búsquedas con datos personales y rutas infinitas.
- Aplica límites de tasa razonables: archivar no justifica degradar el servicio ajeno.
- Cifra archivos sensibles en reposo y restringe su acceso; un WACZ puede contener más que lo visible en la reproducción.
- Analiza capturas potencialmente hostiles en un entorno aislado y actualizado.
- Separa adquisición, revisión, redacción y publicación; registra transformaciones y redacciones.
- No publiques archivos con datos personales solo porque la fuente estuvo abierta. Evalúa necesidad, proporcionalidad y daño.
- Distingue hechos observados, inferencias y huecos. La prudencia forma parte del dato.

## Alternativas y siguientes pasos

- **ArchiveWeb.page** sirve para capturas guiadas e interactivas desde el navegador cuando el analista necesita recorrer manualmente un conjunto pequeño.
- **Browsertrix Crawler** ofrece flujos automatizables y configurables para capturas repetibles.
- **ReplayWeb.page** reproduce WARC y WACZ sin exigir una infraestructura de servidor compleja.
- **Wayback Machine** aporta una copia mantenida por un tercero y puede corroborar una cronología, aunque no sustituye una adquisición propia documentada.
- **Hunchly** se orienta a registrar sesiones de investigación; **Auto Archiver** coordina capturas con distintos servicios. Elige según la pregunta y el modelo de evidencia, no por acumulación de herramientas.

El siguiente paso natural es diseñar una **prueba de completitud limitada**: lista de URL críticas, recursos esperados, resultado de reproducción y explicación de cada ausencia. Es más honesta y útil que prometer una copia perfecta de una web dinámica.

## Conclusión

El takeaway accionable es concreto: **antes de lanzar un rastreo, escribe semillas, exclusiones, límites y cinco páginas críticas; después no cierres la captura hasta reproducir y revisar esas cinco páginas**.

Browsertrix y WACZ convierten una observación web efímera en un paquete transportable y revisable. El rigor aparece cuando conservamos además la pregunta, la configuración, los fallos y la corroboración. Un archivo no es la verdad congelada: es una observación técnica cuya fuerza depende de que podamos explicar exactamente cómo nació y qué dejó fuera.

## Fuentes consultadas

- [Browsertrix: introducción a los flujos de captura](https://docs.browsertrix.com/user-guide/crawl-workflows/)
- [Browsertrix Crawler: alcance del rastreo](https://crawler.docs.browsertrix.com/user-guide/crawl-scope/)
- [Browsertrix: revisión y control de calidad](https://docs.browsertrix.com/user-guide/qa-review/)
- [Browsertrix: perfiles de navegador y riesgos de privacidad](https://docs.browsertrix.com/user-guide/browser-profiles/browser-profiles-overview/)
- [Especificación WACZ](https://specs.webrecorder.net/wacz/1.2.0/)
- [ReplayWeb.page: repositorio y arquitectura](https://github.com/webrecorder/replayweb.page)
- [ReplayWeb.page: guía de integración](https://replayweb.page/docs/embedding/)
