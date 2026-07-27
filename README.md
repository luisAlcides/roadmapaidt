# Roadmap · De mantenimiento a ingeniería de datos e IA

App Django para seguir el plan de formación de 15–18 meses del PDF
`roadmap-data-ia-alcides.pdf`: cinco niveles, 65 items entre cursos, entregables,
libros y advertencias. Se marca lo que se va completando y se puede agregar lo
que falte.

## Qué hace

- **Mapa de niveles**: cada etapa es un nodo del recorrido; se ilumina cuando la
  empiezas y se marca con ✓ cuando la terminas.
- **Tachar items**: un clic marca y desmarca, sin recargar la página.
- **Agregar y borrar**: cursos, libros, entregables o notas propias en cualquier
  etapa, y etapas nuevas al final del recorrido.
- **Progreso**: global en la barra superior y por etapa en cada tarjeta.
- **Admin de Django** en `/admin/` para ediciones en lote.

## Correr en local

Corre sobre PostgreSQL, igual que en producción. Necesitas un Postgres andando.

```bash
# 1. Base de datos (una sola vez)
sudo -u postgres psql \
  -c "CREATE ROLE roadmap LOGIN PASSWORD 'roadmap_local';" \
  -c "CREATE DATABASE roadmap OWNER roadmap;"

# 2. Configuración
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
# pega esa clave en SECRET_KEY dentro de .env

# 3. App
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_roadmap     # carga el contenido del PDF
python manage.py cargar_extras      # agrega el contenido complementario
python manage.py cargar_ai_ml       # agrega la ruta especializada de AI/ML
python manage.py runserver
```

Queda en http://127.0.0.1:8000/.

`SECRET_KEY` y `DATABASE_URL` son obligatorias: si falta alguna, la app no
arranca y dice cuál. El `.env` lo lee python-dotenv y está en `.gitignore`.

Para entrar al admin: `python manage.py createsuperuser`.

### Los tres comandos de contenido

`cargar_roadmap` carga el plan tal como está en el PDF: 5 etapas, 65 items.

`cargar_extras` agrega contenido complementario que **no** viene del PDF —
herramientas que las vacantes piden y el documento no menciona (window
functions, Docker Compose, tests de datos, MLflow, pgvector, evaluación de RAG),
más dos etapas nuevas: portafolio y el trámite de salida. Todo queda marcado con
la etiqueta **Extra** en la interfaz y con `generado=True` en la base, así que se
distingue de un vistazo y se borra entero con `cargar_extras --quitar` sin tocar
lo del PDF ni tu progreso.

`cargar_ai_ml` agrega la ruta especializada de **AI/ML Engineer**, con fuentes
que van más allá de Platzi y Udemy: Stanford (CS229, CS224N, CS231n), MIT 6.S191,
fast.ai, Neural Networks Zero to Hero de Karpathy, Hugging Face, DeepLearning.AI,
MLOps Zoomcamp, Full Stack Deep Learning, documentación oficial y papers de arXiv.
Son cuatro etapas nuevas —deep learning desde los cimientos, MLOps, LLM
engineering avanzado, y papers/entrevistas— más extras en las etapas 0, 2 y 3.
Cada item trae su **enlace directo**: los cursos y papers apuntan a la página
oficial, y los libros a su versión gratuita cuando existe o a Open Library si no.
Casi todo el material es gratuito; lo que no lo es va marcado. Se borra entero con
`cargar_ai_ml --quitar` sin tocar lo demás.

Los tres son idempotentes: se pueden correr las veces que sea sin duplicar items
ni perder lo que ya marcaste (identifican cada item por etapa + título). Solo
`cargar_roadmap --reset` borra todo y empieza de cero — ahí sí pierdes el
progreso.

Un detalle entre los dos comandos de extras: `cargar_ai_ml --quitar` borra solo
lo suyo, pero `cargar_extras --quitar` es más viejo y arrasa con **todo** lo
marcado `generado=True`, incluida la ruta de AI/ML. Si eso pasa, se recupera
volviendo a correr `cargar_ai_ml`.

Ojo con la etapa 6: los requisitos de visa y las evaluaciones de credenciales
cambian seguido. Lo que dice ahí es orientativo; confirma siempre en `canada.ca`
y en `immi.homeaffairs.gov.au`.

## Deploy en Railway

1. Sube el repo a GitHub.
2. En Railway: **New Project → Deploy from GitHub repo** y elige este repo.
3. En el mismo proyecto: **New → Database → Add PostgreSQL**. Railway inyecta
   `DATABASE_URL` automáticamente en el servicio web — no la definas a mano.
4. En el servicio web, pestaña **Variables**, agrega:

   | Variable | Valor |
   |---|---|
   | `SECRET_KEY` | una clave larga y aleatoria (ver abajo) |
   | `DEBUG` | `False` |

   Genera la clave con:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
   ```
5. En **Settings → Networking**, pulsa **Generate Domain**.

Las migraciones y la carga de contenido corren **al arrancar el servicio**, no
en el build: durante el build la red privada de Railway todavía no resuelve
`postgres.railway.internal`. El arranque completo es:

```
esperar_db → migrate → cargar_roadmap → cargar_extras → cargar_ai_ml → gunicorn
```

Todo eso es idempotente, así que se repite sin daño en cada deploy y la primera
vez deja la base poblada sola. `railway.json` define el build
(`collectstatic`, lo único que sí necesita estar en build), el start command y
el healthcheck en `/`.

Los estáticos los sirve WhiteNoise, así que no hace falta S3 ni CDN.

### Si el deploy falla

**`ImproperlyConfigured: Falta la variable de entorno SECRET_KEY`**
No la definiste en **Variables** del servicio web, o la pusiste en el servicio
equivocado (tiene que ir en el web, no en el de Postgres). Va sin comillas.

**`Falta la variable de entorno DATABASE_URL`**
El servicio de Postgres no está enlazado al web. Agrégalo desde el mismo
proyecto con **New → Database → Add PostgreSQL**; Railway la inyecta sola.

**`failed to resolve host 'postgres.railway.internal'`**
Algo está intentando hablar con la base **durante el build**, donde la red
privada de Railway no existe todavía. Revisa en **Settings → Build** que el
*Custom Build Command* no incluya `migrate` — lo que la UI de Railway tenga
configurado tiene precedencia sobre `railway.json`. Las migraciones van en el
start command, no en el build.

Si aparece al arrancar y no en el build, suele ser que el Postgres está en otro
proyecto o en otro environment: la red privada solo conecta servicios del mismo
environment.

**`password authentication failed`**
Pasa en local, no en Railway: el rol de Postgres no existe todavía o la clave
del `.env` no coincide con la que le pusiste. Revisa el paso 1 de arriba.

Nota: `collectstatic` corre durante el build, donde las variables del servicio
pueden no estar disponibles. Como solo copia archivos, `settings.py` lo deja
pasar con valores efímeros. Todo lo demás —incluido servir tráfico— sí exige las
variables reales.

## Estructura

```
config/          settings, urls, wsgi
roadmap/
  models.py      Etapa e Item
  views.py       índice, alternar, crear, borrar
  management/commands/cargar_roadmap.py   el contenido del PDF
templates/roadmap/index.html              toda la interfaz (CSS y JS incluidos)
```

## Nota sobre acceso

La app no tiene login: quien tenga la URL puede marcar y editar. Para un
roadmap personal en un dominio que no se comparte, alcanza. Si en algún momento
quieres cerrarlo, el camino corto es envolver las vistas en
`@login_required` y usar el login que ya trae Django.
