"""
Settings del proyecto. Corre sobre PostgreSQL tanto en local como en Railway;
lo único que cambia entre los dos entornos son las variables de entorno.
"""

import os
import sys
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# En local lee el .env; en Railway las variables ya vienen del entorno.
load_dotenv(BASE_DIR / ".env")

# collectstatic solo copia archivos al disco: no firma nada ni toca la base.
# Corre durante el build de Railway, donde las variables del servicio pueden no
# estar disponibles todavía, así que ahí no las exigimos. Cualquier otro
# comando —y sobre todo servir tráfico— sí las necesita de verdad.
ES_BUILD = "collectstatic" in sys.argv


def requerido(nombre, marcador=None):
    """Variable de entorno obligatoria: mejor fallar claro que arrancar roto."""
    valor = os.environ.get(nombre)
    if valor:
        return valor
    if ES_BUILD and marcador:
        return marcador
    raise ImproperlyConfigured(
        f"Falta la variable de entorno {nombre}. "
        "En local, cópiala en el archivo .env (ver .env.example). "
        "En Railway, defínela en Variables del servicio."
    )


# En build, una clave efímera que muere con el proceso y nunca sirve tráfico.
SECRET_KEY = requerido("SECRET_KEY", marcador=get_random_secret_key())

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".railway.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.railway.app"]

# Railway expone el dominio público en esta variable.
RAILWAY_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_DOMAIN}")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "roadmap",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# PostgreSQL siempre. En Railway, DATABASE_URL la inyecta el servicio de Postgres
# al enlazarlo; en local sale del .env.
DATABASES = {
    "default": dj_database_url.parse(
        # En build no hay a qué conectarse ni hace falta; el marcador nunca se usa
        # porque collectstatic no abre conexiones.
        requerido("DATABASE_URL", marcador="postgresql://build@localhost/build"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if not DATABASES["default"]["ENGINE"].endswith(("postgresql", "postgresql_psycopg2")):
    raise ImproperlyConfigured(
        "DATABASE_URL debe apuntar a PostgreSQL "
        "(postgresql://usuario:clave@host:puerto/base)."
    )


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    # Railway termina el TLS antes de llegar a gunicorn.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Una hora: conservador a propósito, HSTS es difícil de revertir.
    SECURE_HSTS_SECONDS = 3600
