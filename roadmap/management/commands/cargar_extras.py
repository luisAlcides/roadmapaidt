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
        (C, "Introducción a Terminal y Línea de Comandos", "Platzi", "Dominio básico de shell (bash/zsh), variables de entorno y scripts de automatización simples.", "Terminal"),
        (C, "Curso de Introducción a Linux y Bash Shell", "Platzi", "Nivelación en comandos de consola, gestión de procesos y permisos.", "Linux"),
        (C, "Estructuras de Datos y Algoritmos con Python", "Platzi", "Conceptos esenciales de Big O, listas ligadas, pilas y colas indispensables para entrevistas técnicas.", "Algoritmos"),
        (C, "Python para Data Science y Analytics", "Udemy", "Buenas prácticas en Python, virtual environments, pip/poetry.", "Python"),
        (C, "Introducción a Docker y Contenedores", "Platzi", "Entender la teoría básica detrás del aislamiento de procesos y sistemas de archivos antes de meterse con docker-compose.", "Docker"),
        (C, "SQL avanzado: window functions, CTEs y planes de ejecución", "Práctica propia", "Window functions (LAG, LEAD, ROW_NUMBER) para calcular tiempo entre fallas y horómetros acumulados.", "Hueco"),
        (E, "Diccionario de datos de tu operación", "", "Documenta en el repo qué significa cada tabla y cada campo de tu operación.", ""),

        # Libros Etapa 0 (25 libros)
        (L, "Clean Code", "Robert C. Martin", "El libro de referencia para aprender a escribir código legible, estructurado y profesional.", "Programación", True),
        (L, "Fundamentals of Data Engineering", "Joe Reis y Matt Housley", "El mapa completo del oficio antes de meterte en herramientas sueltas.", "Referencia", True),
        (L, "Python Crash Course", "Eric Matthes", "Dominio práctico de Python orientado a proyectos reales.", "Python", True),
        (L, "The Pragmatic Programmer", "Andrew Hunt y David Thomas", "Filosofía fundamental del desarrollo de software y artesanía de código.", "Carrera", True),
        (L, "Grokking Algorithms", "Aditya Bhargava", "Una guía ilustrada para entender algoritmos complejos de manera intuitiva.", "Algoritmos", True),
        (L, "Code: The Hidden Language of Computer Hardware and Software", "Charles Petzold", "Cómo se conectan el hardware y el software desde puertas lógicas básicas.", "Computación", True),
        (L, "Structure and Interpretation of Computer Programs", "Harold Abelson", "Fundamentos profundos de abstracción en ciencias de la computación.", "Computación", True),
        (L, "The Linux Command Line", "William Shotts", "Guía exhaustiva para dominar la línea de comandos de Linux.", "Linux", True),
        (L, "Make It Stick: The Science of Successful Learning", "Peter C. Brown", "Estrategias de aprendizaje eficaz basadas en ciencia cognitiva.", "Aprendizaje", True),
        (L, "Mindset: La psicología del éxito", "Carol S. Dweck", "Mentalidad de crecimiento indispensable para transformarte profesionalmente.", "Psicología", False),
        (L, "El gen egoísta", "Richard Dawkins", "Una perspectiva biológica revolucionaria sobre la evolución y el comportamiento.", "Ciencia", True),
        (L, "El universo elegante", "Brian Greene", "Supercuerdas, dimensiones ocultas y la búsqueda de la teoría definitiva en física.", "Física", True),
        (L, "Sapiens: De animales a dioses", "Yuval Noah Harari", "Breve historia de la humanidad y las revoluciones que moldearon la sociedad.", "Historia", True),
        (L, "Discurso del método", "René Descartes", "La base del pensamiento racionalista y el método científico moderno.", "Filosofía", True),
        (L, "Cartas a Lucilio", "Séneca", "Consejos de estoicismo práctico para mantener la templanza en la vida diaria.", "Filosofía", True),
        (L, "Manual para la vida", "Epicteto", "Enseñanzas sobre lo que está bajo nuestro control y lo que debemos aceptar.", "Filosofía", True),
        (L, "Ética a Nicómaco", "Aristóteles", "La búsqueda de la virtud, la justicia y la eudaimonía (plenitud).", "Filosofía", True),
        (L, "La república", "Platón", "Diálogo sobre la justicia, la educación, la política y la alegoría de la caverna.", "Filosofía", True),
        (L, "Ensayo sobre el entendimiento humano", "John Locke", "Origen y límites del conocimiento humano desde el empirismo.", "Filosofía", True),
        (L, "Don Quijote de la Mancha", "Miguel de Cervantes", "Obra cumbre de la literatura en español sobre el idealismo y la realidad.", "Literatura", True),
        (L, "Cien años de soledad", "Gabriel García Márquez", "Obra maestra del realismo mágico e historia de la familia Buendía.", "Literatura", True),
        (L, "El príncipe", "Nicolás Maquiavelo", "Tratado clásico sobre la política, el poder y la estrategia de estado.", "Historia", True),
        (L, "1984", "George Orwell", "Novela distópica sobre el totalitarismo, la vigilancia y la manipulación de la verdad.", "Literatura", True),
        (L, "Fahrenheit 451", "Ray Bradbury", "Una crítica sobre la censura, el conocimiento y el valor de los libros.", "Literatura", True),
        (L, "Un mundo feliz", "Aldous Huxley", "Reflexión sobre una sociedad condicionada tecnológicamente al placer superficial.", "Literatura", True),
        (L, "El principito", "Antoine de Saint-Exupéry", "Fábula filosófica sobre el amor, la amistad, la inocencia y la condición humana.", "Filosofía", False),
        (L, "Los cuatro acuerdos", "Don Miguel Ruiz", "Guía práctica de sabiduría tolteca para la libertad personal y la eliminación de creencias limitantes.", "Autoconocimiento", False),
        (L, "Tus Zonas Erróneas", "Wayne W. Dyer", "Principios para superar pensamientos autodestructivos, culpa y dependencia emocional.", "Autoconocimiento", False),
        (L, "El cerebro y la inteligencia emocional", "Daniel Goleman", "Hallazgos sobre el funcionamiento cerebral, la autorregulación emocional y el rendimiento.", "Autoconocimiento", False),
        (L, "El monje que vendió su Ferrari", "Robin Sharma", "Fábula espiritual sobre cómo vivir con sentido, foco y equilibrio personal.", "Autoconocimiento", False),
        (L, "Aprender a aprender", "Barbara Oakley", "Técnicas científicas de estudio, memoria y superación de la procrastinación.", "Aprendizaje", False),
        (L, "Los desafíos de la memoria", "Joshua Foer", "Investigación periodística y práctica sobre cómo funciona la memoria y los palacios de la memoria.", "Productividad", False),
        (L, "El sutil arte de que te importe un carajo", "Mark Manson", "Enfoque realista y contraintuitivo sobre la gestión de prioridades y valores personales.", "Autoconocimiento", False),
        (L, "Focus", "Daniel Goleman", "El valor de la atención, la concentración profunda y la empatía en un mundo distráido.", "Productividad", False),
        (L, "Los 7 hábitos de la gente altamente efectiva", "Stephen Covey", "Principios fundamentales para la efectividad personal e interpersonal sostenible.", "Productividad", False),
        (L, "El poder del ahora", "Eckhart Tolle", "Guía de iluminación espiritual e introspección sobre la presencia consciente.", "Autoconocimiento", False),
        (L, "En defensa de la Ilustración", "Steven Pinker", "Análisis basado en datos sobre el progreso humano, la razón, la ciencia y el humanismo.", "Filosofía", False),
    ],
    1: [
        (C, "Arquitectura Medallion en Delta Lake", "Databricks Academy", "Estándar de diseño de almacenamiento estructurado (capas Bronze, Silver y Gold).", "Delta Lake"),
        (C, "Fundamentos de Lakehouse con Apache Iceberg", "Udemy", "Apache Iceberg como alternativa moderna a Delta Lake.", "Iceberg"),
        (C, "Orquestación Moderna: Prefect y Dagster", "Documentación oficial", "Alternativas contemporáneas a Airflow enfocadas en tipado de datos.", "Orquestadores"),
        (C, "Apache Kafka: Fundamentos y Arquitectura", "Platzi", "Conceptos básicos de mensajería asíncrona y diseño de tópicos streaming.", "Streaming"),
        (C, "Modelado de Datos Dimensionales (Kimball)", "Udemy", "Técnicas de modelado dimensional (hechos y dimensiones).", "Modelado"),
        (C, "Data Warehousing con Snowflake y BigQuery", "Udemy", "Diseño de almacenes de datos analíticos en la nube.", "Cloud DW"),
        (C, "PySpark Avanzado para Data Engineering", "Udemy", "Optimizaciones de Spark, particionamiento y shuffles.", "Spark"),
        (C, "Docker Compose y GitHub Actions", "Documentación oficial", "Integración CI/CD y despliegue de stack completo en contenedores.", "Hueco"),
        (C, "Calidad de datos: tests en dbt y Great Expectations", "Documentación oficial", "Validación y declaración de expectativas en datos de producción.", "Hueco"),
        (E, "README del pipeline con diagrama de arquitectura", "", "Documentación clara con diagramas de decisiones técnicas.", ""),

        # Libros Etapa 1 (25 libros)
        (L, "Designing Data-Intensive Applications", "Martin Kleppmann", "El libro técnico de referencia para sistemas distribuidos y datos.", "Referencia", True),
        (L, "Data Pipelines Pocket Reference", "James Densmore", "Guía práctica con patrones para construir y orquestar pipelines.", "Pipelines", True),
        (L, "Building Data Pipelines with Python", "Bas P. van Beek", "Arquitectura de datos mantenible y patrones de pipelines con Python.", "Pipelines", True),
        (L, "Data Engineering with AWS", "Gareth Eagar", "Construcción de soluciones de datos escalables en la nube de AWS.", "AWS", True),
        (L, "Database Internals", "Alex Petrov", "Estructuras de almacenamiento, árboles B+, WAL y motores de bases de datos.", "Bases de Datos", True),
        (L, "Streaming Systems", "Tyler Akidau", "Modelos de procesamiento de eventos en tiempo real y semantics exactas.", "Streaming", True),
        (L, "System Design Interview – An Insider's Guide", "Alex Xu", "Diseño de sistemas distribuidos a gran escala explicado de forma práctica.", "Arquitectura", True),
        (L, "Data Management at Scale", "Piethein Strengholt", "Arquitecturas modernas de datos, Data Mesh y gobierno corporativo.", "Arquitectura", True),
        (L, "Building Event-Driven Microservices", "Adam Bellemare", "Diseño de sistemas desacoplados basados en eventos y streaming.", "Arquitectura", True),
        (L, "Accelerate", "Nicole Forsgren et al.", "La ciencia detrás de DevOps y la entrega de software de alto rendimiento.", "DevOps", True),
        (L, "Breve historia del tiempo", "Stephen Hawking", "Orígenes del universo, hoyos negros y la naturaleza del espacio-tiempo.", "Física", True),
        (L, "La estructura de las revoluciones científicas", "Thomas S. Kuhn", "Cómo avanzan las ciencias a través de cambios de paradigma.", "Ciencia", True),
        (L, "La riqueza de las naciones", "Adam Smith", "Cimientos de la economía moderna, división del trabajo y libre mercado.", "Economía", True),
        (L, "El capital en el siglo XXI", "Thomas Piketty", "Análisis histórico de la acumulación de riqueza y la desigualdad.", "Economía", True),
        (L, "Los cañones de agosto", "Barbara Tuchman", "Estudio histórico del desencadenamiento de la Primera Guerra Mundial.", "Historia", True),
        (L, "La lógica de la investigación científica", "Karl Popper", "El principio de falsabilidad y la definición del conocimiento científico.", "Epistemología", True),
        (L, "Tratado de la naturaleza humana", "David Hume", "Análisis empirista sobre la percepción, la causalidad y las emociones.", "Filosofía", True),
        (L, "Crítica de la razón pura", "Immanuel Kant", "Investigación sobre los límites del conocimiento a priori y a posteriori.", "Filosofía", True),
        (L, "Crimen y castigo", "Fiódor Dostoyevski", "Exploración psicológica de la culpa, el dilema moral y la redención.", "Literatura", True),
        (L, "Los hermanos Karamázov", "Fiódor Dostoyevski", "Novela sobre la fe, la duda, la moral y la dinámica familiar.", "Literatura", True),
        (L, "Guerra y paz", "León Tolstói", "Monumental retrato de la invasión napoleónica a Rusia y la condición humana.", "Literatura", True),
        (L, "La odisea", "Homero", "El poema épico clásico sobre el regreso de Odiseo a Ítaca.", "Literatura", True),
        (L, "La divina comedia", "Dante Alighieri", "El viaje alegórico a través del Infierno, Purgatorio y Paraíso.", "Literatura", True),
        (L, "Pedro Páramo", "Juan Rulfo", "Obra maestra de la literatura mexicana sobre la memoria, la muerte y el pueblo de Comala.", "Literatura", True),
        (L, "La montaña mágica", "Thomas Mann", "Reflexión filosófica y cultural ambientada en un sanatorio suizo.", "Literatura", True),
        (L, "Breves respuestas a las grandes preguntas", "Stephen Hawking", "Reflexiones finales de Hawking sobre el origen del universo, los agujeros negros y la IA.", "Ciencia", False),
        (L, "El universo en una cáscara de nuez", "Stephen Hawking", "Exploración ilustrada de la física teórica, cosmología y teoría de cuerdas.", "Ciencia", False),
        (L, "Seis piezas fáciles", "Richard Feynman", "Las explicaciones más esenciales y accesibles de la física elemental por Richard Feynman.", "Ciencia", False),
        (L, "La realidad no es lo que parece", "Carlo Rovelli", "La evolución de la física desde la antigüedad hasta la gravedad cuántica de bucles.", "Ciencia", False),
        (L, "El comienzo del infinito", "David Deutsch", "Explicaciones sobre el progreso del conocimiento, la ciencia y la infinitud de las explicaciones.", "Ciencia", False),
    ],
    2: [
        (C, "Procesamiento de Señales para Mantenimiento Predictivo", "Udemy", "Análisis espectral y FFT para interpretar vibraciones.", "Sensores"),
        (C, "Modelos de Supervivencia para Confiabilidad", "Udemy", "Curvas de Kaplan-Meier y modelos de Cox para estimar RUL.", "Mantenimiento"),
        (C, "Kubeflow para ML Pipelines Industriales", "Udemy", "Diseño y orquestación de flujos de ML sobre Kubernetes.", "MLOps"),
        (C, "Álgebra Lineal y Cálculo para Machine Learning", "Platzi", "Las bases matemáticas del descenso de gradiente.", "Matemáticas"),
        (C, "Machine Learning Interpretability con Python", "Udemy", "SHAP y LIME para explicar decisiones del modelo.", "Explicabilidad"),
        (C, "Time Series Analysis con Prophet y ARIMA", "Udemy", "Descomposición de tendencia, estacionalidad y pronóstico.", "Series de Tiempo"),
        (C, "Feature Engineering Avanzado en Datos Tabulares", "Udemy", "Encodings, transformaciones Box-Cox y selección de variables.", "Feature Eng."),
        (C, "Seguimiento de experimentos con MLflow", "Documentación oficial", "Registro de parámetros y modelos.", "Hueco"),
        (N, "Valida en el tiempo, nunca al azar", "", "Evita filtrados temporales en validación.", "Ojo"),
        (E, "Traducir el modelo a dinero", "", "Matriz de confusión ponderada financieramente.", ""),

        # Libros Etapa 2 (25 libros)
        (L, "Reliability-Centered Maintenance", "John Moubray", "El texto definitivo para entender la confiabilidad operacional.", "Dominio", True),
        (L, "An Introduction to Statistical Learning", "Gareth James et al.", "Rigor matemático claro aplicado a regresión, clasificación y árboles.", "Estadística", True),
        (L, "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow", "Aurélien Géron", "La guía práctica indispensable para machine learning y aprendizaje profundo.", "Machine Learning", True),
        (L, "Forecasting: Principles and Practice", "Rob J Hyndman", "El manual de referencia mundial para predicción de series temporales.", "Series de Tiempo", True),
        (L, "Feature Engineering and Selection", "Max Kuhn y Kjell Johnson", "Metodologías rigurosas para la preparación de datos predictivos.", "Feature Eng.", True),
        (L, "Python Data Science Handbook", "Jake VanderPlas", "Manual completo de NumPy, Pandas, Matplotlib y Scikit-Learn.", "Data Science", True),
        (L, "The Elements of Statistical Learning", "Trevor Hastie et al.", "El tratamiento estadístico avanzado de los algoritmos de machine learning.", "Estadística", True),
        (L, "Mathematics for Machine Learning", "Marc Peter Deisenroth", "Álgebra lineal, cálculo multivariable y probabilidad para ML.", "Matemáticas", True),
        (L, "Causal Inference in Statistics: A Primer", "Judea Pearl", "Introducción al análisis causal y modelos estructurales.", "Estadística", True),
        (L, "Probabilistic Programming & Bayesian Methods for Hackers", "Cameron Davidson-Pilon", "Estadística bayesiana orientada a código y práctica.", "Estadística", True),
        (L, "El cisne negro", "Nassim Nicholas Taleb", "El impacto de lo altamente improbable y los límites de la predicción.", "Riesgo", True),
        (L, "¿Existe la suerte? (Fooled by Randomness)", "Nassim Nicholas Taleb", "Sobre cómo tendemos a confundir el azar con la destreza.", "Riesgo", True),
        (L, "Gödel, Escher, Bach", "Douglas Hofstadter", "Un estudio sobre autorreferencia, mente y matemática.", "Ciencia", True),
        (L, "El cerebro se cambia a sí mismo", "Norman Doidge", "Historias reales sobre neuroplasticidad y la adaptación cerebral.", "Neurociencia", True),
        (L, "La tabla rasa", "Steven Pinker", "La naturaleza humana frente al condicionamiento cultural.", "Psicología", True),
        (L, "Más allá del bien y del mal", "Friedrich Nietzsche", "Crítica a los dogmas filosóficos tradicionales y la voluntad de poder.", "Filosofía", True),
        (L, "El mito de Sísifo", "Albert Camus", "Ensayo filosófico sobre el absurdo, el sentido y la libertad.", "Filosofía", True),
        (L, "El hombre en busca de sentido", "Viktor Frankl", "La psicología del significado surgida del sufrimiento en campos de concentración.", "Psicología", True),
        (L, "El aleph", "Jorge Luis Borges", "Relatos sobre el infinito, el tiempo y los laberintos del pensamiento.", "Literatura", True),
        (L, "Rayuela", "Julio Cortázar", "La anti-novela innovadora que desafía el orden de lectura tradicional.", "Literatura", True),
        (L, "Moby Dick", "Herman Melville", "La obsesión épica del capitán Ahab contra la ballena blanca.", "Literatura", True),
        (L, "El proceso", "Franz Kafka", "La alienación individual frente a una burocracia absurda e impenetrable.", "Literatura", True),
        (L, "El viejo y el mar", "Ernest Hemingway", "Una metáfora sobre la lucha, el esfuerzo y la dignidad humana.", "Literatura", True),
        (L, "Ensayo sobre la ceguera", "José Saramago", "Una epidemia de ceguera que desnuda la condición humana.", "Literatura", True),
        (L, "La metamorfosis", "Franz Kafka", "La transformación de Gregorio Samsa y el aislamiento social.", "Literatura", True),
        (L, "Factfulness", "Hans Rosling", "Diez razones por las que estamos equivocados sobre el mundo y por qué las cosas están mejor de lo que pensamos.", "Pensamiento", False),
        (L, "Armas de destrucción matemática", "Cathy O’Neil", "Cómo los algoritmos y el Big Data pueden amplificar la desigualdad y la discriminación.", "Sesgos", False),
        (L, "Algoritmos para la vida cotidiana", "Brian Christian & Tom Griffiths", "Aplicación de algoritmos informáticos a la toma de decisiones en la vida diaria.", "Algoritmos", False),
        (L, "El ruido: Una falla en el juicio humano", "Daniel Kahneman", "Estudio sobre la variabilidad indeseada en el juicio humano y cómo reducirla.", "Pensamiento", False),
        (L, "Pensar en sistemas", "Donella Meadows", "Introducción esencial a la dinámica de sistemas y el análisis de interconexiones complejas.", "Sistemas", False),
    ],
    3: [
        (C, "RAG Local con Ollama y Llama 3", "Práctica propia", "Despliegue local y seguro de modelos de lenguaje privado.", "Local AI"),
        (C, "Inferencia de LLMs Optimizada: vLLM y Hugging Face TGI", "Práctica propia", "Motores de inferencia optimizados para servir LLMs open-source.", "Inferencia"),
        (C, "Agentes Autónomos con CrewAI y AutoGen", "Udemy", "Orquestación de múltiples agentes trabajando coordinados.", "Agentes"),
        (C, "Fine-Tuning de LLMs con LoRA y Unsloth", "Udemy", "Ajuste fino eficiente de modelos Llama 3 y Mistral en hardware local.", "Fine-Tuning"),
        (C, "Bases de Datos Vectoriales: Qdrant y ChromaDB", "Platzi", "Indexación HNSW, métricas de similitud y filtrado híbrido.", "Vector DB"),
        (C, "pgvector: embeddings dentro de Postgres", "Documentación oficial", "Uso de pgvector en tu Postgres de producción.", "Hueco"),
        (C, "Evaluación de sistemas RAG", "RAGAS / documentación", "Medición de fidelidad y relevancia en respuestas de agentes.", "Hueco"),
        (N, "Cuida el costo por consulta", "", "Calcula costos por query de agentes.", "Ojo"),

        # Libros Etapa 3 (25 libros)
        (L, "Building LLM Apps", "Valentina Alto", "Construcción de aplicaciones reales impulsadas por LLMs.", "LLMs", True),
        (L, "Generative AI on AWS", "Chris Fregly y Antje Barth", "Implementación y escalado de IA generativa corporativa.", "Generative AI", True),
        (L, "Designing Autonomous AI Agents", "Harrison Chase", "Patrones de arquitectura para agentes autónomos.", "Agentes", True),
        (L, "AI Engineering: Building Applications with Foundation Models", "Chip Huyen", "Ingeniería de software adaptada a sistemas deterministas y estocásticos.", "AI Engineering", True),
        (L, "Deep Learning", "Ian Goodfellow et al.", "El libro de texto clásico sobre redes neuronales profundas.", "AI Engineering", True),
        (L, "Reinforcement Learning: An Introduction", "Richard S. Sutton", "Fundamentos de aprendizaje por refuerzo.", "AI Engineering", True),
        (L, "Natural Language Processing with Transformers", "Lewis Tunstall et al.", "Construcción y fine-tuning de modelos Hugging Face.", "NLP", True),
        (L, "Speech and Language Processing", "Daniel Jurafsky", "La biblia del procesamiento de lenguaje natural.", "NLP", True),
        (L, "Vector Search Architecture", "Mohamed Ali", "Diseño de índices vectoriales e infraestructura de búsqueda semántica.", "Vector DB", True),
        (L, "Enterprise RAG Systems", "James Wilson", "Patrones de producción para sistemas Retrieval-Augmented Generation.", "RAG", True),
        (L, "Superinteligencia", "Nick Bostrom", "Caminos, peligros y estrategias ante la Inteligencia Artificial General.", "Futuro", True),
        (L, "La era del capitalismo de la vigilancia", "Shoshana Zuboff", "Análisis sobre el uso corporativo de los datos de comportamiento humano.", "Sociedad", True),
        (L, "La señal y el ruido", "Nate Silver", "Cómo distinguir la información relevante entre tanto dato desordenado.", "Estadística", True),
        (L, "Imparables: Diario de un científico", "Neil deGrasse Tyson", "Reflexiones sobre el conocimiento científico y la exploración.", "Ciencia", True),
        (L, "Cosmos", "Carl Sagan", "La historia de la ciencia y la visión humana del universo.", "Ciencia", True),
        (L, "Tractatus Logico-Philosophicus", "Ludwig Wittgenstein", "Los límites del lenguaje y su relación con la realidad.", "Filosofía", True),
        (L, "Leviatán", "Thomas Hobbes", "Sobre la estructura de la sociedad, el contrato social y el poder.", "Filosofía", True),
        (L, "Así habló Zaratustra", "Friedrich Nietzsche", "Filosofía del superhombre y la transvaloración de los valores.", "Filosofía", True),
        (L, "Dune", "Frank Herbert", "Obra maestra de la ciencia ficción sobre ecología, política y religión.", "Literatura", True),
        (L, "Fundación", "Isaac Asimov", "La psicohistoria y la reconstrucción de la civilización galáctica.", "Literatura", True),
        (L, "Yo, Robot", "Isaac Asimov", "Relatos clásicos sobre las tres leyes de la robótica y sus dilemas.", "Literatura", True),
        (L, "Neuromante", "William Gibson", "La novela pionera del género cyberpunk que acuñó el término ciberespacio.", "Literatura", True),
        (L, "El problema de los tres cuerpos", "Cixin Liu", "Trilogía de ciencia ficción china sobre el contacto con una civilización ajena.", "Literatura", True),
        (L, "¿Sueñan los androides con ovejas eléctricas?", "Philip K. Dick", "Reflexión sobre qué nos hace humanos frente a réplicas artificiales.", "Literatura", True),
        (L, "Guía del autoestopista galáctico", "Douglas Adams", "Sátira cómica y absurda de la ciencia ficción.", "Literatura", True),
        (L, "Crónicas marcianas", "Ray Bradbury", "Relatos entrelazados sobre la colonización de Marte y la naturaleza humana.", "Ficción", False),
        (L, "La guerra de los mundos", "H.G. Wells", "La novela clásica pionera sobre invasiones extraterrestres y resistencia.", "Ficción", False),
    ],
    4: [
        (C, "Inglés Técnico para Entrevistas de Data & AI", "Platzi", "Simulación de entrevistas técnicas, pitch personal y storytelling en inglés.", "Inglés"),
        (C, "Preparación Intensiva para IELTS General & Academic 7.0+", "Udemy", "Estrategias específicas para Listening, Reading, Writing y Speaking.", "IELTS"),
        (E, "Simulacro de IELTS Academic cada dos meses", "", "Medición periódica de banda IELTS.", "Inglés"),
        (N, "Habla, no solo leas", "", "Práctica de conversación semanal.", "Inglés"),

        # Libros Etapa 4 (25 libros)
        (L, "Never Split the Difference", "Chris Voss", "Negociación táctica de ofertas laborales y salarios internacionales.", "Negociación", True),
        (L, "The Hard Thing About Hard Things", "Ben Horowitz", "Gestión de la incertidumbre y la resiliencia en situaciones difíciles.", "Liderazgo", True),
        (L, "Essentialism: The Disciplined Pursuit of Less", "Greg McKeown", "Enfoque deliberado en lo verdaderamente esencial.", "Productividad", True),
        (L, "The Personal MBA", "Josh Kaufman", "Conceptos clave de negocios, finanzas y estrategia comercial.", "Negocios", True),
        (L, "Crucial Conversations", "Kerry Patterson", "Habilidades de comunicación para escenarios de alta presión.", "Comunicación", True),
        (L, "Influence: The Psychology of Persuasion", "Robert Cialdini", "Los seis principios universales de persuasión e influencia.", "Psicología", True),
        (L, "Good to Great", "Jim Collins", "Por qué algunas empresas dan el salto hacia la excelencia y otras no.", "Negocios", True),
        (L, "High Output Management", "Andrew Grove", "Principios de gestión de equipos por el legendario CEO de Intel.", "Liderazgo", True),
        (L, "Principles for Dealing with the Changing World Order", "Ray Dalio", "Análisis histórico de los grandes ciclos económicos y geopolíticos.", "Economía", True),
        (L, "The Intelligent Investor", "Benjamin Graham", "La biblia del valor de inversión y finanzas personales.", "Finanzas", True),
        (L, "Zero to One", "Peter Thiel", "Cómo construir startups que creen un futuro verdaderamente nuevo.", "Estrategia", True),
        (L, "Thinking in Bets", "Annie Duke", "Toma de decisiones inteligentes cuando no tienes toda la información.", "Toma de Decis.", True),
        (L, "Lombardi on Leadership", "Vince Lombardi", "Principios de ejecución, disciplina y liderazgo de alto impacto.", "Liderazgo", True),
        (L, "Armas, gérmenes y acero", "Jared Diamond", "Cómo la geografía y el entorno determinaron el destino de las civilizaciones.", "Historia", True),
        (L, "Historia de la filosofía occidental", "Bertrand Russell", "Recorrido ameno por la historia del pensamiento humano.", "Filosofía", True),
        (L, "El arte de la guerra", "Sun Tzu", "Principios milenarios de estrategia y resolución de conflictos.", "Estrategia", True),
        (L, "Homo Deus: Breve historia del mañana", "Yuval Noah Harari", "Hacia dónde se dirige la humanidad en el siglo XXI.", "Historia", True),
        (L, "Hamlet", "William Shakespeare", "Tragedia sobre la duda, la traición y la justicia.", "Literatura", True),
        (L, "Macbeth", "William Shakespeare", "Tragedia sobre la ambición desmedida y el poder.", "Literatura", True),
        (L, "Orgullo y prejuicio", "Jane Austen", "Clásico de la literatura inglesa sobre expectativas sociales y afecto.", "Literatura", True),
        (L, "El gran Gatsby", "F. Scott Fitzgerald", "Retrato del sueño americano y la decadencia en los años veinte.", "Literatura", True),
        (L, "El retrato de Dorian Gray", "Oscar Wilde", "Exploración estética sobre la juventud, la belleza y la moral.", "Literatura", True),
        (L, "100 Poems", "Seamus Heaney", "Antología poética del Premio Nobel irlandés.", "Literatura", True),
        (L, "Cumbres borrascosas", "Emily Brontë", "Pasión y venganza en los páramos ingleses.", "Literatura", True),
        (L, "El conde de Montecristo", "Alexandre Dumas", "La historia épica de justicia, traición y venganza.", "Literatura", True),
        (L, "Palabras que venden", "Phil M. Jones", "Frases mágicas e influencia verbal para la comunicación efectiva y las ventas.", "Ventas", False),
        (L, "El hombre más rico de Babilonia", "George S. Clason", "Parábolas clásicas sobre el ahorro, la inversión y la gestión del dinero.", "Finanzas", False),
        (L, "Dinero: Domina el juego", "Tony Robbins", "Guía paso a paso para la libertad financiera basada en entrevistas a grandes inversionistas.", "Finanzas", False),
        (L, "La vía rápida del millonario", "M.J. DeMarco", "Crítica a las rutas financieras tradicionales y mapa para crear riqueza activa.", "Finanzas", False),
        (L, "Háblame para que te escuche", "Adele Faber y Elaine Mazlish", "Técnicas de comunicación empática y resolución de conflictos interpersonales.", "Comunicación", False),
        (L, "El poder de la empatía", "Helen Riess", "Neurociencia y práctica de la empatía para mejorar la conexión humana y el liderazgo.", "Comunicación", False),
        (L, "Piense y hágase rico", "Napoleon Hill", "El clásico sobre la mentalidad de logro, la perseverancia y el éxito financiero.", "Finanzas", False),
        (L, "The Art of Spending Money", "Morgan Housel", "Reflexión sobre el arte de gastar el dinero con propósito y felicidad.", "Finanzas", True),
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
        "objetivo": "Hacer visibles tus repositorios, artículos y demostraciones de mantenimiento predictivo.",
        "items": [
            (E, "Tres repos públicos pulidos", "", "Repos con README, diagramas y datos anonimizados.", ""),
            (E, "Un caso de estudio escrito", "", "Caso de estudio de dos páginas enfocado en ROI de mantenimiento.", ""),
            (C, "Perfil de LinkedIn en inglés", "Trabajo propio", "Orientado al rol de Data Engineer / ML en minería.", ""),
            (C, "CV en formato del país destino", "Trabajo propio", "Sin foto, orientado a logros cuantificables.", ""),
            (C, "Creación de Portafolios Técnicos y GitHub Showcase", "Platzi", "Estructuración de repositorios profesionales.", "Portafolio"),
            (C, "Storytelling con Datos para Ejecutivos", "Udemy", "Presentación de resultados técnicos de impacto.", "Storytelling"),
            (N, "Escribe cuatro artículos", "", "Publica tus aprendizajes en LinkedIn/Medium.", ""),

            # Libros Etapa 5 (25 libros)
            (L, "Storytelling with Data", "Cole Nussbaumer Knaflic", "Cómo presentar hallazgos para que una gerencia actúe.", "Comunicación", True),
            (L, "Show Your Work!", "Austin Kleon", "10 maneras de compartir tu creatividad y hacerte descubrir.", "Carrera", True),
            (L, "The Tech Resume Inside Out", "Gergely Orosz", "Cómo escribir un currículum que supere filtros.", "Carrera", True),
            (L, "Cracking the Coding Interview", "Gayle Laakmann McDowell", "Preparación para entrevistas técnicas.", "Entrevistas", True),
            (L, "On Writing Well", "William Zinsser", "La guía clásica para escribir en prosa clara y convincente.", "Redacción", True),
            (L, "The Elements of Style", "William Strunk Jr.", "Principios fundamentales de gramática y estilo en inglés.", "Redacción", True),
            (L, "Steal Like an Artist", "Austin Kleon", "Manifiesto sobre la creatividad en la era digital.", "Creatividad", True),
            (L, "Resonate", "Nancy Duarte", "Cómo crear presentaciones visuales persuasivas.", "Comunicación", True),
            (L, "How to Win Friends and Influence People", "Dale Carnegie", "Habilidades interpersonales y de comunicación.", "Relaciones", True),
            (L, "Ego is the Enemy", "Ryan Holiday", "Cómo mantener la humildad y la objetividad profesional.", "Psicología", True),
            (L, "Drive", "Daniel H. Pink", "La motivación intrínseca: autonomía, maestría y propósito.", "Psicología", True),
            (L, "Flow", "Mihaly Csikszentmihalyi", "La psicología de la experiencia óptima y el estado de flujo.", "Psicología", True),
            (L, "La condición humana", "Hannah Arendt", "Análisis sobre la labor, el trabajo y la acción política.", "Filosofía", True),
            (L, "El choque de civilizaciones", "Samuel P. Huntington", "Análisis de la política mundial en la era posguerra fría.", "Geopolítica", True),
            (L, "El origen de las especies", "Charles Darwin", "La teoría fundamental de la evolución por selección natural.", "Ciencia", True),
            (L, "Madame Bovary", "Gustave Flaubert", "La búsqueda de la pasión frente a la monotonía burguesa.", "Literatura", True),
            (L, "La metamorfosis y otros relatos", "Franz Kafka", "Antología de cuentos fundamentales de Kafka.", "Literatura", True),
            (L, "El jugador", "Fiódor Dostoyevski", "Novela sobre la adicción al juego y el azar en las relaciones humanas.", "Literatura", True),
            (L, "Veinte poemas de amor y una canción desesperada", "Pablo Neruda", "La poesía lírica hispanoamericana más célebre.", "Literatura", True),
            (L, "El amor en los tiempos del cólera", "Gabriel García Márquez", "Historia de amor y paciencia a lo largo de décadas.", "Literatura", True),
            (L, "La ciudad y los perros", "Mario Vargas Llosa", "Novela ambientada en el colegio militar Leoncio Prado.", "Literatura", True),
            (L, "La tía Julia y el escribidor", "Mario Vargas Llosa", "Novela semiautobiográfica y comedia romántica urbana.", "Literatura", True),
            (L, "Los detectives salvajes", "Roberto Bolaño", "La búsqueda de la poeta Cesárea Tinajero por México y el mundo.", "Literatura", True),
            (L, "2666", "Roberto Bolaño", "Novela monumental sobre el mal, la literatura y la violencia contemporánea.", "Literatura", True),
            (L, "La insoportable levedad del ser", "Milan Kundera", "Reflexión filosófica sobre la libertad, el amor y el destino.", "Literatura", True),
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
        "objetivo": "Preparar la relocalización internacional, credenciales y postulaciones laborales.",
        "items": [
            (E, "IELTS Academic rendido de verdad", "", "Examen oficial de certificación de inglés.", ""),
            (E, "Evaluación de credenciales iniciada", "", "WES para Canadá o Engineers Australia.", ""),
            (N, "Verifica todo en las fuentes oficiales", "", "Revisar canada.ca e immi.homeaffairs.gov.au.", "Ojo"),
            (C, "Preparación de entrevista técnica", "Práctica propia", "Ensayar en inglés la historia de tu reconversión.", ""),
            (C, "Guía Práctica Skilled Migration Australia (Subclass 189/190)", "Oficial", "Cálculo de puntos EOI y proceso.", "Australia"),
            (C, "Guía Práctica Express Entry Canadá & PNP", "Oficial", "Sistema CRS y nominaciones provinciales.", "Canadá"),
            (E, "Un objetivo semanal de aplicaciones, sostenido", "", "Cinco aplicaciones dirigidas por semana.", ""),
            (N, "Apunta al nicho, no al puesto genérico", "", "Focus en mining analytics / industrial IoT.", ""),

            # Libros Etapa 6 (15 libros)
            (L, "The Culture Map", "Erin Meyer", "Navegar las diferencias culturales en entornos globales.", "Cultura", True),
            (L, "The Express Entry & Overseas Career Guide", "Immigration Experts", "Planificación de relocalización internacional.", "Inmigración", True),
            (L, "Getting to Yes", "Roger Fisher y William Ury", "Principios de negociación ganar-ganar para ofertas de trabajo.", "Negociación", True),
            (L, "Working Backward", "Colin Bryar", "Prácticas de ejecución y cultura operacional dentro de Amazon.", "Gestión", True),
            (L, "The Software Engineer's Guidebook", "Gergely Orosz", "Manual de carrera de ingeniero junior a director técnico.", "Carrera", True),
            (L, "Por qué fracasan los países", "Daron Acemoglu", "El papel de las instituciones inclusivas en la prosperidad.", "Economía", True),
            (L, "El siglo de China", "Henry Kissinger", "Análisis histórico de las relaciones geopolíticas globales.", "Geopolítica", True),
            (L, "Diplomacia", "Henry Kissinger", "Historia de las relaciones internacionales desde Westfalia.", "Geopolítica", True),
            (L, "Postguerra: Una historia de Europa desde 1945", "Tony Judt", "Historia exhaustiva del continente europeo tras la Segunda Guerra Mundial.", "Historia", True),
            (L, "En el camino (On the Road)", "Jack Kerouac", "Obra cumbre de la generación beat sobre la libertad de viajar.", "Literatura", True),
            (L, "El corazón de las tinieblas", "Joseph Conrad", "Un viaje al interior del Congo y la naturaleza de la civilización.", "Literatura", True),
            (L, "Viaje al centro de la tierra", "Julio Verne", "Aventura clásica de exploración científica subterránea.", "Literatura", True),
            (L, "La vuelta al mundo en ochenta días", "Julio Verne", "El reto clásico de circunnavegación y precisión.", "Literatura", True),
            (L, "Un tranvía llamado Deseo", "Tennessee Williams", "Obra teatral sobre el choque entre fantasía y realidad.", "Literatura", True),
            (L, "La náusea", "Jean-Paul Sartre", "La obra filosófica existencialista sobre la experiencia de existir.", "Filosofía", True),
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
        "objetivo": "Conectar telemetría en tiempo real desde sensores industriales (SCADA/PLC) a la nube.",
        "items": [
            (C, "Arquitectura IoT: Ingesta con MQTT y Apache Kafka", "Udemy / Documentación oficial", "Ingesta masiva de sensores.", "Streaming"),
            (C, "Procesamiento de Flujos en Tiempo Real con Apache Flink", "Udemy", "Ventanas de tiempo y joins en tiempo real.", "Flink"),
            (C, "TimescaleDB: PostgreSQL optimizado para series de tiempo", "Documentación oficial", "Base hiper-rápida para millones de métricas.", "Timescale"),
            (C, "Monitoreo Industrial con Grafana y Prometheus", "Documentación oficial", "Tableros de alerta operacional.", "Monitoreo"),
            (C, "OPC-UA y Protocolos Industriales para Data Engineers", "Udemy", "Conexión a PLCs y SCADA.", "IoT"),
            (C, "Arquitectura de Sistemas Tolerantes a Fallos en la Nube", "Udemy", "Alta disponibilidad e infraestructura crítica.", "Arquitectura"),
            (E, "Dashboard SCADA en tiempo real conectado a sensor IoT sim", "", "Pipeline streaming sim con Grafana.", ""),
            (E, "Ingesta resiliente ante pérdida de conectividad en mina", "", "Buffer local Edge con re-sincronización.", ""),
            (N, "Telemetría fallida != equipo fallado", "", "Diferencia sensor roto de falla mecánica.", "Ojo"),

            # Libros Etapa 7 (15 libros)
            (L, "Designing Connected Products", "Claire Rowland", "Diseño de productos conectados e infraestructuras IoT.", "IoT", True),
            (L, "Site Reliability Engineering (SRE)", "Betsy Beyer et al.", "Prácticas de confiabilidad y operación a gran escala.", "SRE", True),
            (L, "Building Microservices", "Sam Newman", "Diseño y modelado de microservicios acoplados libremente.", "Arquitectura", True),
            (L, "Industrial IoT Architectures and Protocols", "Alasdair Gilchrist", "Integración de redes OT e IT en minería e industria.", "IoT", True),
            (L, "Software Architecture in Practice", "Len Bass et al.", "Principios fundamentales de arquitectura de software.", "Arquitectura", True),
            (L, "Clean Architecture", "Robert C. Martin", "Estructuración de componentes y capas de software mantenibles.", "Arquitectura", True),
            (L, "Enterprise Integration Patterns", "Gregor Hohpe", "Patrones de diseño para integración de sistemas corporativos.", "Arquitectura", True),
            (L, "Domain-Driven Design", "Eric Evans", "Modelado de software complejo a partir del dominio de negocio.", "Arquitectura", True),
            (L, "Distributed Systems: Principles and Paradigms", "Andrew S. Tanenbaum", "Principios teóricos y prácticos de sistemas distribuidos.", "Sistemas", True),
            (L, "High Performance Browser Networking", "Ilya Grigorik", "Protocolos de red (HTTP/2, WebSockets, TLS) y optimización de latencia.", "Redes", True),
            (L, "El diseño de las cosas cotidianas", "Don Norman", "Diseño centrado en el usuario e interacción con máquinas.", "Diseño", True),
            (L, "Estructuras o por qué las cosas no se caen", "J.E. Gordon", "Principios de física e ingeniería estructural explicados de forma amena.", "Ingeniería", True),
            (L, "Skunk Works", "Ben R. Rich", "Memorias sobre la ingeniería secreta de Lockheed y proyectos avanzados.", "Ingeniería", True),
            (L, "Invención e innovación", "Vaclav Smil", "Breve historia de las tecnologías que prometieron cambiar el mundo.", "Historia", True),
            (L, "Energía y civilización: Una historia", "Vaclav Smil", "El papel de la energía en la evolución de las sociedades humanas.", "Historia", True),
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
