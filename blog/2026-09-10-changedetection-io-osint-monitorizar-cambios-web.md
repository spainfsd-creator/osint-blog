---
title: "changedetection.io en OSINT: vigilar cambios web sin confundir una alerta con una prueba"
slug: /changedetection-io-osint-monitorizar-cambios-web
authors: [osint-writter]
tags: [osint, automation, verification, methodology, tooling, privacy]
date: 2026-09-10
image: /img/blog/2026-09-10-changedetection-io-osint-cambios-web.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista comparando dos versiones fechadas de una página pública, con diferencias, alertas y procedencia](/img/blog/2026-09-10-changedetection-io-osint-cambios-web.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/changedetection-io-osint-monitorizar-cambios-web.m4a)


*Imagen generada mediante inteligencia artificial.*

Una administración publica las condiciones de una ayuda y, tres días después, modifica silenciosamente un requisito. Si solo conservamos la página actual, sabremos qué dice ahora, pero no **qué cambió, cuándo lo observamos ni si el cambio afecta realmente a nuestra investigación**. Visitar la web cada mañana tampoco resuelve el problema: la memoria humana es un comparador pésimo.

[changedetection.io](https://github.com/dgtlmoon/changedetection.io) automatiza esa vigilancia: consulta páginas, conserva estados, muestra diferencias y puede avisar cuando detecta cambios. En OSINT es útil para seguir fuentes públicas con un propósito legítimo, siempre que filtremos el ruido, preservemos el material original y tratemos cada alerta como una pista que exige verificación.

<!-- truncate -->

> **Transparencia editorial:** esta entrada ha sido generada mediante inteligencia artificial y se publica sin revisión humana ni *fact-checking* humano. Las fuentes técnicas se consultaron el 10 de septiembre de 2026.

## Qué es changedetection.io y para qué sirve

changedetection.io es una aplicación de código abierto para detectar modificaciones en páginas web y enviar notificaciones. Puede ejecutarse como servicio alojado o en infraestructura propia. Su [repositorio oficial](https://github.com/dgtlmoon/changedetection.io) documenta dos formas de obtener contenido: una petición HTTP sencilla para páginas estáticas y un navegador basado en Chrome para sitios que necesitan JavaScript.

El proyecto incorpora filtros CSS, XPath, JSONPath y `jq`; historial de cambios; selector visual; pasos de navegador; monitorización de respuestas JSON y notificaciones mediante múltiples canales. La [API oficial](https://changedetection.io/docs/api_v1/) permite administrar vigilancias, etiquetas y notificaciones de forma programática.

Nada de eso demuestra por sí solo por qué cambió una página o quién ordenó el cambio. Conviene separar funciones:

| Capa | Pregunta que responde | Lo que no demuestra |
| --- | --- | --- |
| captura periódica | «¿qué devolvió esta URL en cada consulta?» | que el servidor mostrase lo mismo a todo el mundo |
| filtro | «¿qué parte queremos comparar?» | que el resto de la página sea irrelevante |
| diff | «¿qué texto observado difiere?» | intención, autoría o importancia |
| alerta | «¿cuándo detectó el sistema una diferencia?» | momento exacto de publicación |
| preservación externa | «¿qué material podemos revisar después?» | autenticidad completa sin más corroboración |

## Caso de uso legítimo: seguir un pliego público ficticio

Imaginemos que el Ayuntamiento de **Bahía Clara**, entidad ficticia, publica una convocatoria de subvenciones. Nuestro encargo es documentar cambios en requisitos, fechas y anexos durante el periodo de alegaciones. No buscamos información personal ni intentamos acceder a zonas restringidas.

Definimos antes de configurar nada:

- URL oficial de la convocatoria y de sus anexos;
- campos relevantes: plazo, cuantía, criterios y versión de los documentos;
- frecuencia proporcionada, por ejemplo una comprobación diaria;
- zona horaria y reloj de referencia;
- canal de alerta sin datos sensibles;
- procedimiento de preservación y verificación.

La hipótesis operativa no es «la administración oculta algo», sino una afirmación comprobable: «queremos saber si el contenido público que sostiene una decisión cambia durante el periodo observado».

## Flujo recomendado

### 1. Registra el estado inicial y el alcance

Antes de activar el monitor, guarda la URL canónica, la fecha y hora UTC, el título visible, el código HTTP y, cuando sea lícito y proporcionado, una copia del documento original con su hash. Anota también desde qué red y con qué idioma o cabeceras se hizo la consulta: una web puede variar por sesión, ubicación o dispositivo.

Limita el alcance a fuentes públicas necesarias para la investigación. No añadas perfiles personales, páginas de familiares o paneles autenticados por mera curiosidad. Que una herramienta pueda ejecutar pasos de navegador no convierte en legítimo el acceso ni elimina las condiciones de uso del sitio.

### 2. Elige el método de captura más sencillo

Empieza con el recuperador HTTP para contenido estático. Reduce complejidad, consumo y variaciones causadas por JavaScript. Usa el navegador solo si la información relevante se genera en cliente o requiere una interacción permitida. El [README oficial](https://github.com/dgtlmoon/changedetection.io#readme) indica que los *Browser Steps* y el selector visual dependen del soporte de navegador.

Documenta el método porque dos capturadores pueden observar representaciones distintas. Si una página devuelve un reto anti-bot, un error o contenido incompleto, no lo interpretes como una eliminación editorial.

### 3. Filtra la zona relevante sin borrar contexto

Cabeceras rotatorias, contadores, banners de cookies y sellos de tiempo producen alertas inútiles. Usa el selector visual o un filtro CSS/XPath para aislar, por ejemplo, el bloque principal de requisitos. Para una API JSON pública, JSONPath o `jq` permiten comparar solo campos definidos.

Un ejemplo ficticio y deliberadamente inocuo sería:

```text
CSS: main article .requisitos
XPath: //main//section[@id='requisitos']
jq: {plazo: .convocatoria.plazo, cuantia: .convocatoria.cuantia}
```

Conserva tanto la regla como una muestra del contenido excluido. Un filtro demasiado ancho genera ruido; uno demasiado estrecho puede silenciar el cambio importante. La propia documentación del proyecto enumera [CSS, XPath, JSONPath y `jq`](https://github.com/dgtlmoon/changedetection.io#filters) como mecanismos disponibles, pero la calidad del resultado depende de cómo los configuremos.

### 4. Ajusta frecuencia, calendario y condiciones

La frecuencia debe corresponder al riesgo y a la cadencia real de publicación. Consultar cada pocos segundos una convocatoria mensual no mejora la evidencia y puede sobrecargar el servidor. Anota periodos sin comprobación y fallos de red: la ausencia de una alerta durante un hueco no demuestra estabilidad.

Si solo importan adiciones, el tutorial oficial explica el filtro de [texto añadido o eliminado](https://changedetection.io/tutorial/how-monitor-website-new-content). Aun así, revisa el diff completo antes de concluir: una frase añadida puede corregir otra eliminada o mover contenido sin alterar su significado.

### 5. Diseña alertas como triage, no como veredictos

Configura un mensaje que incluya como mínimo:

- identificador de la vigilancia;
- URL y etiqueta de la fuente;
- instante de detección con zona horaria;
- enlace al historial o diff;
- estado de la consulta;
- instrucción de verificación.

changedetection.io integra notificaciones a través de [Apprise](https://github.com/caronc/apprise), según su documentación. Guarda secretos fuera de capturas, repositorios y cuerpos de alerta. Comprueba además los límites del canal: las [notas oficiales sobre notificaciones](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes) advierten de que mensajes extensos pueden fallar según el destino.

### 6. Verifica el cambio en la fuente y en otra evidencia

Cuando llegue una alerta:

1. abre la URL oficial en una sesión limpia;
2. comprueba estado HTTP, fecha declarada y documento enlazado;
3. compara la captura anterior y la nueva;
4. busca una nota de cambios, resolución, RSS o repositorio oficial;
5. preserva el original relevante con fecha, URL y hash;
6. clasifica el resultado como hecho observado, inferencia o incógnita.

El instante de detección acota una ventana: el cambio ocurrió después de la última captura válida y antes de la nueva. No lo conviertas en una hora de publicación exacta salvo que otra fuente fiable la aporte.

### 7. Automatiza con la API sin automatizar conclusiones

La [API de changedetection.io](https://changedetection.io/docs/api_v1/) expone `/api/v1/` y permite crear una vigilancia a partir de una URL, configurar el intervalo, el recuperador, filtros y notificaciones, entre otros campos. En un equipo puede servir para aplicar una plantilla común y auditar la configuración.

Un inventario mínimo por vigilancia debería conservar:

```yaml
watch_id: convocatoria-bahia-clara
purpose: verificar cambios en requisitos públicos
source_url: https://publico.ejemplo/convocatoria
scope: sección de requisitos y anexos
check_interval: 24h
owner: equipo-verificacion
retention: 90d
review_required: true
```

No incluyas tokens, cookies ni credenciales en ese fichero. Y no programes respuestas públicas automáticas basadas en un diff: la automatización debe abrir una tarea de revisión, no acusar a nadie.

## Limitaciones y falsos positivos

La detección de cambios hereda la inestabilidad de la web:

- **contenido dinámico:** anuncios, recomendaciones, contadores o identificadores de sesión varían sin cambio editorial;
- **personalización:** idioma, ubicación, cookies, autenticación o pruebas A/B pueden ofrecer versiones distintas;
- **renderizado incompleto:** un fallo de JavaScript puede parecer una retirada masiva;
- **bloqueos y CAPTCHA:** la herramienta puede recibir una página de error en lugar del contenido esperado;
- **estructura cambiante:** un nuevo selector o plantilla puede romper el filtro aunque la información siga presente;
- **documentos enlazados:** que cambie el enlace no garantiza que haya cambiado el PDF, y al revés;
- **ventana temporal:** solo conocemos el intervalo entre dos capturas correctas;
- **silencio ambiguo:** no detectar diferencias puede significar estabilidad, filtro incorrecto o fallo de consulta.

Introduce controles de salud separados de las alertas de contenido: código HTTP esperado, tamaño mínimo, presencia de una frase estable y aviso cuando el filtro deja de devolver datos. Así evitamos que una vigilancia rota parezca una fuente inmóvil.

## Buenas prácticas de OPSEC, ética y privacidad

- Monitoriza únicamente fuentes y campos necesarios para una finalidad legítima y documentada.
- Respeta condiciones de uso, `robots.txt` cuando proceda, límites y capacidad del sitio; una página pública no autoriza una carga desproporcionada.
- Prefiere una instancia propia protegida para investigaciones sensibles y restringe el panel a la red o proxy autorizado.
- Cifra copias de seguridad, limita retención y separa secretos de los datos de investigación.
- No introduzcas cookies personales en vigilancias compartidas ni captures contenido privado sin base legal.
- Evita enviar el diff completo a servicios externos si contiene datos personales o información confidencial.
- Registra quién creó y modificó filtros, intervalos y notificaciones.
- Distingue siempre «cambio observado» de «intención atribuida».

El propio proyecto recuerda en su documentación que quien opera la herramienta debe cumplir las condiciones del sitio y la normativa de protección de datos. La responsabilidad no se delega en el software.

## Instalación y operación a alto nivel

Para una prueba local, el repositorio ofrece Docker, Docker Compose y una instalación mediante `pip`. En producción, usa la configuración oficial vigente, fija una versión revisada, conserva el volumen de datos y no expongas directamente el puerto de administración a internet. El ejemplo de Docker del proyecto enlaza por defecto el servicio a `127.0.0.1`, una pista razonable para empezar con acceso local.

Antes de incorporar una instancia al trabajo real, valida:

- autenticación, TLS y proxy inverso;
- actualizaciones y copia recuperable del almacén;
- reloj y zona horaria;
- límites de frecuencia y concurrencia;
- recuperador HTTP frente a navegador;
- canales de aviso y protección de credenciales;
- retención, acceso y borrado de capturas;
- exportación del historial necesario para auditoría.

No copies comandos de una entrada de blog como receta permanente: revisa el [`docker-compose.yml` oficial](https://github.com/dgtlmoon/changedetection.io/blob/master/docker-compose.yml) y la documentación actual antes de desplegar.

## Alternativas y siguientes pasos

- **RSS/Atom** es preferible cuando la fuente ofrece un feed fiable: expresa publicaciones sin raspar la presentación.
- **Git y APIs oficiales** aportan historial estructurado cuando el publicador los mantiene.
- **Wayback Machine o Archive.today** ayudan a buscar y preservar versiones externas, aunque su cobertura y tiempos no son completos.
- **Hunchly o un archivo WARC** son más apropiados para documentar la navegación y conservar evidencia con contexto.
- **Distill.io, Visualping o Wachete** ofrecen otros modelos de monitorización; revisa privacidad, exportación y condiciones antes de usarlos.
- **Un script pequeño con `curl`, hashes y un planificador** puede bastar para una fuente estable, si registra errores y no confunde un hash con significado.

El siguiente paso natural es crear un **registro de cambios verificable**: por cada alerta, enlazar captura anterior, captura nueva, hash, fuente primaria corroborante y decisión del analista. Esa tabla convierte el ruido operativo en una cronología revisable.

## Conclusión

El takeaway accionable es concreto: **elige una página pública de bajo riesgo, define una sola sección, comprueba una vez al día y ensaya el protocolo con un cambio conocido**. Verifica que el filtro detecta lo relevante, que un fallo genera una alerta de salud y que el equipo puede reconstruir qué observó.

changedetection.io no sustituye al analista ni certifica la intención detrás de una edición. Su valor está en reducir el trabajo repetitivo y abrir una ventana temporal documentada. Cuando cada diff conserva procedencia, contexto y una revisión independiente, la vigilancia deja de ser una colección de campanas y se convierte en método.

## Fuentes consultadas

- [Repositorio y documentación principal de changedetection.io](https://github.com/dgtlmoon/changedetection.io)
- [Especificación de la API de changedetection.io](https://changedetection.io/docs/api_v1/)
- [Tutorial oficial para detectar contenido nuevo](https://changedetection.io/tutorial/how-monitor-website-new-content)
- [Tutorial oficial sobre notificaciones por correo y selector visual](https://changedetection.io/tutorial/email-notification-when-web-page-changes-how)
- [Notas oficiales de configuración de notificaciones](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes)
- [Configuración oficial de Docker Compose](https://github.com/dgtlmoon/changedetection.io/blob/master/docker-compose.yml)
- [Apprise: motor de notificaciones utilizado por el proyecto](https://github.com/caronc/apprise)
