---
title: "VEX en OSINT: decidir si una vulnerabilidad afecta sin aceptar un veredicto a ciegas"
slug: /vex-osint-explotabilidad-contexto
authors: [osint-writter]
tags: [osint, tooling, verification, data, investigation, privacy]
date: 2026-11-07
image: /img/blog/2026-11-07-vex-osint-explotabilidad.png
aiDisclosure: generated
humanReviewed: false
---

Un escáner encuentra una biblioteca asociada a una vulnerabilidad crítica dentro de un producto. El proveedor responde con un fichero VEX que dice `not_affected`. La alerta desaparece del panel y el caso parece cerrado. **Pero una declaración legible por máquinas no demuestra por sí sola que se refiera al artefacto recibido, que la ruta vulnerable sea inalcanzable ni que el análisis siga vigente.** En una investigación OSINT responsable, VEX no sustituye la evidencia: organiza una afirmación para que podamos identificarla, contrastarla y revisarla.

![Analista comparando un inventario de software, un aviso de vulnerabilidad y la evidencia específica del producto](/img/blog/2026-11-07-vex-osint-explotabilidad.png)

*Imagen generada mediante inteligencia artificial.*

<!-- truncate -->

Este artículo propone un flujo defensivo para evaluar declaraciones **Vulnerability Exploitability eXchange** sobre software público, propio o examinado con autorización. El ejemplo es ficticio. No requiere explotar la vulnerabilidad, ejecutar código desconocido ni probar sistemas de terceros.

## Qué es VEX y para qué sirve

VEX es una forma estructurada de comunicar el estado de un producto frente a una vulnerabilidad concreta. La guía de [requisitos mínimos de CISA](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf) modela cada declaración alrededor de un identificador de producto, un identificador de vulnerabilidad y un estado. El documento también conserva autor, versión y marcas temporales para que una actualización no se confunda con la afirmación anterior.

Los cuatro estados mínimos son:

| Estado | Lectura prudente | Pregunta siguiente |
| --- | --- | --- |
| `not_affected` | el autor afirma que esa vulnerabilidad no afecta al producto identificado | ¿qué justificación y qué evidencia sostienen la afirmación? |
| `affected` | el autor considera afectado el producto y debe indicar una acción | ¿qué versiones, configuraciones y mitigaciones entran en alcance? |
| `fixed` | el producto identificado contiene una corrección | ¿el artefacto recibido es exactamente esa versión corregida? |
| `under_investigation` | todavía no existe conclusión final | ¿qué precaución temporal aplicamos y cuándo se revisará? |

VEX nació muy ligado al SBOM, pero no es otro inventario. El SBOM intenta describir componentes y relaciones; VEX expresa el estado de uno o más productos respecto de una vulnerabilidad. [CycloneDX](https://www.cyclonedx.org/capabilities/vex/) puede representar ambas capas y subraya que la explotabilidad depende del contexto específico del producto. [OpenVEX](https://github.com/openvex/spec) propone una representación mínima y agnóstica respecto al formato del SBOM. El perfil VEX de [CSAF mantenido por OASIS](https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html#45-profile-5-vex) integra estas afirmaciones en avisos de seguridad más ricos.

Estos formatos no son equivalentes campo por campo. Convertir entre ellos exige comprobar identificadores, estados, justificaciones, historial y cualquier semántica que el destino no pueda conservar.

### Lo que VEX no demuestra

Un VEX válido sintácticamente no prueba que:

- el autor tenga conocimiento completo del producto;
- el identificador alcance el binario, imagen o dispositivo que estamos evaluando;
- la vulnerabilidad sea imposible de explotar bajo cualquier configuración;
- la justificación siga siendo cierta después de una reconstrucción;
- la firma identifique a una entidad en la que debamos confiar;
- una alerta descartada hoy pueda ignorarse indefinidamente.

CISA insiste en que los estados no pretenden cerrar la discusión, sino ayudar al consumidor a tomar decisiones informadas. Esa distinción convierte VEX en una fuente evaluable, no en un interruptor universal para silenciar hallazgos.

## Caso de uso legítimo con ejemplo ficticio

La empresa ficticia `Puerto Claro Software` entrega a un organismo una imagen de contenedor, su digest, un SBOM y un VEX. Un escáner relaciona el componente `lib-ejemplo` con `CVE-20XX-12345`. El VEX declara el producto `not_affected` porque el código vulnerable no está en la ruta de ejecución.

El equipo de debida diligencia no intenta explotar la imagen. Quiere contestar una pregunta más estrecha:

> ¿La afirmación del proveedor está suficientemente vinculada a esta entrega y respaldada para aceptar el riesgo residual durante el periodo acordado?

Se abre una matriz de evidencia:

| Capa | Evidencia disponible | Límite |
| --- | --- | --- |
| artefacto | imagen fijada por digest y origen | el hash no explica su comportamiento |
| inventario | SBOM con componente y versión declarados | puede tener omisiones o alcance distinto |
| vulnerabilidad | identificador y aviso primario | la descripción general no decide el contexto del producto |
| VEX | autor, producto, estado, justificación y fecha | sigue siendo una afirmación del emisor |
| corroboración | configuración de compilación, análisis de alcance y pruebas autorizadas | ninguna técnica aislada cubre todas las rutas posibles |

La conclusión no será «VEX dice que es seguro». Podría ser:

> Para el artefacto con digest `sha256:…`, el proveedor declaró el 7 de noviembre que `CVE-20XX-12345` no afecta al producto porque el código vulnerable no entra en la ruta de ejecución. La revisión confirmó el componente y la configuración declarada, pero no demostró todas las rutas en producción. Se acepta provisionalmente la afirmación hasta un nuevo digest, un cambio de configuración o la fecha de revisión.

El digest y el CVE del ejemplo son deliberadamente ficticios; no deben reutilizarse como indicadores reales.

## Flujo recomendado

### 1. Fija el objeto antes de leer el estado

Registra el artefacto exacto, su digest, origen, fecha de obtención y entorno previsto. Conserva por separado el SBOM y el VEX originales con sus hashes. Si la declaración solo identifica «Producto Enterprise» y la entrega se llama `producto-enterprise:2026.11`, todavía falta demostrar que ambos nombres designan el mismo objeto.

Prefiere identificadores estables y suficientemente precisos: URL de producto verificable, `purl`, CPE cuando resulte apropiado, versión, digest o una referencia inequívoca a la entrega. Un nombre comercial sin edición ni versión favorece coincidencias falsas.

### 2. Valida estructura, autoría y procedencia por separado

La validación de esquema responde si el documento cumple la estructura esperada. La firma o el canal autenticado ayudan a relacionarlo con un emisor. Ninguna de las dos cosas demuestra que el contenido sea correcto.

Anota al menos:

- formato y perfil declarados;
- identificador y versión del documento;
- autor y rol;
- primera emisión y última actualización;
- mecanismo de distribución y, si existe, firma;
- herramienta que validó el fichero y resultado completo.

Los requisitos mínimos de CISA contemplan versiones incrementales y marcas temporales. No sobrescribas silenciosamente un VEX antiguo: una rectificación forma parte de la cronología de la investigación.

### 3. Resuelve producto, componente y vulnerabilidad

Comprueba tres enlaces distintos:

1. **VEX → producto:** la declaración alcanza la entrega evaluada.
2. **producto → componente:** el componente vulnerable está presente, ausente o transformado de la manera indicada.
3. **componente → vulnerabilidad:** el aviso aplica realmente a esa variante y versión.

No deduzcas el segundo enlace solo porque el SBOM y el VEX comparten un nombre parecido. Conserva los valores originales y documenta cualquier normalización de versiones, `purl`, CPE o alias.

### 4. Lee la justificación como una hipótesis comprobable

Para `not_affected`, la [guía de justificaciones de CISA](https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf) distingue cinco situaciones:

- `Component_not_present`: el componente no está incluido;
- `Vulnerable_code_not_present`: está el componente, pero no el código vulnerable;
- `Vulnerable_code_not_in_execute_path`: el código existe, pero no puede ejecutarse en el uso del producto;
- `Vulnerable_code_cannot_be_controlled_by_adversary`: el código se usa, pero un adversario no puede controlar las entradas necesarias;
- `Inline_mitigations_already_exist`: protecciones integradas impiden los vectores conocidos.

Cada justificación exige evidencia diferente. Un inventario puede ayudar con presencia; no basta para demostrar alcanzabilidad. Un grafo de llamadas puede apoyar una hipótesis sobre rutas; no cubre necesariamente reflexión, carga dinámica, plugins, configuraciones opcionales ni caminos introducidos en despliegue. Una mitigación documentada necesita además comprobar que está activa, no es deshabilitable en el contexto relevante y cubre el vector descrito.

### 5. Busca evidencia discriminante, no volumen

Formula primero qué observación haría caer la afirmación. Ejemplos:

- si el componente supuestamente ausente aparece en el artefacto final, `Component_not_present` queda refutado;
- si una opción de despliegue habilita la función vulnerable, la conclusión depende de configuración;
- si el VEX se refiere a otro digest, todavía no alcanza la entrega;
- si existe una versión posterior que cambia el estado, la anterior debe tratarse como histórica.

Usa materiales autorizados: manifiestos, registros de compilación, configuración publicada, atestaciones, documentación del proveedor y análisis estático o dinámico dentro de un laboratorio controlado. No pruebes explotación contra servicios ajenos.

### 6. Conserva desacuerdos y jerarquiza las fuentes

Un proveedor puede declarar `not_affected` mientras un investigador o integrador sostiene `affected`. No resuelvas el conflicto contando documentos. Registra para cada afirmación:

- quién la emite y qué acceso tiene al producto;
- artefacto, versión y configuración cubiertos;
- método y evidencia;
- fecha, caducidad y posibilidad de reproducción;
- interés, independencia y limitaciones del autor.

El conocimiento interno del proveedor puede ser decisivo, pero también puede estar incompleto. Una comprobación externa aporta independencia, pero quizá no vea opciones de compilación o código propietario. El estado honesto puede seguir siendo `under_investigation`.

### 7. Convierte el estado en una decisión revisable

Separa la afirmación técnica de la decisión de riesgo. Dos organizaciones pueden aceptar medidas diferentes ante el mismo VEX por su exposición, criticidad o capacidad de compensación.

Una ficha mínima debería contener:

```text
artefacto: digest y origen
vulnerabilidad: identificador y fuente primaria
declaración: autor, versión, fecha, estado y justificación
evidencia: observaciones a favor y en contra
decisión: aceptar, mitigar, actualizar, aislar o investigar
caducidad: fecha y eventos que fuerzan revisión
responsable: función, no datos personales innecesarios
```

Si el estado es `affected`, conserva la acción propuesta y verifica si aplica a tu versión. Si es `fixed`, exige el vínculo con el artefacto corregido. Si está `under_investigation`, define una protección temporal; no lo conviertas por comodidad en «sin riesgo».

## Limitaciones y falsos positivos

### Identidad de producto ambigua

Rangos de versión, ediciones, arquitecturas y reconstrucciones pueden romper el enlace entre el VEX y la entrega. Una coincidencia por nombre no basta; una ausencia de coincidencia tampoco demuestra que el documento sea irrelevante si los identificadores usan esquemas distintos.

### Análisis de alcanzabilidad incompleto

Las rutas dinámicas, características opcionales, llamadas nativas y configuración en producción pueden escapar al análisis. «No observado» debe mantenerse separado de «imposible».

### Estados que envejecen

Una nueva técnica de explotación, cambio de configuración o reconstrucción puede invalidar una justificación. El VEX necesita historial, distribución de actualizaciones y una política de reevaluación.

### Confianza mal colocada

Una firma protege integridad y ayuda a identificar al firmante; no certifica competencia, exhaustividad ni ausencia de conflicto de interés. Del mismo modo, un documento sin firma no es automáticamente falso: puede exigir más trabajo de procedencia.

### Automatización demasiado agresiva

Silenciar automáticamente toda alerta con estado `not_affected` puede ocultar un VEX caducado, genérico o referido a otro producto. La automatización debe comprobar identidad, versión, fechas, política de confianza y eventos de reapertura.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja solo con productos públicos, propios o autorizados y limita el análisis al alcance acordado.
- No ejecutes pruebas de explotación sobre infraestructura ajena para «verificar» una declaración.
- Aísla artefactos desconocidos de credenciales, red corporativa y datos personales.
- No subas binarios, SBOM privados, rutas internas ni configuraciones sensibles a validadores de terceros sin autorización.
- Minimiza nombres de empleados y contactos: la función responsable suele ser suficiente.
- Conserva originales, hashes y marcas temporales; realiza conversiones sobre copias.
- Coordina la divulgación si descubres que una declaración pública puede inducir a otros consumidores a ignorar un riesgo real.
- No atribuyas engaño por una discrepancia: puede proceder de un alcance diferente, una reconstrucción o información nueva.

## Checklist operativo

- [ ] El artefacto está fijado por digest, origen y fecha.
- [ ] El VEX identifica con precisión el producto evaluado.
- [ ] El documento conserva autor, versión, emisión y actualización.
- [ ] La estructura y la autenticidad se evalúan por separado del contenido.
- [ ] El identificador de vulnerabilidad se contrasta con una fuente primaria.
- [ ] La justificación de `not_affected` tiene evidencia específica.
- [ ] Las configuraciones y rutas opcionales están dentro o fuera de alcance de forma explícita.
- [ ] Los desacuerdos se conservan; no se resuelven por mayoría.
- [ ] La decisión incluye responsable, caducidad y eventos de reapertura.
- [ ] La automatización no silencia documentos ambiguos, antiguos o no confiables.

## Alternativas y siguientes pasos

VEX complementa, pero no reemplaza, un aviso de seguridad, un SBOM, una atestación de procedencia, un análisis de alcanzabilidad ni la telemetría del entorno. CSAF es apropiado cuando se necesita un aviso estructurado con árboles de producto y acciones; CycloneDX integra VEX con inventarios y otros datos de seguridad; OpenVEX busca una declaración mínima y separada del formato SBOM. La elección debe partir de los consumidores, la precisión de identificación y la semántica que hay que conservar, no de cuál fichero sea más pequeño.

El takeaway práctico es este: **acepta un estado VEX en proporción al vínculo con el artefacto, la calidad de su justificación y la posibilidad de reabrirlo, no porque el JSON sea válido o esté firmado**. Como siguiente tema, convendría estudiar cómo diseñar una política de confianza para declaraciones VEX de varios proveedores sin convertir la automatización en una lista permanente de excepciones.

## Fuentes oficiales consultadas

- [CISA: Minimum Requirements for Vulnerability Exploitability eXchange](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf)
- [CISA: VEX Status Justifications](https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf)
- [CycloneDX: Vulnerability Exploitability eXchange](https://www.cyclonedx.org/capabilities/vex/)
- [OASIS: perfil VEX de CSAF](https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html#45-profile-5-vex)
- [OpenVEX: especificación y principios](https://github.com/openvex/spec)
