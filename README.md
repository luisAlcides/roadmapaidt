# Roadmap · De mantenimiento a AI/ML Engineer

App Django para seguir un plan de formación de doce meses. Se marca lo que se va
completando y se puede agregar lo que falte.

## Qué es

Una sola ruta: **AI/ML Engineer con especialidad industrial**, doce meses,
seis etapas, 83 items entre cursos, entregables y advertencias. Cada item trae
enlace directo al recurso.

El catálogo viejo —los cuatro oficios del PDF más los complementos— se podó:
dispersaba el esfuerzo en cuatro carreras a la vez y ninguna quedaba
demostrable. Lo único que se conservó de él es la biblioteca.

**La biblioteca son ~270 libros** en una etapa aparte que no se dibuja en el
mapa: no tienen fecha ni orden, se leen cuando toca. Por eso la barra de
progreso de arriba mide solo el plan de doce meses, y los libros llevan su
propio contador.

Si algún día quieres el catálogo de vuelta, sigue reproducible con
`cargar_roadmap`, `cargar_extras` y `cargar_ai_ml` — lo que no vuelve son las
marcas de completado que tenía.

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
python manage.py cargar_ruta_enfocada   # el plan de doce meses
python manage.py cargar_biblioteca      # los ~270 libros
python manage.py runserver
```

Queda en http://127.0.0.1:8000/.

`SECRET_KEY` y `DATABASE_URL` son obligatorias: si falta alguna, la app no
arranca y dice cuál. El `.env` lo lee python-dotenv y está en `.gitignore`.

Para entrar al admin: `python manage.py createsuperuser`.

### Los comandos de contenido

| Comando | Qué hace |
|---|---|
| `cargar_ruta_enfocada` | Las seis etapas del plan de doce meses. |
| `cargar_biblioteca` | Los ~270 libros, en su etapa oculta. |
| `podar_catalogo --si` | Borra el catálogo viejo si existe, rescatando sus libros primero. No hace nada si ya se podó. |
| `cargar_roadmap`, `cargar_extras`, `cargar_ai_ml` | El catálogo viejo. Quedan disponibles pero no se corren en el despliegue. |

Todos son idempotentes: se pueden correr las veces que sea sin duplicar items
ni perder lo que ya marcaste (identifican cada item por etapa + título).
`podar_catalogo` es la excepción en un sentido: es destructivo por diseño y
pide confirmación salvo que se le pase `--si`.

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
esperar_db → migrate → cargar_ruta_enfocada → cargar_biblioteca →
podar_catalogo --si → gunicorn
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
  management/commands/cargar_ruta_enfocada.py  el plan de doce meses
  management/commands/cargar_biblioteca.py     los libros
  management/commands/podar_catalogo.py        borra el catálogo viejo
templates/roadmap/index.html              toda la interfaz (CSS y JS incluidos)
```

## Nota sobre acceso

La app no tiene login: quien tenga la URL puede marcar y editar. Para un
roadmap personal en un dominio que no se comparte, alcanza. Si en algún momento
quieres cerrarlo, el camino corto es envolver las vistas en
`@login_required` y usar el login que ya trae Django.
