"""Complementos al roadmap del PDF.

Nada de esto viene del documento original: son huecos que quedan abiertos si
sigues el plan al pie de la letra —herramientas que las vacantes piden y el PDF
no menciona, la parte de portafolio, y el trámite real de la salida a Australia
o Canadá—. Todo queda marcado como `generado=True`, así que puedes revisarlo
aparte y borrarlo entero con `--quitar` si no te sirve.

Los plazos y requisitos de visa son orientativos y cambian: confírmalos siempre
en las fuentes oficiales de cada país.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from roadmap.models import Etapa, Item

C, L, E, N = Item.Tipo.CURSO, Item.Tipo.LIBRO, Item.Tipo.ENTREGABLE, Item.Tipo.NOTA

# Items que se enganchan a etapas que ya existen, por número de orden.
EXTRAS_POR_ETAPA = {
    0: [
        (
            C,
            "Introducción a Terminal y Línea de Comandos",
            "Platzi",
            "Dominio básico de shell (bash/zsh), variables de entorno y scripts de automatización simples.",
            "Terminal",
        ),
        (
            C,
            "Curso de Introducción a Linux y Bash Shell",
            "Platzi",
            "Nivelación en comandos de consola, gestión de procesos y permisos.",
            "Linux",
        ),
        (
            C,
            "Estructuras de Datos y Algoritmos con Python",
            "Platzi",
            "Conceptos esenciales de Big O, listas ligadas, pilas y colas indispensables para entrevistas técnicas.",
            "Algoritmos",
        ),
        (
            C,
            "Python para Data Science y Analytics",
            "Udemy",
            "Buenas prácticas en Python, virtual environments, pip/poetry.",
            "Python",
        ),
        (
            C,
            "Introducción a Docker y Contenedores",
            "Platzi",
            "Entender la teoría básica detrás del aislamiento de procesos y sistemas de archivos antes de meterse con docker-compose.",
            "Docker",
        ),
        (
            C,
            "SQL avanzado: window functions, CTEs y planes de ejecución",
            "Práctica propia",
            "El bootcamp de Portilla llega hasta joins y agregación. Lo que "
            "realmente te van a preguntar en entrevista son window functions "
            "(LAG, LEAD, ROW_NUMBER) para calcular tiempo entre fallas y "
            "horómetros acumulados. Practícalo sobre tu propia base.",
            "Hueco",
        ),
        (
            E,
            "Diccionario de datos de tu operación",
            "",
            "Documenta en el repo qué significa cada tabla y cada campo: qué es "
            "un horómetro, qué cuenta como falla, qué estados tiene una orden de "
            "trabajo. Es lo que te va a diferenciar de cualquier candidato "
            "genérico, y lo escribes una sola vez.",
            "",
        ),
        (
            L,
            "Clean Code",
            "Robert C. Martin",
            "El libro de referencia para aprender a escribir código legible, estructurado y profesional.",
            "Programación",
            True,
        ),
        (
            L,
            "Fundamentals of Data Engineering",
            "Joe Reis y Matt Housley",
            "El mapa completo del oficio antes de meterte en herramientas "
            "sueltas. Léelo en paralelo a la etapa 1 y sabrás por qué existe "
            "cada pieza que vas a instalar.",
            "Referencia",
            True,
        ),
        (
            L,
            "Python Crash Course",
            "Eric Matthes",
            "Dominio práctico de Python orientado a proyectos reales.",
            "Python",
            True,
        ),
        (
            L,
            "The Pragmatic Programmer",
            "Andrew Hunt y David Thomas",
            "Filosofía fundamental del desarrollo de software y artesanía de código.",
            "Carrera",
            True,
        ),
        (
            L,
            "Make It Stick: The Science of Successful Learning",
            "Peter C. Brown",
            "Estrategias de aprendizaje eficaz basadas en ciencia cognitiva.",
            "Aprendizaje",
            True,
        ),
        (
            L,
            "Mindset: La psicología del éxito",
            "Carol S. Dweck",
            "Mentalidad de crecimiento indispensable para transformarte profesionalmente.",
            "Psicología",
            False,
        ),
    ],
    1: [
        (
            C,
            "Arquitectura Medallion en Delta Lake",
            "Databricks Academy",
            "Estándar de diseño de almacenamiento estructurado (capas Bronze, Silver y Gold) óptimo para telemetría industrial.",
            "Delta Lake",
        ),
        (
            C,
            "Fundamentos de Lakehouse con Apache Iceberg",
            "Udemy",
            "Apache Iceberg como alternativa moderna a Delta Lake para optimizar el rendimiento de consultas analíticas a gran escala.",
            "Iceberg",
        ),
        (
            C,
            "Orquestación Moderna: Prefect y Dagster",
            "Documentación oficial",
            "Alternativas contemporáneas a Airflow enfocadas en tipado de datos y desarrollo local rápido.",
            "Orquestadores",
        ),
        (
            C,
            "Apache Kafka: Fundamentos y Arquitectura",
            "Platzi",
            "Conceptos básicos de mensajería asíncrona, productores, consumidores y diseño de tópicos streaming.",
            "Streaming",
        ),
        (
            C,
            "Modelado de Datos Dimensionales (Kimball)",
            "Udemy",
            "Técnicas de modelado dimensional (hechos y dimensiones) necesarias para diseñar almacenes analíticos sólidos.",
            "Modelado",
        ),
        (
            C,
            "Data Warehousing con Snowflake y BigQuery",
            "Udemy",
            "Diseño de almacenes de datos analíticos en la nube para petabytes de datos.",
            "Cloud DW",
        ),
        (
            C,
            "PySpark Avanzado para Data Engineering",
            "Udemy",
            "Optimizaciones de Spark, particionamiento y shuffles en clusters grandes.",
            "Spark",
        ),
        (
            C,
            "Docker Compose y GitHub Actions",
            "Documentación oficial",
            "Docker solo no alcanza: tu pipeline va a ser Airflow + Postgres + "
            "dbt corriendo juntos, y eso es Compose. Súmale un CI en Actions que "
            "corra los tests de dbt en cada push; sale en una tarde y aparece en "
            "toda vacante.",
            "Hueco",
        ),
        (
            C,
            "Calidad de datos: tests en dbt y Great Expectations",
            "Documentación oficial",
            "La telemetría de mina llega sucia por defecto. Saber declarar "
            "expectativas (este horómetro nunca decrece, este sensor no reporta "
            "-999) es lo que separa un pipeline de juguete de uno de producción.",
            "Hueco",
        ),
        (
            E,
            "README del pipeline con diagrama de arquitectura",
            "",
            "Un diagrama y veinte líneas explicando decisiones: por qué Postgres "
            "y no un data lake, por qué corre diario y no cada hora. Quien revise "
            "tu repo en una selección lee esto y nada más.",
            "",
        ),
        (
            L,
            "Designing Data-Intensive Applications",
            "Martin Kleppmann",
            "El libro técnico de referencia del área. Denso: no lo leas de "
            "corrido, usa los capítulos de almacenamiento y replicación como "
            "consulta mientras construyes el pipeline.",
            "Referencia",
            True,
        ),
        (
            L,
            "Data Pipelines Pocket Reference",
            "James Densmore",
            "Guía práctica con patrones comunes para construir, monitorear y orquestar pipelines de datos en producción.",
            "Pipelines",
            True,
        ),
        (
            L,
            "Building Data Pipelines with Python",
            "Bas P. van Beek",
            "Arquitectura de datos mantenible y patrones de pipelines con Python.",
            "Pipelines",
            True,
        ),
        (
            L,
            "Data Engineering with AWS",
            "Gareth Eagar",
            "Construcción de soluciones de datos escalables en la nube de AWS.",
            "AWS",
            True,
        ),
        (
            L,
            "Database Internals",
            "Alex Petrov",
            "Estructuras de almacenamiento, árboles B+, WAL y motores de bases de datos.",
            "Bases de Datos",
            True,
        ),
        (
            L,
            "Streaming Systems",
            "Tyler Akidau",
            "Modelos de procesamiento de eventos en tiempo real y semantics exactas.",
            "Streaming",
            True,
        ),
    ],
    2: [
        (
            C,
            "Procesamiento de Señales para Mantenimiento Predictivo",
            "Udemy",
            "Análisis espectral y transformadas rápidas de Fourier (FFT) para interpretar vibraciones de motores y rodamientos.",
            "Sensores",
        ),
        (
            C,
            "Modelos de Supervivencia para Confiabilidad",
            "Udemy",
            "Uso de curvas de Kaplan-Meier y modelos de Cox para estimar el tiempo restante hasta la falla (RUL) de un equipo industrial.",
            "Mantenimiento",
        ),
        (
            C,
            "Kubeflow para ML Pipelines Industriales",
            "Udemy",
            "Diseño y orquestación de flujos de trabajo de Machine Learning robustos sobre Kubernetes.",
            "MLOps",
        ),
        (
            C,
            "Álgebra Lineal y Cálculo para Machine Learning",
            "Platzi",
            "Las bases matemáticas del descenso de gradiente y algoritmos de optimización.",
            "Matemáticas",
        ),
        (
            C,
            "Machine Learning Interpretability con Python",
            "Udemy",
            "Uso de SHAP y LIME para explicar decisiones del modelo de falla a los mecánicos y operadores.",
            "Explicabilidad",
        ),
        (
            C,
            "Time Series Analysis con Prophet y ARIMA",
            "Udemy",
            "Descomposición de tendencia, estacionalidad y pronóstico para sensores.",
            "Series de Tiempo",
        ),
        (
            C,
            "Feature Engineering Avanzado en Datos Tabulares",
            "Udemy",
            "Encodings, transformaciones Box-Cox y selección de características.",
            "Feature Eng.",
        ),
        (
            C,
            "Seguimiento de experimentos con MLflow",
            "Documentación oficial",
            "El curso de MLOps de Platzi lo toca por encima. Si vas a defender un "
            "modelo que manda a parar un equipo, necesitas poder mostrar qué "
            "probaste y por qué elegiste eso.",
            "Hueco",
        ),
        (
            N,
            "Valida en el tiempo, nunca al azar",
            "",
            "El error más común en mantenimiento predictivo: hacer train/test "
            "aleatorio sobre datos temporales. Filtras el futuro al pasado y el "
            "modelo se ver perfecto hasta que llega a producción. Corta siempre "
            "por fecha.",
            "Ojo",
        ),
        (
            E,
            "Traducir el modelo a dinero",
            "",
            "Una tabla que compare el costo de un falso positivo (parada "
            "innecesaria) contra el de un falso negativo (falla en operación). "
            "Con eso eliges el umbral del modelo con criterio de negocio y no por "
            "F1. Es la conversación que tiene un ingeniero senior y no un junior.",
            "",
        ),
        (
            L,
            "Reliability-Centered Maintenance",
            "John Moubray",
            "Tu dominio escrito con rigor. Te da el vocabulario formal —modos de "
            "falla, criticidad, patrones de vida— para hablar con confiabilidad y "
            "con datos en la misma frase. Es la ventaja que ningún data scientist "
            "de bootcamp tiene.",
            "Dominio",
            True,
        ),
        (
            L,
            "An Introduction to Statistical Learning",
            "Gareth James et al.",
            "Rigor matemático claro y accesible aplicado a regresión, clasificación y árboles de decisión.",
            "Estadística",
            True,
        ),
        (
            L,
            "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow",
            "Aurélien Géron",
            "La guía práctica indispensable para machine learning y redes neuronales.",
            "Machine Learning",
            True,
        ),
        (
            L,
            "Forecasting: Principles and Practice",
            "Rob J Hyndman y George Athanasopoulos",
            "El manual de referencia mundial para predicción de series temporales.",
            "Series de Tiempo",
            True,
        ),
        (
            L,
            "Feature Engineering and Selection",
            "Max Kuhn y Kjell Johnson",
            "Metodologías rigurosas para la preparación de datos predictivos.",
            "Feature Eng.",
            True,
        ),
        (
            L,
            "Python Data Science Handbook",
            "Jake VanderPlas",
            "Manual completo de NumPy, Pandas, Matplotlib y Scikit-Learn.",
            "Data Science",
            True,
        ),
    ],
    3: [
        (
            C,
            "RAG Local con Ollama y Llama 3",
            "Práctica propia",
            "Despliegue local y seguro de modelos de lenguaje privado para operaciones remotas mineras sin acceso directo a internet.",
            "Local AI",
        ),
        (
            C,
            "Inferencia de LLMs Optimizada: vLLM y Hugging Face TGI",
            "Práctica propia",
            "Uso de motores de inferencia optimizados para servir LLMs open-source de forma veloz y rentable.",
            "Inferencia",
        ),
        (
            C,
            "Agentes Autónomos con CrewAI y AutoGen",
            "Udemy",
            "Orquestación de múltiples agentes trabajando coordinados para resolver tareas de diagnóstico complejas.",
            "Agentes",
        ),
        (
            C,
            "Fine-Tuning de LLMs con LoRA y Unsloth",
            "Udemy",
            "Ajuste fino eficiente de modelos Llama 3 y Mistral en hardware local.",
            "Fine-Tuning",
        ),
        (
            C,
            "Bases de Datos Vectoriales: Qdrant y ChromaDB",
            "Platzi",
            "Indexación HNSW, métricas de similitud y filtrado híbrido.",
            "Vector DB",
        ),
        (
            C,
            "pgvector: embeddings dentro de Postgres",
            "Documentación oficial",
            "No necesitas una base vectorial aparte para tu RAG de manuales. "
            "pgvector vive en el Postgres que ya montaste en la etapa 0 y te "
            "ahorra un servicio entero.",
            "Hueco",
        ),
        (
            C,
            "Evaluación de sistemas RAG",
            "RAGAS / documentación",
            "Un RAG que nadie midió es una demo. Aprende a armar un set de "
            "preguntas con respuesta conocida sobre tus manuales y a medir "
            "fidelidad y relevancia. Sin esto no lo puedes vender a tu empresa.",
            "Hueco",
        ),
        (
            N,
            "Cuida el costo por consulta",
            "",
            "Calcula qué cuesta cada pregunta al agente antes de mostrárselo a un "
            "jefe. Un RAG que responde bien pero cuesta dos dólares por consulta "
            "no se implementa en ninguna operación.",
            "Ojo",
        ),
        (
            L,
            "Building LLM Apps",
            "Valentina Alto",
            "Construcción de aplicaciones reales impulsadas por modelos de lenguaje grande.",
            "LLMs",
            True,
        ),
        (
            L,
            "Generative AI on AWS",
            "Chris Fregly y Antje Barth",
            "Implementación y escalado de IA generativa corporativa.",
            "Generative AI",
            True,
        ),
        (
            L,
            "Designing Autonomous AI Agents",
            "Harrison Chase",
            "Patrones de arquitectura para agentes autónomos y sistemas multi-agente.",
            "Agentes",
            True,
        ),
        (
            L,
            "AI Engineering: Building Applications with Foundation Models",
            "Chip Huyen",
            "Ingeniería de software adaptada a sistemas deterministas y estocásticos con LLMs.",
            "AI Engineering",
            True,
        ),
    ],
    4: [
        (
            C,
            "Inglés Técnico para Entrevistas de Data & AI",
            "Platzi",
            "Simulación de entrevistas técnicas, pitch personal y storytelling en inglés.",
            "Inglés",
        ),
        (
            C,
            "Preparación Intensiva para IELTS General & Academic 7.0+",
            "Udemy",
            "Estrategias específicas para Listening, Reading, Writing y Speaking.",
            "IELTS",
        ),
        (
            E,
            "Simulacro de IELTS Academic cada dos meses",
            "",
            "Medir desde temprano, aunque duela: necesitas saber tu banda real "
            "antes de que el trámite dependa de ella. Australia y Canadá suelen "
            "pedir entre 6.0 y 7.0 por sección según el programa.",
            "Inglés",
        ),
        (
            N,
            "Habla, no solo leas",
            "",
            "El speaking es la sección donde más gente se cae, y leer libros no "
            "la mueve. Media hora semanal de conversación real vale más que tres "
            "horas de app.",
            "Inglés",
        ),
        (
            L,
            "Never Split the Difference",
            "Chris Voss",
            "Negociación táctica de ofertas laborales y salarios internacionales.",
            "Negociación",
            True,
        ),
        (
            L,
            "The Hard Thing About Hard Things",
            "Ben Horowitz",
            "Gestión de la incertidumbre y la resiliencia en situaciones difíciles.",
            "Liderazgo",
            True,
        ),
        (
            L,
            "Essentialism: The Disciplined Pursuit of Less",
            "Greg McKeown",
            "Enfoque deliberado en lo verdaderamente esencial para lograr objetivos elevados.",
            "Productividad",
            True,
        ),
        (
            L,
            "The Personal MBA",
            "Josh Kaufman",
            "Conceptos clave de negocios, finanzas y estrategia comercial.",
            "Negocios",
            True,
        ),
        (
            L,
            "Crucial Conversations",
            "Kerry Patterson",
            "Habilidades de comunicación para escenarios de alta presión o conflicto.",
            "Comunicación",
            True,
        ),
    ],
}

# Etapas nuevas al final del recorrido.
ETAPAS_NUEVAS = [
    {
        "orden": 5,
        "kicker": "Etapa 5 · generada",
        "titulo": "Portafolio y visibilidad",
        "subtitulo": "Que lo construido se vea",
        "duracion": "En paralelo · últimos 6 meses",
        "horas": "~40 horas",
        "color": "#b5543f",
        "objetivo": (
            "Los cuatro entregables del plan no sirven de nada si viven en tu "
            "disco. Esta etapa es el trabajo de hacerlos legibles para alguien "
            "que te dedica cinco minutos."
        ),
        "items": [
            (
                E,
                "Tres repos públicos pulidos, no diez a medias",
                "",
                "El pipeline de la etapa 1, el modelo de la 2 y el RAG de la 3. "
                "Cada uno con README, diagrama, instrucciones para correrlo y "
                "datos de ejemplo anonimizados.",
                "",
            ),
            (
                E,
                "Un caso de estudio escrito de punta a punta",
                "",
                "Problema real de la operación, qué construiste, qué resultado dio "
                "en horas de parada o costo evitado. Dos páginas. Esto es lo que "
                "mandas cuando alguien pregunta qué sabes hacer.",
                "",
            ),
            (
                C,
                "Perfil de LinkedIn en inglés, orientado al rol destino",
                "Trabajo propio",
                "Titular como «Data Engineer · Predictive Maintenance in Mining», "
                "no como tu cargo actual. Reescríbelo al terminar la etapa 1, no "
                "al final de todo.",
                "",
            ),
            (
                C,
                "CV en formato del país destino",
                "Trabajo propio",
                "Canadá y Australia usan convenciones distintas a las "
                "latinoamericanas: sin foto, sin edad, sin estado civil, con "
                "logros cuantificados. Un CV mal formateado te filtra antes de "
                "que alguien lea tu experiencia.",
                "",
            ),
            (
                C,
                "Creación de Portafolios Técnicos y GitHub Showcase",
                "Platzi",
                "Estructuración de repositorios profesionales y documentación atractiva.",
                "Portafolio",
            ),
            (
                C,
                "Storytelling con Datos para Ejecutivos",
                "Udemy",
                "Presentación de resultados técnicos y métricas financieras de impacto.",
                "Storytelling",
            ),
            (
                N,
                "Escribe cuatro artículos, uno por etapa",
                "",
                "Publicar lo que aprendiste obliga a entenderlo y deja rastro "
                "público. Escribir sobre datos de mantenimiento minero te pone en "
                "un nicho donde casi nadie escribe.",
                "",
            ),
            (
                L,
                "Storytelling with Data",
                "Cole Nussbaumer Knaflic",
                "Cómo presentar un hallazgo para que una gerencia lo entienda y "
                "actúe. Aplica igual a tu tablero de Power BI que a la entrevista "
                "donde defiendas tu capstone.",
                "Comunicación",
                True,
            ),
            (
                L,
                "Show Your Work!",
                "Austin Kleon",
                "10 maneras de compartir tu creatividad y hacerte descubrir.",
                "Carrera",
                True,
            ),
            (
                L,
                "The Tech Resume Inside Out",
                "Gergely Orosz",
                "Cómo escribir un currículum de ingeniería que supere filtros de selección.",
                "Carrera",
                True,
            ),
            (
                L,
                "Cracking the Coding Interview",
                "Gayle Laakmann McDowell",
                "Preparación exhaustiva para problemas de código y entrevistas técnicas.",
                "Entrevistas",
                True,
            ),
        ],
    },
    {
        "orden": 6,
        "kicker": "Etapa 6 · generada",
        "titulo": "La salida",
        "subtitulo": "Trámite y búsqueda",
        "duracion": "Últimos 4–6 meses",
        "horas": "Variable",
        "color": "#2f6d6a",
        "objetivo": (
            "El plan técnico termina en la etapa 3, pero mudarse no. Esta parte "
            "tiene tiempos propios, largos y burocráticos, y conviene arrancarla "
            "antes de terminar los cursos."
        ),
        "items": [
            (
                E,
                "IELTS Academic rendido de verdad",
                "",
                "No el simulacro: el examen oficial, con resultado en mano. Es el "
                "insumo que bloquea todo lo demás del trámite.",
                "",
            ),
            (
                E,
                "Evaluación de credenciales iniciada",
                "",
                "Canadá pide un ECA (WES es el más usado) y Australia una "
                "evaluación de Engineers Australia para perfiles de ingeniería. "
                "Ambas tardan meses: empieza mientras estudias, no después.",
                "",
            ),
            (
                N,
                "Verifica todo en las fuentes oficiales",
                "",
                "Los requisitos de Express Entry y de SkillSelect cambian seguido, "
                "igual que los puntajes de corte y las ocupaciones en demanda. "
                "Nada de lo que diga esta app —ni ningún blog— sustituye a "
                "canada.ca y a immi.homeaffairs.gov.au.",
                "Ojo",
            ),
            (
                C,
                "Preparación de entrevista técnica",
                "Práctica propia",
                "SQL en vivo, diseño de pipelines y preguntas de caso. Además, "
                "ensaya en inglés la historia de por qué un ingeniero de "
                "mantenimiento pasa a datos: la vas a contar en cada entrevista y "
                "es tu mejor carta.",
                "",
            ),
            (
                C,
                "Guía Práctica Skilled Migration Australia (Subclass 189/190)",
                "Oficial",
                "Cálculo de puntos EOI y proceso con Engineers Australia / ACS.",
                "Australia",
            ),
            (
                C,
                "Guía Práctica Express Entry Canadá & PNP",
                "Oficial",
                "Sistema CRS, perfiles de entrada rápida y programas provinciales.",
                "Canadá",
            ),
            (
                E,
                "Un objetivo semanal de aplicaciones, sostenido",
                "",
                "La búsqueda es un embudo con tasas de conversión bajas, no una "
                "lotería. Cinco postulaciones bien dirigidas por semana durante "
                "tres meses vencen a cincuenta disparadas en un fin de semana.",
                "",
            ),
            (
                N,
                "Apunta al nicho, no al puesto genérico",
                "",
                "Mining analytics, asset performance management, industrial IoT. "
                "Compites contra cientos en «data engineer» y contra pocos en "
                "«data engineer que entendió una orden de trabajo».",
                "",
            ),
            (
                L,
                "The Culture Map",
                "Erin Meyer",
                "Navegar las diferencias culturales en negocios y entornos globales.",
                "Cultura",
                True,
            ),
            (
                L,
                "The Express Entry & Overseas Career Guide",
                "Immigration Experts",
                "Planificación de relocalización internacional paso a paso.",
                "Inmigración",
                True,
            ),
            (
                L,
                "Getting to Yes",
                "Roger Fisher y William Ury",
                "Principios de negociación ganar-ganar para ofertas de trabajo globales.",
                "Negociación",
                True,
            ),
        ],
    },
    {
        "orden": 7,
        "kicker": "Etapa 7 · generada",
        "titulo": "IoT Industrial y Cloud Data (Edge & Streaming)",
        "subtitulo": "Sensores en tiempo real",
        "duracion": "3 meses",
        "horas": "~60 horas",
        "color": "#3f7db5",
        "objetivo": (
            "Aprender a conectar telemetría en tiempo real desde sensores (SCADA, PLC) "
            "usando protocolos industriales y procesando el flujo en la nube."
        ),
        "items": [
            (
                C,
                "Arquitectura IoT: Ingesta con MQTT y Apache Kafka",
                "Udemy / Documentación oficial",
                "Los sensores de los camiones y plantas concentradoras transmiten por "
                "MQTT o Modbus. Kafka es la espina dorsal para recibir miles de eventos "
                "por segundo sin saturar tu base de datos.",
                "Streaming",
            ),
            (
                C,
                "Procesamiento de Flujos en Tiempo Real con Apache Flink",
                "Udemy",
                "Ingesta y análisis de eventos de telemetría en streaming con ventanas de tiempo avanzadas y joins complejos.",
                "Flink",
            ),
            (
                C,
                "TimescaleDB: PostgreSQL optimizado para series de tiempo",
                "Documentación oficial",
                "TimescaleDB convierte tu Postgres en una base hiper-rápida para millones de métricas por segundo de horómetros y presiones.",
                "Timescale",
            ),
            (
                C,
                "Monitoreo Industrial con Grafana y Prometheus",
                "Documentación oficial",
                "Creación de tableros de alertas en tiempo real y métricas del estado operacional de servidores y nodos de ingesta.",
                "Monitoreo",
            ),
            (
                C,
                "OPC-UA y Protocolos Industriales para Data Engineers",
                "Udemy",
                "Conexión directa a PLCs y sistemas SCADA de planta.",
                "IoT",
            ),
            (
                C,
                "Arquitectura de Sistemas Tolerantes a Fallos en la Nube",
                "Udemy",
                "Diseño de infraestructura crítica de alta disponibilidad.",
                "Arquitectura",
            ),
            (
                E,
                "Dashboard SCADA en tiempo real conectado a sensor IoT sim",
                "",
                "Pipeline de streaming que recibe telemetría simulada de camión minero, procesa anomalías en Flink y grafica en Grafana con alertas.",
                "",
            ),
            (
                E,
                "Ingesta resiliente ante pérdida de conectividad en mina",
                "",
                "Diseño de almacenamiento buffer local en el equipo (Edge) que re-sincroniza automáticamente los datos al recuperar señal Wi-Fi/4G.",
                "",
            ),
            (
                N,
                "Telemetría fallida != equipo fallado",
                "",
                "Aprende a diferenciar cuándo un sensor dejó de transmitir vs. cuándo el equipo realmente se detuvo. Es el error clásico en IoT minero.",
                "Ojo",
            ),
            (
                L,
                "Designing Connected Products",
                "Claire Rowland",
                "Diseño de productos conectados e infraestructuras IoT.",
                "IoT",
                True,
            ),
            (
                L,
                "Site Reliability Engineering (SRE)",
                "Betsy Beyer et al.",
                "Prácticas de confiabilidad y operación de sistemas a gran escala.",
                "SRE",
                True,
            ),
            (
                L,
                "Building Microservices",
                "Sam Newman",
                "Diseño y modelado de microservicios acoplados libremente.",
                "Arquitectura",
                True,
            ),
            (
                L,
                "Industrial IoT Architectures and Protocols",
                "Alasdair Gilchrist",
                "Integración de redes de tecnología operativa (OT) e IT en minería e industria.",
                "IoT",
                True,
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Carga etapas e items complementarios (generado=True) que no vienen en el PDF."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quitar",
            action="store_true",
            help="Borra todos los items y etapas extras generados por este comando.",
        )

    @transaction.atomic
    def handle(self, *args, **opciones):
        if opciones["quitar"]:
            borrados_i, _ = Item.objects.filter(generado=True).delete()
            borrados_e, _ = Etapa.objects.filter(
                orden__in=[e["orden"] for e in ETAPAS_NUEVAS]
            ).delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Eliminados {borrados_i} items extras y {borrados_e} etapas nuevas."
                )
            )
            return

        # 1. Crear etapas nuevas si no existen
        for datos in ETAPAS_NUEVAS:
            items = datos.pop("items")
            etapa, _ = Etapa.objects.update_or_create(
                orden=datos["orden"], defaults=datos
            )
            datos["items"] = items

            for i, fila in enumerate(items):
                tipo, titulo, fuente, detalle, etiqueta = fila[:5]
                en_ingles = fila[5] if len(fila) > 5 else False
                Item.objects.get_or_create(
                    etapa=etapa,
                    titulo=titulo,
                    defaults={
                        "tipo": tipo,
                        "fuente": fuente,
                        "detalle": detalle,
                        "etiqueta": etiqueta,
                        "en_ingles": en_ingles,
                        "generado": True,
                        "orden": i,
                    },
                )

        # 2. Agregar items extras a etapas que ya existían
        nuevos_items = 0
        for orden_etapa, items in EXTRAS_POR_ETAPA.items():
            try:
                etapa = Etapa.objects.get(orden=orden_etapa)
            except Etapa.DoesNotExist:
                continue

            base_orden = (
                etapa.items.order_by("-orden").values_with_type("orden").first()
                if hasattr(etapa.items, "values_with_type")
                else 0
            )
            ultimo = etapa.items.order_by("-orden").first()
            base_orden = (ultimo.orden + 1) if ultimo else 0

            for offset, fila in enumerate(items):
                tipo, titulo, fuente, detalle, etiqueta = fila[:5]
                en_ingles = fila[5] if len(fila) > 5 else False
                _, creado = Item.objects.get_or_create(
                    etapa=etapa,
                    titulo=titulo,
                    defaults={
                        "tipo": tipo,
                        "fuente": fuente,
                        "detalle": detalle,
                        "etiqueta": etiqueta,
                        "en_ingles": en_ingles,
                        "generado": True,
                        "orden": base_orden + offset,
                    },
                )
                nuevos_items += creado

        total_etapas = Etapa.objects.count()
        total_items = Item.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Contenido complementario listo: {nuevos_items} items nuevos. "
                f"Total ahora: {total_items} items en {total_etapas} etapas."
            )
        )
