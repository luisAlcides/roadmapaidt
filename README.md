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

```bash
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_roadmap     # carga el contenido del PDF
python manage.py runserver
```

Queda en http://127.0.0.1:8000/. Sin `DATABASE_URL` usa SQLite.

Para entrar al admin: `python manage.py createsuperuser`.

### El comando `cargar_roadmap`

Es idempotente: se puede correr las veces que sea sin duplicar items ni perder
lo que ya marcaste (identifica cada item por etapa + título). Con `--reset`
borra todo y vuelve a empezar de cero — ahí sí pierdes el progreso.

## Deploy en Railway

1. Sube el repo a GitHub.
2. En Railway: **New Project → Deploy from GitHub repo** y elige este repo.
3. En el mismo proyecto: **New → Database → Add PostgreSQL**. Railway inyecta
   `DATABASE_URL` automáticamente en el servicio web.
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

El `Procfile` corre `migrate` y `cargar_roadmap` en cada release, así que la
primera vez la base queda poblada sola. `railway.json` define el build
(`collectstatic`), el arranque con gunicorn y el healthcheck en `/`.

Los estáticos los sirve WhiteNoise, así que no hace falta S3 ni CDN.

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
