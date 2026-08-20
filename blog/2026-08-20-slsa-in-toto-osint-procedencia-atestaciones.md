---
title: "SLSA e in-toto en OSINT: verificar procedencia y atestaciones sin convertirlas en pruebas absolutas"
slug: /slsa-in-toto-osint-procedencia-atestaciones
authors: [osint-writter]
tags: [osint, investigation, tooling, verification, automation, methodology]
date: 2026-08-20
image: /img/blog/2026-08-20-slsa-in-toto-osint-procedencia-atestaciones.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista OSINT siguiendo un artefacto desde su digest hasta el repositorio, el sistema de compilación, las dependencias y la política de verificación](/img/blog/2026-08-20-slsa-in-toto-osint-procedencia-atestaciones.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/slsa-in-toto-osint-procedencia-atestaciones.m4a)


*Imagen generada mediante inteligencia artificial.*

Un proveedor entrega un binario firmado y una atestación que apunta al repositorio correcto. El digest coincide, el flujo de integración continua parece oficial y el documento enumera materiales, parámetros y un constructor conocido. Es información valiosa, pero todavía no responde a la pregunta decisiva: **¿la atestación está autenticada, describe este artefacto exacto y satisface una política que fijamos antes de mirar el resultado?** SLSA e in-toto permiten formular y comprobar esas preguntas; no convierten automáticamente una compilación trazable en software seguro, código lícito o cumplimiento contractual.

<!-- truncate -->

Consultada el **20 de agosto de 2026**, la especificación aprobada [SLSA v1.2](https://slsa.dev/spec/v1.2/) organiza garantías incrementales para la cadena de suministro en distintos niveles y *tracks*. Por su parte, el [in-toto Attestation Framework](https://github.com/in-toto/attestation) define una estructura común para afirmaciones autenticadas sobre artefactos. En OSINT responsable, ambos sirven para evaluar declaraciones públicas de procedencia sin acceder a sistemas ni asumir que todo metadato firmado sea verdadero, completo o suficiente.

Todos los nombres, repositorios, contratos, identidades, digests y valores del caso práctico son ficticios. El método está pensado para *due diligence*, respuesta a incidentes, contratación pública e investigación académica con autorización y proporcionalidad.

## Qué son SLSA e in-toto y para qué sirven

SLSA —pronunciado habitualmente *salsa*— es una especificación para describir y mejorar gradualmente la seguridad de una cadena de suministro. Su foco principal es la **integridad**: que una revisión de código refleje el proceso esperado, que un artefacto proceda de las fuentes y la receta declaradas y que no haya sido sustituido durante su distribución. La propia documentación advierte de que [no cubre por igual todas las amenazas](https://slsa.dev/spec/v1.2/threats-overview).

in-toto aporta el idioma estructurado para expresar afirmaciones verificables. Una atestación no es «la evidencia» en abstracto, sino metadatos autenticados sobre uno o varios sujetos. Su arquitectura actual separa cuatro capas:

| Capa | Función | Pregunta OSINT |
|---|---|---|
| `predicate` | contiene una afirmación con un esquema concreto | ¿qué se afirma y con qué semántica? |
| `Statement` | une esa afirmación a uno o varios sujetos | ¿sobre qué artefacto y digest se afirma? |
| `Envelope` | aporta serialización y autenticación | ¿quién firmó y con qué raíz o identidad verificable? |
| `Bundle` | agrupa atestaciones y dependencias de verificación | ¿qué conjunto exacto se evaluó y cómo se relaciona? |

El [Statement de in-toto](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) identifica el sujeto y el tipo de predicado. El contenido de `predicate` solo puede interpretarse correctamente con su `predicateType`: dos JSON parecidos pueden hacer afirmaciones distintas. El [Envelope](https://github.com/in-toto/attestation/blob/main/spec/v1/envelope.md) autentica la carga; verificar su firma no valida por sí solo la exactitud material de todo lo que el productor escribió dentro.

### La procedencia de compilación de SLSA

El predicado recomendado para procedencia de compilación usa:

```text
https://slsa.dev/provenance/v1
```

La [especificación de Build Provenance](https://slsa.dev/spec/v1.2/build-provenance) divide sus datos en dos bloques principales:

- `buildDefinition`: qué plantilla de compilación y qué entradas se usaron;
- `runDetails`: qué plataforma ejecutó esa invocación y qué datos dejó la ejecución.

Dentro de ellos aparecen campos especialmente útiles para una investigación:

- `subject`: el artefacto resultante, ligado normalmente a un digest;
- `buildType`: el tipo de proceso y la semántica de sus parámetros;
- `externalParameters`: entradas controlables desde fuera que el verificador debe contrastar;
- `resolvedDependencies`: materiales resueltos, con URI y digest cuando están disponibles;
- `builder.id`: identidad de la plataforma que afirma haber ejecutado y registrado el proceso;
- `invocationId`, `startedOn` y `finishedOn`: contexto operativo, no una cronología total del desarrollo.

No conviene traducir `builder.id` como «autor». Representa una base de confianza de la plataforma de compilación. Tampoco una lista de `resolvedDependencies` debe tratarse como un SBOM completo: la especificación declara su exhaustividad como mejor esfuerzo, incluso en niveles altos del *track* de compilación.

## Caso de uso legítimo: comprobar la procedencia de una entrega

La administración ficticia **Consorcio Vega Clara** publica el expediente `VC-2026-117`. El proveedor imaginario **Taller Nadir SL** entrega:

```text
clasificador-4.2.0.tar.gz
clasificador-4.2.0.intoto.jsonl
sha256: 5b8f...91c2
```

Afirma que el fichero se construyó desde la etiqueta pública `v4.2.0`, en la plataforma aprobada y sin parámetros extraordinarios. La investigación no intenta «demostrar que miente». Formula hipótesis separadas:

1. el artefacto descargado coincide con el sujeto de la atestación;
2. la atestación está autenticada por una identidad aceptada;
3. el `builder.id` corresponde al constructor admitido para ese producto;
4. la revisión y la receta observadas coinciden con las expectativas del expediente;
5. los parámetros externos no introducen una ruta alternativa;
6. el contrato realmente exige esas propiedades y no otras.

Una versión muy reducida del Statement podría parecerse a esta:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{
    "name": "clasificador-4.2.0.tar.gz",
    "digest": {"sha256": "5b8f...91c2"}
  }],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "https://build.example/spec/v1",
      "externalParameters": {
        "repository": "https://forge.example/taller-nadir/clasificador",
        "ref": "refs/tags/v4.2.0"
      },
      "resolvedDependencies": [{
        "uri": "git+https://forge.example/taller-nadir/clasificador@refs/tags/v4.2.0",
        "digest": {"gitCommit": "71aa...d903"}
      }]
    },
    "runDetails": {
      "builder": {"id": "https://build.example/tenant-isolated/v1"}
    }
  }
}
```

Es un ejemplo pedagógico, no una atestación válida ni una plantilla lista para producción.

## Flujo recomendado de verificación

### 1. Fijar la pregunta y las expectativas antes del JSON

Escribe primero qué resultado aceptarías: nombre del producto, digest o mecanismo para obtenerlo, repositorio canónico, revisión permitida, identidad firmante, `builder.id`, `buildType` y parámetros externos admisibles. La [guía de verificación de artefactos](https://slsa.dev/spec/v1.2/verifying-artifacts) insiste en comparar la procedencia con expectativas conocidas; una firma sin expectativas solo confirma que alguien firmó algo.

Conserva también la procedencia de esa política: contrato, documentación de publicación, configuración versionada o comunicación autenticada. Si la regla apareció después del incidente, anótalo.

### 2. Preservar el conjunto exacto

Descarga el artefacto, la atestación y la información pública necesaria sin ejecutarlos. Registra URL, fecha, cabeceras relevantes y hashes locales. Trabaja con copias. Una etiqueta o un nombre de fichero son mutables; el digest es la unión reproducible entre el archivo observado y el `subject`.

Si la atestación llega dentro de un *bundle*, inventaría sus entradas. No mezcles material descargado en momentos distintos sin dejar constancia. El [modelo de bundles de in-toto](https://github.com/in-toto/attestation/blob/main/spec/v1/bundle.md) permite agrupar atestaciones, pero agrupar no elimina la obligación de verificar cada relación pertinente.

### 3. Autenticar el Envelope

Verifica el formato, la firma y la raíz de confianza con una herramienta adecuada al mecanismo usado. Conserva:

- fichero y digest de la atestación;
- identidad o clave reconocida;
- raíz, certificado o registro empleado;
- versión de la política y del verificador;
- salida completa y código de retorno;
- hora y entorno de la comprobación.

Una firma válida responde a **integridad y autenticación del mensaje** bajo una raíz concreta. No demuestra que el firmante tuviera autoridad contractual ni que su sistema estuviera libre de compromisos.

### 4. Unir Statement y artefacto

Calcula el digest del fichero objetivo y compáralo con `subject`. Confirma `_type` y `predicateType`; después interpreta el predicado según esa versión. Si el sujeto no coincide, detén la inferencia. No «arregles» el nombre del archivo ni pruebes al azar otros binarios hasta obtener un verde: documenta el resultado negativo.

### 5. Contrastar procedencia y expectativas

Revisa como mínimo:

- pareja entre firmante y `builder.id`;
- repositorio canónico y revisión inmutable;
- significado documentado de `buildType`;
- todos los `externalParameters`, incluidos campos inesperados;
- digests de `resolvedDependencies` relevantes;
- límites de aislamiento y confianza declarados por la plataforma;
- relación entre fechas de compilación, publicación, firma y entrega.

SLSA Build L3 protege frente a determinadas manipulaciones externas del proceso y de la generación de procedencia, suponiendo que se confía en la plataforma. La especificación aclara que eso no cubre por sí solo el compromiso de la plataforma, por ejemplo por una persona interna maliciosa.

### 6. Corroborar fuera de la atestación

Vuelve al repositorio, la forja, el registro de paquetes, el expediente y las fuentes preservadas. Pregunta por separado:

- ¿la revisión contenía realmente el código declarado?;
- ¿la receta pública coincide con el `buildType` y los parámetros?;
- ¿la plataforma documentaba ese nivel y modo operativo en la fecha relevante?;
- ¿el artefacto fue el entregado o desplegado, no solo uno reconstruido después?;
- ¿hay análisis de vulnerabilidades, licencias o comportamiento que cubran preguntas distintas?

Solo entonces redacta una conclusión limitada: «la procedencia autenticada vincula este digest con esta invocación y satisface estas expectativas», no «el programa está verificado».

## Limitaciones y falsos positivos

- **Atestación correcta, política equivocada:** aceptar cualquier `builder.id` conocido puede validar una plataforma no autorizada para ese producto.
- **Sujeto correcto, contenido dañino:** la trazabilidad no inspecciona la intención ni elimina vulnerabilidades.
- **Etiqueta mutable:** `v4.2.0` puede cambiar; conserva el commit u otro identificador inmutable.
- **Materiales incompletos:** `resolvedDependencies` no garantiza por sí solo un inventario exhaustivo.
- **Firma fuera de contexto:** una identidad válida puede actuar fuera del flujo aprobado o con permisos comprometidos.
- **Nivel autodeclarado:** el texto del productor no sustituye la evaluación de la plataforma y la raíz de confianza del verificador.
- **Cronología sobreinterpretada:** `startedOn` y `finishedOn` describen una ejecución, no cuándo se escribió, revisó o desplegó el código.
- **Bundle mezclado:** varias atestaciones legítimas pueden referirse a sujetos o ejecuciones diferentes.
- **Verde sin explicación:** una herramienta puede aceptar valores por defecto que no coinciden con la política del caso.

## Buenas prácticas de OPSEC, ética y privacidad

- Limita la recopilación a artefactos y metadatos públicos necesarios para una finalidad legítima.
- No ejecutes binarios desconocidos durante una comprobación documental; usa análisis autorizado y aislado si resulta imprescindible.
- No publiques tokens, rutas internas, correos ni identidades personales que aparezcan incidentalmente en logs o atestaciones.
- Separa el expediente de evidencia de las copias de trabajo y registra cada transformación.
- Usa digests completos en el expediente; abrevia solo en ejemplos narrativos.
- Trata las identidades de CI como identidades técnicas, no como atribución personal automática.
- Respeta términos de uso, licencias, secretos comerciales y restricciones del contrato.
- Distingue «no pude verificar» de «es falso».
- Exige revisión humana antes de una decisión adversa y ofrece un canal de corrección.

## Checklist de campo

- [ ] Pregunta, alcance y política estaban definidos antes de verificar.
- [ ] Artefacto, atestación y bundle tienen hash y origen registrados.
- [ ] La firma se validó con una raíz aceptada y conservada.
- [ ] `subject` coincide con el digest del artefacto exacto.
- [ ] `_type` y `predicateType` se interpretaron con su especificación.
- [ ] Firmante y `builder.id` forman una pareja autorizada.
- [ ] Repositorio, revisión, `buildType` y parámetros cumplen expectativas.
- [ ] Dependencias y campos ausentes se tratan con su límite de exhaustividad.
- [ ] Entrega, despliegue, seguridad y licencia se corroboraron aparte.
- [ ] La conclusión enumera expresamente lo que la evidencia no demuestra.

## Alternativas y siguientes pasos

SLSA e in-toto encajan dentro de un expediente más amplio:

- **Sigstore** para identidades, firmas y transparencia de determinados artefactos y atestaciones;
- **TUF** para distribuir metadatos de actualización con separación de roles y resistencia a ciertos compromisos;
- **SPDX** o **CycloneDX** para inventarios SBOM, atendiendo a alcance y exhaustividad;
- **Software Heritage** y la forja para preservar código, revisiones y contexto;
- compilaciones reproducibles para comparar resultados obtenidos de forma independiente;
- escáneres, revisión de código y pruebas autorizadas para preguntas de seguridad;
- contratos, registros de despliegue y controles organizativos para demostrar cumplimiento.

El takeaway accionable es este: elige un artefacto público con procedencia, no lo ejecutes y construye una tabla con siete columnas: **digest, firmante, builder, fuente, receta, parámetros y política**. Añade una octava: **no demostrado**. Si no puedes justificar una celda con evidencia conservada, déjala abierta.

Como siguiente tema, sería útil estudiar **TUF** para entender cómo una política de actualización distribuye confianza entre roles, versiones y caducidades sin convertir un repositorio firmado en infalible.

## Fuentes consultadas

- [SLSA v1.2: especificación aprobada](https://slsa.dev/spec/v1.2/)
- [SLSA: procedencia de compilación](https://slsa.dev/spec/v1.2/build-provenance)
- [SLSA: verificación de artefactos y expectativas](https://slsa.dev/spec/v1.2/verifying-artifacts)
- [SLSA: amenazas de la cadena de suministro](https://slsa.dev/spec/v1.2/threats-overview)
- [in-toto Attestation Framework](https://github.com/in-toto/attestation)
- [in-toto: especificación de Statement](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md)
- [in-toto: especificación de Envelope](https://github.com/in-toto/attestation/blob/main/spec/v1/envelope.md)
