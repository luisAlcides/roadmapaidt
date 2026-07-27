from django.contrib import admin

from .models import Etapa, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    fields = ("orden", "tipo", "titulo", "fuente", "url", "etiqueta", "en_ingles", "completado")


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ("orden", "titulo", "ruta", "paralela", "hechos", "total", "porcentaje")
    list_filter = ("ruta",)
    inlines = [ItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "etapa", "tipo", "fuente", "completado", "generado")
    list_filter = ("etapa__ruta", "etapa", "tipo", "completado", "en_ingles", "generado")
    list_editable = ("completado",)
    search_fields = ("titulo", "fuente", "detalle", "url")
