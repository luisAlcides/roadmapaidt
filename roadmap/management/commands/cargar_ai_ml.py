"""Ruta especializada de AI/ML Engineer, con enlace directo a cada recurso.

El PDF original y `cargar_extras` te dejan como Data Engineer con una capa de ML
encima. Esto es lo otro: el camino de quien vive de construir y operar modelos.
Las fuentes salen de donde realmente está el material bueno —Stanford, MIT,
fast.ai, Karpathy, Hugging Face, DeepLearning.AI, DataTalksClub, papers— y no
solo de Platzi y Udemy. Casi todo es gratuito; lo que no lo es, va marcado.

Cada fila lleva su URL. Los cursos y papers apuntan a la página oficial; los
libros, a su sitio gratuito cuando existe y, si no, a su ficha en Open Library
para que decidas dónde comprarlo o pedirlo prestado.

Todo entra como `generado=True` y se puede borrar entero con
`python manage.py cargar_ai_ml --quitar`.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from roadmap.models import Etapa, Item

C, L, E, N = Item.Tipo.CURSO, Item.Tipo.LIBRO, Item.Tipo.ENTREGABLE, Item.Tipo.NOTA

OL = "https://openlibrary.org/search?q="

# (tipo, título, fuente, detalle, etiqueta, en_inglés, url)
EXTRAS_POR_ETAPA = {
    0: [
        (C, "Essence of Linear Algebra", "3Blue1Brown (YouTube)", "La intuición geométrica de vectores, matrices y autovalores. Ver esto antes de cualquier curso de ML te ahorra meses de fórmulas huecas.", "Matemáticas", True, "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"),
        (C, "Essence of Calculus", "3Blue1Brown (YouTube)", "Derivadas, regla de la cadena y gradientes explicados visualmente: es literalmente lo que hace backpropagation.", "Matemáticas", True, "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr"),
        (C, "Statistics Fundamentals", "StatQuest (Josh Starmer)", "Distribuciones, p-values, sesgo-varianza y validación cruzada en videos cortos y sin misticismo.", "Estadística", True, "https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9"),
        (C, "Machine Learning Crash Course", "Google Developers", "Curso oficial de Google: unas 15 horas, ejercicios interactivos y un glosario de ML que sirve de referencia permanente.", "Fundamentos", True, "https://developers.google.com/machine-learning/crash-course"),
        (C, "Kaggle Learn: Python, Pandas e Intro to ML", "Kaggle", "Micro-cursos de 3-5 horas con notebooks ejecutables. La forma más rápida de tener manos sobre teclado.", "Práctica", True, "https://www.kaggle.com/learn"),
        (C, "Git y GitHub para trabajo en equipo", "Platzi", "Ramas, PRs, rebase y resolución de conflictos: sin esto no puedes colaborar en ningún repo de ML serio.", "Git", False, "https://platzi.com/cursos/git-github/"),
        (C, "Testing en Python con pytest", "Real Python", "Tests unitarios y fixtures. Un modelo sin tests en el preprocesamiento es una bomba de tiempo.", "Calidad", True, "https://realpython.com/pytest-python-testing/"),
        (C, "Type hints, mypy y código Python mantenible", "mypy docs + Ruff", "Anotaciones de tipo y linters. La diferencia entre un notebook y software de producción.", "Python", True, "https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html"),
        (E, "Entorno reproducible: uv + Docker + Makefile", "", "Un template propio de proyecto ML que clones en cada experimento nuevo: dependencias fijadas, seed fija, comandos estandarizados.", "", False, "https://docs.astral.sh/uv/"),
        (N, "La matemática se aprende programándola", "", "No leas álgebra lineal en abstracto: implementa la multiplicación de matrices en NumPy puro y grafica lo que hace. La intuición viene del código.", "Método", False, ""),

        (L, "Mathematics for Machine Learning", "Deisenroth, Faisal y Ong", "El puente formal entre el álgebra lineal de la universidad y lo que usan los papers de ML. PDF gratuito.", "Matemáticas", True, "https://mml-book.github.io/"),
        (L, "Think Stats", "Allen B. Downey", "Estadística enseñada con código Python en vez de tablas. Gratuito en el sitio del autor.", "Estadística", True, "https://allendowney.github.io/ThinkStats/"),
        (L, "Practical Statistics for Data Scientists", "Peter y Andrew Bruce", "Los conceptos estadísticos que realmente usas en el trabajo, sin el relleno de un curso académico.", "Estadística", True, OL + "Practical+Statistics+for+Data+Scientists"),
        (L, "Fluent Python", "Luciano Ramalho", "Python profundo: generadores, descriptores, asyncio. El salto de escribir scripts a escribir librerías.", "Python", True, OL + "Fluent+Python"),
        (L, "Why Machines Learn", "Anil Ananthaswamy", "La matemática elegante detrás del aprendizaje automático, contada como historia intelectual.", "Divulgación", True, OL + "Why+Machines+Learn"),
    ],
    2: [
        (C, "Practical Deep Learning for Coders (Parte 1)", "fast.ai — Jeremy Howard", "El curso top-down: entrenas un clasificador de imágenes en la primera lección y bajas a la teoría después. Gratuito.", "Deep Learning", True, "https://course.fast.ai/"),
        (C, "CS229: Machine Learning", "Stanford", "El curso clásico con toda la derivación matemática: regresión, SVM, EM, teoría del aprendizaje. Notas y videos abiertos.", "Fundamentos", True, "https://cs229.stanford.edu/"),
        (C, "Machine Learning Specialization", "DeepLearning.AI / Coursera", "La versión moderna y accesible del CS229 en tres cursos. Audit gratis, certificado de pago.", "Fundamentos", True, "https://www.deeplearning.ai/courses/machine-learning-specialization/"),
        (C, "Introduction to Machine Learning for Coders", "fast.ai", "Random forests desde cero, interpretación de modelos y validación honesta con datos tabulares.", "Tabular", True, "https://course18.fast.ai/ml"),
        (C, "Dos competencias de Kaggle completas hasta el leaderboard", "Kaggle", "No para ganar: para aprender validación cruzada real, leakage, ensambles y a leer soluciones ajenas.", "Práctica", True, "https://www.kaggle.com/competitions"),
        (C, "Gradient boosting a fondo: XGBoost, LightGBM y CatBoost", "Documentación oficial + StatQuest", "El algoritmo que gana en datos tabulares —que es el 90 % de la industria—. Tuning, early stopping y manejo de categóricas.", "Tabular", True, "https://xgboost.readthedocs.io/en/stable/tutorials/model.html"),
        (C, "Machine Learning en Producción (MLEP)", "DeepLearning.AI / Coursera", "El ciclo de vida completo: definición del problema, datos, modelado y despliegue. Andrew Ng con enfoque de ingeniería.", "MLOps", True, "https://www.deeplearning.ai/courses/machine-learning-in-production/"),
        (C, "Imbalanced learning y métricas más allá del accuracy", "imbalanced-learn", "SMOTE, class weights, precision-recall AUC. En mantenimiento predictivo las fallas son el 1 % de tus filas.", "Métricas", True, "https://imbalanced-learn.org/stable/user_guide.html"),
        (C, "Probabilistic Machine Learning", "Kevin Murphy", "Visión bayesiana unificada de todo el ML. Denso, pero es la referencia moderna. PDFs gratuitos.", "Estadística", True, "https://probml.github.io/pml-book/"),
        (E, "Baseline honesto antes que modelo complejo", "", "Para cada problema: escribe primero la regla heurística tonta y su métrica. Si tu red neuronal no la supera, no tienes modelo.", "", False, ""),
        (E, "Model card de tu modelo de fallas", "", "Documento de una página: datos de entrenamiento, métricas por segmento, limitaciones conocidas y cuándo NO usarlo.", "", False, "https://huggingface.co/docs/hub/model-cards"),
        (N, "Data leakage: el error que arruina proyectos", "", "Si tu AUC es 0.99, no eres un genio: estás filtrando futuro en el pasado. Revisa cada feature preguntando '¿esto existía al momento de predecir?'.", "Ojo", False, ""),

        (L, "Designing Machine Learning Systems", "Chip Huyen", "El libro que convierte científicos de datos en ingenieros: datos, features, despliegue, monitoreo y organización.", "ML Systems", True, "https://huyenchip.com/books/"),
        (L, "Machine Learning Engineering", "Andriy Burkov", "El proceso completo de un proyecto ML del mundo real, con los errores que nadie te cuenta. Lectura libre en el sitio.", "ML Systems", True, "http://www.mlebook.com/wiki/doku.php"),
        (L, "The Hundred-Page Machine Learning Book", "Andriy Burkov", "Todo el campo condensado con rigor. Ideal para repasar antes de una entrevista.", "Referencia", True, "https://themlbook.com/"),
        (L, "Interpretable Machine Learning", "Christoph Molnar", "SHAP, LIME, PDP y modelos intrínsecamente interpretables. Gratuito online y obligatorio si un supervisor debe confiar en tu predicción.", "Explicabilidad", True, "https://christophm.github.io/interpretable-ml-book/"),
        (L, "Approaching (Almost) Any Machine Learning Problem", "Abhishek Thakur", "Recetario práctico de un Kaggle Grandmaster: validación, encoding, tuning y ensambles.", "Práctica", True, OL + "Approaching+Almost+Any+Machine+Learning+Problem"),
        (L, "Pattern Recognition and Machine Learning", "Christopher Bishop", "El tratado bayesiano clásico. Difícil, pero es la fuente de la que beben los papers. PDF liberado por Microsoft.", "Estadística", True, "https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/"),
        (L, "Causal Inference: The Mixtape", "Scott Cunningham", "Diferencias-en-diferencias, variables instrumentales y regresión discontinua. Gratuito online.", "Causalidad", True, "https://mixtape.scunning.com/"),
        (L, "The Book of Why", "Judea Pearl", "Por qué la estadística tradicional no puede responder '¿qué pasa si intervengo?' y cómo los grafos causales sí.", "Causalidad", True, OL + "The+Book+of+Why"),
    ],
    3: [
        (C, "Neural Networks: Zero to Hero", "Andrej Karpathy (YouTube)", "Construyes micrograd, luego un modelo de lenguaje y terminas escribiendo GPT desde cero. El mejor material gratuito que existe sobre el tema.", "Deep Learning", True, "https://karpathy.ai/zero-to-hero.html"),
        (C, "Hugging Face LLM Course", "Hugging Face", "Transformers, tokenizers, datasets y fine-tuning con la librería que usa toda la industria. Gratuito y práctico.", "NLP", True, "https://huggingface.co/learn/llm-course"),
        (C, "CS224N: NLP with Deep Learning", "Stanford", "De word2vec a transformers y LLMs, con rigor académico y assignments públicos.", "NLP", True, "https://web.stanford.edu/class/cs224n/"),
        (C, "Cursos cortos de DeepLearning.AI (LangChain, RAG, agentes)", "DeepLearning.AI", "Decenas de cursos de una hora, gratuitos, hechos con LangChain, LlamaIndex, Anthropic y otros. Directo al código.", "LLM Apps", True, "https://www.deeplearning.ai/short-courses/"),
        (C, "Prompt Engineering Interactive Tutorial", "Anthropic", "Curso oficial de Anthropic: estructura de prompts, few-shot, chain of thought y uso de herramientas.", "Prompting", True, "https://github.com/anthropics/prompt-eng-interactive-tutorial"),
        (C, "Anthropic Cookbook: recetas de producción", "Anthropic", "Notebooks ejecutables de RAG, tool use, extracción estructurada y evaluación con la API de Claude.", "LLM Apps", True, "https://github.com/anthropics/anthropic-cookbook"),
        (C, "Model Context Protocol (MCP): servidores y clientes", "Anthropic / MCP docs", "El estándar abierto para conectar LLMs a herramientas y datos. Se está volviendo requisito en vacantes de AI Engineer.", "Agentes", True, "https://modelcontextprotocol.io/"),
        (C, "Tool use y function calling en producción", "Anthropic docs", "Definición de esquemas, manejo de errores del modelo y bucles agénticos que no se salen de control.", "Agentes", True, "https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview"),
        (C, "LLM Bootcamp", "Full Stack Deep Learning", "Bootcamp grabado y gratuito: prompt engineering, UX de LLMs, evaluación y despliegue de aplicaciones reales.", "LLM Apps", True, "https://fullstackdeeplearning.com/llm-bootcamp/"),
        (C, "DSPy: programar LLMs en vez de escribir prompts", "Stanford NLP", "Optimización automática de prompts y pipelines declarativos. La alternativa seria al prompt artesanal.", "LLM Apps", True, "https://dspy.ai/"),
        (C, "RAGAS: evaluación cuantitativa de sistemas RAG", "Ragas docs", "Faithfulness, answer relevancy y context precision. Métricas para dejar de discutir 'a mí me parece que responde mejor'.", "Evaluación", True, "https://docs.ragas.io/"),
        (E, "Un RAG evaluado, no solo demostrado", "", "Set de 50 preguntas con respuesta esperada, métricas de RAGAS corriendo en CI y comparación de al menos dos estrategias de chunking.", "", False, ""),
        (N, "El benchmark que importa es el tuyo", "", "Que un modelo lidere MMLU no dice nada sobre tus manuales de mantenimiento en español. Construye tu eval set antes de elegir modelo.", "Ojo", False, ""),

        (L, "Build a Large Language Model (From Scratch)", "Sebastian Raschka", "Implementas tokenizer, atención, pre-entrenamiento y fine-tuning línea por línea en PyTorch. El repo con todo el código es público.", "LLMs", True, "https://github.com/rasbt/LLMs-from-scratch"),
        (L, "Hands-On Large Language Models", "Jay Alammar y Maarten Grootendorst", "Ilustrado y práctico: embeddings, búsqueda semántica, fine-tuning y agentes. Notebooks abiertos.", "LLMs", True, "https://github.com/HandsOnLLM/Hands-On-Large-Language-Models"),
        (L, "The Illustrated Transformer", "Jay Alammar", "La explicación visual que hace que la atención por fin tenga sentido. Gratuita en su blog.", "Transformers", True, "https://jalammar.github.io/illustrated-transformer/"),
        (L, "Prompt Engineering for LLMs", "John Berryman y Albert Ziegler", "Diseño de contexto y evaluación de prompts desde la experiencia de construir GitHub Copilot.", "Prompting", True, OL + "Prompt+Engineering+for+LLMs"),
        (L, "Constitutional AI y alignment: lecturas de Anthropic", "Anthropic Research", "RLHF, Constitutional AI y red teaming. Si despliegas un asistente en una operación, esto es parte del trabajo.", "Seguridad", True, "https://www.anthropic.com/research"),
    ],
}

# Etapas nuevas al final del recorrido.
ETAPAS_NUEVAS = [
    {
        "orden": 8,
        "kicker": "Etapa 8 · AI/ML · generada",
        "titulo": "Deep Learning desde los cimientos",
        "subtitulo": "Entender la red, no solo llamarla",
        "duracion": "4 meses",
        "horas": "~120 horas",
        "color": "#7b4fa8",
        "objetivo": "Poder implementar backpropagation, una CNN y un Transformer desde cero en PyTorch, y saber por qué un entrenamiento no converge.",
        "items": [
            (C, "PyTorch: tensores, autograd y ciclo de entrenamiento", "PyTorch — Learn the Basics", "El tutorial oficial hecho a mano, no copiado. Todo lo demás en deep learning se construye sobre esto.", "PyTorch", True, "https://pytorch.org/tutorials/beginner/basics/intro.html"),
            (C, "Deep Learning Specialization", "DeepLearning.AI / Coursera", "Los cinco cursos de Andrew Ng: redes densas, regularización, optimización, CNN y secuencias.", "Deep Learning", True, "https://www.deeplearning.ai/courses/deep-learning-specialization/"),
            (C, "Practical Deep Learning for Coders (Parte 2)", "fast.ai", "Reimplementas Stable Diffusion desde cero. La parte 2 es donde el curso se vuelve realmente profundo.", "Deep Learning", True, "https://course.fast.ai/Lessons/part2.html"),
            (C, "MIT 6.S191: Introduction to Deep Learning", "MIT", "Curso intensivo anual, siempre actualizado con lo último del campo. Videos y labs gratuitos.", "Deep Learning", True, "http://introtodeeplearning.com/"),
            (C, "CS231n: Deep Learning for Computer Vision", "Stanford", "Convoluciones, arquitecturas y detección. Las notas del curso siguen siendo la mejor explicación escrita de backprop.", "Visión", True, "https://cs231n.github.io/"),
            (C, "Dive into Deep Learning (d2l.ai)", "Zhang, Lipton, Li y Smola", "Libro-curso interactivo con código en PyTorch, JAX y TensorFlow. Gratuito y exhaustivo.", "Deep Learning", True, "https://d2l.ai/"),
            (C, "The Annotated Transformer", "Harvard NLP", "El paper 'Attention Is All You Need' acompañado de su implementación comentada línea por línea.", "Transformers", True, "https://nlp.seas.harvard.edu/annotated-transformer/"),
            (C, "Attention Is All You Need (paper original)", "Vaswani et al. — arXiv", "El paper que fundó la era actual. Léelo después del Annotated Transformer y vuelve a él cada año.", "Papers", True, "https://arxiv.org/abs/1706.03762"),
            (C, "Optimización de entrenamiento: mixed precision y checkpointing", "PyTorch docs", "Cómo entrenar modelos que no caben en tu GPU. Requisito para trabajar con hardware modesto.", "Entrenamiento", True, "https://pytorch.org/docs/stable/notes/amp_examples.html"),
            (C, "Weights & Biases: experiment tracking y sweeps", "W&B Courses", "Registro de experimentos, búsqueda de hiperparámetros y reportes compartibles. Gratuito para uso personal.", "Tooling", True, "https://www.wandb.courses/"),
            (C, "A Recipe for Training Neural Networks", "Andrej Karpathy (blog)", "El ensayo sobre cómo depurar entrenamientos. Vale más que muchos cursos completos.", "Método", True, "https://karpathy.github.io/2019/04/25/recipe/"),
            (E, "micrograd propio: autograd en 150 líneas", "", "Reimplementa el motor de diferenciación automática de Karpathy sin mirar el código. Si puedes, entiendes backprop de verdad.", "", False, "https://github.com/karpathy/micrograd"),
            (E, "Detector de anomalías en vibración con un autoencoder", "", "Entrena sobre señales sanas de tus equipos y usa el error de reconstrucción como score de anomalía. Compara contra un baseline estadístico.", "", False, ""),
            (E, "Un Transformer entrenado por ti sobre tus propios datos", "", "Aunque sea diminuto: sobre bitácoras de mantenimiento. Documenta curva de pérdida, hiperparámetros y qué aprendió.", "", False, "https://github.com/karpathy/nanoGPT"),
            (N, "Debuggear redes es un oficio aparte", "", "Sobreajusta primero a un batch de 10 ejemplos. Si no llega a pérdida cero, el bug está en tu código, no en el modelo.", "Método", False, ""),
            (N, "El paper es la documentación real", "", "Acostúmbrate a leer arXiv con Papers with Code al lado. En este campo los libros llegan dos años tarde.", "Método", False, "https://paperswithcode.com/"),

            (L, "Understanding Deep Learning", "Simon J.D. Prince", "Las mejores figuras del campo. PDF gratuito, con notebooks y slides por capítulo.", "Deep Learning", True, "https://udlbook.github.io/udlbook/"),
            (L, "Deep Learning (libro de Goodfellow, versión web)", "Goodfellow, Bengio y Courville", "El texto canónico de redes profundas, leíble gratis en su sitio oficial.", "Deep Learning", True, "https://www.deeplearningbook.org/"),
            (L, "Deep Learning with PyTorch", "Stevens, Antiga y Viehmann", "Escrito por el equipo de PyTorch: del tensor a un proyecto médico completo. PDF gratuito en pytorch.org.", "PyTorch", True, "https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf"),
            (L, "The Little Book of Deep Learning", "François Fleuret", "Todo el campo en unas 170 páginas en formato móvil. Perfecto para repasar en el bus.", "Referencia", True, "https://fleuret.org/francois/lbdl.html"),
            (L, "Deep Learning: Foundations and Concepts", "Christopher y Hugh Bishop", "La actualización 2024 del clásico de Bishop, ya con transformers y modelos de difusión.", "Deep Learning", True, "https://www.bishopbook.com/"),
            (L, "Deep Learning for Coders with fastai and PyTorch", "Jeremy Howard y Sylvain Gugger", "El libro del curso fast.ai. Los notebooks completos están en GitHub.", "Deep Learning", True, "https://github.com/fastai/fastbook"),
            (L, "Machine Learning with PyTorch and Scikit-Learn", "Sebastian Raschka", "Puente entre ML clásico y deep learning con el mismo código y las mismas convenciones.", "Deep Learning", True, "https://github.com/rasbt/machine-learning-book"),
            (L, "The Deep Learning Revolution", "Terrence Sejnowski", "Historia contada por dentro: de las redes de los ochenta al boom actual.", "Divulgación", True, OL + "The+Deep+Learning+Revolution"),
            (L, "Genius Makers", "Cade Metz", "La crónica periodística de Hinton, LeCun, Bengio y la carrera industrial por la IA.", "Divulgación", True, OL + "Genius+Makers"),
            (L, "El algoritmo maestro", "Pedro Domingos", "Las cinco tribus del machine learning y la búsqueda de un algoritmo universal de aprendizaje.", "Divulgación", False, OL + "El+algoritmo+maestro"),
        ],
    },
    {
        "orden": 9,
        "kicker": "Etapa 9 · AI/ML · generada",
        "titulo": "MLOps: modelos que viven en producción",
        "subtitulo": "El 90 % del trabajo real",
        "duracion": "3 meses",
        "horas": "~90 horas",
        "color": "#2f7d4f",
        "objetivo": "Llevar un modelo de un notebook a un servicio versionado, monitoreado, con reentrenamiento automático y rollback.",
        "items": [
            (C, "MLOps Zoomcamp", "DataTalksClub", "Nueve semanas gratuitas con proyecto evaluado: tracking, orquestación, despliegue y monitoreo. El mejor curso gratis de MLOps.", "MLOps", True, "https://github.com/DataTalksClub/mlops-zoomcamp"),
            (C, "Made With ML — MLOps Course", "Goku Mohandas", "De experimentación a producción con testing, CI/CD y Ray. Código abierto y muy bien escrito.", "MLOps", True, "https://madewithml.com/"),
            (C, "Full Stack Deep Learning", "FSDL", "Lo que ningún curso de ML cubre: gestión de datos, troubleshooting, despliegue, monitoreo y ética.", "ML Systems", True, "https://fullstackdeeplearning.com/course/"),
            (C, "MLflow: tracking, registry y despliegue", "MLflow docs", "Tracking, artefactos, stages (staging/production) y comparación de runs. La pieza mínima de todo stack MLOps.", "Tracking", True, "https://mlflow.org/docs/latest/"),
            (C, "Feature stores: Feast en la práctica", "Feast docs", "Consistencia entre features de entrenamiento y de inferencia. La causa número uno de modelos que fallan en producción.", "Features", True, "https://docs.feast.dev/"),
            (C, "Serving de modelos con BentoML", "BentoML docs", "Empaquetado, versionado y APIs de inferencia con batching adaptativo, sin escribir el boilerplate a mano.", "Serving", True, "https://docs.bentoml.com/"),
            (C, "FastAPI para servicios de inferencia", "FastAPI docs", "Validación con Pydantic, async y documentación automática. El estándar de facto para exponer un modelo.", "Serving", True, "https://fastapi.tiangolo.com/"),
            (C, "KServe: modelos sobre Kubernetes", "KServe docs", "Autoescalado a cero, canary deployments y GPUs compartidas. Nivel intermedio, no hace falta ser SRE.", "Kubernetes", True, "https://kserve.github.io/website/"),
            (C, "Monitoreo de drift con Evidently AI", "Evidently docs", "Data drift, concept drift y degradación silenciosa. Un modelo que no se monitorea es un modelo que ya falló.", "Monitoreo", True, "https://docs.evidentlyai.com/"),
            (C, "Versionado de datos y pipelines con DVC", "DVC docs", "Git para datasets y pipelines reproducibles. Sin esto no puedes explicar por qué el modelo de marzo daba otra cosa.", "Versionado", True, "https://dvc.org/doc"),
            (C, "CI/CD para ML con GitHub Actions", "GitHub docs", "Tests de datos, entrenamiento automático en cada PR y despliegue con aprobación manual.", "CI/CD", True, "https://docs.github.com/en/actions"),
            (C, "AWS Certified Machine Learning Engineer – Associate", "AWS", "Una certificación cloud de ML pesa en los filtros de reclutadores en Australia y Canadá. De pago.", "Certificación", True, "https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/"),
            (C, "Professional Machine Learning Engineer", "Google Cloud", "La alternativa de GCP, con ruta de estudio gratuita en Google Cloud Skills Boost.", "Certificación", True, "https://cloud.google.com/learn/certification/machine-learning-engineer"),
            (C, "Optimización de inferencia con ONNX Runtime", "ONNX Runtime docs", "Cuantización y aceleración de gráficos: 2-10x menos latencia sin reentrenar. Crítico si el modelo corre en el borde, dentro de la mina.", "Inferencia", True, "https://onnxruntime.ai/docs/"),
            (E, "Servicio de predicción de fallas desplegado end-to-end", "", "API con FastAPI, imagen Docker, tests, tracking en MLflow, dashboard de drift y pipeline de reentrenamiento programado.", "", False, ""),
            (E, "Runbook de incidentes del modelo", "", "Qué hacer cuando el modelo empieza a alucinar predicciones: cómo detectarlo, a quién avisar, cómo hacer rollback en menos de 15 minutos.", "", False, ""),
            (E, "Prueba de carga de tu endpoint con k6", "", "p95 de latencia, throughput máximo y comportamiento bajo saturación, documentado en el README.", "", False, "https://grafana.com/docs/k6/latest/"),
            (N, "Un modelo sin plan de reentrenamiento es deuda técnica", "", "Define desde el día uno cada cuánto se reentrena, con qué datos y qué métrica dispara el reentrenamiento automático.", "Ojo", False, ""),
            (N, "Shadow mode antes que producción", "", "Corre el modelo nuevo en paralelo al viejo, sin que decida nada, durante dos semanas. Compara. Después promueve.", "Método", False, ""),

            (L, "Machine Learning Design Patterns", "Lakshmanan, Robinson y Munn", "30 patrones repetibles para problemas de diseño de sistemas ML, con código en GitHub.", "ML Systems", True, "https://github.com/GoogleCloudPlatform/ml-design-patterns"),
            (L, "Building Machine Learning Powered Applications", "Emmanuel Ameisen", "De la idea al producto: definición del problema, iteración y despliegue con criterio de producto.", "ML Systems", True, "https://github.com/hundredblocks/ml-powered-applications"),
            (L, "Practical MLOps", "Noah Gift y Alfredo Deza", "Operacionalización de modelos en AWS, Azure y GCP con enfoque DevOps.", "MLOps", True, OL + "Practical+MLOps"),
            (L, "Reliable Machine Learning", "Cathy Chen et al.", "SRE aplicado a ML: SLOs para modelos, on-call e incidentes de datos. Escrito por gente de Google.", "SRE", True, OL + "Reliable+Machine+Learning"),
            (L, "Site Reliability Engineering (libro completo, gratis)", "Google", "El libro que definió el oficio de operar sistemas. Lectura íntegra en el sitio de Google SRE.", "SRE", True, "https://sre.google/sre-book/table-of-contents/"),
            (L, "Data Mesh", "Zhamak Dehghani", "Descentralización del dato como producto. Relevante cuando el ML depende de datos de varias áreas.", "Arquitectura", True, OL + "Data+Mesh+Dehghani"),
            (L, "The Phoenix Project", "Gene Kim", "Novela sobre DevOps que explica, mejor que cualquier manual, por qué los despliegues manuales matan equipos.", "DevOps", True, OL + "The+Phoenix+Project"),
            (L, "Release It!", "Michael Nygard", "Patrones de estabilidad —circuit breakers, bulkheads, timeouts— para servicios que no pueden caerse.", "Arquitectura", True, OL + "Release+It+Nygard"),
            (L, "Kubernetes Up & Running", "Brendan Burns et al.", "Fundamentos de Kubernetes por uno de sus creadores.", "Kubernetes", True, OL + "Kubernetes+Up+and+Running"),
            (L, "Observability Engineering", "Charity Majors et al.", "Trazas, métricas y logs con alta cardinalidad. Cómo saber qué está pasando dentro de tu sistema.", "Monitoreo", True, OL + "Observability+Engineering"),
        ],
    },
    {
        "orden": 10,
        "kicker": "Etapa 10 · AI/ML · generada",
        "titulo": "LLM Engineering avanzado",
        "subtitulo": "Modelos grandes, presupuesto pequeño",
        "duracion": "3 meses",
        "horas": "~90 horas",
        "color": "#b5543f",
        "objetivo": "Adaptar, servir y evaluar modelos de lenguaje propios: fine-tuning eficiente, cuantización, evals rigurosas y agentes confiables.",
        "items": [
            (C, "LLM Course (Maxime Labonne)", "GitHub — open source", "El roadmap más completo de LLM engineering: fundamentos, fine-tuning, cuantización y despliegue, con notebooks Colab.", "LLMs", True, "https://github.com/mlabonne/llm-course"),
            (C, "Fine-tuning con LoRA, QLoRA y PEFT", "Hugging Face PEFT", "Adaptar un modelo de 7B en una sola GPU de consumo. La técnica que hace viable el fine-tuning sin presupuesto corporativo.", "Fine-Tuning", True, "https://huggingface.co/docs/peft/index"),
            (C, "Alignment práctico: SFT y DPO con TRL", "Hugging Face TRL", "De instruction tuning a preferencias humanas. DPO es hoy la vía práctica; RLHF, la conceptual.", "Alignment", True, "https://huggingface.co/docs/trl/index"),
            (C, "Fine-tuning rápido con Unsloth", "Unsloth docs", "2-5x más rápido y con menos memoria que el stack estándar. Notebooks listos para Colab gratuito.", "Fine-Tuning", True, "https://docs.unsloth.ai/"),
            (C, "Cuantización: GGUF, AWQ, GPTQ y bitsandbytes", "llama.cpp", "Correr modelos grandes en hardware modesto. Compromisos reales entre bits, calidad y velocidad.", "Cuantización", True, "https://github.com/ggml-org/llama.cpp"),
            (C, "Serving de LLMs con vLLM: PagedAttention y batching continuo", "vLLM docs", "El motor de inferencia estándar de la industria. Throughput muy superior a transformers puro.", "Inferencia", True, "https://docs.vllm.ai/"),
            (C, "Ollama: correr modelos locales sin fricción", "Ollama", "La vía más corta para tener un LLM privado en tu máquina o en un servidor de la operación.", "Local AI", True, "https://ollama.com/"),
            (C, "Evaluación de LLMs con promptfoo", "promptfoo docs", "Suites de evaluación versionadas, comparación de modelos y red teaming, ejecutables en CI.", "Evaluación", True, "https://www.promptfoo.dev/docs/intro/"),
            (C, "OWASP Top 10 for LLM Applications", "OWASP", "Prompt injection, fuga de datos y los demás riesgos específicos de aplicaciones LLM, con mitigaciones. Gratuito y citable.", "Seguridad", True, "https://genai.owasp.org/llm-top-10/"),
            (C, "Observabilidad de LLMs con Langfuse", "Langfuse docs", "Trazar cada llamada, su costo, latencia y calidad. Depurar un agente sin trazas es imposible.", "Observabilidad", True, "https://langfuse.com/docs"),
            (C, "Embeddings: elegir modelo con el benchmark MTEB", "Hugging Face MTEB", "Comparar embeddings por dominio e idioma antes de casarte con uno. Mejora el RAG más que cambiar de LLM.", "Embeddings", True, "https://huggingface.co/spaces/mteb/leaderboard"),
            (C, "Sentence-Transformers: entrenar tu propio embedding", "SBERT docs", "Fine-tuning con pares del negocio para que 'chumacera' y 'rodamiento' queden cerca en tu espacio vectorial.", "Embeddings", True, "https://sbert.net/"),
            (C, "Reranking y búsqueda híbrida", "Cohere Rerank / BM25", "Retrieval en dos etapas. Es la mejora con mejor relación esfuerzo-resultado en cualquier RAG.", "RAG", True, "https://docs.cohere.com/docs/rerank-overview"),
            (C, "Building effective agents", "Anthropic Engineering", "Cuándo un flujo determinista gana a un agente, y cómo diseñar el que sí hace falta. Lectura obligatoria.", "Agentes", True, "https://www.anthropic.com/engineering/building-effective-agents"),
            (C, "Small Language Models para el borde: Gemma y Qwen", "Hugging Face", "Modelos de 1B-3B corriendo dentro de la mina, sin conectividad y sin enviar datos afuera.", "Edge AI", True, "https://huggingface.co/models?pipeline_tag=text-generation&sort=trending"),
            (E, "Un modelo fine-tuneado con datos de tu operación", "", "QLoRA sobre bitácoras de mantenimiento reales anonimizadas, con eval set propio y comparación honesta contra el modelo base.", "", False, ""),
            (E, "Eval suite versionada corriendo en CI", "", "50-100 casos con respuesta esperada, métricas automáticas y umbral que bloquea el merge si baja la calidad.", "", False, ""),
            (E, "Reporte de costo y latencia por caso de uso", "", "Tabla comparando API comercial vs. modelo propio en vLLM: costo por 1000 consultas, p95 y calidad. Con recomendación.", "", False, ""),
            (N, "Fine-tuning enseña forma, RAG aporta hechos", "", "Si el modelo no sabe un dato, no lo arregles con fine-tuning: dale contexto. El fine-tuning es para tono, formato y jerga del dominio.", "Ojo", False, ""),
            (N, "Todo lo que aprendas aquí caduca en 12 meses", "", "Aprende los principios —atención, contexto, evaluación, costo— y trata las herramientas como intercambiables. Lo son.", "Método", False, ""),

            (L, "LLM Engineer's Handbook", "Paul Iusztin y Maxime Labonne", "Ciclo completo de un producto LLM: datos, fine-tuning, RAG, despliegue y monitoreo, en un solo proyecto. Repo público.", "LLMs", True, "https://github.com/PacktPublishing/LLM-Engineers-Handbook"),
            (L, "AI Engineering", "Chip Huyen", "El libro de referencia del rol: modelos fundacionales, evaluación, RAG, agentes y costos.", "AI Engineering", True, "https://huyenchip.com/books/"),
            (L, "Natural Language Processing with Transformers", "Tunstall, von Werra y Wolf", "Escrito por el equipo de Hugging Face: fine-tuning, destilación, cuantización y modelos multilingües. Notebooks abiertos.", "NLP", True, "https://github.com/nlp-with-transformers/notebooks"),
            (L, "Speech and Language Processing (3.ª ed., borrador gratuito)", "Jurafsky y Martin", "La biblia del NLP, actualizada con LLMs y disponible en PDF desde Stanford.", "NLP", True, "https://web.stanford.edu/~jurafsky/slp3/"),
            (L, "Designing Large Language Model Applications", "Suhas Pai", "Arquitectura de aplicaciones LLM: decisiones de diseño, trade-offs y patrones de producción.", "LLM Apps", True, OL + "Designing+Large+Language+Model+Applications"),
            (L, "Generative Deep Learning", "David Foster", "VAE, GAN, difusión y modelos autoregresivos explicados con código. Repo público.", "Generative AI", True, "https://github.com/davidADSP/Generative_Deep_Learning_2nd_Edition"),
            (L, "The Alignment Problem", "Brian Christian", "Cómo hacer que los sistemas de IA hagan lo que queremos. Técnico y filosófico a la vez.", "Alignment", True, OL + "The+Alignment+Problem"),
            (L, "Human Compatible", "Stuart Russell", "El coautor del libro canónico de IA sobre cómo diseñar máquinas que sigan siendo controlables.", "Alignment", True, OL + "Human+Compatible"),
            (L, "Co-Intelligence: Living and Working with AI", "Ethan Mollick", "Cómo cambia el trabajo real con LLMs de por medio. Útil para vender proyectos internamente.", "Trabajo", True, OL + "Co-Intelligence+Mollick"),
            (L, "Atlas of AI", "Kate Crawford", "El costo material de la IA: minería de litio, energía y trabajo humano. Ironía útil para quien viene de minería.", "Sociedad", True, OL + "Atlas+of+AI"),
        ],
    },
    {
        "orden": 11,
        "kicker": "Etapa 11 · AI/ML · generada",
        "titulo": "Papers, entrevistas y el salto al mercado AI",
        "subtitulo": "Demostrar que sabes",
        "duracion": "En paralelo · últimos 5 meses",
        "horas": "~70 horas",
        "color": "#8a6d3b",
        "objetivo": "Leer literatura técnica con criterio, aprobar entrevistas de ML system design y llegar al mercado con evidencia pública.",
        "items": [
            (C, "How to Read a Paper (método de tres pasadas)", "S. Keshav — Waterloo", "Ensayo de dos páginas que cambia tu relación con arXiv. Léelo hoy mismo.", "Método", True, "https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf"),
            (C, "Papers with Code: papers con su implementación al lado", "Papers with Code", "Cómo pasar de leer un abstract a correr el código en una tarde.", "Papers", True, "https://paperswithcode.com/"),
            (C, "arXiv cs.LG y cs.CL: lectura semanal dirigida", "arXiv", "Una hora fija a la semana leyendo abstracts del área. Sostenido un año, te vuelve la persona informada del equipo.", "Papers", True, "https://arxiv.org/list/cs.LG/recent"),
            (C, "Dataset C-MAPSS de degradación de turbofan", "NASA Prognostics Data Repository", "El benchmark clásico de vida útil remanente (RUL). Tu terreno: úsalo para tu proyecto insignia.", "Dominio", True, "https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/"),
            (C, "Machine Learning System Design Interview", "ByteByteGo (Aminian y Xu)", "El formato de entrevista que define tu nivel y tu salario en empresas grandes.", "Entrevistas", True, "https://bytebytego.com/"),
            (C, "Grokking the Machine Learning Interview", "Educative.io", "Casos completos —ranking, búsqueda, recomendación— con la estructura de respuesta esperada. De pago.", "Entrevistas", True, "https://www.educative.io/courses/grokking-the-machine-learning-interview"),
            (C, "NeetCode 150 en Python", "NeetCode", "Los problemas de algoritmos que sí aparecen. Las entrevistas de ML siguen incluyendo una ronda de coding.", "Algoritmos", True, "https://neetcode.io/practice"),
            (C, "Contribuir a un proyecto open source de ML", "GitHub", "Un PR aceptado en scikit-learn, Hugging Face o LangChain vale más que diez certificados en un CV internacional.", "Open Source", True, "https://scikit-learn.org/stable/developers/contributing.html"),
            (C, "Comunicación técnica: explicar un modelo a un gerente de mina", "Práctica propia", "Traducir precision-recall a paradas evitadas y dólares. La habilidad que más se paga y menos se enseña.", "Comunicación", False, ""),
            (E, "Un paper implementado y publicado en GitHub", "", "Reproduce los resultados de un paper de PHM sobre datos públicos (C-MAPSS o similar), documenta las diferencias y publícalo.", "", False, ""),
            (E, "Blog técnico con seis artículos en inglés", "", "Un artículo por mes explicando algo que construiste. Es tu portafolio real y tu práctica de inglés escrito a la vez.", "", False, ""),
            (E, "Cuarenta preguntas de entrevista ML respondidas por escrito", "", "Desde bias-variance hasta diseño de un sistema de detección de anomalías. Escríbelas: escribir revela lo que no entiendes.", "", False, ""),
            (E, "Perfil de Hugging Face con un modelo y un dataset publicados", "", "Un modelo fine-tuneado con model card y un dataset limpio. Los reclutadores técnicos de IA sí lo revisan.", "", False, "https://huggingface.co/new"),
            (N, "Especialízate en el cruce, no en el centro", "", "Hay miles de AI Engineers genéricos. AI Engineers que entienden vibración, horómetros y confiabilidad minera hay una decena. Ahí está tu oferta.", "Estrategia", False, ""),
            (N, "Aplica antes de sentirte listo", "", "Las vacantes de AI/ML listan requisitos aspiracionales. Cumplir el 60 % y tener proyectos demostrables basta para pasar el filtro.", "Estrategia", False, ""),

            (L, "Machine Learning System Design Interview", "Ali Aminian y Alex Xu", "Siete casos de diseño resueltos con el marco de respuesta que esperan los entrevistadores.", "Entrevistas", True, OL + "Machine+Learning+System+Design+Interview"),
            (L, "Deep Learning Interviews", "Shlomo Kashani", "Cientos de problemas resueltos de matemática, ML clásico y deep learning. Gratuito en arXiv.", "Entrevistas", True, "https://arxiv.org/abs/2201.00650"),
            (L, "Ace the Data Science Interview", "Kevin Huo y Nick Singh", "Preguntas de SQL, estadística, ML y producto, con soluciones.", "Entrevistas", True, OL + "Ace+the+Data+Science+Interview"),
            (L, "Artificial Intelligence: A Modern Approach", "Stuart Russell y Peter Norvig", "El libro canónico de IA. No lo lees entero: lo consultas toda la carrera.", "Referencia", True, "https://aima.cs.berkeley.edu/"),
            (L, "The Staff Engineer's Path", "Tanya Reilly", "Cómo crece un ingeniero técnico sin volverse gerente: influencia, alcance y decisiones de arquitectura.", "Carrera", True, OL + "The+Staff+Engineer%27s+Path"),
            (L, "Staff Engineer: Leadership Beyond the Management Track", "Will Larson", "Los arquetipos de ingeniero senior y cómo llegar a ellos. Lectura libre en staffeng.com.", "Carrera", True, "https://staffeng.com/book/"),
            (L, "A Philosophy of Software Design", "John Ousterhout", "Complejidad, profundidad de módulos y diseño incremental. Corto y de los mejores libros de software escritos.", "Diseño", True, OL + "A+Philosophy+of+Software+Design"),
            (L, "The Art of Doing Science and Engineering", "Richard Hamming", "Las conferencias de Hamming sobre cómo hacer trabajo que importe y elegir problemas grandes.", "Carrera", True, OL + "The+Art+of+Doing+Science+and+Engineering"),
            (L, "So Good They Can't Ignore You", "Cal Newport", "El capital de carrera se construye con habilidades raras y valiosas, no siguiendo la pasión.", "Carrera", True, OL + "So+Good+They+Can%27t+Ignore+You"),
            (L, "Deep Work", "Cal Newport", "Concentración sostenida como ventaja competitiva. Aplicable directo a un plan de estudio de dos años.", "Productividad", True, OL + "Deep+Work+Newport"),
            (L, "Prediction Machines", "Agrawal, Gans y Goldfarb", "La IA vista como una caída en el costo de predecir. El marco económico para justificar proyectos ante dirección.", "Negocio", True, OL + "Prediction+Machines"),
            (L, "Competing in the Age of AI", "Marco Iansiti y Karim Lakhani", "Cómo se reorganizan las empresas alrededor de datos y modelos.", "Negocio", True, OL + "Competing+in+the+Age+of+AI"),
            (L, "The Worlds I See", "Fei-Fei Li", "Memorias de la creadora de ImageNet: inmigración, ciencia y la construcción de la visión por computadora moderna.", "Divulgación", True, OL + "The+Worlds+I+See"),
            (L, "Chip War", "Chris Miller", "La guerra geopolítica por los semiconductores que hacen posible todo esto.", "Geopolítica", True, OL + "Chip+War"),
        ],
    },
]


class Command(BaseCommand):
    help = "Carga la ruta especializada de AI/ML Engineer (etapas 8-11 y extras en 0, 2 y 3)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quitar",
            action="store_true",
            help="Borra solo el contenido cargado por este comando.",
        )

    @staticmethod
    def _campos(fila):
        tipo, titulo, fuente, detalle, etiqueta = fila[:5]
        en_ingles = fila[5] if len(fila) > 5 else False
        url = fila[6] if len(fila) > 6 else ""
        return {
            "tipo": tipo,
            "titulo": titulo,
            "fuente": fuente,
            "detalle": detalle,
            "etiqueta": etiqueta,
            "en_ingles": en_ingles,
            "url": url,
        }

    @transaction.atomic
    def handle(self, *args, **opciones):
        ordenes_nuevas = [e["orden"] for e in ETAPAS_NUEVAS]

        if opciones["quitar"]:
            titulos = [
                fila[1] for items in EXTRAS_POR_ETAPA.values() for fila in items
            ]
            borrados_i, _ = Item.objects.filter(
                generado=True, titulo__in=titulos
            ).delete()
            borrados_e, _ = Etapa.objects.filter(orden__in=ordenes_nuevas).delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Eliminados {borrados_i} items extras y {borrados_e} etapas AI/ML."
                )
            )
            return

        nuevos, actualizados = 0, 0

        # 1. Etapas nuevas
        for datos in ETAPAS_NUEVAS:
            items = datos.pop("items")
            etapa, _ = Etapa.objects.update_or_create(
                orden=datos["orden"], defaults=datos
            )
            datos["items"] = items

            for i, fila in enumerate(items):
                campos = self._campos(fila)
                titulo = campos.pop("titulo")
                obj, creado = Item.objects.get_or_create(
                    etapa=etapa,
                    titulo=titulo,
                    defaults={**campos, "generado": True, "orden": i},
                )
                nuevos += creado
                # Si ya existía sin enlace, se lo ponemos.
                if not creado and campos["url"] and obj.url != campos["url"]:
                    obj.url = campos["url"]
                    obj.save(update_fields=["url"])
                    actualizados += 1

        # 2. Extras sobre etapas existentes
        for orden_etapa, items in EXTRAS_POR_ETAPA.items():
            try:
                etapa = Etapa.objects.get(orden=orden_etapa)
            except Etapa.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Etapa {orden_etapa} no existe todavía; sus extras se omiten."
                    )
                )
                continue

            ultimo = etapa.items.order_by("-orden").first()
            base_orden = (ultimo.orden + 1) if ultimo else 0

            for offset, fila in enumerate(items):
                campos = self._campos(fila)
                titulo = campos.pop("titulo")
                obj, creado = Item.objects.get_or_create(
                    etapa=etapa,
                    titulo=titulo,
                    defaults={
                        **campos,
                        "generado": True,
                        "orden": base_orden + offset,
                    },
                )
                nuevos += creado
                if not creado and campos["url"] and obj.url != campos["url"]:
                    obj.url = campos["url"]
                    obj.save(update_fields=["url"])
                    actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Ruta AI/ML lista: {nuevos} items nuevos, {actualizados} enlaces "
                f"actualizados. Total ahora: {Item.objects.count()} items en "
                f"{Etapa.objects.count()} etapas."
            )
        )
