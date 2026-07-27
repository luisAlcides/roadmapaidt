"""La ruta de una sola carrera: AI/ML Engineer con especialidad industrial.

El roadmap del PDF —y los dos comandos que lo complementan— cubren cuatro
oficios a la vez: Data Engineer, Data Scientist, AI Engineer y una capa de IoT.
Eso sirve como catálogo, pero como plan es imposible: nadie sostiene 700 items
en 18 meses, y un perfil que toca todo no gana ninguna entrevista.

Esto es lo contrario: doce meses, seis etapas, una sola carrera. Está diseñada
alrededor de la pregunta de qué te contrata y qué se paga, no de qué es
interesante. La ingeniería de datos aparece solo como herramienta —lo que un
ML Engineer necesita para alimentar sus modelos—, no como especialidad aparte.

La apuesta: ML Engineer que sabe llevar modelos a producción, con mantenimiento
predictivo y confiabilidad como nicho. El nicho no es decoración; es la única
parte del perfil que un candidato con bootcamp no puede copiar.

Se carga y se borra sin tocar el catálogo completo:
    python manage.py cargar_ruta_enfocada
    python manage.py cargar_ruta_enfocada --quitar
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from roadmap.models import Etapa, Item

C, L, E, N = Item.Tipo.CURSO, Item.Tipo.LIBRO, Item.Tipo.ENTREGABLE, Item.Tipo.NOTA

OL = "https://openlibrary.org/search?q="

# (tipo, título, fuente, detalle, etiqueta, en_inglés, url)
RUTA = [
    {
        "orden": 0,
        "kicker": "Mes 1–2",
        "titulo": "Base de ingeniero de software",
        "subtitulo": "Sin esto, lo demás no se sostiene",
        "duracion": "6 semanas",
        "horas": "~70 horas",
        "color": "#6b7f8c",
        "objetivo": "Escribir Python que otra persona pueda leer, versionar y desplegar. Es el filtro que separa a quien hace notebooks de quien es contratable.",
        "items": [
            (C, "Python intermedio: módulos, clases y entornos virtuales", "Real Python", "Estructura de proyecto, imports, dataclasses y manejo de errores. Nada de esto se aprende en un curso de pandas.", "Python", True, "https://realpython.com/learning-paths/python3-introduction/"),
            (C, "SQL: joins, agregaciones y window functions", "Mode SQL Tutorial", "Window functions para horómetros acumulados y tiempo entre fallas. Es la consulta que vas a escribir mil veces.", "SQL", True, "https://mode.com/sql-tutorial/"),
            (C, "Git y GitHub: ramas, PRs y resolución de conflictos", "Git Book (Pro Git)", "Trabajar en equipo sobre el mismo repo sin romper nada. Gratuito y completo.", "Git", True, "https://git-scm.com/book/es/v2"),
            (C, "Línea de comandos y Linux para desarrolladores", "MIT — Missing Semester", "El curso del MIT sobre lo que ninguna carrera enseña: shell, scripting, tmux, depuración. Seis clases.", "Linux", True, "https://missing.csail.mit.edu/"),
            (C, "Docker: imágenes, volúmenes y docker compose", "Documentación oficial", "Tu modelo tiene que correr igual en tu laptop y en el servidor. Docker es cómo se logra eso.", "Docker", True, "https://docs.docker.com/get-started/"),
            (C, "pytest: tests que atrapan errores de datos", "Real Python", "Un test sobre el preprocesamiento vale más que diez sobre la API. Ahí es donde se rompen los modelos.", "Calidad", True, "https://realpython.com/pytest-python-testing/"),
            (C, "uv y entornos reproducibles", "Astral", "Dependencias fijadas y entornos que se recrean en segundos. Reemplaza pip, venv y poetry.", "Tooling", True, "https://docs.astral.sh/uv/"),
            (C, "Álgebra lineal, visualmente", "3Blue1Brown", "Solo lo necesario: vectores, matrices, proyecciones. Ver la serie completa toma una tarde y ahorra meses.", "Matemáticas", True, "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"),
            (C, "Estadística sin misticismo", "StatQuest", "Distribuciones, sesgo-varianza, validación cruzada, p-values. En videos de diez minutos.", "Estadística", True, "https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9"),
            (E, "Template propio de proyecto ML", "", "Repo plantilla con estructura de carpetas, uv, Dockerfile, pytest, ruff y Makefile. Lo clonas en cada proyecto de aquí en adelante.", "", False, "https://cookiecutter-data-science.drivendata.org/"),
            (E, "Tu operación en una base Postgres", "", "Carga histórico real de fallas, horómetros y órdenes de trabajo. Todo lo que sigue se construye sobre estos datos, no sobre datasets de juguete.", "", False, ""),
            (N, "No estudies matemáticas 'por si acaso'", "", "Aprende el álgebra lineal que necesita el algoritmo que estás usando hoy, cuando lo estés usando. La ruta larga por teoría pura mata a la mayoría de los que se reconvierten.", "Método", False, ""),
        ],
    },
    {
        "orden": 1,
        "kicker": "Mes 3–5",
        "titulo": "ML que decide bien",
        "subtitulo": "Datos tabulares y series de tiempo",
        "duracion": "3 meses",
        "horas": "~150 horas",
        "color": "#2f6d6a",
        "objetivo": "Construir modelos que un gerente pueda usar para decidir un paro de máquina, con validación honesta y el error medido en dinero, no en accuracy.",
        "items": [
            (C, "Machine Learning Specialization", "DeepLearning.AI / Coursera", "Los fundamentos con Andrew Ng. Audit gratis. Hazlo completo: es la base sobre la que todo lo demás se apoya.", "Fundamentos", True, "https://www.deeplearning.ai/courses/machine-learning-specialization/"),
            (C, "Practical Deep Learning for Coders (Parte 1)", "fast.ai", "Entrenas modelos útiles desde la primera lección. El mejor curso gratuito para no quedarse atascado en teoría.", "Práctica", True, "https://course.fast.ai/"),
            (C, "Gradient boosting: XGBoost, LightGBM y CatBoost", "Documentación oficial", "El algoritmo que gana en datos tabulares, que es el 90 % de lo que verás en la industria. Domínalo antes que las redes.", "Tabular", True, "https://xgboost.readthedocs.io/en/stable/tutorials/model.html"),
            (C, "Series de tiempo: validación temporal y pronóstico", "Kaggle Learn — Time Series", "Lags, ventanas móviles y por qué nunca se valida al azar con datos temporales. Corto y directo.", "Series", True, "https://www.kaggle.com/learn/time-series"),
            (C, "Forecasting: Principles and Practice", "Hyndman y Athanasopoulos", "El manual de referencia de pronóstico, gratuito online. Los capítulos de descomposición y evaluación son obligatorios.", "Series", True, "https://otexts.com/fpp3/"),
            (C, "Datos desbalanceados y métricas que importan", "imbalanced-learn", "Las fallas son el 1 % de tus filas. Accuracy 99 % significa que tu modelo no sirve. Precision-recall, class weights, umbrales.", "Métricas", True, "https://imbalanced-learn.org/stable/user_guide.html"),
            (C, "Explicabilidad con SHAP", "SHAP docs", "Un supervisor no para una máquina porque 'el modelo dijo'. SHAP es cómo justificas la predicción.", "Explicabilidad", True, "https://shap.readthedocs.io/"),
            (C, "Análisis de señales: FFT y features de vibración", "SciPy Signal", "RMS, kurtosis, envolvente y espectro. Es lo que convierte un acelerómetro en features de modelo.", "Señales", True, "https://docs.scipy.org/doc/scipy/tutorial/signal.html"),
            (C, "Análisis de supervivencia para confiabilidad", "lifelines docs", "Kaplan-Meier y Cox para estimar vida útil remanente. El puente exacto entre tu oficio actual y el ML.", "Confiabilidad", True, "https://lifelines.readthedocs.io/"),
            (C, "Una competencia de Kaggle, completa", "Kaggle", "Una sola, hasta el final, leyendo las soluciones de los ganadores. Enseña más sobre validación que cualquier curso.", "Práctica", True, "https://www.kaggle.com/competitions"),
            (E, "Modelo de vida útil remanente sobre C-MAPSS", "", "El benchmark público de degradación de turbinas de la NASA. Es tu carta de presentación: dominio industrial demostrable con datos que cualquiera puede verificar.", "", False, "https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/"),
            (E, "El mismo modelo, sobre los datos de tu operación", "", "Predicción de falla en tus equipos, con validación temporal y comparado contra la regla actual de mantenimiento preventivo.", "", False, ""),
            (E, "La matriz de confusión traducida a dólares", "", "Cuánto cuesta un falso negativo (falla no detectada) y cuánto un falso positivo (paro innecesario). Ese número define tu umbral, no el F1.", "", False, ""),
            (N, "Baseline tonto antes que modelo listo", "", "Escribe primero la regla heurística que ya usa mantenimiento. Si tu modelo no la supera, no tienes modelo — tienes un notebook.", "Método", False, ""),
            (N, "Validación temporal, siempre", "", "Entrenar con datos de junio y validar con datos de marzo es filtrar el futuro. Es el error que más proyectos de mantenimiento predictivo ha matado.", "Ojo", False, ""),
        ],
    },
    {
        "orden": 2,
        "kicker": "Mes 6–7",
        "titulo": "Deep learning donde sí paga",
        "subtitulo": "Solo lo que aplica a señales y texto",
        "duracion": "2 meses",
        "horas": "~90 horas",
        "color": "#7b4fa8",
        "objetivo": "Manejar PyTorch con soltura y saber cuándo una red neuronal gana y cuándo es un capricho caro frente a un gradient boosting.",
        "items": [
            (C, "PyTorch: tensores, autograd y ciclo de entrenamiento", "PyTorch — Learn the Basics", "El tutorial oficial, escrito a mano. Todo lo demás se construye encima.", "PyTorch", True, "https://pytorch.org/tutorials/beginner/basics/intro.html"),
            (C, "Neural Networks: Zero to Hero", "Andrej Karpathy", "Construyes micrograd y después GPT desde cero. El mejor material que existe sobre cómo funciona una red por dentro, y es gratis.", "Fundamentos", True, "https://karpathy.ai/zero-to-hero.html"),
            (C, "Deep Learning Specialization", "DeepLearning.AI / Coursera", "Redes densas, regularización, optimización y secuencias. Los cursos 1, 2 y 5 son los que te sirven; los de visión puedes saltarlos.", "Deep Learning", True, "https://www.deeplearning.ai/courses/deep-learning-specialization/"),
            (C, "Autoencoders y detección de anomalías", "PyTorch / papers", "Entrenas con señales sanas y usas el error de reconstrucción como score. Es el patrón más útil para mantenimiento predictivo.", "Anomalías", True, "https://pytorch.org/tutorials/beginner/introyt/introyt1_tutorial.html"),
            (C, "Redes para series de tiempo: 1D CNN, LSTM y Temporal Fusion", "PyTorch Forecasting", "Las arquitecturas que sí aplican a datos de sensores, sin desviarte a visión o audio.", "Series", True, "https://pytorch-forecasting.readthedocs.io/"),
            (C, "The Annotated Transformer", "Harvard NLP", "El paper fundacional con su implementación comentada línea por línea. Es la base de todo lo de la etapa 4.", "Transformers", True, "https://nlp.seas.harvard.edu/annotated-transformer/"),
            (C, "A Recipe for Training Neural Networks", "Andrej Karpathy", "Cómo depurar un entrenamiento que no converge. Un ensayo que vale más que un curso entero.", "Método", True, "https://karpathy.github.io/2019/04/25/recipe/"),
            (C, "Experimentos rastreables con Weights & Biases", "W&B", "Si no registras hiperparámetros y métricas, en dos semanas no sabrás cuál corrida fue la buena. Gratis para uso personal.", "Tooling", True, "https://docs.wandb.ai/"),
            (E, "micrograd reescrito por ti", "", "El motor de autograd en 150 líneas, sin mirar el original. Si te sale, entendiste backpropagation de verdad.", "", False, "https://github.com/karpathy/micrograd"),
            (E, "Detector de anomalías de vibración en producción de mentira", "", "Autoencoder sobre señales sanas de tus equipos, con umbral calibrado y comparado contra un control estadístico clásico.", "", False, ""),
            (N, "Casi siempre gana el boosting", "", "En datos tabulares con pocos miles de filas, XGBoost le gana a una red neuronal. Usa deep learning para señales crudas, texto e imágenes; para el resto, no.", "Ojo", False, ""),
        ],
    },
    {
        "orden": 3,
        "kicker": "Mes 8–10",
        "titulo": "Producción: donde está el sueldo",
        "subtitulo": "MLOps y el dato como herramienta",
        "duracion": "3 meses",
        "horas": "~140 horas",
        "color": "#2f7d4f",
        "objetivo": "Convertir un notebook en un servicio versionado, monitoreado y con rollback. Esta es la etapa que separa a un ML Engineer de un data scientist, y la que explica la diferencia de sueldo.",
        "items": [
            (C, "MLOps Zoomcamp", "DataTalksClub", "Nueve semanas gratuitas con proyecto evaluado: tracking, orquestación, despliegue y monitoreo. El curso central de esta etapa — hazlo completo.", "MLOps", True, "https://github.com/DataTalksClub/mlops-zoomcamp"),
            (C, "Made With ML", "Goku Mohandas", "El complemento: testing, CI/CD y diseño de sistemas ML, muy bien escrito y gratuito.", "MLOps", True, "https://madewithml.com/"),
            (C, "MLflow: tracking, registry y stages", "MLflow docs", "Qué modelo está en producción, entrenado con qué datos y por quién. La pieza mínima de todo stack serio.", "Tracking", True, "https://mlflow.org/docs/latest/"),
            (C, "FastAPI para servir modelos", "FastAPI docs", "Validación con Pydantic, async y documentación automática. Es como se expone un modelo hoy.", "Serving", True, "https://fastapi.tiangolo.com/"),
            (C, "Orquestación de pipelines con Airflow o Dagster", "Documentación oficial", "Reentrenamiento programado, dependencias y reintentos. Aquí entra la ingeniería de datos: como herramienta, no como carrera.", "Pipelines", True, "https://docs.dagster.io/"),
            (C, "dbt: transformaciones versionadas y testeadas", "dbt docs", "Tus features definidas en SQL, con tests y linaje. Lo mínimo de data engineering que un ML Engineer necesita.", "Datos", True, "https://docs.getdbt.com/"),
            (C, "Monitoreo de drift con Evidently", "Evidently docs", "Un modelo que no se monitorea es un modelo que ya falló y nadie se enteró.", "Monitoreo", True, "https://docs.evidentlyai.com/"),
            (C, "CI/CD con GitHub Actions", "GitHub docs", "Tests en cada PR, entrenamiento automático y despliegue con aprobación manual.", "CI/CD", True, "https://docs.github.com/en/actions"),
            (C, "Una nube, a fondo: AWS o GCP", "AWS Skill Builder / Google Cloud Skills Boost", "Elige una y quédate ahí. Saber una bien pesa mucho más que tocar tres por encima.", "Cloud", True, "https://explore.skillbuilder.aws/"),
            (C, "AWS Machine Learning Engineer – Associate", "AWS", "La certificación que abre filtros de reclutador en Australia y Canadá. De pago, y vale la pena al final de esta etapa.", "Certificación", True, "https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/"),
            (C, "Inferencia rápida y barata con ONNX Runtime", "ONNX Runtime", "Cuantización y aceleración: menos latencia y menos costo sin reentrenar. Importante si el modelo corre dentro de la mina.", "Inferencia", True, "https://onnxruntime.ai/docs/"),
            (E, "Tu modelo de fallas, desplegado de verdad", "", "API en FastAPI, imagen Docker, tests en CI, tracking en MLflow, dashboard de drift y reentrenamiento programado. Este es el proyecto que te consigue el trabajo.", "", False, ""),
            (E, "Runbook de incidentes del modelo", "", "Cómo se detecta que el modelo se degradó, a quién se avisa y cómo se hace rollback en menos de 15 minutos. Escrito, en el repo.", "", False, ""),
            (E, "Diagrama de arquitectura de una página", "", "De sensor a decisión: ingesta, features, entrenamiento, serving y monitoreo. Es lo que dibujarás en la pizarra de la entrevista.", "", False, ""),
            (N, "Shadow mode antes de producción", "", "El modelo nuevo corre en paralelo al viejo sin decidir nada durante dos semanas. Se compara. Después se promueve.", "Método", False, ""),
            (N, "Aquí está la diferencia de sueldo", "", "Miles de personas entrenan modelos. Las que los mantienen vivos en producción son muchas menos y cobran bastante más. No saltes esta etapa.", "Estrategia", False, ""),
        ],
    },
    {
        "orden": 4,
        "kicker": "Mes 11–12",
        "titulo": "AI Engineering con LLMs",
        "subtitulo": "La capa que hoy más se paga",
        "duracion": "2 meses",
        "horas": "~80 horas",
        "color": "#b5543f",
        "objetivo": "Construir y evaluar aplicaciones con modelos de lenguaje: RAG sobre documentación técnica, agentes con herramientas y evaluación cuantitativa.",
        "items": [
            (C, "Hugging Face LLM Course", "Hugging Face", "Transformers, tokenizers y fine-tuning con la librería que usa toda la industria. Gratuito.", "LLMs", True, "https://huggingface.co/learn/llm-course"),
            (C, "Cursos cortos de DeepLearning.AI", "DeepLearning.AI", "Decenas de cursos de una hora sobre RAG, agentes y evaluación, gratuitos y directo al código.", "LLM Apps", True, "https://www.deeplearning.ai/short-courses/"),
            (C, "Prompt Engineering Interactive Tutorial", "Anthropic", "El curso oficial: estructura de prompts, few-shot, chain of thought y uso de herramientas.", "Prompting", True, "https://github.com/anthropics/prompt-eng-interactive-tutorial"),
            (C, "Building effective agents", "Anthropic Engineering", "Cuándo un flujo determinista le gana a un agente, y cómo diseñar el que sí hace falta. Léelo antes de escribir código de agentes.", "Agentes", True, "https://www.anthropic.com/engineering/building-effective-agents"),
            (C, "Model Context Protocol (MCP)", "MCP docs", "El estándar abierto para conectar modelos a herramientas y datos. Está apareciendo en descripciones de vacantes.", "Agentes", True, "https://modelcontextprotocol.io/"),
            (C, "RAG: chunking, embeddings y reranking", "LlamaIndex docs", "Búsqueda híbrida y retrieval en dos etapas. Es la mejora con mejor relación esfuerzo-resultado.", "RAG", True, "https://docs.llamaindex.ai/"),
            (C, "pgvector: embeddings dentro de tu Postgres", "pgvector", "No necesitas una base vectorial aparte para empezar. Menos infraestructura que mantener.", "Vector DB", True, "https://github.com/pgvector/pgvector"),
            (C, "Evaluación con promptfoo y RAGAS", "promptfoo / Ragas", "Suites de evaluación versionadas que corren en CI. Sin esto no puedes afirmar que mejoraste nada.", "Evaluación", True, "https://www.promptfoo.dev/docs/intro/"),
            (C, "Fine-tuning eficiente con LoRA y QLoRA", "Hugging Face PEFT", "Adaptar un modelo mediano en una sola GPU de consumo. Para tono y jerga del dominio, no para hechos.", "Fine-Tuning", True, "https://huggingface.co/docs/peft/index"),
            (C, "Modelos locales con Ollama y vLLM", "Ollama / vLLM", "Un LLM privado dentro de la operación, sin mandar datos afuera. En minería eso suele ser requisito, no preferencia.", "Local AI", True, "https://docs.vllm.ai/"),
            (C, "OWASP Top 10 for LLM Applications", "OWASP", "Prompt injection y fuga de datos. Si expones un asistente a usuarios, esto es parte del trabajo.", "Seguridad", True, "https://genai.owasp.org/llm-top-10/"),
            (E, "Asistente sobre tus manuales de mantenimiento", "", "RAG sobre manuales de equipos y bitácoras, con citas a la fuente y set de 50 preguntas evaluado automáticamente.", "", False, ""),
            (E, "Reporte de costo por consulta", "", "API comercial contra modelo propio: costo por 1000 consultas, latencia p95 y calidad medida. Con una recomendación al final.", "", False, ""),
            (N, "RAG para hechos, fine-tuning para forma", "", "Si el modelo no sabe un dato, dale contexto; no lo entrenes. El fine-tuning es para tono, formato y jerga.", "Ojo", False, ""),
            (N, "El único benchmark que importa es el tuyo", "", "Que un modelo lidere una tabla pública no dice nada sobre tus manuales en español. Construye tu eval set antes de elegir modelo.", "Ojo", False, ""),
        ],
    },
    {
        "orden": 5,
        "kicker": "Desde el mes 1",
        "titulo": "Inglés, portafolio y mercado",
        "subtitulo": "Corre en paralelo todo el año",
        "duracion": "12 meses",
        "horas": "~5 horas/semana",
        "color": "#c2703d",
        "paralela": True,
        "objetivo": "Que al terminar el mes 12 existan un IELTS rendido, tres proyectos públicos y un flujo de aplicaciones abierto. Esto no se hace al final: se hace desde el primer día.",
        "items": [
            (C, "Inglés técnico y de entrevistas", "Práctica diaria", "Una hora al día, todos los días. Es la variable que más determina el sueldo final y la que más se pospone.", "Inglés", False, ""),
            (C, "Preparación IELTS Academic 7.0+", "IELTS oficial", "Estrategia por sección y simulacros cronometrados. Reserva la fecha del examen con seis meses de anticipación: eso te obliga.", "IELTS", True, "https://ielts.org/take-a-test/preparation-resources"),
            (C, "Machine Learning System Design Interview", "ByteByteGo", "El formato de entrevista que define tu nivel y tu banda salarial. Practícalo desde el mes 6, no en el 12.", "Entrevistas", True, "https://bytebytego.com/"),
            (C, "NeetCode 150", "NeetCode", "Las entrevistas de ML siguen teniendo una ronda de algoritmos. Dos problemas por semana, sostenido, basta.", "Algoritmos", True, "https://neetcode.io/practice"),
            (C, "Cómo leer un paper", "S. Keshav", "El método de tres pasadas, en dos páginas. Después, una hora fija por semana en arXiv.", "Papers", True, "https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf"),
            (E, "Tres repos públicos pulidos", "", "RUL sobre C-MAPSS, el servicio desplegado y el asistente RAG. Con README, diagrama, tests y resultados. Tres bien hechos ganan a diez a medias.", "", False, ""),
            (E, "Un artículo técnico al mes, en inglés", "", "Sobre lo que construiste ese mes. Es portafolio y práctica de escritura al mismo tiempo.", "", False, ""),
            (E, "Perfil de Hugging Face con un modelo publicado", "", "Un modelo con su model card. Los reclutadores técnicos de IA sí lo revisan.", "", False, "https://huggingface.co/new"),
            (E, "LinkedIn y CV en formato del país destino", "", "Sin foto, orientado a logros cuantificables, con el nicho al frente: mantenimiento predictivo y confiabilidad industrial.", "", False, ""),
            (E, "Cinco aplicaciones dirigidas por semana, desde el mes 9", "", "Dirigidas: minería, energía, manufactura, industrial IoT. No al puesto genérico de 'Data Scientist'.", "", False, ""),
            (E, "IELTS rendido y evaluación de credenciales iniciada", "", "WES para Canadá o Engineers Australia. Los trámites tardan meses: empiézalos antes de tener la oferta.", "", False, ""),
            (N, "Verifica visas en las fuentes oficiales", "", "Los requisitos cambian seguido. Solo canada.ca e immi.homeaffairs.gov.au valen; nada de blogs de agencias.", "Ojo", False, "https://www.canada.ca/en/immigration-refugees-citizenship.html"),
            (N, "Especialízate en el cruce, no en el centro", "", "AI/ML Engineers genéricos hay miles. Que entiendan vibración, horómetros y confiabilidad, una decena. Ahí está tu precio.", "Estrategia", False, ""),
            (N, "Aplica antes de sentirte listo", "", "Las vacantes listan requisitos aspiracionales. Con el 60 % y proyectos demostrables ya pasas el filtro.", "Estrategia", False, ""),
        ],
    },
]


class Command(BaseCommand):
    help = "Carga la ruta enfocada de AI/ML Engineer industrial (12 meses, una sola carrera)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quitar",
            action="store_true",
            help="Borra la ruta enfocada entera. No toca el catálogo completo.",
        )

    @transaction.atomic
    def handle(self, *args, **opciones):
        enfocada = Etapa.objects.filter(ruta=Etapa.Ruta.ENFOCADA)

        if opciones["quitar"]:
            borradas, _ = enfocada.delete()
            self.stdout.write(
                self.style.WARNING(f"Ruta enfocada borrada ({borradas} registros).")
            )
            return

        nuevos = 0
        for datos in RUTA:
            items = datos.pop("items")
            etapa, _ = Etapa.objects.update_or_create(
                ruta=Etapa.Ruta.ENFOCADA, orden=datos["orden"], defaults=datos
            )
            datos["items"] = items  # por si el comando corre dos veces en la misma sesión

            for i, fila in enumerate(items):
                tipo, titulo, fuente, detalle, etiqueta = fila[:5]
                en_ingles = fila[5] if len(fila) > 5 else False
                url = fila[6] if len(fila) > 6 else ""
                obj, creado = Item.objects.get_or_create(
                    etapa=etapa,
                    titulo=titulo,
                    defaults={
                        "tipo": tipo,
                        "fuente": fuente,
                        "detalle": detalle,
                        "etiqueta": etiqueta,
                        "en_ingles": en_ingles,
                        "url": url,
                        "orden": i,
                    },
                )
                nuevos += creado
                if not creado and url and obj.url != url:
                    obj.url = url
                    obj.save(update_fields=["url"])

        total = Item.objects.filter(etapa__ruta=Etapa.Ruta.ENFOCADA).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Ruta enfocada lista: {enfocada.count()} etapas, {total} items "
                f"({nuevos} nuevos)."
            )
        )
