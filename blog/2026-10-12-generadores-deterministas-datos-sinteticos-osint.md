---
title: "Generadores deterministas de datos sintéticos en OSINT: variedad reproducible sin copiar el caso real"
slug: /generadores-deterministas-datos-sinteticos-osint
authors: [osint-writter]
tags: [osint, methodology, testing, automation, data, privacy]
date: 2026-10-12
image: /img/blog/2026-10-12-generadores-deterministas-datos-sinteticos-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando un generador determinista de datos sintéticos para un pipeline OSINT](/img/blog/2026-10-12-generadores-deterministas-datos-sinteticos-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/generadores-deterministas-datos-sinteticos-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Un parser falla solo cuando recibe dos eventos con la misma hora, un dominio vacío y una IP repetida. El equipo necesita conservar ese borde para que la corrección no regrese, pero el incidente original contiene nombres, infraestructura activa y una cronología reconocible. **Copiar el expediente a `fixtures/` preservaría el fallo a costa de preservar también el riesgo.**

Un generador determinista permite describir la forma del problema, producir entradas ficticias y reconstruir exactamente la misma muestra cuando una prueba falla. La semilla ayuda a repetir; el esquema y las invariantes ayudan a que lo repetido sea útil. Ninguna de las tres cosas convierte por sí sola un conjunto en anónimo, representativo o verdadero.

<!-- truncate -->

Todos los nombres, dominios, direcciones IP, fechas e identificadores del ejemplo son ficticios o proceden de rangos reservados para documentación. Este método sirve para probar software y flujos propios con una finalidad legítima; no justifica modelar a una persona real, reconstruir información retirada ni generar identidades plausibles para engañar.

## Qué es un generador determinista (y para qué sirve)

Un generador de datos sintéticos crea registros artificiales a partir de reglas. Es **determinista** cuando, bajo las mismas condiciones relevantes, produce la misma salida. Esas condiciones no son solo una semilla: también incluyen el código, la plantilla, el orden de llamadas, la configuración regional y las versiones de las dependencias.

La documentación de [Faker](https://faker.readthedocs.io/en/stable/index.html#seeding-the-generator) indica que una semilla reproduce resultados cuando se invocan los mismos métodos con la misma versión, pero advierte de que sus conjuntos de datos pueden cambiar entre versiones de parche. Por eso una receta reproducible debe registrar al menos:

- identificador y versión del generador;
- semilla o identificador de escenario;
- versión del esquema y de las plantillas;
- locale y zona horaria;
- versiones fijadas de las dependencias;
- hash del fichero generado, si se conserva como artefacto.

El objetivo no es imitar a la perfección el mundo real. En pruebas OSINT suele ser más valioso generar **casos que ejerciten una propiedad**: duplicados, campos ausentes, codificaciones, límites de fecha, relaciones uno-a-muchos o cambios de esquema.

Conviene separar tres conceptos:

1. **Datos sintéticos:** registros construidos, no simples copias con nombres sustituidos.
2. **Reproducibilidad:** capacidad de reconstruir una muestra bajo condiciones declaradas.
3. **Cobertura:** comportamientos del pipeline que esa muestra pone a prueba.

Una salida puede ser reproducible y, aun así, cubrir muy poco. También puede ser totalmente inventada y mantener una combinación tan parecida al caso real que revele información.

## Caso legítimo: eventos web que llegan desordenados

El observatorio ficticio **Faro Norte** procesa avisos públicos de disponibilidad web. Tras una corrección descubre que su agregador cuenta dos veces un evento cuando coinciden tres condiciones:

- dos filas comparten `observed_at`;
- una trae el dominio vacío;
- ambas conservan el mismo `event_id` tras normalizar.

No necesita guardar los avisos originales. Diseña el escenario `duplicate-null-domain-v1` con cuatro filas artificiales y estas invariantes:

- los dos eventos duplicados deben colapsar en uno;
- el dominio vacío debe ir a cuarentena, no completarse por intuición;
- el total publicado debe contar solo registros válidos y únicos;
- ejecutar dos veces la transformación debe producir el mismo resultado.

Para evitar que una prueba escape y consulte activos reales, usa `example.com`, reservado para ejemplos por el [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606), y direcciones de `192.0.2.0/24`, `198.51.100.0/24` y `203.0.113.0/24`, reservadas para documentación por el [RFC 5737](https://www.rfc-editor.org/rfc/rfc5737).

## Flujo recomendado

### 1. Escribe primero la propiedad

Antes de elegir una librería, formula qué debe seguir siendo cierto. Una ficha pequeña evita que «generar datos variados» se convierta en un fin sin criterio:

```yaml
scenario_id: duplicate-null-domain-v1
schema_version: 3
generator_version: 2
seed: 74021
purpose: verificar deduplicación y cuarentena
invariants:
  - no_duplicate_event_id
  - blank_domain_is_quarantined
  - second_run_is_idempotent
forbidden_inputs:
  - production_exports
  - real_domains
  - personal_identifiers
```

La propiedad debe ser observable. «Parece realista» no sirve como oráculo; «ningún `event_id` aparece dos veces en la salida válida» sí.

### 2. Construye desde restricciones, no desde filas reales

Define tipos, cardinalidades y relaciones mínimas. Si el fallo depende de una fecha ambigua, genera fechas artificiales en varios formatos. Si depende de un grafo, crea nodos ficticios y aristas que representen el patrón. No empieces copiando una tabla de producción para después borrar columnas.

El [NIST SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) distingue la generación sintética de otras técnicas de desidentificación y advierte de los límites de fidelidad y del riesgo de que el público confunda datos sintéticos con datos operativos. Etiqueta el conjunto dentro del propio artefacto, no solo en un README que puede separarse de él.

Un campo explícito ayuda:

```json
{
  "dataset_class": "SYNTHETIC_TEST_DATA",
  "scenario_id": "duplicate-null-domain-v1",
  "event_id": "evt-synth-0001",
  "domain": "alpha.example",
  "ip": "192.0.2.17"
}
```

### 3. Aísla el estado aleatorio

Evita un generador global compartido por toda la suite. Un test que consume un valor adicional puede desplazar la secuencia de los demás. Crea una instancia por escenario y registra su semilla.

Este ejemplo pequeño genera siempre el mismo lote mientras permanezcan fijados código, orden y versión de Faker:

```python
from faker import Faker
from random import Random

SEED = 74021
fake = Faker("es_ES")
fake.seed_instance(SEED)
rng = Random(SEED)

reserved_ips = [
    "192.0.2.17",
    "198.51.100.24",
    "203.0.113.31",
]

rows = [
    {
        "dataset_class": "SYNTHETIC_TEST_DATA",
        "event_id": f"evt-synth-{index:04d}",
        "analyst_alias": fake.first_name(),
        "domain": f"node-{index}.example",
        "ip": rng.choice(reserved_ips),
    }
    for index in range(1, 5)
]
```

El alias solo aporta variedad visual; no debe usarse como prueba de unicidad. La propiedad `.unique` de Faker conserva estado y puede agotar espacios pequeños, por lo que identificadores y claves conviene construirlos con reglas explícitas.

### 4. Inyecta bordes de forma deliberada

La aleatoriedad uniforme rara vez encuentra por casualidad los casos que más importan. Añade mutadores con nombre:

- `duplicate_event_id` duplica una clave tras normalizar;
- `blank_domain` deja un campo obligatorio vacío;
- `out_of_order_timestamp` altera el orden sin cambiar los instantes;
- `unknown_enum_value` introduce un valor futuro del contrato;
- `invalid_utf8_boundary` prueba el tratamiento de bytes defectuosos en una capa aislada.

Cada mutador debe declarar qué invariante pretende desafiar. Así un fallo dice más que «la semilla 74021 salió mal»: explica qué borde se estaba probando.

### 5. Comprueba determinismo e invariantes por separado

Genera dos veces con la misma receta, serializa con orden canónico y compara hashes. Después ejecuta las reglas de dominio. Son preguntas diferentes:

- ¿la receta reconstruye los mismos bytes?
- ¿los registros cumplen el esquema?
- ¿el pipeline responde correctamente a los bordes intencionados?
- ¿una segunda ejecución es idempotente?

No fijes un snapshot enorme si bastan propiedades pequeñas. Un snapshot puede detectar cualquier cambio, pero no explica cuál importa.

### 6. Conserva la receta; limita la salida

Si el conjunto puede regenerarse, quizá no necesites versionar miles de filas. Conserva código, manifiesto, dependencias y casos de regresión mínimos. Publica el fichero generado solo cuando facilite revisión, interoperabilidad o pruebas de otro sistema.

Si lo conservas, registra el hash y una cabecera visible que lo marque como sintético. Aplica también caducidad: una semilla estable no convierte un fixture obsoleto en útil.

## Semillas, fallos y exploración

Una semilla fija es buena para repetir una suite rápida, pero mala si se convierte en el único universo que el software ve. Combina dos carriles:

- **CI determinista:** escenarios conocidos, versiones fijadas y resultados repetibles;
- **exploración periódica:** nuevas combinaciones, más volumen y registro del contraejemplo que falle.

[Hypothesis](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html) guarda ejemplos fallidos para reproducirlos y recomienda convertir un fallo permanente en un ejemplo explícito cuando corresponda. Su opción `derandomize` permite ejecuciones deterministas, aunque los resultados pueden variar si cambian Hypothesis, Python o la función probada. La reproducción también falla si el test depende de red, reloj, orden de hilos o estado externo.

La semilla es un dato de depuración, no una garantía criptográfica. La documentación de [`random` de Python](https://docs.python.org/3/library/random.html) señala que su generador es determinista y no debe usarse para fines de seguridad. No generes contraseñas, tokens o secretos operativos con el mismo mecanismo de los fixtures.

## Limitaciones y falsos positivos

### Determinista no significa idéntico para siempre

Actualizar una dependencia, un locale o una plantilla puede cambiar la salida aunque la semilla sea la misma. Fija versiones cuando compares bytes; si actualizas, revisa el diff y aumenta la versión del generador.

### Sintético no significa privado automáticamente

Un modelo entrenado o calibrado sobre datos sensibles puede memorizar casos o conservar combinaciones singulares. Un dataset inventado a mano también puede replicar sin querer una cronología real. Evalúa procedencia, similitud y riesgo de divulgación; no presentes «sintético» como certificado de anonimato.

### Realismo no significa representatividad

Faker produce valores plausibles, no una muestra estadística de la población ni del universo investigado. Un apellido, ciudad o empresa de aspecto realista no valida tasas, correlaciones o sesgos.

### Los datos demasiado limpios esconden defectos

Si todas las filas tienen campos completos, orden estable y UTF-8 perfecto, el generador enseñará al pipeline un mundo que no existe. Diseña nulos, duplicados y formatos inesperados dentro de límites seguros.

### Una colisión puede ser intencionada o accidental

No uses nombres generados como claves. Mantén identificadores sintéticos inequívocos y valida cardinalidades. Si una colisión forma parte del escenario, márcala en el manifiesto para que no se diagnostique como defecto del generador.

## Buenas prácticas de OPSEC, ética y privacidad

- Genera desde un esquema nuevo; no desde un volcado de producción maquillado.
- Usa dominios, IP y otros recursos reservados para documentación.
- Marca cada registro o paquete como sintético.
- No construyas identidades completas ni combinaciones que puedan confundirse con personas reales.
- Separa semillas de prueba de secretos, tokens y credenciales.
- Impide acceso a red en tests que no la necesitan.
- Fija locale, zona horaria, dependencias y orden de serialización.
- Registra propósito, cobertura, propietario y fecha de revisión del escenario.
- Escanea salidas y logs para detectar datos personales o secretos antes del commit.
- Conserva contraejemplos mínimos; elimina artefactos generados que ya no aporten valor.
- Declara que una prueba verde demuestra comportamiento técnico bajo el escenario, no verdad factual.

## Alternativas y siguientes pasos

Para dos o tres bordes conocidos, una tabla escrita a mano puede ser más legible que un generador. Para dominios combinatorios, usa estrategias de *property-based testing*. Para distribuciones con utilidad analítica, hacen falta métricas de fidelidad y privacidad mucho más exigentes que las de un fixture de software. Si solo necesitas ocultar datos reales, detente: enmascarar, seudonimizar y sintetizar resuelven problemas distintos.

Un patrón práctico es una pirámide:

1. ejemplos explícitos para incidentes confirmados;
2. generadores deterministas para familias de bordes;
3. exploración variable para descubrir casos nuevos;
4. validación separada sobre datos autorizados cuando el resultado vaya a publicarse.

## Checklist de cierre

- [ ] La propiedad y el propósito están escritos antes del generador.
- [ ] Ninguna entrada procede de un exporte real sin evaluación específica.
- [ ] El conjunto se identifica como sintético dentro del artefacto.
- [ ] Se usan dominios e IP reservados.
- [ ] Semilla, locale, zona horaria, esquema y dependencias están registrados.
- [ ] Dos ejecuciones equivalentes producen la misma salida canónica.
- [ ] Los bordes importantes se inyectan de forma deliberada.
- [ ] Identificadores y unicidad no dependen de nombres plausibles.
- [ ] Los tests no acceden a red ni reutilizan secretos.
- [ ] El fallo conserva un contraejemplo mínimo reproducible.
- [ ] Existe una política de revisión y retirada.
- [ ] La salida verde no se presenta como garantía de exactitud del mundo real.

El takeaway accionable es sencillo: toma un fixture sensible, escribe la propiedad exacta que protege y reconstruye desde cero el escenario mínimo con `example.com`, rangos TEST-NET e identificadores marcados como sintéticos. Ejecuta la receta dos veces y compara hashes; después demuestra que la versión defectuosa falla y la corregida pasa. Si necesitas mirar el expediente para entender la muestra, todavía no has separado bien el mecanismo del caso.

Como siguiente tema, sería útil estudiar la **revisión de similitud y riesgo de divulgación en datos sintéticos OSINT**: cómo detectar cuándo una muestra artificial se parece demasiado a un registro real sin convertir el control de privacidad en una falsa garantía.

## Fuentes consultadas

- [Faker: Basic Usage, valores únicos y semillas](https://faker.readthedocs.io/en/stable/index.html)
- [Faker: integración y semillas en pytest](https://faker.readthedocs.io/en/stable/pytest-fixtures.html)
- [Hypothesis: reproducir fallos](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
- [Hypothesis: configuración y modo determinista](https://hypothesis.readthedocs.io/en/latest/settings.html)
- [NIST SP 800-188: De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final)
- [RFC 2606: nombres DNS reservados](https://www.rfc-editor.org/rfc/rfc2606)
- [RFC 5737: bloques IPv4 reservados para documentación](https://www.rfc-editor.org/rfc/rfc5737)
- [Python: generadores pseudoaleatorios y advertencia de seguridad](https://docs.python.org/3/library/random.html)
