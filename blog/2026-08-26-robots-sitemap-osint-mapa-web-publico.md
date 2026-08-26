---
title: "robots.txt y sitemap.xml en OSINT: mapear una web sin confundir indicios con acceso"
slug: /robots-sitemap-osint-mapa-web-publico
authors: [osint-writter]
tags: [osint, investigation, web, methodology, verification, privacy]
date: 2026-08-26
image: /img/blog/2026-08-26-robots-sitemap-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de un analista OSINT comparando robots.txt, un sitemap XML y la estructura pública de una web](/img/blog/2026-08-26-robots-sitemap-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/robots-sitemap-osint-mapa-web-publico.m4a)


*Imagen generada mediante inteligencia artificial.*

Una empresa ficticia anuncia que ha retirado una línea de producto, pero su buscador interno sigue devolviendo fichas antiguas y el menú público ya no enlaza algunas páginas. El impulso fácil es lanzar un rastreador sobre todo el dominio. El método prudente empieza de forma más pequeña: consultar los mapas que el propio sitio publica para los robots, registrar qué declaran y comprobar cada URL relevante con peticiones normales. **`robots.txt` y `sitemap.xml` pueden revelar cómo quiere presentarse una web a los rastreadores; no demuestran que una ruta sea privada, importante, vigente ni siquiera accesible.**

<!-- truncate -->

Este artículo propone un flujo reproducible y de bajo impacto para analizar esos dos artefactos en investigaciones legítimas de *due diligence*, verificación web o inventario autorizado. Las fuentes técnicas se consultaron el **26 de agosto de 2026**. El dominio, la organización, las rutas, los productos y las fechas del caso son ficticios. No se prueban credenciales, no se eluden controles ni se fuerzan rutas que el servidor no publique.

## Qué son y para qué sirven en OSINT

El archivo `robots.txt` implementa el **Robots Exclusion Protocol** (REP). El [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html) lo estandariza como un mecanismo mediante el cual un servicio indica a clientes automáticos —los *crawlers*— qué rutas pueden solicitar. Se publica en la raíz del servicio, por ejemplo `https://www.ejemplo.test/robots.txt`, y organiza reglas alrededor de agentes de usuario, permisos y prohibiciones.

Un sitemap cumple otra función: enumera URLs que el editor desea facilitar a los buscadores. El [protocolo Sitemaps](https://www.sitemaps.org/protocol.html) define el formato XML básico y sus campos; también admite índices que enlazan varios sitemaps. La [documentación de Google](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=es) insiste en una distinción esencial: un sitemap ayuda a descubrir contenido, pero no garantiza que una URL sea rastreada ni indexada.

Para un analista, ambos son **declaraciones públicas de operación**, no inventarios autoritativos:

| Artefacto | Qué puede aportar | Qué no demuestra |
| --- | --- | --- |
| `robots.txt` | Patrones de rutas, grupos por *user-agent* y ubicaciones de sitemaps | Confidencialidad, existencia de todas las rutas o obediencia de todos los robots |
| Sitemap | URLs preferidas, agrupación editorial y, a veces, `lastmod` | Publicación original, disponibilidad actual, indexación o fecha probada del contenido |
| Respuesta HTTP de una URL | Estado observado, redirecciones, cabeceras y cuerpo en ese momento | Qué vio otro usuario, qué existía antes o cuál era la intención del editor |
| Archivo web o captura propia | Una representación conservada con fecha de observación | Que nunca hubiera otras versiones ni que el contenido fuera verdadero |

El valor OSINT aparece al **comparar capas**. Una URL presente en el sitemap pero ausente del menú puede ser contenido legítimo poco enlazado. Una ruta desautorizada puede ser un patrón genérico de un CMS. Una fecha `lastmod` puede reflejar una regeneración técnica. Cada señal abre una pregunta; ninguna cierra el caso por sí sola.

## Caso de uso legítimo: auditar un catálogo público

Supongamos que `https://catalogo-ejemplo.test/` pertenece a una cooperativa ficticia que comunica el fin de la familia de productos «Lumen». Una revisión autorizada quiere responder solo a tres preguntas:

1. ¿Qué URLs sobre «Lumen» declara actualmente el sitio?
2. ¿Cuáles responden mediante navegación HTTP normal?
3. ¿Qué cambios pueden documentarse sin atribuir intención?

El alcance escrito incluye el host público y excluye áreas autenticadas, formularios, endpoints de administración y cualquier carga intensiva. Antes de consultar, se crea una nota con hora UTC, finalidad, agente de usuario identificable y límites de peticiones. Después se recuperan únicamente los puntos de entrada previsibles:

```bash
curl -fsS --max-time 15 \
  -A 'AuditoriaPublicaOSINT/1.0 contacto@example.test' \
  'https://catalogo-ejemplo.test/robots.txt'

curl -fsS --max-time 15 \
  -A 'AuditoriaPublicaOSINT/1.0 contacto@example.test' \
  'https://catalogo-ejemplo.test/sitemap.xml'
```

El ejemplo usa un dominio reservado y datos ficticios: no debe copiarse contra un objetivo real sin base legítima, alcance y una frecuencia proporcionada. Si `robots.txt` declara otro sitemap mediante una línea `Sitemap:`, se registra esa URL exacta. No se adivinan decenas de nombres ni se convierten los errores `404` en una enumeración agresiva.

Imaginemos que el sitemap enlaza `/productos/lumen-azul`, mientras `robots.txt` contiene `Disallow: /busqueda-interna/`. La conclusión correcta no es «hemos encontrado una zona secreta». La nota sería mucho más estrecha:

> A las 08:40 UTC, el sitemap publicado declaró una ficha Lumen. El REP desaconsejó a ciertos rastreadores solicitar rutas bajo `/busqueda-interna/`. No se accedió a esa zona ni se infirió su contenido.

Después se solicita solo la ficha declarada, se conserva el estado HTTP, la cadena de redirecciones y una copia permitida. Si devuelve `301` hacia una categoría histórica, eso prueba una redirección observada, no cuándo se retiró el producto. Para una cronología hará falta contrastar notas oficiales, capturas archivadas y observaciones anteriores.

## Flujo recomendado paso a paso

### 1. Define pregunta, autoridad y presupuesto de acceso

Escribe qué necesitas demostrar y qué dominios están incluidos. Fija un máximo de solicitudes, una pausa razonable y criterios de parada. Para una comprobación manual suelen bastar `robots.txt`, los sitemaps declarados y unas pocas URLs relevantes; no hace falta rastrear todo lo encontrado.

Separa también los roles:

- **propietario del sitio**: publica los artefactos y controla el servidor;
- **rastreador**: decide si interpreta y respeta las reglas aplicables;
- **buscador**: rastrea, procesa e indexa según sus propios sistemas;
- **analista**: observa respuestas públicas dentro de un propósito y alcance legítimos.

Confundir esos roles lleva a afirmar, por ejemplo, que una prohibición equivale a un control de acceso. No es así.

### 2. Captura la respuesta completa, no solo el texto

Registra la URL solicitada, fecha UTC, código HTTP, tipo de contenido, redirecciones y hash del cuerpo. Conserva por separado lo recibido y tu interpretación. Un esquema mínimo puede ser:

```text
observed_at: 2026-08-26T08:40:00Z
requested_url: https://catalogo-ejemplo.test/robots.txt
final_url: https://catalogo-ejemplo.test/robots.txt
status: 200
content_type: text/plain
sha256: <hash-ficticio>
method: GET manual, una solicitud
```

El RFC 9309 describe el tratamiento de redirecciones, errores y caché para clientes automáticos. El analista no debe rellenar los huecos: si recibe un error, documenta el error observado; si una redirección sale del alcance, se detiene.

### 3. Analiza `robots.txt` como reglas dirigidas

No leas cada `Disallow` aislado. Identifica primero el grupo de `User-agent` al que pertenece y conserva el orden y la codificación originales. Comprueba:

- si existe un grupo global `*` y otros específicos;
- qué patrones se declaran y para qué agente;
- si hay reglas `Allow` que matizan una prohibición más amplia;
- si aparecen una o varias líneas `Sitemap:`;
- si el contenido parece generado por una plataforma común;
- si la respuesta cambia entre HTTP/HTTPS, host principal y subdominios incluidos en alcance.

La [guía de Google sobre `robots.txt`](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=es) advierte que las reglas no son un mecanismo para mantener una página fuera de Google ni para proteger información: otros robots pueden interpretarlas de manera distinta, y una URL desautorizada puede llegar a conocerse mediante enlaces externos. En OSINT responsable, esa limitación se traduce en una regla sencilla: **no trates una ruta declarada como invitación a visitarla**.

### 4. Resuelve sitemaps e índices sin perder procedencia

Un sitemap puede ser XML, texto o un feed compatible. En XML, `urlset` contiene entradas `url`; cada una requiere `loc`, mientras que `lastmod`, `changefreq` y `priority` son opcionales. Un `sitemapindex` enlaza otros sitemaps.

Para cada nivel conserva la relación:

```text
robots.txt
└── Sitemap: /sitemap-index.xml
    ├── /sitemaps/productos.xml
    └── /sitemaps/noticias.xml
        └── https://catalogo-ejemplo.test/noticias/retirada-lumen
```

No mezcles URLs de distintos ficheros sin registrar su origen. La ubicación del sitemap condiciona qué rutas puede representar según el protocolo, y un índice grande puede cambiar mientras lo recorres. Anota el hash y la hora de cada fichero para que otra persona sepa qué versión analizaste.

La especificación permite hasta **50.000 URLs o 50 MB sin comprimir por sitemap**. Ese límite técnico no es un objetivo de descarga. En una investigación concreta, filtra localmente por la pregunta y evita solicitar masivamente todas las páginas listadas.

### 5. Interpreta `lastmod` como una afirmación, no como un reloj forense

El protocolo indica que `lastmod` debe expresar la última modificación de la página, no la hora de generación del sitemap. Sin embargo, el valor lo publica el propio sistema y su calidad depende de la implementación. Puede referirse a una actualización de plantilla, a un cambio del contenido o a un proceso automático.

Por tanto, etiqueta tres tiempos distintos:

- **fecha declarada** en `lastmod`;
- **fecha de observación** de tu descarga;
- **fecha corroborada** por otra fuente o versión conservada.

Si no coinciden, no elijas la que mejor encaje con la hipótesis. Describe la discrepancia y busca evidencia independiente.

### 6. Verifica una muestra relevante y guarda negativos

Para cada URL seleccionada registra `200`, redirección, `404`, `410`, bloqueo o error transitorio. Una respuesta negativa también tiene procedencia y caducidad: «devolvió `404` a tal hora» no significa «nunca existió».

Compara, cuando sea proporcional:

- presencia en sitemap frente a navegación pública;
- URL declarada frente a canonical de la página;
- `lastmod` frente a cabeceras HTTP y contenido visible;
- estado actual frente a una captura web legítima;
- afirmación comercial frente a documentación oficial.

### 7. Redacta hallazgos con niveles de confianza

Una tabla evita convertir pistas en hechos:

| Hallazgo | Lectura prudente | Confianza |
| --- | --- | --- |
| URL en sitemap de productos | El editor la declaró al rastreador en la versión observada | Alta para la declaración; baja para vigencia comercial |
| Patrón en `Disallow` | Ese grupo REP pidió no rastrear rutas coincidentes | Alta para el texto; nula para confidencialidad o contenido |
| `lastmod` anterior al anuncio | El sistema publicó esa fecha | Media para la afirmación; baja para el cambio real sin corroboración |
| Redirección actual a archivo | El servidor redirigió la solicitud observada | Alta para ese momento; baja para el inicio de la redirección |

## Limitaciones y falsos positivos

### `robots.txt` no es una lista de secretos

Muchos CMS publican patrones genéricos aunque no exista contenido sensible detrás. Otros conservan reglas antiguas después de una migración. Una ruta también puede coincidir con recursos públicos que simplemente generan mucho ruido para un buscador.

### El sitemap no contiene necesariamente toda la web

Puede excluir páginas válidas, incluir URLs obsoletas o dividirse por tipo, idioma, fecha o tecnología. Google recalca que una web bien enlazada puede descubrirse sin sitemap y que enviarlo es una pista, no una garantía. La ausencia en el fichero no prueba ocultación.

### Las reglas no equivalen entre agentes

El REP dirige grupos a tokens de agente de usuario. Extensiones históricas o comportamientos de proveedores pueden variar. Si tu conclusión depende de cómo actúa un crawler concreto, cita la documentación de ese crawler y la fecha de consulta; no generalices desde Googlebot a todos los robots.

### La publicación no demuestra autoría ni intención

Un fichero puede proceder de un plugin, una plantilla o una infraestructura compartida. Que una URL aparezca en un sitemap no identifica quién la creó. Que desaparezca tampoco demuestra encubrimiento: puede deberse a despliegues, errores, cambios editoriales o caducidad normal.

### JavaScript, idiomas y hosts fragmentan la imagen

La navegación renderizada puede descubrir rutas que el HTML inicial o el sitemap no muestran. Los subdominios tienen ámbitos separados, y una versión localizada puede declarar otros recursos. Amplía el alcance solo si la pregunta y la autorización lo justifican.

## Buenas prácticas de OPSEC, ética y privacidad

- Usa una identidad de agente honesta cuando proceda y un canal de contacto operativo.
- Respeta las reglas aplicables, los términos del servicio, la legislación y el alcance acordado.
- Limita velocidad, volumen y profundidad; detente ante errores repetidos o degradación del servicio.
- No visites rutas de administración, copias, exportaciones o datos personales solo porque aparezcan declaradas.
- No intentes eludir autenticación, restricciones geográficas, CAPTCHA ni controles técnicos.
- Minimiza datos personales en notas, capturas y ejemplos; redacta identificadores que no sean necesarios.
- Conserva hashes, horas UTC y respuestas originales, pero protege el archivo de trabajo y define retención.
- Separa observación, inferencia e hipótesis en el informe.
- Si detectas exposición accidental, no la amplifiques: pausa, preserva lo mínimo y usa un canal responsable.

El RFC 9309 es especialmente claro en sus consideraciones de seguridad: publicar reglas puede revelar rutas y **no sustituye a medidas de seguridad válidas**. Esta advertencia sirve tanto al propietario como al investigador. El primero debe proteger con autorización real lo que no deba ser público; el segundo no debe interpretar una mala configuración como permiso.

## Checklist operativo

- [ ] Pregunta de investigación y alcance escritos.
- [ ] Host, esquema y subdominios autorizados identificados.
- [ ] Presupuesto de solicitudes y criterio de parada definidos.
- [ ] `robots.txt` capturado con estado, hora, cabeceras y hash.
- [ ] Sitemaps declarados resueltos conservando su árbol de procedencia.
- [ ] Grupos `User-agent`, `Allow` y `Disallow` interpretados en contexto.
- [ ] `lastmod` etiquetado como dato declarado.
- [ ] Solo se verificó una muestra pertinente de URLs públicas.
- [ ] Redirecciones fuera de alcance no se siguieron.
- [ ] Hallazgos corroborados con otra clase de fuente cuando fue posible.
- [ ] Informe separa hechos observados, inferencias y ausencias.
- [ ] Datos y capturas tienen protección y retención proporcionadas.

## Alternativas y siguientes pasos

`robots.txt` y los sitemaps funcionan bien como punto de partida ligero. Para completar el mapa sin convertirlo en una campaña de enumeración puedes usar:

- navegación y enlaces internos, que muestran la arquitectura presentada a personas;
- feeds RSS o Atom, útiles para cambios recientes pero normalmente incompletos;
- cabeceras `Link` y etiquetas canonical, que expresan relaciones entre representaciones;
- archivos web, para comparar versiones observadas en el tiempo;
- Search Console, únicamente cuando eres propietario o tienes autorización sobre el sitio;
- un inventario del CMS o del servidor, si trabajas desde el lado defensivo con permiso.

El takeaway accionable es este: **captura primero la declaración, verifica después una muestra y concluye solo lo que ambas capas sostienen**. `robots.txt` expresa preferencias de rastreo; un sitemap expresa URLs que el editor quiere facilitar; la respuesta HTTP expresa lo que el servidor entregó en un instante. Mantener esas frases separadas produce informes más útiles y evita presentar un mapa parcial como una puerta abierta.

El siguiente tema natural será estudiar `canonical`, `hreflang` y redirecciones como grafo de identidad de páginas, sin asumir que dos URLs representan siempre el mismo contenido.

## Fuentes consultadas

- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html)
- [Sitemaps.org: protocolo XML de Sitemaps](https://www.sitemaps.org/protocol.html)
- [Google Search Central: introducción a robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=es)
- [Google Search Central: qué es un sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=es)
- [Google Search Central: crear y enviar un sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=es)
