"""Carga el roadmap del PDF en la base de datos.

Idempotente: vuelve a crear las etapas base sin tocar lo que agregaste tú,
salvo que pases --reset. Los items ya existentes conservan su estado de
completado — se identifican por (etapa, titulo).
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from roadmap.models import Etapa, Item

C, L, E, N = Item.Tipo.CURSO, Item.Tipo.LIBRO, Item.Tipo.ENTREGABLE, Item.Tipo.NOTA

ROADMAP = [
    {
        "orden": 0,
        "kicker": "Etapa 0",
        "titulo": "Nivelación",
        "subtitulo": "Cimientos",
        "duracion": "1–2 meses",
        "horas": "~50 horas",
        "color": "#6b8f71",
        "objetivo": (
            "Cerrar los dos huecos que bloquean todo lo demás —SQL serio y control "
            "de versiones— sin repetir lo que ya sabes."
        ),
        "items": [
            (C, "Curso de Git y GitHub", "Platzi", "", ""),
            (C, "Curso de Fundamentos de Bases de Datos y SQL", "Platzi", "", ""),
            (C, "Curso de PostgreSQL Aplicado a Ciencia de Datos", "Platzi", "", ""),
            (
                C,
                "Curso de Estadística Inferencial para Data Science e IA",
                "Platzi",
                "",
                "",
            ),
            (
                C,
                "The Complete SQL Bootcamp: Go from Zero to Hero",
                "Udemy · Jose Portilla",
                "Está montado sobre PostgreSQL y tiene mucho más ejercicio práctico "
                "que el equivalente de Platzi.",
                "",
            ),
            (
                N,
                "SÁLTATE: ruta de Fundamentos de Data Science y AI",
                "",
                "Python básico, Pandas, entornos con Anaconda, matemáticas "
                "introductorias. Ya lo tienes andando.",
                "Sáltate",
            ),
            (
                E,
                "Migrar reportes de mantenimiento a PostgreSQL",
                "",
                "De Excel/CSV a una base PostgreSQL con esquema propio: equipos, "
                "órdenes de trabajo, horómetros, eventos de falla, consumos. Sin esta "
                "base, las etapas siguientes no tienen sobre qué correr.",
                "",
            ),
            (
                L,
                "Hábitos atómicos",
                "James Clear",
                "Estudiar 5–10 h/semana con turnos largos no es un problema de "
                "motivación, es de diseño de sistema. Este libro es literalmente sobre eso.",
                "Hábitos",
            ),
            (
                L,
                "Ultraaprendizaje",
                "Scott Young",
                "Metodología para aprender por cuenta propia de forma agresiva y sin "
                "aula. Léelo al inicio, no al final: cambia cómo tomas los cursos que siguen.",
                "Aprendizaje",
            ),
            (
                L,
                "Meditaciones",
                "Marco Aurelio",
                "Escrito por alguien que trabajaba agotado y lejos de casa. Se lee en "
                "fragmentos de cinco minutos, que es exactamente el tiempo que tienes "
                "en un cambio de turno.",
                "Filosofía",
            ),
            (
                L,
                "Siddhartha",
                "Hermann Hesse",
                "Corto, de prosa muy simple en inglés, y trata sobre alguien que "
                "descubre que el conocimiento transmitido no sustituye a la experiencia "
                "propia. Buen primer libro completo en inglés.",
                "Ficción",
                True,
            ),
        ],
    },
    {
        "orden": 1,
        "kicker": "Etapa 1 · 40 % del perfil",
        "titulo": "Data Engineer",
        "subtitulo": "Sistemas y oficio",
        "duracion": "3–4 meses",
        "horas": "~100 horas",
        "color": "#c2703d",
        "objetivo": (
            "Tu hueco más grande y, paradójicamente, lo que más rápido te vuelve "
            "contratable. Un científico de datos que además construye la "
            "infraestructura vale el doble en una operación minera."
        ),
        "items": [
            (C, "Curso de Fundamentos de Ingeniería de Datos", "Platzi", "", ""),
            (C, "Curso de Docker", "Platzi", "", ""),
            (C, "Curso de Fundamentos de Apache Airflow", "Platzi", "", ""),
            (C, "Curso de Fundamentos de Spark para Big Data", "Platzi", "", ""),
            (C, "Curso de Databricks: Arquitectura Delta Lake", "Platzi", "", ""),
            (
                C,
                "Curso de Big Data y Machine Learning con Google Cloud Platform",
                "Platzi",
                "",
                "",
            ),
            (
                C,
                "Apache Airflow: The Hands-On Guide",
                "Udemy · Marc Lamberti",
                "Es el estándar de facto y bastante superior al curso equivalente de Platzi.",
                "",
            ),
            (
                C,
                "The Complete dbt (Data Build Tool) Bootcamp",
                "Udemy",
                "dbt no existe en el catálogo de Platzi y aparece en casi toda vacante "
                "de data engineer en Canadá y Australia. Es el hueco más caro de dejar abierto.",
                "",
            ),
            (
                N,
                "SÁLTATE: MongoDB, DynamoDB y Optimización de SQL Server",
                "",
                "El mundo minero-industrial corre sobre SQL relacional, bases de series "
                "temporales y Spark.",
                "Sáltate",
            ),
            (
                E,
                "Pipeline diario orquestado con Airflow",
                "",
                "Ingesta de telemetría de flota → Postgres / Delta Lake → "
                "transformaciones modeladas en dbt → tablero. Todo versionado en Git y "
                "corriendo en contenedores.",
                "",
            ),
            (
                L,
                "Deep Work",
                "Cal Newport",
                "Con 5–10 h semanales no puedes permitirte estudiar distraído. Newport "
                "escribe en inglés claro y directo; es un buen segundo libro en el idioma.",
                "Foco",
                True,
            ),
            (
                L,
                "Zen y el arte del mantenimiento de la motocicleta",
                "Robert Pirsig",
                "Un libro sobre qué significa la calidad, escrito desde el punto de "
                "vista de quien repara máquinas. Es el libro de esta lista que más habla "
                "de tu oficio actual, aunque no lo parezca.",
                "Filosofía",
            ),
            (
                L,
                "La psicología de los objetos cotidianos",
                "Don Norman",
                "Diseñar un pipeline o un tablero es diseñar algo que otro humano tiene "
                "que usar bajo presión. Norman te enseña a ver por qué las cosas fallan "
                "en manos del usuario.",
                "Conocim.",
            ),
            (
                L,
                "El Proyecto Phoenix",
                "Gene Kim",
                "Novela sobre una operación de TI en crisis. Es la mejor forma de "
                "entender por qué existen Docker, Airflow y el pensamiento DevOps antes "
                "de tocarlos. Se lee en un fin de semana.",
                "Ficción",
            ),
        ],
    },
    {
        "orden": 2,
        "kicker": "Etapa 2 · 40 % del perfil",
        "titulo": "Data Scientist / Machine Learning",
        "subtitulo": "Incertidumbre y juicio",
        "duracion": "4–5 meses",
        "horas": "~120 horas",
        "color": "#4a6fa5",
        "objetivo": (
            "Pasar del análisis descriptivo a la predicción de fallas, con el rigor "
            "estadístico que exige tomar decisiones de parada de equipo."
        ),
        "items": [
            (C, "Curso de Análisis Exploratorio de Datos", "Platzi", "", ""),
            (
                C,
                "Curso de Manejo de Datos Faltantes: Detección y Exploración",
                "Platzi",
                "No es relleno: la telemetría de sensores en mina llega con huecos "
                "permanentes, y ese manejo es literalmente la mitad del trabajo real.",
                "",
            ),
            (C, "Curso de Manejo de Datos Faltantes: Imputación", "Platzi", "", ""),
            (C, "Curso Profesional de Machine Learning con scikit-learn", "Platzi", "", ""),
            (
                C,
                "Curso de Decision Trees y Random Forest con Python y scikit-learn",
                "Platzi",
                "",
                "",
            ),
            (C, "Curso de MLOPS: Despliegue de Modelos de Machine Learning", "Platzi", "", ""),
            (
                C,
                "Feature Engineering for Machine Learning",
                "Udemy · Soledad Galli",
                "Lo más importante de esta etapa para datos de sensores.",
                "",
            ),
            (C, "Deployment of Machine Learning Models", "Udemy · Soledad Galli", "", ""),
            (
                C,
                "The Complete Guide to Time Series Analysis and Forecasting",
                "Udemy",
                "Indispensable para modelar degradación de componentes y vida útil remanente.",
                "",
            ),
            (
                N,
                "Deep learning: baja prioridad para ti",
                "",
                "Los cursos de TensorFlow y PyTorch de Platzi son buenos, pero en datos "
                "tabulares de mantenimiento XGBoost y LightGBM le ganan a las redes "
                "neuronales casi siempre. La excepción: si entras a análisis de "
                "vibraciones o inspección visual, ahí sí toma el Curso de Visión "
                "Artificial con Python.",
                "Prioridad",
            ),
            (
                E,
                "Capstone de predicción de fallas desplegado como API",
                "",
                "Con FastAPI dentro de un contenedor, con seguimiento de experimentos. "
                "No como notebook. La diferencia entre 'hice un modelo' y 'puse un modelo "
                "en producción' es la diferencia de salario.",
                "",
            ),
            (
                L,
                "Amplitud (Range)",
                "David Epstein",
                "La tesis defiende exactamente lo que estás intentando: que el que "
                "combina dominios le gana al ultraespecialista. Es el argumento que vas a "
                "necesitar para explicar tu propio perfil en una entrevista.",
                "Carrera",
                True,
            ),
            (
                L,
                "Antifrágil",
                "Nassim Taleb",
                "Fragilidad, redundancia, sistemas que mejoran bajo estrés. Es un libro "
                "de mantenimiento disfrazado de ensayo de riesgo; te dará vocabulario "
                "para pensar la confiabilidad de flota.",
                "Riesgo",
            ),
            (
                L,
                "Pensar rápido, pensar despacio",
                "Daniel Kahneman",
                "Catálogo de todas las formas en que tu intuición te va a engañar al "
                "leer datos. Es el complemento obligatorio de cualquier curso de estadística.",
                "Conocim.",
            ),
            (
                L,
                "Ficciones",
                "Jorge Luis Borges",
                "Lee primero 'Funes el memorioso': la historia de un hombre que recuerda "
                "absolutamente todo y por eso es incapaz de pensar. Es la mejor "
                "explicación que existe de por qué dato crudo no es conocimiento.",
                "Ficción",
            ),
        ],
    },
    {
        "orden": 3,
        "kicker": "Etapa 3 · 20 % del perfil",
        "titulo": "AI Engineer",
        "subtitulo": "Máquinas y escepticismo",
        "duracion": "3–4 meses",
        "horas": "~90 horas",
        "color": "#8b5fa8",
        "objetivo": (
            "Montar sistemas con LLM sobre la base ya construida. Es la capa que más "
            "rápido se vuelve obsoleta, por eso va al final y no al principio."
        ),
        "items": [
            (C, "Curso de Fundamentos de LLMs", "Platzi", "", ""),
            (C, "Curso de Configuración de APIs de LLMs", "Platzi", "", ""),
            (C, "Curso de FastAPI", "Platzi", "", ""),
            (C, "Curso de LangChain", "Platzi", "", ""),
            (
                C,
                "Curso de LangChain para Manejo y Recuperación de Documentos",
                "Platzi",
                "",
                "",
            ),
            (C, "Curso de RAG con Microsoft Azure", "Platzi", "", ""),
            (C, "Curso de Agentes AI", "Platzi", "", ""),
            (C, "Curso de MCP con Microsoft Azure", "Platzi", "", ""),
            (C, "Curso de Observabilidad de Agentes AI con LangSmith", "Platzi", "", ""),
            (
                C,
                "AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents",
                "Udemy · Ed Donner",
                "Recorrido de ocho semanas por el pipeline completo: RAG, fine-tuning "
                "con QLoRA, agentes y ocho aplicaciones que construyes y despliegas. Con "
                "RTX 5060 Ti puedes correr el fine-tuning localmente en vez de pagar nube.",
                "",
            ),
            (
                C,
                "LangGraph — Develop LLM Powered AI Agents",
                "Udemy · Eden Marco",
                "Solo si después quieres profundizar en orquestación de agentes.",
                "",
            ),
            (
                E,
                "RAG sobre manuales OEM + histórico de órdenes de trabajo",
                "",
                "Con un agente que consulte tu warehouse de Postgres y responda "
                "preguntas del tipo: «¿por qué el camión 214 lleva tres fallas de sistema "
                "hidráulico este trimestre y qué tienen en común?». Eso es un producto "
                "vendible, no un ejercicio.",
                "",
            ),
            (
                L,
                "El mundo y sus demonios",
                "Carl Sagan",
                "Un manual de detección de tonterías, y esta es la etapa donde más las "
                "vas a encontrar. El campo de la IA produce más humo que resultados; "
                "necesitas el filtro antes de entrar.",
                "Criterio",
            ),
            (
                L,
                "Vida 3.0",
                "Max Tegmark",
                "Panorama serio de hacia dónde puede ir la IA, escrito por un físico y "
                "no por un vendedor. Te da el marco general que los cursos técnicos no dan.",
                "Conocim.",
            ),
            (
                L,
                "Tecnópolis",
                "Neil Postman",
                "La crítica opuesta: qué pierde una sociedad cuando entrega su criterio "
                "a la tecnología. Léelo justo cuando estés más entusiasmado con los "
                "agentes; ese es el momento en que sirve.",
                "Filosofía",
            ),
            (
                L,
                "Klara y el Sol",
                "Kazuo Ishiguro",
                "Narrado por una máquina que intenta entender a las personas. Ishiguro "
                "escribe con frases cortas y vocabulario simple: de lo más accesible que "
                "hay en inglés para un nivel B1.",
                "Ficción",
                True,
            ),
        ],
    },
    {
        "orden": 4,
        "kicker": "En paralelo · desde el día uno",
        "titulo": "Inglés, negocio y salida",
        "subtitulo": "Todo el recorrido",
        "duracion": "15–18 meses",
        "horas": "2–3 h semanales",
        "color": "#3d5a80",
        "objetivo": (
            "Con nivel A2–B1 no calificas para roles en Australia ni en Canadá, y ambos "
            "países exigen IELTS para la visa de trabajo cualificado. Ninguna cantidad "
            "de cursos técnicos compensa este hueco."
        ),
        "items": [
            (
                C,
                "Platzi English Academy",
                "Platzi",
                "Rutas Inglés Intermedio B1 → Intermedio Alto B2 → Avanzado C1.",
                "Inglés",
            ),
            (
                C,
                "Curso de Inglés para el Uso de Inteligencia Artificial",
                "Platzi",
                "Vocabulario técnico específico, útil hacia la etapa 3.",
                "Inglés",
            ),
            (
                C,
                "Curso de Power BI",
                "Platzi",
                "No está en la ruta principal, pero la minería corre sobre Power BI. Te "
                "da valor visible en tu empresa actual mientras el resto del plan madura.",
                "Power BI",
            ),
            (C, "Curso de DAX para Power BI", "Platzi", "", "Power BI"),
            (
                N,
                "Un libro en inglés por etapa",
                "",
                "10–15 páginas diarias. Cuatro libros completos en 15 meses mueve el "
                "nivel más que cualquier app.",
                "Inglés",
            ),
            (
                L,
                "So Good They Can't Ignore You",
                "Cal Newport",
                "El antídoto contra «sigue tu pasión»: la libertad se compra con capital "
                "profesional escaso, no con entusiasmo. Es la justificación teórica de por "
                "qué este plan apuesta a un nicho y no a la generalidad.",
                "Carrera",
                True,
            ),
            (
                L,
                "La psicología del dinero",
                "Morgan Housel",
                "Sobre libertad financiera entendida como control del propio tiempo, que "
                "es lo que realmente estás buscando. Sin fórmulas mágicas ni promesas.",
                "Dinero",
            ),
            (
                L,
                "Sobre la brevedad de la vida",
                "Séneca",
                "Cincuenta páginas sobre cómo se nos va el tiempo trabajando para otros. "
                "Léelo una vez al año durante todo este proceso.",
                "Filosofía",
            ),
            (
                L,
                "Americanah",
                "Chimamanda Ngozi Adichie",
                "Sobre emigrar, adaptarse y lo que cuesta reconstruirse en otro país. Si "
                "el plan termina en Australia o Canadá, este libro te prepara para la "
                "parte que ningún roadmap técnico menciona.",
                "Ficción",
            ),
        ],
    },
]

# Camino mínimo si solo hubiera seis meses (página de cierre del PDF).
RUTA_COMPRIMIDA = [
    "Fundamentos de Ingeniería de Datos (Platzi)",
    "Docker (Platzi)",
    "Apache Airflow: The Hands-On Guide (Udemy · Lamberti)",
    "The Complete dbt Bootcamp (Udemy)",
    "Feature Engineering for Machine Learning (Udemy · Galli)",
    "MLOPS: Despliegue de Modelos (Platzi)",
]


class Command(BaseCommand):
    help = "Carga el roadmap del PDF en la base de datos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Borra todas las etapas e items antes de cargar (pierdes tu progreso).",
        )

    @transaction.atomic
    def handle(self, *args, **opciones):
        if opciones["reset"]:
            Etapa.objects.all().delete()
            self.stdout.write(self.style.WARNING("Etapas e items borrados."))

        nuevos = 0
        for datos in ROADMAP:
            items = datos.pop("items")
            etapa, _ = Etapa.objects.update_or_create(
                orden=datos["orden"], defaults=datos
            )
            datos["items"] = items  # el comando puede correr dos veces en la misma sesión

            for i, fila in enumerate(items):
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
                        "orden": i,
                    },
                )
                nuevos += creado

        self.stdout.write(
            self.style.SUCCESS(
                f"Roadmap cargado: {Etapa.objects.count()} etapas, "
                f"{Item.objects.count()} items ({nuevos} nuevos)."
            )
        )
