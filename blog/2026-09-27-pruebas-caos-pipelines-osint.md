---
title: "Pruebas de caos en pipelines OSINT: ensayar fallos sin poner en riesgo la evidencia"
slug: /pruebas-caos-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, automation, privacy]
date: 2026-09-27
image: /img/blog/2026-09-27-pruebas-caos-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista ensayando fallos controlados dentro de un pipeline OSINT aislado](/img/blog/2026-09-27-pruebas-caos-pipelines-osint.png)

*Imagen generada mediante inteligencia artificial.*

La descarga de un portal público se interrumpe en el 83 %, pero el proceso conserva el fichero parcial con el nombre definitivo. La siguiente tarea lo interpreta como una adquisición completa, genera una tabla y deja el informe listo para publicar. No hubo una intrusión ni un algoritmo sofisticado: **solo un fallo ordinario que el pipeline convirtió silenciosamente en evidencia aparente**.

Las pruebas de caos controladas introducen condiciones adversas —latencia, cortes, respuestas truncadas, disco lleno o servicios temporalmente indisponibles— para comprobar cómo se comporta un sistema. En OSINT sirven para evaluar la resiliencia de nuestra propia infraestructura, nunca para perturbar una fuente ajena. Tampoco demuestran que los datos sean verdaderos: comprueban si el flujo falla de forma visible, conserva la procedencia y evita publicar resultados incompletos.

<!-- truncate -->

## Qué son y para qué sirven

La ingeniería del caos no consiste en romper cosas al azar. Los [Principios de Chaos Engineering](https://principlesofchaos.org/) proponen partir de un estado estable medible, formular una hipótesis, introducir una variable parecida a un fallo real y comparar el comportamiento del grupo de control con el experimental. También recomiendan reducir el radio de impacto.

Traducido a un pipeline OSINT, el estado estable no debería ser solo «el proceso termina con código cero». Puede incluir:

- cada adquisición terminada tiene tamaño, hash, hora UTC y URL registrados;
- ningún fichero parcial entra en transformación;
- un reintento no duplica registros ni sobrescribe un original válido;
- una caída del almacenamiento detiene la publicación;
- las alertas distinguen fuente inaccesible, dato inválido y error interno;
- el último dataset válido permanece identificable, pero no se presenta como actual.

El experimento intenta refutar una hipótesis concreta: «si la respuesta queda truncada, el adaptador la pone en cuarentena y ninguna tabla derivada se publica». Si el sistema genera igualmente una salida, hemos encontrado una debilidad reproducible. Si se detiene de forma segura, solo hemos ganado confianza en esa condición ensayada; no en todas las averías posibles.

Esta técnica complementa el [contract testing](/contract-testing-osint), que pregunta si una entrada cumple la interfaz esperada. El caos pregunta qué ocurre cuando una dependencia tarda, desaparece o entrega solo una parte. Ninguna de las dos valida por sí sola el contenido factual de la fuente.

## Caso legítimo: el observatorio ficticio de Villa Serena

Imaginemos un equipo que elabora una serie mensual agregada sobre contratación pública del ayuntamiento ficticio de **Villa Serena**. El flujo consulta una API institucional respetando sus condiciones, guarda cada respuesta cruda, valida el esquema, normaliza importes y publica únicamente totales agregados. No perfila personas ni prueba nada contra el portal real.

El equipo prepara un entorno aislado con fixtures sintéticos y un servidor local que imita las respuestas necesarias. Define esta hipótesis:

> Si una página JSON llega cortada, el adaptador no la renombra como completa, no avanza el cursor y no reemplaza el último snapshot válido.

El control procesa tres páginas ficticias completas. El experimento devuelve los mismos bytes en las dos primeras y corta la tercera a mitad de un objeto. Las observaciones esperadas son precisas:

| Señal | Resultado esperado |
| --- | --- |
| Estado de la ejecución | fallo explícito de adquisición |
| Fichero parcial | sufijo temporal y cuarentena |
| Snapshot anterior | intacto y con su hash original |
| Cursor de paginación | no avanza |
| Transformación | no se inicia |
| Publicación | bloqueada |
| Alerta | identifica truncado, intento y fixture |

No basta con comprobar que aparece una excepción. Hay que observar los efectos laterales: archivos, checkpoints, colas, métricas, logs y artefactos publicables. Un error bien registrado puede convivir con una tabla incorrecta si la frontera de publicación no está protegida.

## Flujo recomendado paso a paso

### 1. Elige una propiedad que deba sobrevivir

Empieza por una sola afirmación observable. «El pipeline es resiliente» no se puede probar; «un timeout no deja un artefacto con nombre definitivo» sí. Relaciona la propiedad con un riesgo editorial o probatorio: incompletitud invisible, pérdida de originales, duplicación, mezcla de ejecuciones o publicación obsoleta.

Describe primero la línea base con un fixture pequeño y determinista. Debe producir siempre los mismos archivos, hashes, recuentos y códigos de salida. Conserva la salida del control para compararla con el experimento.

### 2. Dibuja el radio de impacto

El blanco es **tu copia de pruebas**, no el portal público. Separa credenciales, buckets, bases de datos, colas y dominios de producción. Usa identificadores ficticios y un directorio temporal desechable. Bloquea el tráfico saliente salvo hacia servicios locales explícitos.

Fija además condiciones de parada. La documentación de [AWS Fault Injection Service](https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html) describe las *stop conditions* como alarmas que detienen un experimento al alcanzar un umbral. Aunque no uses AWS, el patrón es útil: duración máxima, consumo máximo, número máximo de reintentos y un interruptor manual verificable.

### 3. Construye una matriz pequeña de fallos

No combines diez averías en la primera ejecución. Aísla una variable cada vez:

| Frontera | Fallo simulado | Propiedad a comprobar |
| --- | --- | --- |
| HTTP | timeout antes de cabeceras | backoff acotado y error visible |
| Descarga | cuerpo truncado | no promover el temporal a definitivo |
| API | `429` o `503` sintético | respetar espera y limitar reintentos |
| Paginación | cursor repetido | detectar bucle y no duplicar |
| Disco | escritura incompleta | no registrar un hash de éxito |
| Almacén | indisponibilidad | bloquear derivados y publicación |
| Cola | entrega repetida | operación idempotente |
| Reloj | marca temporal inesperada | conservar UTC y señalizar anomalía |

Una matriz útil incluye precondición, inyección, oráculo, límite temporal, limpieza y evidencia del resultado. «Parece que aguantó» no es un criterio de aceptación.

### 4. Inyecta cerca de la frontera que controlas

Para pruebas unitarias, sustituye el cliente HTTP, el reloj o la función de escritura. La fixture [`monkeypatch` de pytest](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) permite cambiar atributos, diccionarios y variables de entorno durante un test y deshacer los cambios al terminar. `tmp_path` ofrece un directorio temporal único para cada prueba.

Un ejemplo conceptual, con datos inventados, sería:

```python
def test_un_truncado_no_se_publica(tmp_path, monkeypatch):
    destino = tmp_path / "adjudicaciones.json"

    monkeypatch.setattr(
        cliente,
        "descargar",
        lambda _url: b'{"results":[{"id":"VS-001"}'
    )

    resultado = adquirir("https://example.test/api", destino)

    assert resultado.ok is False
    assert not destino.exists()
    assert (tmp_path / "adjudicaciones.json.part").exists()
    assert publicar_fue_invocado() is False
```

El código real necesitará un oráculo más sólido que «el JSON no parsea»: longitud declarada, checksum cuando exista, contrato estructural, conteo de páginas y reglas de completitud. El objetivo del ejemplo es que el fallo no atraviese la frontera de publicación.

Para una integración local que dependa de TCP, [Toxiproxy](https://github.com/Shopify/toxiproxy) permite introducir latencia, limitar ancho de banda, cortar datos o deshabilitar un proxy. Está diseñado para entornos de desarrollo, pruebas y CI. Colócalo entre el cliente de pruebas y un servicio simulado; no delante de infraestructura de terceros.

### 5. Observa estado, no solo excepciones

Registra un identificador de ejecución y de experimento, fallo inyectado, instante de inicio y fin, fixture, versión del código y condición de parada. Compara:

- códigos de salida y excepciones tipadas;
- temporales, definitivos y hashes;
- checkpoints y cursores;
- número y calendario de reintentos;
- filas antes y después de deduplicar;
- tareas en cola;
- artefactos que llegan a publicación;
- mensaje que recibiría la persona analista.

Los logs no deben copiar tokens, cabeceras de autenticación ni cuerpos sensibles. Un experimento de resiliencia no justifica ampliar la recogida de datos.

### 6. Limpia y convierte el hallazgo en regresión

Retira la inyección aunque falle una aserción, destruye el entorno efímero y confirma que no quedan proxies, reglas o temporales activos. Después reduce el fallo a un caso determinista. La prueba de caos descubre una condición; una prueba automatizada más pequeña evita que reaparezca en cada cambio.

Documenta tres resultados por separado:

1. **Fallo introducido:** por ejemplo, corte tras 2 KiB.
2. **Comportamiento observado:** el temporal recibió nombre definitivo.
3. **Riesgo para el análisis:** una adquisición incompleta podía llegar a transformación.

No escribas «la fuente manipuló la descarga». El experimento solo habla de cómo reacciona nuestro sistema a una condición fabricada.

## Qué conviene ensayar primero

Prioriza fallos frecuentes y de alto impacto, no escenarios espectaculares:

### Timeout y reintentos

Comprueba que existe un timeout finito por operación, que el número de intentos está limitado y que la espera no sincroniza cientos de tareas. Una ejecución agotada debe terminar en estado inequívoco. Nunca conviertas «no se pudo consultar» en cero resultados.

### Respuesta truncada o mal codificada

Escribe primero en un fichero temporal dentro del mismo sistema de archivos, valida y solo entonces promueve el artefacto. Conserva la respuesta problemática en cuarentena cuando sea legal y necesario, con retención limitada y sin mezclarla con originales válidos.

### Almacenamiento indisponible

Si no se puede preservar la adquisición, el pipeline no debería continuar como si existiera una cadena de procedencia. Ensaya también el caso en que los bytes se guardan pero falla el registro de metadatos: datos sin contexto no equivalen a evidencia lista para analizar.

### Duplicación y reordenación

Las colas pueden volver a entregar una tarea y las páginas pueden aparecer en distinto orden. Usa claves estables, operaciones idempotentes y deduplicación explícita. Comprueba que repetir una ejecución no duplica el total y que dos respuestas distintas nunca comparten por accidente el mismo identificador de adquisición.

### Recuperación tras interrupción

Mata una tarea entre escritura y commit en el entorno de pruebas. Al reiniciar, el sistema debe distinguir lo completo, lo parcial y lo desconocido. La recuperación correcta quizá descarte trabajo; es preferible a reutilizar un fragmento como si estuviera validado.

## Limitaciones y falsos positivos

Una prueba puede fallar porque el inyector está mal configurado, no porque el pipeline sea débil. Verifica primero que el fallo ocurrió donde esperabas. También puede pasar en local y fallar en producción por diferencias de permisos, latencia, límites o topología.

Otros límites importantes:

- una lista de fallos nunca es exhaustiva;
- el estado estable elegido puede ignorar una degradación relevante;
- mocks demasiado simples no reproducen streaming, cachés o cierres de conexión;
- dos fallos simultáneos pueden interactuar de forma distinta a dos ensayos aislados;
- una recuperación técnica correcta puede reutilizar datos antiguos sin avisarlo;
- una ejecución verde no valida cobertura, actualidad ni veracidad de la fuente;
- inyectar fallos en producción requiere autoridad, observabilidad y salvaguardas que este flujo deliberadamente no presupone.

Evita medir el éxito solo por disponibilidad. En OSINT, «seguir publicando» puede ser peor que detenerse si se ha perdido integridad, completitud o procedencia.

## Buenas prácticas de OPSEC, ética y privacidad

- Limita los experimentos a sistemas propios o expresamente autorizados.
- Usa fixtures sintéticos; no copies expedientes personales a herramientas externas.
- Deniega por defecto el tráfico hacia internet desde el entorno de pruebas.
- Retira credenciales reales y aplica permisos mínimos.
- Define duración, radio de impacto, condición de parada y responsable antes de ejecutar.
- Preserva originales válidos como solo lectura y trabaja sobre copias.
- Separa el almacén de cuarentena del publicable.
- No registres cuerpos completos cuando basten tamaño, hash y tipo de error.
- Trata la indisponibilidad de una fuente como limitación, no como sospecha.
- Exige revisión humana antes de difundir conclusiones sensibles.

## Lista de control

- [ ] La hipótesis describe una propiedad observable.
- [ ] La línea base es determinista y está guardada.
- [ ] El experimento usa datos ficticios y servicios propios.
- [ ] Producción y fuentes públicas quedan fuera del radio de impacto.
- [ ] Hay timeout, límite de reintentos y condición de parada.
- [ ] Solo se introduce una variable nueva por primera ejecución.
- [ ] Se observan archivos, estado, cursores, colas y publicación.
- [ ] Temporales y definitivos no pueden confundirse.
- [ ] Un snapshot anterior nunca se presenta como actual sin aviso.
- [ ] Los logs están minimizados y no contienen secretos.
- [ ] La limpieza se ejecuta también cuando falla el test.
- [ ] Cada debilidad termina en una regresión reproducible.
- [ ] Un resultado verde se presenta como resiliencia acotada, no como verdad.

## Alternativas y siguientes pasos

El [contract testing](/contract-testing-osint) protege la interfaz entre adquisición y transformación; el [mutation testing](/mutation-testing-pipelines-osint) evalúa si los tests detectan cambios peligrosos; y las [pruebas metamórficas](/pruebas-metamorficas-osint-invariantes) comprueban propiedades entre ejecuciones relacionadas. Las pruebas de caos ocupan otra capa: fuerzan condiciones operativas adversas y observan si el sistema conserva sus garantías.

El takeaway accionable es modesto: toma hoy un fixture sintético, haz que tu cliente local devuelva la mitad del cuerpo y comprueba que no aparece ningún fichero definitivo ni artefacto publicable. Añade después una aserción sobre el snapshot anterior y otra sobre el mensaje de alerta. Si el proceso termina «bien», has encontrado un fallo de seguridad editorial antes de que lo encuentre una caída real.

Como próximo tema, merece la pena estudiar **property-based testing en pipelines OSINT**: generar muchas entradas sintéticas sujetas a restricciones para descubrir combinaciones que nuestros ejemplos manuales no contemplaron, sin confundir invariantes del software con verdad factual.

## Fuentes consultadas

- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- [AWS Fault Injection Service: stop conditions](https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html)
- [AWS Fault Injection Service: componentes de una plantilla de experimento](https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html)
- [Toxiproxy: repositorio y documentación oficial](https://github.com/Shopify/toxiproxy)
- [pytest: uso seguro de monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest: directorios temporales con tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
