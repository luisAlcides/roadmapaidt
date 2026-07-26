# Railway no ejecuta una fase `release:` como Heroku, y durante el build la red
# privada (postgres.railway.internal) todavía no resuelve. Por eso las
# migraciones y la carga de contenido van aquí, en el arranque: es el primer
# momento en que el servicio puede hablar con Postgres.
web: python manage.py esperar_db && python manage.py migrate --noinput && python manage.py cargar_roadmap && python manage.py cargar_extras && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
