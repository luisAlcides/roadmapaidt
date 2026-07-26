"""Espera a que Postgres acepte conexiones antes de seguir.

La red privada de Railway tarda unos segundos en levantar cuando arranca el
contenedor. Sin esta espera, el `migrate` del arranque falla de vez en cuando
con un error de DNS —postgres.railway.internal no resuelve todavía— y el
deploy se cae por algo que se resuelve solo en tres segundos.
"""

import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Espera a que la base de datos esté disponible."

    def add_arguments(self, parser):
        parser.add_argument("--intentos", type=int, default=12)
        parser.add_argument("--espera", type=float, default=2.5)

    def handle(self, *args, **opciones):
        intentos, espera = opciones["intentos"], opciones["espera"]

        for intento in range(1, intentos + 1):
            try:
                connections["default"].cursor().close()
            except OperationalError as e:
                if intento == intentos:
                    self.stderr.write(
                        self.style.ERROR(
                            f"La base no respondió tras {intentos} intentos: {e}"
                        )
                    )
                    raise
                self.stdout.write(
                    f"Base no disponible (intento {intento}/{intentos}), "
                    f"reintentando en {espera}s…"
                )
                time.sleep(espera)
            else:
                self.stdout.write(self.style.SUCCESS("Base disponible."))
                return
