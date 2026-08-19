---
title: "Sigstore en OSINT: verificar firmas, identidad y transparencia sin confundirlas con seguridad"
slug: /sigstore-osint-firmas-identidad-transparencia
authors: [osint-writter]
tags: [osint, investigation, tooling, verification, methodology, privacy]
date: 2026-08-19
image: /img/blog/2026-08-19-sigstore-osint-firmas-identidad-transparencia.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT separando identidad, firma digital, registro de transparencia, digest del artefacto y política de verificación](/img/blog/2026-08-19-sigstore-osint-firmas-identidad-transparencia.png)

*Imagen generada mediante inteligencia artificial.*

Un proveedor asegura que el binario entregado a una administración es «el oficial» porque su firma aparece en un registro público. El certificado nombra un flujo de integración continua conocido y el digest coincide. Parece una conclusión cerrada, pero todavía faltan preguntas decisivas: **¿verificamos el artefacto exacto, esperábamos esa identidad y ese emisor, y la política de publicación autorizaba ese flujo?** Sigstore aporta evidencia criptográfica y transparencia; no certifica que el programa sea seguro, esté libre de componentes maliciosos o cumpla un contrato.

<!-- truncate -->

Consultada el **19 de agosto de 2026**, la [documentación oficial de Sigstore](https://docs.sigstore.dev/about/tooling/) presenta un conjunto de tecnologías para firmar y verificar artefactos de software, gestionar certificados de corta duración y registrar eventos de firma de forma auditable. En una investigación OSINT legítima, permite comprobar afirmaciones públicas sobre procedencia y publicación sin convertir una firma válida en un veredicto universal de confianza.

Todos los nombres, repositorios, contratos, identidades y digests del caso siguiente son ficticios. El método sirve para *due diligence*, respuesta a incidentes, investigación académica y verificación de la cadena de suministro; no para acceder a sistemas, explotar artefactos ni perfilar a desarrolladores.

## Qué es Sigstore y para qué sirve en OSINT

Sigstore reduce parte de la fricción clásica de la firma de software. En su modalidad basada en identidad, una persona o carga de trabajo se autentica mediante OpenID Connect (OIDC), **Fulcio** emite un certificado de firma de corta duración que vincula una clave efímera con esa identidad y **Rekor** registra material verificable sobre el evento. **Cosign** reúne estas piezas para firmar y verificar contenedores y otros artefactos.

Conviene separar desde el principio cinco capas:

| Capa | Pregunta que responde | Lo que no demuestra por sí sola |
|---|---|---|
| artefacto y digest | ¿qué bytes o manifiesto quedaron cubiertos? | que ese contenido sea seguro o funcional |
| firma | ¿la clave correspondiente produjo una firma válida? | quién debía estar autorizado a firmar |
| certificado | ¿qué identidad y emisor quedaron vinculados a la clave? | intención, cargo actual o aprobación contractual |
| transparencia | ¿hay evidencia de inclusión en el registro y de un momento anterior a su incorporación? | fecha de creación del código o ausencia de compromisos |
| política | ¿coinciden identidad, emisor, repositorio, flujo y referencia con lo esperado? | que una política incompleta cubra todos los riesgos |

La [visión oficial de la firma basada en identidad](https://docs.sigstore.dev/cosign/signing/overview/) explica que la clave efímera se genera para la operación, el certificado vincula esa clave con una identidad OIDC y el evento se anota en Rekor. La raíz de confianza necesaria para verificar Fulcio y Rekor se distribuye mediante The Update Framework (TUF). El resultado es auditable, pero solo es útil si el investigador conserva qué raíz, artefacto y expectativas empleó.

### Un bundle no es un simple justificante

Para un fichero, Cosign puede reunir la firma, el certificado y la prueba del registro en un **bundle**. La documentación actual recomienda aportar ese bundle a `cosign verify-blob`. Esto permite conservar el material de verificación junto al objeto, incluso para determinados flujos sin conexión, pero el bundle debe corresponder al fichero exacto y verificarse contra una raíz de confianza apropiada.

En contenedores, además, hay una diferencia importante entre una etiqueta mutable y un digest. `proveedor/app:estable` puede resolver mañana a otra imagen; `proveedor/app@sha256:…` identifica un manifiesto concreto. Una investigación reproducible registra ambos, pero formula conclusiones sobre el digest observado.

## Caso de uso legítimo: comprobar una entrega pública

La empresa ficticia **Faro Norte Sistemas SL** publica `validador-2.4.1.tar.gz` y afirma que es el mismo artefacto evaluado en el contrato imaginario `EXP-2026-041`. Junto al fichero ofrece `validador-2.4.1.sigstore.json`. La documentación del proyecto dice que las versiones solo son oficiales cuando las firma este flujo:

```text
https://github.com/faro-norte/validador/.github/workflows/release.yml@refs/tags/v*
```

y cuando el emisor es:

```text
https://token.actions.githubusercontent.com
```

La pregunta prudente no es «¿Sigstore confirma que el proveedor cumplió?», sino:

> ¿El bundle verifica el archivo descargado, qué identidad y emisor certifica, qué inclusión en transparencia acredita y coincide todo ello con la política publicada para esa versión?

Antes de ejecutar nada, construimos una tabla de afirmaciones:

| Afirmación | Evidencia esperada | Corroboración independiente |
|---|---|---|
| el fichero no cambió | digest calculado y firma válida sobre esos bytes | hash del expediente o repositorio oficial |
| lo firmó el flujo previsto | identidad exacta y emisor del certificado | política de publicación versionada |
| la firma era observable | prueba de inclusión y tiempo integrado en Rekor | bundle conservado y verificación criptográfica |
| corresponde a la versión 2.4.1 | etiqueta, commit, procedencia de compilación | repositorio, notas y, si existe, atestación |
| fue el artefacto entregado | identificador o hash en el expediente | acta, registro de entrega o sistema autorizado |
| es seguro | evaluación técnica y controles específicos | análisis reproducible, no la firma |

Esta última fila es esencial: la firma puede ser perfectamente válida sobre software vulnerable.

## Flujo recomendado, paso a paso

### 1. Congela la afirmación y el alcance

Guarda la página que formula la afirmación, URL exacta de descarga, fecha y hora UTC, nombre anunciado, tamaño y headers relevantes. Define qué identidad, emisor, repositorio, flujo y referencia deberían aceptarse **antes** de inspeccionar el resultado. Si adaptas la expectativa después de verlo, documenta el cambio.

Trabaja con un artefacto público, no sensible y necesario para la investigación. No ejecutes un binario desconocido: la verificación de procedencia puede hacerse sobre sus bytes sin concederle ejecución.

### 2. Conserva el artefacto y calcula su digest

Descarga el fichero y el bundle desde la fuente declarada. Mantén una copia original de solo lectura y calcula al menos SHA-256 con una herramienta local. Registra el comando, la ruta, el resultado y la hora. Si existe un digest publicado en el expediente, compáralo como una afirmación independiente.

No renombres una copia y asumas equivalencia: el nombre no forma parte de la garantía criptográfica. Tampoco uses el hash como prueba de autoría; solo identifica contenido cuando el algoritmo y los bytes coinciden.

### 3. Verifica con expectativas explícitas

Para el ejemplo ficticio, la forma general documentada por Cosign es:

```bash
cosign verify-blob validador-2.4.1.tar.gz \
  --bundle validador-2.4.1.sigstore.json \
  --certificate-identity \
  'https://github.com/faro-norte/validador/.github/workflows/release.yml@refs/tags/v2.4.1' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
```

La sintaxis se muestra como patrón didáctico con datos ficticios; antes de usarla hay que contrastarla con la [documentación vigente de `verify-blob`](https://docs.sigstore.dev/cosign/verifying/verify/). Evita comodines amplios y expresiones regulares permisivas. «Cualquier flujo del repositorio» no equivale a «el flujo de publicación autorizado».

Conserva la salida completa y el código de retorno. Un éxito significa que las comprobaciones ejecutadas pasaron bajo esas expectativas; no amplíes la conclusión a propiedades que el comando no evaluó.

### 4. Inspecciona certificado, identidad y emisor

Registra el sujeto del certificado, el emisor OIDC y las extensiones pertinentes para la identidad de carga de trabajo. En automatización, la identidad puede codificar repositorio, archivo de workflow y referencia. Esas cadenas son sensibles a cambios: una rama, una etiqueta y una solicitud de cambios no representan el mismo contexto de publicación.

Pregunta quién controla la cuenta o workflow, qué protección tenía la referencia y qué política estaba vigente. Fulcio acredita la relación con una identidad presentada por un emisor confiado durante la emisión; no prueba que el operador actuara correctamente ni que sus credenciales no estuvieran comprometidas.

### 5. Comprueba transparencia sin sobrefechar

[Rekor](https://docs.sigstore.dev/logging/overview/) utiliza una estructura verificable y de solo adición para registrar metadatos firmados. La prueba de inclusión permite comprobar que una entrada se incorporó al registro; la verificación del árbol ayuda a detectar alteraciones o inconsistencias.

La marca temporal integrada sostiene una afirmación acotada: el material existía antes de cierto momento de registro. No demuestra cuándo se escribió el código, cuándo empezó a usarse, cuándo se entregó contractualmente ni quién revisó su seguridad. Además, el [modelo de seguridad de Sigstore](https://docs.sigstore.dev/about/security/) subraya la importancia de monitorizar los registros: la transparencia facilita detectar certificados o firmas inesperados, pero alguien debe mirar.

### 6. Une la firma con la política y la procedencia

Verifica la política de publicación en una revisión histórica pertinente, no solo en el estado actual del repositorio. Relaciona el digest con la etiqueta o commit, el workflow, las notas de versión y, cuando existan, atestaciones de procedencia. Mantén separadas estas proposiciones:

- «el artefacto está firmado»;
- «la identidad satisface nuestra política»;
- «el artefacto procede de este proceso de compilación»;
- «el expediente recibió exactamente estos bytes»;
- «el contenido superó una evaluación de seguridad».

Una firma resuelve bien la primera y puede contribuir a las siguientes; no las fusiona.

### 7. Corrobora fuera de Sigstore

Busca el digest en el registro OCI, las notas oficiales, el archivo del expediente o un catálogo de paquetes. Revisa el commit y la configuración de compilación preservados en la fecha relevante. Si la investigación afecta a una decisión adversa, exige una segunda revisión y permite al proveedor explicar rotaciones de identidad, migraciones de workflow o firmas legítimas ausentes.

## Limitaciones y falsos positivos

- **Identidad comprometida:** una cuenta o proveedor OIDC comprometidos pueden originar certificados no autorizados; el registro mejora su detectabilidad, no impide todo abuso.
- **Workflow demasiado amplio:** una identidad válida puede corresponder a un flujo que no debería publicar versiones.
- **Etiqueta mutable:** verificar una referencia por nombre sin fijar digest puede mezclar artefactos distintos.
- **Bundle equivocado:** un bundle válido de otro fichero no acredita el objeto investigado.
- **Ausencia de entrada:** puede indicar un fallo de publicación, infraestructura distinta o material antiguo; no prueba manipulación por sí sola.
- **Firma posterior:** alguien autorizado puede firmar hoy un artefacto antiguo. La integración no retrotrae la fecha de creación.
- **Registro sin monitorización:** la transparencia aporta auditabilidad, pero la detección depende de verificadores y monitores.
- **Software firmado y dañino:** autenticidad e integridad no equivalen a seguridad, calidad, licencia correcta o cumplimiento.
- **Raíz de confianza incorrecta:** una verificación contra infraestructura privada requiere conocer la raíz y política correspondientes; no debe asumirse la pública por defecto.

## Buenas prácticas de OPSEC, ética y privacidad

- Define una finalidad legítima y proporcional; evita buscar firmas para elaborar perfiles personales.
- Usa artefactos públicos y no ejecutes contenido desconocido en el equipo de investigación.
- Conserva originales, digests, bundles, raíces de confianza, comandos y salidas en un expediente controlado.
- Minimiza la exposición de correos u otras identidades presentes en certificados y registros públicos.
- No publiques tokens OIDC, credenciales, secretos encontrados ni rutas internas irrelevantes.
- Respeta condiciones de uso y cuotas; una API pública no autoriza una recolección indiscriminada.
- Distingue observación, inferencia y conclusión; cita exactamente qué comprobó cada herramienta.
- Evita acusaciones basadas en una ausencia o cambio de workflow sin pedir contexto.
- Solicita revisión humana antes de atribuir incumplimiento, autoría o conducta maliciosa.
- Establece retención y acceso adecuados para bundles y notas que puedan contener identidades.

## Checklist de validación

- [ ] La afirmación, el periodo y la finalidad están definidos.
- [ ] El artefacto se conserva sin ejecutarlo y tiene digest local.
- [ ] La referencia mutable se ha resuelto a contenido concreto.
- [ ] El bundle corresponde exactamente al artefacto objetivo.
- [ ] Identidad y emisor esperados se fijaron antes de verificar.
- [ ] La verificación conserva comando, salida, versión de herramienta y raíz.
- [ ] La inclusión en Rekor se interpreta con un alcance temporal prudente.
- [ ] La política de publicación histórica autoriza ese flujo y referencia.
- [ ] Procedencia, entrega contractual y seguridad se corroboran aparte.
- [ ] Se han registrado explicaciones alternativas y resultados negativos.
- [ ] Los datos personales se han minimizado.
- [ ] Una persona revisará cualquier conclusión sensible.

## Alternativas y siguientes pasos

Sigstore encaja mejor como una pieza de un sistema de procedencia:

- **in-toto** y atestaciones para describir pasos y materiales de la cadena de suministro;
- **SLSA** como marco para razonar sobre procedencia y niveles de garantía;
- **TUF** para distribuir metadatos confiables y resistir ciertos ataques de actualización;
- **SPDX** o **CycloneDX** para inventariar componentes mediante SBOM, sin asumir exhaustividad;
- firmas con claves gestionadas, KMS o hardware cuando la política requiera otro modelo;
- **Software Heritage** y la forja original para preservar código y contexto histórico;
- análisis de dependencias, revisión reproducible y pruebas de seguridad para evaluar el contenido.

El takeaway accionable es este: elige un artefacto público firmado, fija **digest, identidad, emisor y política esperados**, verifica su bundle y crea cinco columnas: **integridad, identidad, transparencia, procedencia y seguridad**. Rellena solo lo que la evidencia permita. Una firma válida es una respuesta precisa a una pregunta precisa, no un sello mágico.

Como siguiente tema, sería útil estudiar **SLSA e in-toto** para distinguir una firma del artefacto de una atestación sobre cómo, dónde y con qué materiales se produjo.

## Fuentes consultadas

- [Herramientas y componentes de Sigstore](https://docs.sigstore.dev/about/tooling/)
- [Firma basada en identidad con Cosign](https://docs.sigstore.dev/cosign/signing/overview/)
- [Verificación de firmas con Cosign](https://docs.sigstore.dev/cosign/verifying/verify/)
- [Referencia oficial de `cosign verify-blob`](https://github.com/sigstore/cosign/blob/main/doc/cosign_verify-blob.md)
- [Rekor: registro de transparencia](https://docs.sigstore.dev/logging/overview/)
- [Modelo de seguridad y límites de Sigstore](https://docs.sigstore.dev/about/security/)
