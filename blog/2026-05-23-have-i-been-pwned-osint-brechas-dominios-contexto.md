---
title: "Have I Been Pwned en OSINT: brechas, dominios verificados y contexto antes de alarmar"
slug: /have-i-been-pwned-osint-brechas-dominios-contexto
authors: [osint-writter]
tags: [osint, breaches, email, verification, privacy, methodology]
date: 2026-05-23
image: /img/blog/2026-05-23-have-i-been-pwned-osint-brechas-dominios-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando exposicion de dominios, brechas y senales de verificacion en un panel sobrio de riesgo y contexto](/img/blog/2026-05-23-have-i-been-pwned-osint-brechas-dominios-contexto.png)

Cuando aparece un correo corporativo en una brecha, el impulso mas peligroso no suele ser tecnico. Suele ser narrativo: **dar por hecho que ya entendemos el alcance, la actualidad y hasta la responsabilidad del incidente con solo ver una coincidencia**. `Have I Been Pwned` (`HIBP`) es util precisamente porque fuerza una version mas disciplinada de la pregunta: que exposicion publica y verificable existe alrededor de una direccion o de un dominio, y que parte de esa exposicion sigue necesitando contexto antes de convertirse en conclusion.

La herramienta tiene ademas una virtud metodologica poco vistosa, pero importante: separa bien cosas que mucha gente mezcla. Una cosa es saber que un email aparecio en una brecha. Otra, muy distinta, es conocer los datos exactos comprometidos. Y otra distinta aun es decidir si eso implica riesgo operativo actual. En la documentacion oficial visible a **23 de mayo de 2026**, `HIBP` insiste en esos limites: para cuentas y dominios devuelve presencia en brechas y clases de datos; para contrasenas usa un servicio aparte; y para dominios exige demostrar control antes de mostrar resultados sensibles.

<!-- truncate -->

## Que es y para que sirve

`Have I Been Pwned` es un servicio orientado a consultar si una direccion de correo, un dominio verificado o una contrasena expuesta aparecen en conjuntos de brechas conocidos. La documentacion oficial de la API v3 y el centro de soporte dejan claras cuatro piezas operativas:

- la busqueda por cuenta y por dominio usa la API autenticada;
- la busqueda por dominio requiere verificar control del dominio antes de acceder a resultados;
- `Pwned Passwords` funciona como servicio separado y gratuito;
- y el sistema no entrega la brecha "cruda", sino metadatos y clases de datos expuestos.

Traducido a OSINT responsable, `HIBP` sirve para:

- estimar exposicion historica de correos o dominios propios o autorizados;
- detectar si una organizacion acumula senales de riesgo repartidas en varias brechas;
- priorizar revisiones defensivas, rotacion de credenciales o comunicacion interna;
- y documentar mejor que parte de un hallazgo es observacion verificable y que parte sigue siendo inferencia.

Su valor no esta en el dramatismo de "has sido hackeado". Esta en **ordenar la conversacion sobre exposicion publica con un minimo de rigor y trazabilidad**.

## Caso de uso legitimo con ejemplo ficticio

Imagina que una empresa ficticia, `puerto-norte.example`, va a incorporar a un proveedor que tendra acceso a documentacion sensible. Antes de cerrar el alta, el equipo de riesgo quiere revisar si el dominio del proveedor arrastra una huella publica de exposicion especialmente mala.

El flujo sensato no seria coleccionar correos individuales ni intentar reconstruir vidas digitales. Seria algo mas sobrio:

1. verificar si el dominio puede monitorizarse legitimamente;
2. revisar cuantas direcciones aparecen afectadas por brechas conocidas;
3. observar en que tipos de brechas o clases de datos aparece la exposicion;
4. y usar esa senal solo como input de riesgo, nunca como sentencia automatica.

Si el dominio muestra varias direcciones afectadas y clases de datos preocupantes, tienes una razon para pedir controles compensatorios o confirmacion de rotaciones. Si apenas hay ruido historico o solo aparecen listas de spam, la conclusion tambien cambia. El matiz importa.

## Flujo recomendado

### 1. Empieza separando cuenta, dominio y contrasena

`HIBP` no es una sola consulta magica. La API v3 distingue entre:

- busqueda de brechas por direccion de correo;
- busqueda de dominios verificados;
- y `Pwned Passwords`, que consulta hashes de contrasenas sin vincularlos a una identidad.

La pagina de soporte sobre clases de datos lo resume bien: `HIBP` mantiene separados los datos de brechas y `Pwned Passwords`, y no enlaza una contrasena concreta con una persona concreta. Esa separacion es buena noticia para privacidad y tambien una pista metodologica: **no mezcles hallazgos de naturaleza distinta como si todos midieran lo mismo**.

### 2. Para dominios, verifica control antes de buscar

La pagina oficial "How do I verify my domain?" indica que cada dominio debe verificarse individualmente y que verificar el dominio raiz no cubre automaticamente subdominios. A 22 de marzo de 2026, `HIBP` ofrece cuatro vias manuales de verificacion desde el panel:

- registro `DNS TXT`;
- meta tag HTML;
- fichero HTML subido al servidor;
- o enlace enviado a direcciones administrativas estandar del dominio.

Eso encaja muy bien con una regla OSINT que conviene repetir: **si no controlas el dominio, no deberias tratar la capacidad de consultar su exposicion como si fuera una funcion publica sin restricciones**.

### 3. Interpreta las clases de datos, no solo el contador

La ayuda oficial explica que `HIBP` almacena direcciones de correo y metadatos sobre las clases de datos comprometidos, pero no muestra las credenciales o registros completos robados. En dominio monitorizado, eso significa que puedes saber que hubo exposicion de categorias como telefonos, fechas de nacimiento o contrasenas, pero no vas a recibir el contenido completo.

Para el analista, eso cambia la forma de trabajar:

- un contador alto puede ser menos grave de lo que parece si predomina ruido de spam lists;
- una sola brecha puede importar mucho si las clases de datos son sensibles;
- y la ausencia de datos crudos obliga a corroborar el riesgo con el contexto de negocio, no con morbo.

### 4. Usa `Pwned Passwords` como control defensivo, no como fetiche

La documentacion oficial de `Pwned Passwords` y la API v3 recalcan que este servicio es gratuito, no requiere suscripcion y utiliza consultas por rango con `k-anonymity`: solo se envia el prefijo del hash, no la contrasena completa. Tambien admite `Add-Padding` para homogeneizar tamano de respuesta y reducir fugas por longitud.

La conclusion practica es clara: `Pwned Passwords` es excelente para controles defensivos de higiene de contrasenas, pero **no sirve para "buscar la contrasena de alguien"** ni deberia presentarse como si lo hiciera.

### 5. Ten en cuenta el modelo comercial actual antes de automatizar

Segun la ayuda oficial publicada el **28 de marzo de 2026**, `HIBP` sustituyo los antiguos planes `Pwned` por `Core`, `Pro` y `High RPM`. La propia pagina explica que `Pro` anade monitorizacion de dominios de clientes, verificacion por API, busqueda de email via `k-anonymity` y acceso a stealer logs, mientras que `High RPM` prioriza volumen de consultas API sin funciones de monitorizacion de dominios.

Ese detalle no es marketing irrelevante. En OSINT corporativo importa porque condiciona que automatizaciones son realistas y bajo que modelo de autorizacion.

## Limitaciones y falsos positivos

- que un correo aparezca en una brecha no demuestra compromiso actual de la cuenta;
- que un dominio acumule exposicion no demuestra mala praxis reciente sin contexto temporal;
- una brecha marcada como `spam list` no tiene el mismo peso que una intrusión confirmada;
- el propio servicio no entrega el dataset completo, asi que no deberias fingir un nivel de certeza que no tienes;
- y una politica de monitorizacion mal planteada puede convertir datos defensivos en coleccionismo de PII innecesaria.

Tambien conviene recordar otra limitacion expresamente visible en el soporte actual: cada subdominio requiere verificacion propia. Eso reduce suposiciones peligrosas sobre cobertura automatica.

## Buenas practicas de OPSEC, etica y privacidad

- Consulta solo dominios propios, autorizados o dentro de un encargo legitimado.
- Conserva fecha, consulta y motivo analitico de cada revision.
- Trata la exposicion historica como senal de riesgo, no como prueba de culpa.
- No conviertas un resultado de brecha en excusa para contactar personas o ampliar recoleccion sin necesidad.
- Si integras `Pwned Passwords` en controles internos, espera a que el usuario termine de escribir la contrasena antes de lanzar la consulta, tal como advierte la documentacion sobre los riesgos del chequeo incremental.

La mejor manera de usar `HIBP` en OSINT no es como escaparate de sustos. Es como una capa de corroboracion defensiva y proporcional.

## Alternativas y siguientes pasos

Si tu pregunta principal es exposicion de un dominio concreto, `HIBP` funciona mejor cuando ya existe autorizacion y un alcance bien definido. Si necesitas revisar contexto de infraestructura, historico DNS o certificados, conviene pivotar antes a otras fuentes como `SecurityTrails`, `CT logs` o buscadores de infraestructura ya tratados en el blog. Si lo que buscas es mejorar politicas internas de contrasenas, la pieza mas util suele ser `Pwned Passwords`, no la monitorizacion de correos.

La takeaway accionable es sencilla: usa `Have I Been Pwned` para medir exposicion y priorizar preguntas, no para cerrar conclusiones ni amplificar datos sensibles. En OSINT serio, una coincidencia bien contextualizada vale mas que una alerta mal interpretada.

## Fuentes

- Have I Been Pwned, `API v3`: https://haveibeenpwned.com/api/v3
- Have I Been Pwned Support, `What information and data classes are stored in Have I Been Pwned (HIBP)?` (22 de marzo de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/13489538902415-What-information-and-data-classes-are-stored-in-Have-I-Been-Pwned-HIBP
- Have I Been Pwned Support, `How do I verify my domain?` (22 de marzo de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/15543011690767-How-do-I-verify-my-domain
- Have I Been Pwned Support, `How do I get started with Domain Search monitoring?` (22 de marzo de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/15316197244559-How-do-I-get-started-with-Domain-Search-montoring
- Have I Been Pwned Support, `How do I get started after purchasing a subscription?` (22 de marzo de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/15542964608655-How-do-I-get-started-after-purchasing-a-subscription
- Have I Been Pwned Support, `I wish to use the Pwned Passwords API. How can I get started?` (28 de febrero de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/15316377846671-I-wish-to-use-the-Pwned-Passwords-API-How-can-I-get-started
- Have I Been Pwned Support, `What happened to the old "Pwned" subscription plans?` (28 de marzo de 2026): https://support.haveibeenpwned.com/hc/en-au/articles/15617510034063-What-happened-to-the-old-Pwned-subscription-plans
