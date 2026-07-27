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
            "Fundamentals of Data Engineering",
            "Joe Reis y Matt Housley",
            "El mapa completo del oficio antes de meterte en herramientas "
            "sueltas. Léelo en paralelo a la etapa 1 y sabrás por qué existe "
            "cada pieza que vas a instalar.",
            "Referencia",
            True,
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
    ],
    4: [
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
                "La telemetría son series de tiempo (marcas de tiempo + sensor + valor). "
                "TimescaleDB se instala sobre el Postgres que ya conoces y permite "
                "hacer consultas analíticas ultra rápidas sobre millones de filas.",
                "Bases Datos",
            ),
            (
                C,
                "Monitoreo Industrial con Grafana y Prometheus",
                "Documentación oficial",
                "Creación de tableros de control en tiempo real para visualizar series de tiempo de sensores e infraestructura de datos.",
                "Grafana",
            ),
            (
                E,
                "Pipeline de streaming simulado con Kafka",
                "",
                "Un script en Python que simule sensores de temperatura de motor "
                "publicando en Kafka, procesado en tiempo real para generar alertas "
                "de sobrecalentamiento instantáneas.",
                "",
            ),
            (
                C,
                "AWS o Azure Data Lake: Almacenamiento a escala industrial",
                "Rutas oficiales cloud",
                "Aprende a usar S3 (AWS) o ADLS Gen2 (Azure) para guardar los datos "
                "crudos (raw data) antes de cargarlos al warehouse. Es el estándar de "
                "la industria minera actual.",
                "Nube",
            ),
            (
                L,
                "Designing Cloud Data Platforms",
                "Danil Zburivsky y Lyuba Hooby",
                "Libro de referencia sobre cómo diseñar arquitecturas de datos en la "
                "nube modernas que sean escalables y seguras. Muy valorado en empresas "
                "multinacionales.",
                "Arquitect.",
                True,
            ),
            (
                N,
                "Edge Computing vs Cloud Computing en minería",
                "",
                "En minas a rajo abierto, la conectividad satelital o LTE puede "
                "caerse. Entender cuándo correr un modelo de predicción dentro del "
                "mismo camión (Edge) y cuándo mandar los datos a la nube es clave.",
                "Diseño",
            )
        ]
    },
]


class Command(BaseCommand):
    help = "Agrega contenido complementario (no viene del PDF) al roadmap."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quitar",
            action="store_true",
            help="Borra todo lo generado y deja solo el roadmap del PDF.",
        )

    @transaction.atomic
    def handle(self, *args, **opciones):
        if opciones["quitar"]:
            n, _ = Item.objects.filter(generado=True).delete()
            Etapa.objects.filter(orden__gte=5, items__isnull=True).delete()
            self.stdout.write(self.style.WARNING(f"Quitados {n} items generados."))
            return

        if not Etapa.objects.exists():
            self.stdout.write(
                self.style.ERROR("Corre primero: python manage.py cargar_roadmap")
            )
            return

        nuevos = 0

        for orden, items in EXTRAS_POR_ETAPA.items():
            etapa = Etapa.objects.filter(orden=orden).first()
            if not etapa:
                continue
            base = (etapa.items.order_by("-orden").first().orden or 0) + 1
            nuevos += self._crear_items(etapa, items, base)

        for datos in ETAPAS_NUEVAS:
            items = datos["items"]
            etapa, _ = Etapa.objects.update_or_create(
                orden=datos["orden"],
                defaults={k: v for k, v in datos.items() if k != "items"},
            )
            nuevos += self._crear_items(etapa, items, 0)

        self.stdout.write(
            self.style.SUCCESS(
                f"Contenido complementario listo: {nuevos} items nuevos. "
                f"Total ahora: {Item.objects.count()} items en "
                f"{Etapa.objects.count()} etapas."
            )
        )

    def _crear_items(self, etapa, items, base):
        nuevos = 0
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
                    "orden": base + i,
                    "generado": True,
                },
            )
            nuevos += creado
        return nuevos
