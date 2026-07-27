"""Deja solo la ruta enfocada, rescatando la biblioteca antes de borrar.

Los libros vivían repartidos por las etapas del catálogo. Si se borra el
catálogo sin más, se van con él. Este comando los mueve primero a la etapa
oculta de biblioteca —conservando lo que ya tuvieras marcado como leído— y
recién entonces borra las etapas del catálogo.

Es destructivo y no se puede deshacer: el contenido del catálogo se recupera
con `cargar_roadmap`, `cargar_extras` y `cargar_ai_ml`, pero las marcas de
completado de esos items se pierden. Por eso pide confirmación salvo que se
pase `--si`.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from roadmap.models import Etapa, Item

ORDEN_BIBLIOTECA = 99


class Command(BaseCommand):
    help = "Borra el catálogo completo y conserva sus libros en la biblioteca."

    def add_arguments(self, parser):
        parser.add_argument(
            "--si",
            action="store_true",
            help="No preguntar. Para usarlo en scripts de despliegue.",
        )

    @transaction.atomic
    def handle(self, *args, **opciones):
        catalogo = Etapa.objects.filter(ruta=Etapa.Ruta.COMPLETO)
        if not catalogo.exists():
            self.stdout.write("No hay catálogo que podar: ya está solo la enfocada.")
            return

        items = Item.objects.filter(etapa__ruta=Etapa.Ruta.COMPLETO)
        libros = items.filter(tipo=Item.Tipo.LIBRO)
        a_borrar = items.exclude(tipo=Item.Tipo.LIBRO)
        marcados = a_borrar.filter(completado=True).count()

        if not opciones["si"]:
            self.stdout.write(
                f"Se van a borrar {catalogo.count()} etapas y {a_borrar.count()} "
                f"items del catálogo ({marcados} de ellos marcados como hechos).\n"
                f"Se conservan {libros.count()} libros en la biblioteca."
            )
            if input("Escribe 'si' para continuar: ").strip().lower() != "si":
                self.stdout.write(self.style.WARNING("Cancelado. No se borró nada."))
                return

        biblioteca, _ = Etapa.objects.update_or_create(
            ruta=Etapa.Ruta.ENFOCADA,
            orden=ORDEN_BIBLIOTECA,
            defaults={
                "kicker": "Lectura",
                "titulo": "Biblioteca",
                "subtitulo": "Sin fecha y sin orden",
                "objetivo": "Los libros no se planifican: se leen cuando toca.",
                "color": "#c2703d",
                "oculta": True,
            },
        )

        # Un mismo título puede estar repetido entre etapas del catálogo; la
        # biblioteca se queda con una sola copia y prefiere la que ya esté leída.
        rescatados, descartados = 0, 0
        ya_en_biblioteca = set(
            biblioteca.items.values_list("titulo", flat=True)
        )
        for libro in libros.order_by("-completado"):
            if libro.titulo in ya_en_biblioteca:
                libro.delete()
                descartados += 1
                continue
            ya_en_biblioteca.add(libro.titulo)
            libro.etapa = biblioteca
            libro.save(update_fields=["etapa"])
            rescatados += 1

        borradas, _ = catalogo.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo podado: {rescatados} libros rescatados "
                f"({descartados} duplicados descartados), {borradas} registros "
                f"borrados. Queda solo la ruta enfocada."
            )
        )
