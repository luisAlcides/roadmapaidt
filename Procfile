release: python manage.py migrate --noinput && python manage.py cargar_roadmap
web: gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -
