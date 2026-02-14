# Posibles posts (OSINT blog)

Fuente: Google Doc 1lskgX8KPVEQAeo9JeDHZCEbqTjCiSZ44oNLygc-BIk0
Actualizado: 2026-02-09T05:14:32.462Z

## Ideas (candidatas)

Regla: al publicar una idea, moverla a "Publicados" con fecha y titulo del post.

Regla editorial (nuevo): alternar herramientas e historias
- Objetivo: que el blog no sea solo "catalogo de herramientas". Publicar alternando:
  - 1 post de herramienta (lista de abajo)
  - 1 post de historia OSINT (lista nueva mas abajo)
- Estilo obligatorio para posts de historia: mini-relatos emocionantes y divertidos de leer (con metodo y evidencias).
- Para ampliar contexto de las historias (fuentes y casos): ver
  - /home/ubuntu/Documents/resources/investigaciones/2026-02-14--casos-reales-resueltos-o-impulsados-por-osint-global.md
  - ideas/historias-osint.md

## Historias (candidatas, basadas en investigacion)

Nota: estas ideas no sustituyen a las herramientas; se deben alternar (1 herramienta, 1 historia).

- [ ] Historia: MH17 (2014-2022) - geolocalizacion/cronologia y salto a tribunal
- [ ] Historia: Skripal (2018) - identidades de cobertura y triangulacion OSINT
- [ ] Historia: Navalny (2020) - patrones de viaje + confirmacion tecnica (OPAQ)
- [ ] Historia: "Jihadi John" (2014-2015) - identificacion publica y corroboracion periodistica
- [ ] Historia: Siria (2013-2020) - verificacion de material y atribucion formal (OPAQ)
- [ ] Historia: Khashoggi (2018-2021) - atribucion publica + informes ONU/EE.UU.
- [ ] Historia: Rohingya (2017) - satelite antes/despues para documentar destruccion
- [ ] Historia: Jan 6 (2021) - un oceano de videos y como evitar errores de identificacion
- [ ] Historia: Bucha (2022) - satelite + cronologia para fijar hechos
- [ ] Historia: Ngarbuh (Camerun, 2020) - satelite para corroborar incendios y destruccion
- [ ] Historia: Pandora Papers (2021) - filtracion validada/ampliada con OSINT (nota: no OSINT puro)

- [ ] SpiderFoot
- [ ] Amass (OWASP)
- [ ] Recon-ng
- [ ] Sherlock
- [ ] Maigret
- [ ] ADS-B Exchange & MarineTraffic
- [ ] Arkham Intelligence & DeBank
- [ ] Blackbird
- [ ] Castrick y la Geolocalización Precisa
- [ ] El Estrato Fundamental: Motores de Búsqueda y Arquitectura de la Información
- [ ] ExifTool & InVID
- [ ] Ghunt (Google OSINT)
- [ ] Herramientas de Verificación de Contacto y Correo Electrónico
- [ ] Holehe
- [ ] Inteligencia Centrada en Personas (SOCMINT): De la Fama al Nicho
- [ ] Inteligencia de Plataformas Específicas y Nichos Técnicos
- [ ] Inteligencia Geoespacial (GEOINT) y Forense Multimedia (IMINT)
- [ ] Introducción: El Estado del Arte en la Inteligencia Abierta
- [ ] La Frontera Financiera: Blockchain y Criptomonedas
- [ ] La Potencia Comunitaria: Automatización y Scripts de Código Abierto (GitHub)
- [ ] Los Gigantes de la Infraestructura y la Visualización
- [ ] Lynir y la IA Predictiva
- [ ] OSINTgram (Instagram)
- [ ] PhoneInfoga
- [ ] Tendencias Emergentes y Herramientas del Futuro (2026)
- [ ] Toutatis (TikTok)
- [ ] WhatsMyName

## Publicados

- 2026-02-14: theHarvester en OSINT: reconocimiento de dominio y exposicion de correo con enfoque defensivo
- 2026-02-13: Maltego en OSINT: analisis de enlaces y grafos para investigar con metodo
- 2026-02-12: Shodan en OSINT: cartografiar superficie expuesta con enfoque defensivo
- 2026-02-11: Wayback Machine en OSINT: analisis historico web con metodo
- 2026-02-08: Que es OSINT: origenes, historia y estado actual
- 2026-02-10: Google Dorks para OSINT responsable: auditoria defensiva y verificacion

## Fuente (raw)

Panorama Integral de Herramientas de Inteligencia de Fuentes Abiertas (OSINT) 2025-2026: Una Taxonomía Operativa Jerarquizada por Popularidad y Especialización Técnica
Introducción: El Estado del Arte en la Inteligencia Abierta
El ecosistema de la Inteligencia de Fuentes Abiertas (OSINT, por sus siglas en inglés) ha experimentado una metamorfosis radical en el bienio 2025-2026. Lo que comenzó como una disciplina auxiliar, relegada a la verificación de datos periodísticos o a la fase preliminar de las auditorías de seguridad, se ha consolidado como el pilar central de la inteligencia moderna, tanto en el ámbito corporativo como en el gubernamental. Las proyecciones de mercado, que anticipaban una valoración global cercana a los 29.19 mil millones de dólares para 2026 con una tasa de crecimiento anual compuesta del 24.7% , se han visto validadas por la omnipresencia de estas herramientas en los centros de operaciones de seguridad (SOC) y en las unidades de investigación financiera.
La democratización del acceso a herramientas sofisticadas, impulsada por comunidades de código abierto en plataformas como GitHub y el surgimiento de soluciones SaaS (Software as a Service) potenciadas por inteligencia artificial, ha creado un entorno donde la barrera de entrada técnica disminuye mientras que la complejidad del análisis aumenta. Sin embargo, esta accesibilidad conlleva el desafío de la saturación: el analista contemporáneo se enfrenta a un océano de utilidades redundantes, "abandonware" y scripts no mantenidos.
El presente informe técnico tiene como objetivo desglosar este complejo panorama, no a través de una lista arbitraria, sino mediante una jerarquización rigurosa basada en la popularidad, la adopción industrial y la especificidad técnica. Comenzando por los "titanes" de la industria —herramientas cuya ubicuidad las convierte en estándares de facto— y descendiendo hacia utilidades de nicho y scripts emergentes que, aunque menos conocidos, ofrecen capacidades críticas para vectores de investigación específicos. Este análisis integra las tendencias más recientes observadas en 2025 y 2026, incluyendo el auge de la inteligencia sobre blockchain, la automatización mediante agentes de IA y la necesidad imperiosa de herramientas de contrainteligencia para preservar la seguridad operativa (OPSEC) del investigador.
1. El Estrato Fundamental: Motores de Búsqueda y Arquitectura de la Información
En la cúspide de la pirámide de popularidad se encuentran las herramientas que no requieren instalación compleja, sino una comprensión profunda de la sintaxis de consulta. Estas son las primeras paradas obligatorias en cualquier ciclo de inteligencia, utilizadas universalmente por su capacidad para filtrar el ruido de la web superficial y acceder a la memoria histórica de Internet.
1.1 Google Dorks (Google Hacking)
La técnica de "Google Dorking" permanece, en 2026, como la habilidad más esencial y extendida en el arsenal del investigador OSINT. A pesar de los avances en herramientas automatizadas, la capacidad de manipular los operadores de búsqueda de Google para extraer información indexada inadvertidamente sigue siendo insuperable en términos de relación costo-efectividad.
Mecanismo Técnico y Aplicación: El funcionamiento de los Google Dorks se basa en el uso de operadores avanzados que restringen las consultas a campos específicos de los metadatos de las páginas indexadas. Operadores como filetype:, site:, inurl:, intitle: y intext: permiten a los investigadores realizar incisiones quirúrgicas en la base de datos de Google.
* Recuperación de Documentos Sensibles: La combinación filetype:pdf "confidential" site:target.com sigue siendo una vía primaria para la exfiltración pasiva de documentos corporativos, contratos o manuales internos que han sido expuestos por configuraciones erróneas de servidores web.
* Identificación de Vulnerabilidades: Consultas como inurl:admin intext:login o intitle:"index of" permiten localizar paneles de administración desprotegidos o directorios abiertos que exponen archivos del sistema, una práctica común en la fase de reconocimiento de pruebas de penetración.
Evolución y Contexto 2026: Hacia 2026, la relevancia de Google Dorks ha evolucionado para integrarse con la automatización. Herramientas de terceros ahora rotan estos "dorks" de manera programática para evitar los CAPTCHAs y las restricciones de tasa de Google, permitiendo el escaneo masivo de dominios en busca de fugas de información. Además, la técnica se ha adaptado para "dorkear" otros motores de búsqueda que han ganado tracción por su menor censura o diferentes algoritmos de indexación, aunque Google mantiene la hegemonía por el volumen de su índice.
1.2 The Wayback Machine (Internet Archive)
La "memoria" de la web es una herramienta crítica para la investigación forense y la verificación de hechos. Su popularidad es transversal, abarcando desde periodistas hasta analistas de amenazas cibernéticas.
Capacidades Forenses: La Wayback Machine permite acceder a instantáneas (snapshots) de páginas web tal como existían en el pasado. Esto es fundamental para:
* Análisis de Defacement y Compromiso: Los equipos de respuesta a incidentes utilizan el archivo para determinar cuándo un sitio web fue modificado maliciosamente, comparando el código fuente de versiones archivadas con la versión actual comprometida.
* Recuperación de Inteligencia Eliminada: En investigaciones corporativas, permite recuperar ofertas de trabajo antiguas que a menudo revelan detalles técnicos específicos sobre la infraestructura de TI (versiones de software, sistemas operativos utilizados) que posteriormente fueron eliminados por seguridad.
* Verificación de Desinformación: Es la herramienta estándar para contrarrestar el "gaslighting" digital, permitiendo probar que una declaración pública fue hecha y posteriormente borrada o alterada.
Limitaciones y Alternativas: A pesar de su inmensa utilidad, la Wayback Machine no es infalible; los sitios pueden solicitar la exclusión de su índice mediante robots.txt o peticiones legales. Por ello, herramientas complementarias como Archive.today han ganado popularidad en el estrato medio por su capacidad para capturar páginas "bajo demanda" y sortear algunos bloqueos que afectan al Internet Archive.
2. Los Gigantes de la Infraestructura y la Visualización
Descendiendo un nivel en abstracción pero manteniendo una popularidad masiva en el sector de la ciberseguridad, encontramos las plataformas diseñadas para mapear la infraestructura técnica y visualizar relaciones complejas. Estas herramientas son estándares industriales, presentes en casi todas las distribuciones de seguridad ofensiva y defensiva.
2.1 Shodan
Frecuentemente malinterpretado por el público general como un "Google para hackers", Shodan es, en realidad, un motor de búsqueda de banners de servicio. Su enfoque no es el contenido web, sino la respuesta técnica de los dispositivos conectados a Internet.
Funcionalidad y Casos de Uso Críticos: Shodan escanea incesantemente el espacio de direcciones IPv4 (y crecientemente IPv6) en busca de puertos abiertos. Al interactuar con estos puertos, captura los metadatos que los servicios devuelven.
* Superficie de Ataque IoT: Es la herramienta preeminente para identificar cámaras de seguridad, sistemas de control industrial (SCADA), semáforos y electrodomésticos inteligentes que están expuestos a Internet sin autenticación o con credenciales por defecto.
* Inteligencia de Vulnerabilidades: En 2026, Shodan ha perfeccionado su capacidad para etiquetar dispositivos vulnerables a CVEs específicos en tiempo real. Los analistas pueden buscar vuln:CVE-2025-XXXX para mapear la prevalencia global de una nueva vulnerabilidad crítica horas después de su divulgación.
* Monitoreo Defensivo: Las organizaciones utilizan Shodan Monitor para recibir alertas cuando sus rangos de IP exponen servicios no autorizados, actuando como un sistema de alerta temprana externo.
Integración: Su API es un componente central en muchas otras herramientas OSINT (como Maltego y TheHarvester), lo que multiplica su relevancia en el ecosistema. Aunque ofrece acceso gratuito limitado, las capacidades completas de filtrado y escaneo bajo demanda son características premium que definen su modelo de negocio "Freemium".
2.2 Maltego
Maltego es sinónimo de análisis de enlaces y visualización de grafos en el mundo OSINT. Es la herramienta que define cómo se "ve" una investigación compleja.
Arquitectura de Transformadas: La potencia de Maltego reside en su arquitectura modular basada en "transformadas". El usuario introduce una entidad semilla (por ejemplo, un dominio empresa.com) y ejecuta transformadas que consultan fuentes de datos externas (servidores DNS, bases de datos whois, redes sociales) para devolver entidades relacionadas (direcciones IP, correos electrónicos, nombres de personas).
* Visualización de Relaciones: Su capacidad para representar visualmente redes complejas permite a los investigadores identificar patrones no obvios, como la infraestructura compartida entre dos grupos de amenazas aparentemente distintos o la conexión entre una empresa pantalla y sus beneficiarios reales.
* El "Hub" de Datos: Maltego actúa como un agregador, permitiendo integrar datos de proveedores comerciales (como Recorded Future o Social Links) y fuentes gratuitas en un solo gráfico.
Posicionamiento en 2026: Sigue siendo la herramienta preferida para la presentación de informes de inteligencia debido a su capacidad para contar una historia visual. Sin embargo, su curva de aprendizaje y el costo de las licencias comerciales para acceder a transformadas avanzadas mantienen una barrera de entrada para investigadores independientes, quienes a menudo dependen de la versión "Community".
2.3 TheHarvester
Un clásico indiscutible en la fase de reconocimiento, incluido por defecto en Kali Linux y manteniendo una base de usuarios fiel y masiva.
Misión y Ejecución: Diseñado para la simplicidad y la eficacia, TheHarvester automatiza la recolección de correos electrónicos, subdominios, nombres de empleados, puertos abiertos y banners desde fuentes públicas.
* Fuentes Diversificadas: Consulta múltiples motores de búsqueda (Google, Bing, Baidu), servidores de claves PGP y la base de datos de Shodan para construir un perfil inicial del objetivo.
* Popularidad en GitHub: Con más de 15,600 estrellas, es una de las herramientas de reconocimiento más "estrelladas" y mantenidas, lo que garantiza su actualización constante frente a cambios en las APIs de los motores de búsqueda.
* Valor Táctico: Es ideal para la enumeración rápida en las primeras etapas de un pentest, proporcionando una lista de vectores de ataque potenciales (correos para phishing, subdominios para toma de control) en cuestión de segundos.
3. La Potencia Comunitaria: Automatización y Scripts de Código Abierto (GitHub)
En este estrato encontramos herramientas que, aunque carecen a veces de la interfaz pulida de las soluciones comerciales, son veneradas por la comunidad técnica por su potencia, flexibilidad y costo cero. Estas herramientas suelen residir en GitHub y su popularidad se mide en "estrellas" y "forks", indicadores directos de su utilidad y mantenimiento activo.
3.1 SpiderFoot
Conocida como la "navaja suiza" del OSINT automatizado, SpiderFoot ha trascendido su origen como script para convertirse en una plataforma completa con versiones tanto de código abierto como comerciales (SpiderFoot HX).
Automatización Modular: SpiderFoot destaca por su capacidad para encadenar consultas. Si un módulo encuentra una dirección de correo electrónico, automáticamente dispara otros módulos para buscar ese correo en bases de datos de brechas, redes sociales y registros de dominio, sin intervención del usuario.
* Cobertura Exhaustiva: Integra cientos de módulos que consultan desde listas negras de spam hasta registros de blockchain y archivos de la web oscura.
* Reconocimiento: Con más de 16,600 estrellas en GitHub, es una de las herramientas más respetadas por su capacidad para generar una cantidad masiva de inteligencia a partir de un solo dato de entrada (target).
* Visualización: A diferencia de muchos scripts de línea de comandos, SpiderFoot ofrece una interfaz web (GUI) que permite visualizar los datos en tablas y gráficos, haciéndola accesible a analistas menos técnicos.
3.2 Amass (OWASP)
Desarrollada bajo el paraguas de OWASP (Open Web Application Security Project), Amass es la herramienta definitiva para el mapeo de la superficie de ataque y el descubrimiento de subdominios, superando a menudo a herramientas comerciales en profundidad.
Técnicas Avanzadas de Enumeración: Amass no se limita al scraping pasivo. Utiliza técnicas activas y pasivas, incluyendo fuerza bruta recursiva, transferencias de zona DNS (cuando es posible), y análisis de certificados SSL/TLS para descubrir subdominios que no están listados públicamente.
* Mapeo de Infraestructura: Es capaz de mapear redes completas, identificando sistemas autónomos (ASN) y bloques de netblock asociados a una organización.
* Gestión de Base de Datos: Una característica distintiva es su capacidad para mantener una base de datos de grafos local, lo que permite rastrear cómo cambia la infraestructura de un objetivo a lo largo del tiempo (monitorización de deriva).
* Estatus: Con más de 14,100 estrellas en GitHub, es el estándar de facto para la fase de reconocimiento de subdominios en auditorías de seguridad modernas.
3.3 Recon-ng
Inspirado en el framework Metasploit, Recon-ng ofrece un entorno de consola familiar para los pentesters, modularizando el proceso de reconocimiento web.
Estructura de Framework: A diferencia de herramientas de "clic y ejecutar", Recon-ng proporciona un entorno interactivo donde los analistas cargan módulos específicos (reconocimiento de contactos, perfiles de empresas, dominios), configuran claves API y gestionan una base de datos interna de hallazgos.
* Flexibilidad: Su diseño modular permite a la comunidad contribuir con nuevos módulos rápidamente cuando surgen nuevas fuentes de datos o técnicas.
* Popularidad: Aunque su curva de aprendizaje es más pronunciada que la de SpiderFoot, mantiene una base de usuarios sólida (~5,300 estrellas en GitHub) debido a su potencia y capacidad de personalización.
4. Inteligencia Centrada en Personas (SOCMINT): De la Fama al Nicho
El rastreo de individuos a través de su huella digital es una de las disciplinas más demandadas y sensibles del OSINT. Aquí, la jerarquía de herramientas va desde buscadores de nombres de usuario masivos hasta scripts quirúrgicos para plataformas específicas.
4.1 Sherlock
Sherlock es el rey indiscutible de la búsqueda de nombres de usuario por volumen de popularidad en la comunidad de desarrolladores.
Funcionamiento y Alcance: Con más de 72,000 estrellas en GitHub, este script en Python busca un nombre de usuario específico a través de más de 400 redes sociales y sitios web.
* Simplicidad: Su éxito radica en su premisa simple: "¿Existe el usuario 'X' en la plataforma 'Y'?". Devuelve una lista de URLs directas a los perfiles encontrados.
* Limitaciones: Sherlock es una herramienta de detección, no de extracción. Confirma la existencia, pero no descarga la información del perfil ni analiza el contenido, lo que a menudo requiere pasos manuales posteriores.
4.2 Maigret
Considerada la evolución técnica de Sherlock, Maigret ha ganado tracción rápidamente (~18,900 estrellas) entre los investigadores que necesitan profundidad además de amplitud.
Capacidades Enriquecidas: Maigret no solo verifica la existencia de una cuenta, sino que extrae metadatos valiosos del perfil (nombre completo, biografía, localización, ID numérico, fecha de registro) y genera informes detallados (HTML, PDF).
* Búsqueda Recursiva: Una de sus características más potentes es la capacidad de realizar búsquedas recursivas: si encuentra un nuevo alias o nombre de usuario dentro de un perfil descubierto, puede iniciar automáticamente una nueva búsqueda para ese alias, ampliando la red de investigación.
* Análisis de Etiquetas: Clasifica los sitios donde se encuentra al objetivo (por ejemplo, "sitios de citas", "foros de hacking", "comercio electrónico"), permitiendo al analista perfilar los intereses y el comportamiento del sujeto.
4.3 Blackbird
Una herramienta emergente en la categoría de búsqueda de usuarios, compitiendo directamente con Sherlock por su velocidad y precisión.
Optimización y Velocidad: Blackbird (~5,600 estrellas) se distingue por su arquitectura asíncrona optimizada, lo que le permite realizar comprobaciones en cientos de sitios mucho más rápido que sus predecesores.
* Reducción de Falsos Positivos: Utiliza comprobaciones más sofisticadas para evitar los falsos positivos comunes que plagan a herramientas más antiguas cuando los sitios web cambian sus páginas de error 404.
4.4 WhatsMyName
Más que una herramienta, es un proyecto comunitario que mantiene una de las bases de datos más precisas de patrones de URL para la enumeración de usuarios.
El Estándar de Definición: El proyecto "WhatsMyName" ( ~2,400 estrellas en GitHub) proporciona los archivos JSON que alimentan a muchas otras herramientas (incluida SpiderFoot). Su aplicación web asociada permite realizar búsquedas rápidas y exportar resultados, siendo una favorita para verificaciones rápidas sin necesidad de usar la línea de comandos.
5. Herramientas de Verificación de Contacto y Correo Electrónico
Descendiendo hacia herramientas más específicas, entramos en el terreno de la validación de identidad a través de selectores primarios como el correo electrónico y el teléfono. Estas herramientas son menos "famosas" que Sherlock pero críticas para la atribución.
5.1 Holehe
Holehe es una herramienta de nicho pero de valor incalculable para la inteligencia de correo electrónico (~2k-3k estrellas).
Técnica de Recuperación de Contraseña: A diferencia de las herramientas que buscan en bases de datos de brechas, Holehe verifica si un correo electrónico está registrado en más de 120 sitios (Twitter, Instagram, Imgur, etc.) abusando de la función de "olvidé mi contraseña".
* Sigilo: La herramienta está diseñada para no alertar al objetivo (no envía el correo de recuperación final, solo verifica que el sitio acepte la dirección), lo que la hace superior en términos de OPSEC.
* Caso de Uso: Permite confirmar qué servicios utiliza activamente un objetivo, lo que puede revelar intereses, afiliaciones o plataformas alternativas de comunicación.
5.2 PhoneInfoga
El estándar de facto para la inteligencia de números de teléfono (OSINT telefónico), con ~15,800 estrellas en GitHub.
Rastreo Telefónico: PhoneInfoga escanea números de teléfono internacionales para extraer información detallada:
* Identificación de Operador y Línea: Determina si es un móvil, fijo o VoIP (Voz sobre IP), lo cual es crucial para identificar números desechables (burners).
* Huella Digital: Busca el número en motores de búsqueda, dorks específicos y directorios para encontrar asociaciones con anuncios clasificados, perfiles sociales o documentos públicos.
6. Inteligencia de Plataformas Específicas y Nichos Técnicos
En este nivel encontramos herramientas diseñadas para explotar una sola plataforma o tecnología. Son menos populares en términos generales porque su utilidad está restringida a un objetivo concreto, pero son insustituibles cuando ese objetivo es el centro de la investigación.
6.1 Ghunt (Google OSINT)
Una herramienta especializada en la extracción de inteligencia de cuentas de Google.
Profundidad sobre Amplitud: Ghunt permite investigar a fondo una dirección de Gmail o un ID de Gaia.
* Datos Extraídos: Puede revelar el nombre del perfil, la última vez que se editó, fotos de perfil (y sus metadatos), y, crucialmente, las reseñas de Google Maps escritas por el usuario. Esto último puede permitir geolocalizar la residencia o los lugares frecuentados por el objetivo.
* Requisitos Técnicos: Requiere la extracción de cookies de sesión para funcionar, lo que eleva la barrera técnica de entrada, manteniéndola como una herramienta para investigadores avanzados.
6.2 Toutatis (TikTok)
Con el ascenso de TikTok como plataforma global, herramientas como Toutatis (~3,700 estrellas) han emergido para llenar el vacío de inteligencia en esta red.
Extracción de Datos de TikTok: Permite extraer información de perfiles, incluyendo correos electrónicos y números de teléfono (si están vinculados y semiexpuestos), IDs de usuario y metadatos de videos. Es fundamental para investigaciones modernas donde la huella digital del objetivo se ha desplazado de Facebook a TikTok.
6.3 OSINTgram (Instagram)
Herramienta de línea de comandos para realizar análisis profundo de cuentas de Instagram.
Capacidades Interactivas: Ofrece una consola interactiva para listar seguidores, seguidos, comentarios, hashtags más usados y geolocalizaciones de publicaciones.
* Desafíos: Debido a las agresivas medidas anti-scraping de Instagram, OSINTgram requiere que el investigador inicie sesión con una cuenta real, lo que conlleva un riesgo significativo de bloqueo de cuenta (shadowban o suspensión), limitando su uso a cuentas "sockpuppet" (falsas) desechables.
7. La Frontera Financiera: Blockchain y Criptomonedas
El auge de las criptomonedas ha dado lugar a una nueva categoría de herramientas OSINT especializadas en el rastreo de activos digitales. Aunque menos conocidas por el público general, son estándares en la investigación de fraudes financieros y lavado de dinero.
7.1 Arkham Intelligence & DeBank
Estas plataformas representan la vanguardia de la inteligencia blockchain, moviéndose más allá de los simples exploradores de bloques.
Desanonimización de la Blockchain:
* Arkham: Utiliza inteligencia artificial para etiquetar direcciones de billeteras con identidades del mundo real (exchanges, fondos de cobertura, individuos conocidos). Permite visualizar flujos de fondos complejos entre entidades, transformando hashes ininteligibles en mapas de relaciones claros.
* DeBank: Enfocado en las finanzas descentralizadas (DeFi), permite rastrear el portafolio completo de una dirección a través de múltiples cadenas (EVM), revelando no solo saldos sino interacciones con protocolos de préstamo y pools de liquidez.
8. Inteligencia Geoespacial (GEOINT) y Forense Multimedia (IMINT)
Estas herramientas cierran la brecha entre el mundo digital y el físico, permitiendo verificar ubicaciones y la integridad de archivos multimedia.
8.1 ADS-B Exchange & MarineTraffic
Para el seguimiento de activos físicos globales (aviones y barcos).
* ADS-B Exchange: A diferencia de competidores comerciales que filtran datos a petición de propietarios de aeronaves, ADS-B Exchange ofrece datos "crudos" y sin censura, permitiendo el rastreo de aviones militares, policiales y jets privados de alto perfil.
* MarineTraffic: Estándar para el rastreo marítimo mediante AIS, crucial para analizar cadenas de suministro y movimientos en zonas de conflicto.
8.2 ExifTool & InVID
Herramientas esenciales para la verificación de contenido multimedia.
* ExifTool: La librería definitiva para leer y editar metadatos. Permite descubrir coordenadas GPS ocultas, modelos de cámara y fechas de creación originales en archivos que no han sido "limpiados" por las plataformas sociales.
* InVID/WeVerify: Un plugin de navegador vital para periodistas, diseñado para verificar videos y fotos, detectando manipulaciones, realizando búsquedas inversas en múltiples motores simultáneamente y analizando el flujo de fotogramas.
9. Tendencias Emergentes y Herramientas del Futuro (2026)
En la periferia de la popularidad, pero con un alto potencial disruptivo, se encuentran herramientas que aprovechan la IA y nuevas metodologías.
9.1 Lynir y la IA Predictiva
Lynir es un ejemplo de la nueva ola de herramientas de "inteligencia visual" y predictiva. A diferencia del monitoreo tradicional de palabras clave, utiliza IA para analizar objetos y logos dentro de imágenes y videos, y emplea análisis de sentimientos para predecir tendencias de riesgo social antes de que escalen.
9.2 Castrick y la Geolocalización Precisa
Herramientas como Castrick (ClatScope) están emergiendo para integrar múltiples vectores de geolocalización (DNS, WHOIS, datos de brechas) en una sola interfaz, facilitando la tarea de ubicar físicamente una infraestructura digital.
Tabla Resumen: Selección Estratégica de Herramientas (2025-2026)
Categoría
	Herramienta
	Nivel de Popularidad
	Caso de Uso Principal
	Tipo de Acceso
	Búsqueda Web
	Google Dorks
	Ubicua
	Filtrado de información indexada
	Gratuito
	Infraestructura
	Shodan
	Estándar Industrial
	IoT y Servicios Expuestos
	Freemium
	Visualización
	Maltego
	Estándar Industrial
	Análisis de Enlaces y Grafos
	Freemium
	Automatización
	SpiderFoot
	Alta (GitHub)
	Reconocimiento Pasivo Automático
	Open Source / Pagado
	Personas
	Sherlock
	Alta (GitHub)
	Verificación de Usuarios
	Open Source
	Personas (Profundo)
	Maigret
	Media-Alta
	Perfilado y Reportes de Usuarios
	Open Source
	Subdominios
	Amass
	Alta (OWASP)
	Mapeo de Superficie de Ataque
	Open Source
	Email
	Holehe
	Nicho
	Validación de Registro de Email
	Open Source
	Plataforma
	Ghunt
	Nicho Técnico
	Inteligencia de Cuentas Google
	Open Source
	Blockchain
	Arkham
	Emergente
	Inteligencia Crypto/DeFi
	Freemium
	Forense
	ExifTool
	Estándar Técnico
	Análisis de Metadatos
	Open Source
	Este panorama refleja un ecosistema maduro donde la especialización es la clave. Mientras herramientas generalistas como Maltego o Google Dorks proporcionan la amplitud necesaria para iniciar cualquier investigación, el verdadero valor de inteligencia en 2026 reside a menudo en la aplicación quirúrgica de herramientas de nicho como Holehe, Ghunt o Arkham, capaces de extraer datos que permanecen invisibles para los escaneos superficiales.
Obras citadas
1. Top 15 Free OSINT Tools To Collect Data From Open Sources - Recorded Future, https://www.recordedfuture.com/threat-intelligence-101/tools-and-technologies/osint-tools 2. Top 12 Best Open Source Intelligence Tools (OSINT Tools) for ..., https://www.cryptika.com/top-12-best-open-source-intelligence-tools-osint-tools-for-penetration-testing-2026/ 3. The Ultimate OSINT Toolkit: 15 Free Tools to Become a Digital Detective in 2025 - Reddit, https://www.reddit.com/r/PrivatePackets/comments/1m3s2ih/the_ultimate_osint_toolkit_15_free_tools_to/ 4. Best OSINT Tools 2025: A Hands-On Guide for Cybersecurity Investigations, https://pentesting.dhound.io/blog/best-osint-tools-2025 5. Top 10 OSINT Tools for Image and Video Verification in 2025 | by VerifyHQ - Medium, https://medium.com/@VerifyHQ/top-10-osint-tools-for-image-and-video-verification-in-2025-139f06458172 6. 15 Best OSINT tools in 2026 - Lampyre, https://lampyre.io/blog/15-best-osint-tools-in-2025/ 7. 13 Best OSINT (Open Source Intelligence) Tools for 2025 [UPDATED] - Talkwalker, https://www.talkwalker.com/blog/best-osint-tools 8. Top 9 OSINT Tools | Wiz, https://www.wiz.io/academy/threat-intel/osint-tools 9. Best OSINT Tools for Intelligence Gathering (2026) Free and Paid - ShadowDragon.io, https://shadowdragon.io/blog/best-osint-tools/ 10. Open Source Intelligence with theHarvester - Spread Security, https://spreadsecurity.github.io/2016/08/22/open-source-intelligence-with-theharvester.html 11. laramies/theHarvester: E-mails, subdomains and names Harvester - OSINT - GitHub, https://github.com/laramies/theHarvester 12. SpiderFoot automates OSINT for threat intelligence and mapping your attack surface. - GitHub, https://github.com/smicallef/spiderfoot 13. OSINT TOOLKIT: SPIDERFOOT, A CYBER-FOCUSED GITHUB TOOL THAT AUTOMATES DATA COLLECTION AND MAPS DIGITAL FOOTPRINTS - The Counterterrorism Group, https://www.counterterrorismgroup.com/post/osint-toolkit-spiderfoot-a-cyber-focused-github-tool-that-automates-data-collection-and-maps-digit 14. The Ultimate List of Top 10 OSINT Tools in 2025 - ExamCollection, https://www.examcollection.com/blog/the-ultimate-list-of-top-10-osint-tools-in-2025/ 15. Top 10 Open Source ASM Software Based on GitHub Stars - AIMultiple, https://aimultiple.com/open-source-asm 16. owasp-amass/amass: In-depth attack surface mapping and asset discovery - GitHub, https://github.com/owasp-amass/amass 17. lanmaster53/recon-ng: Open Source Intelligence gathering tool aimed at reducing the time spent harvesting information from open sources. - GitHub, https://github.com/lanmaster53/recon-ng 18. rxerium/stars: A list of all of my starred repos, automated using Github Actions, https://github.com/rxerium/stars 19. sherlock-project/sherlock: Hunt down social media accounts by username across social networks - GitHub, https://github.com/sherlock-project/sherlock 20. maigret/README.md at main - GitHub, https://github.com/soxoj/maigret/blob/main/README.md 21. Soxoj - GitHub, https://github.com/soxoj 22. p1ngul1n0/blackbird: An OSINT tool to search for accounts by username and email in social networks. - GitHub, https://github.com/p1ngul1n0/blackbird 23. OSINT TOOLKIT: BLACKBIRD, A PYTHON-BASED TOOL THAT INVESTIGATES USERNAMES TO MAP A TARGET'S DIGITAL FOOTPRINT ACROSS SOCIAL MEDIA PLATFORMS - The Counterterrorism Group, https://www.counterterrorismgroup.com/post/osint-toolkit-blackbird-a-python-based-tool-that-investigates-usernames-to-map-a-target-s-digital 24. WebBreacher/WhatsMyName: This repository has the JSON file required to perform user enumeration on various websites. - GitHub, https://github.com/WebBreacher/WhatsMyName 25. The Best Open Source Intelligence Tools in 2026 - YouTube, https://www.youtube.com/watch?v=V10Q_t7Gdho 26. holehe allows you to check if the mail is used on different sites like twitter, instagram and will retrieve information on sites with the forgotten password function. - GitHub, https://github.com/megadose/holehe 27. sundowndev/phoneinfoga: Information gathering framework for phone numbers - GitHub, https://github.com/sundowndev/phoneinfoga 28. FOGSEC/PhoneInfoga: Information gathering & OSINT reconnaissance tool for phone numbers - GitHub, https://github.com/FOGSEC/PhoneInfoga 29. GitHub Search API: Get the number of stars for a repository - GitHub Gist, https://gist.github.com/jasonrudolph/6057563 30. What Is the OSINT Framework? Tools, Uses & Benefits - ShadowDragon.io, https://shadowdragon.io/blog/what-is-the-osint-framework/ 31. Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more - GitHub, https://github.com/megadose/toutatis 32. osintgram · GitHub Topics, https://github.com/topics/osintgram?l=python&o=asc&s=stars 33. Osintgram is a OSINT tool on Instagram. It offers an interactive shell to perform analysis on Instagram account of any users by its nickname - GitHub, https://github.com/Datalux/Osintgram 34. The Best Open Source Intelligence Tools in 2026 - Frank's World of Data Science & AI, https://www.franksworld.com/2026/01/28/the-best-open-source-intelligence-tools-in-2026/ 35. OSINT TOOLKIT: MARINETRAFFIC, A REAL-TIME VESSEL TRACKING TOOL THAT ENHANCES MARITIME SECURITY AND VERIFIES NAVAL OPERATIONS DURING CRITICAL SITUATIONS - The Counterterrorism Group, https://www.counterterrorismgroup.com/post/osint-toolkit-marinetraffic-a-real-time-vessel-tracking-tool-that-enhances-maritime-security-and-v 36. osint-reconnaissance · GitHub Topics, https://github.com/topics/osint-reconnaissance?o=desc&s=stars 37. ClatScope Info Tool – The best and most versatile OSINT utility for retrieving geolocation, DNS, WHOIS, phone, email, data breach information and much more (70+ features). Perfect for investigators, pentesters, or anyone looking for an effective reconnaissance / OSINT tool. - GitHub, https://github.com/Clats97/ClatScope
