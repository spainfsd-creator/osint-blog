---
title: "GitHub Actions en OSINT: probar la reproducibilidad sin exponer fuentes"
slug: /github-actions-osint-reproducibilidad
authors: [osint-writter]
tags: [osint, methodology, automation, verification, privacy, tooling]
date: 2026-09-16
image: /img/blog/2026-09-16-github-actions-osint-reproducibilidad.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista revisando una canalización automatizada con datos sintéticos, procedencia y permisos mínimos](/img/blog/2026-09-16-github-actions-osint-reproducibilidad.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/github-actions-osint-reproducibilidad.m4a)


*Imagen generada mediante inteligencia artificial.*

Un análisis sobre contratación pública funciona en el portátil de su autor y produce 317 adjudicaciones. Al ejecutarlo otra persona aparecen 314. Nadie ha falsificado nada: una dependencia cambió, tres fechas se interpretaron con otra configuración regional y un fichero auxiliar nunca entró en el repositorio. **La conclusión puede ser razonable y, aun así, el proceso que la sostiene no ser reproducible.**

[GitHub Actions](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows) permite ejecutar comprobaciones declaradas en el propio repositorio cuando ocurre un evento, como un `push`, una propuesta de cambio o una ejecución manual. En OSINT puede servir para detectar que un análisis ya no se reproduce desde cero. No convierte el resultado en verdad, no legitima la recogida de datos y no es un lugar seguro por defecto para subir fuentes sensibles.

<!-- truncate -->

## Qué es GitHub Actions y para qué sirve en OSINT

Un *workflow* es un fichero YAML almacenado en `.github/workflows/`. Define el evento que lo activa, uno o más trabajos, el tipo de *runner* y una secuencia de pasos. Cada trabajo se ejecuta en un entorno determinado; en los *runners* alojados por GitHub, salvo una excepción documentada para los de una sola CPU, cada trabajo empieza en una máquina virtual nueva.

Esa limpieza resulta útil para responder una pregunta concreta: **¿el repositorio contiene de verdad todo lo necesario para repetir el cálculo?** Si el proceso solo funciona porque el portátil conserva una variable, una caché, una credencial o un fichero olvidado, una ejecución limpia tiende a revelarlo.

En una investigación legítima, el CI puede comprobar:

- que el entorno se instala desde un fichero de dependencias bloqueadas;
- que los esquemas, tipos y recuentos de control siguen siendo los esperados;
- que los datos de prueba producen siempre las mismas transformaciones;
- que un manifiesto conserva URL, hora UTC, licencia, método y hash de cada adquisición;
- que el análisis falla de forma explícita cuando faltan campos o aparecen duplicados inesperados;
- que las salidas publicables no contienen columnas clasificadas como sensibles;
- que el informe se genera desde cero sin pasos manuales invisibles.

La palabra importante es **comprobar**. Un indicador verde solo demuestra que las condiciones programadas se cumplieron en esa ejecución. Si las pruebas son pobres, el flujo automatizará una falsa tranquilidad.

## Caso de uso ficticio: contratos sin datos personales en el *runner*

Imaginemos una investigación de debida diligencia sobre adjudicaciones de un organismo ficticio, el Consorcio del Río Norte. El equipo descarga cada semana un CSV público y quiere detectar cambios en importes, identificadores y fechas.

El conjunto real se conserva en un entorno de investigación con acceso restringido. El repositorio contiene únicamente:

1. el código de normalización y análisis;
2. un esquema que declara campos y tipos admitidos;
3. un conjunto sintético con sociedades, contratos e importes inventados;
4. pruebas para casos límite conocidos;
5. un manifiesto de ejemplo sin credenciales ni datos personales;
6. instrucciones para reproducir localmente el resultado.

Antes de publicar una conclusión, el equipo ejecuta localmente el flujo sobre la adquisición preservada. GitHub Actions repite el mismo código sobre los datos sintéticos y confirma que una fecha ambigua, un importe vacío o un identificador duplicado provocan el comportamiento previsto. El CI verifica el mecanismo; **no recibe ni valida el expediente real**.

Esta separación reduce exposición y evita que cada propuesta de cambio descargue otra vez una fuente viva. También conserva una distinción esencial: el hash prueba igualdad de bytes, las pruebas comprueban reglas conocidas y la corroboración independiente sostiene la afirmación factual.

## Flujo recomendado, paso a paso

### 1. Define qué significa «reproducible»

Escribe primero el contrato del análisis. Por ejemplo:

- misma revisión de código y mismas entradas producen la misma tabla normalizada;
- cada fila de salida conserva un identificador de procedencia;
- las exclusiones quedan contadas y justificadas;
- los resultados se generan desde un entorno vacío;
- ninguna prueba necesita red, una cuenta personal o una fuente viva.

No prometas reproducibilidad absoluta si intervienen servicios externos, relojes, aleatoriedad o paquetes no fijados. Registra esos límites y controla lo que sí depende de ti.

### 2. Separa originales, *fixtures* y resultados publicables

Los originales no deben terminar en Git por accidente. Mantén rutas distintas y reglas claras:

```text
data/raw/          # adquisición real; fuera del repositorio público
tests/fixtures/    # ejemplos sintéticos o anonimizados con criterio documentado
src/               # transformaciones
tests/             # expectativas y casos límite
reports/public/    # salidas revisadas para difusión
```

Un *fixture* útil representa la estructura y los errores que quieres probar, pero no copia nombres, correos, direcciones ni combinaciones que permitan reconstruir a una persona. «Anonimizado» no significa simplemente sustituir el nombre si el resto de atributos sigue identificando.

### 3. Haz que el proceso falle con información útil

Convierte supuestos importantes en pruebas:

- esquema y codificación esperados;
- zona horaria y formato de fecha;
- unicidad de claves;
- rangos imposibles;
- cardinalidad de las uniones;
- número y motivo de filas descartadas;
- ausencia de columnas prohibidas en el resultado publicable.

No fijes el recuento total real en una prueba pública si revela información sensible. Usa datos sintéticos y guarda los controles del caso real en el entorno adecuado.

### 4. Declara un workflow pequeño y sin privilegios

Este esquema es deliberadamente ilustrativo: los marcadores de SHA deben sustituirse por identificadores completos que tu equipo haya revisado.

```yaml
name: reproducibilidad

on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  prueba:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA-COMPLETO-REVISADO>
      - uses: actions/setup-python@<SHA-COMPLETO-REVISADO>
        with:
          python-version: "3.12"
          cache: "pip"
      - run: python -m pip install --require-hashes -r requirements.txt
      - run: python -m pytest
      - run: python scripts/build_report.py tests/fixtures/caso_sintetico.csv
      - run: git diff --exit-code -- reports/public/
```

La [sintaxis oficial de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) permite limitar `GITHUB_TOKEN` con `permissions`. Al declarar `contents: read`, el trabajo expresa que solo necesita leer el repositorio. Todo permiso no declarado queda en `none` cuando se especifica al menos uno.

GitHub recomienda fijar acciones de terceros a un SHA completo: es la única forma documentada de tratarlas como una referencia inmutable. La legibilidad puede conservarse con un comentario que indique la versión revisada, pero el valor ejecutado debe ser el SHA.

### 5. Trata cada entrada como no confiable

Una rama, el título de una propuesta, un nombre de fichero o un campo del CSV pueden contener caracteres inesperados. No insertes directamente valores del contexto de GitHub dentro de un script de shell. Pásalos como argumentos o variables de entorno y valídalos antes de usarlos.

Evita `pull_request_target` para ejecutar código procedente de una rama no confiable con permisos o secretos elevados. La documentación de GitHub advierte de sus riesgos específicos. Para las pruebas ordinarias de una propuesta externa, usa un evento y permisos que no entreguen credenciales de escritura.

### 6. Distingue cachés de artefactos

Una caché acelera instalaciones; no debe ser una fuente de verdad. El trabajo tiene que poder reconstruirse si la caché desaparece. GitHub advierte además que no se almacenen tokens ni credenciales en ella y que el contenido restaurado se trate como entrada no confiable.

Un artefacto conserva una salida de un trabajo para examinarla o compartirla con otro. Antes de subirlo, pregúntate:

- ¿contiene datos personales, rutas locales, URLs firmadas o registros de depuración?
- ¿quién puede descargarlo?
- ¿cuánto tiempo debe conservarse?
- ¿es un resultado publicable o solo un diagnóstico?

La retención es configurable y un artefacto borrado no es recuperable. Para un informe no sensible puede bastar un plazo corto; una fuente probatoria requiere una política de conservación distinta y un almacén apropiado, no una decisión improvisada en YAML.

### 7. Conserva el vínculo entre ejecución y conclusión

Registra, como mínimo:

- SHA del commit;
- identificadores o hashes de las entradas;
- fichero de dependencias bloqueadas;
- versión o digest del entorno;
- pruebas ejecutadas y sus resultados;
- artefactos producidos y sus hashes;
- fecha y hora UTC;
- limitaciones conocidas.

Una insignia verde en la portada del repositorio pierde contexto con el tiempo. Un manifiesto unido a la revisión permite reconstruir qué se comprobó realmente.

## Limitaciones y falsos positivos

### El CI no valida la verdad de la fuente

Una tabla inventada puede superar todas las pruebas si respeta el esquema. La autenticidad, cobertura y veracidad de la fuente exigen otras comprobaciones. El CI detecta desviaciones respecto a reglas; no sustituye el juicio investigador.

### Un entorno limpio no es idéntico a un entorno fijado

`ubuntu-latest` cambia con el tiempo. Los repositorios de paquetes cambian. Las imágenes pueden incorporar actualizaciones. Para resultados sensibles, fija dependencias, registra el entorno y considera contenedores identificados por digest. Incluso así, documenta componentes externos que no controlas.

### Los secretos no vuelven seguro un flujo inseguro

GitHub oculta muchos secretos en los registros, pero su documentación aclara que la redacción no es una frontera de seguridad garantizada. Un paso que ejecuta código malicioso puede intentar exfiltrar credenciales. Reduce secretos, usa permisos mínimos, evita credenciales de larga duración y no los expongas a cambios no confiables.

### Los datos sintéticos pueden ocultar el caso difícil

Si el conjunto de prueba es demasiado limpio, no representa errores de codificación, columnas ausentes, duplicados, fechas imposibles o uniones ambiguas. Incorpora casos límite inventados a medida que los descubras, sin copiar registros sensibles.

### Un fallo también puede ser operativo

Una caída del registro de paquetes o un límite temporal no invalida la metodología. Separa fallos de infraestructura, fallos de prueba y cambios sustantivos en los datos. Reintentar ciegamente puede ocultar el problema en vez de explicarlo.

## Buenas prácticas de OPSEC, ética y privacidad

- No subas al repositorio, a la caché, a los registros ni a los artefactos una fuente que no publicarías deliberadamente.
- Ejecuta sobre datos reales solo en un entorno autorizado y acorde con su sensibilidad.
- Usa `permissions` explícitos y concede a cada trabajo únicamente lo necesario.
- Fija acciones externas a SHA completo y revisa su código y procedencia.
- No ejecutes código de una propuesta no confiable con secretos o permisos de escritura.
- Sustituye credenciales permanentes por identidades de corta duración cuando el proveedor lo permita.
- Desactiva la red durante pruebas que no la necesiten o limita destinos de salida en entornos controlados.
- Revisa qué imprimen las excepciones: un error puede volcar filas, cabeceras o tokens.
- Define retención y borrado para registros y artefactos.
- Conserva una vía manual: automatizar una comprobación no elimina la responsabilidad de interpretar el resultado.

## Lista de control antes de confiar en el verde

- [ ] La pregunta y el significado de «reproducible» están escritos.
- [ ] Las tres últimas entradas del blog y el histórico del tema se revisaron para evitar duplicados.
- [ ] El CI usa únicamente datos sintéticos o expresamente publicables.
- [ ] Las dependencias y el entorno están fijados o sus variaciones se documentan.
- [ ] Las pruebas cubren esquema, fechas, uniones, duplicados, exclusiones y privacidad.
- [ ] `GITHUB_TOKEN` tiene permisos mínimos explícitos.
- [ ] Las acciones externas apuntan a SHA completo revisado.
- [ ] Ningún cambio no confiable recibe secretos ni permisos de escritura.
- [ ] Cachés y artefactos excluyen información sensible y tienen retención definida.
- [ ] El manifiesto une commit, entradas, pruebas, salida, hashes y UTC.
- [ ] La conclusión se corrobora fuera del CI con fuentes primarias independientes.

## Alternativas y siguientes pasos

GitHub Actions no es obligatorio. GitLab CI/CD, sistemas locales como `tox` o `nox`, y ejecutores autocustodiados pueden aplicar el mismo patrón. Un *runner* propio ofrece más control, pero también exige aislamiento, actualización y limpieza; no debe recibir automáticamente código no confiable.

[Jupyter y Jupytext](/jupyter-jupytext-osint-cuadernos-reproducibles) ayudan a convertir una exploración en explicación revisable. [DVC](/dvc-versionado-datos-osint) conecta revisiones con datos y canalizaciones. [Great Expectations](/great-expectations-osint-calidad-datos) formaliza controles de calidad. La integración continua une esas piezas en una prueba repetida, pero no reemplaza ninguna.

El takeaway accionable es pequeño: toma tu último análisis, crea un *fixture* sintético con tres errores deliberados y consigue que una ejecución limpia falle por la razón correcta. Después registra commit, entradas y salida. Si el proceso solo funciona con tu historial local, todavía no es una investigación reproducible.

Como siguiente tema, convendría estudiar cómo construir un paquete de evidencia publicable: manifiesto, hashes, consultas, licencia, límites y resultados, sin incluir fuentes que deban permanecer protegidas.

## Fuentes consultadas

- [GitHub Docs: Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- [GitHub Docs: sintaxis de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Docs: uso seguro de GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Docs: runners alojados por GitHub](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners)
- [GitHub Docs: secretos en GitHub Actions](https://docs.github.com/en/actions/concepts/security/secrets)
- [GitHub Docs: caché de dependencias](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching)
- [GitHub Docs: almacenar y compartir artefactos](https://docs.github.com/en/actions/tutorials/store-and-share-data)
