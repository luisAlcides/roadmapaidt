from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Etapa, Item


def index(request):
    etapas = Etapa.objects.prefetch_related("items")

    total = Item.objects.count()
    hechos = Item.objects.filter(completado=True).count()
    libros = Item.objects.filter(tipo=Item.Tipo.LIBRO)

    contexto = {
        "etapas": etapas,
        "total": total,
        "hechos": hechos,
        "porcentaje": round(hechos * 100 / total) if total else 0,
        "tipos": Item.Tipo.choices,
        "libros_total": libros.count(),
        "libros_hechos": libros.filter(completado=True).count(),
    }
    return render(request, "roadmap/index.html", contexto)


@require_POST
def alternar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    completado = item.alternar()
    etapa = item.etapa

    if request.headers.get("x-requested-with") == "fetch":
        total = Item.objects.count()
        hechos = Item.objects.filter(completado=True).count()
        return JsonResponse(
            {
                "completado": completado,
                "etapa_id": etapa.pk,
                "etapa_hechos": etapa.hechos,
                "etapa_total": etapa.total,
                "etapa_porcentaje": etapa.porcentaje,
                "etapa_completa": etapa.completa,
                "global_hechos": hechos,
                "global_total": total,
                "global_porcentaje": round(hechos * 100 / total) if total else 0,
            }
        )
    return redirect("index")


@require_POST
def crear_item(request, etapa_pk):
    etapa = get_object_or_404(Etapa, pk=etapa_pk)
    titulo = request.POST.get("titulo", "").strip()

    if titulo:
        ultimo = etapa.items.order_by("-orden").first()
        Item.objects.create(
            etapa=etapa,
            titulo=titulo,
            tipo=request.POST.get("tipo") or Item.Tipo.CURSO,
            fuente=request.POST.get("fuente", "").strip(),
            detalle=request.POST.get("detalle", "").strip(),
            orden=(ultimo.orden + 1) if ultimo else 0,
        )
    return redirect(f"/#etapa-{etapa.pk}")


@require_POST
def borrar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    etapa_pk = item.etapa_id
    item.delete()
    return redirect(f"/#etapa-{etapa_pk}")


@require_POST
def crear_etapa(request):
    titulo = request.POST.get("titulo", "").strip()
    if titulo:
        ultima = Etapa.objects.order_by("-orden").first()
        Etapa.objects.create(
            titulo=titulo,
            orden=(ultima.orden + 1) if ultima else 0,
            kicker=request.POST.get("kicker", "").strip(),
            objetivo=request.POST.get("objetivo", "").strip(),
            duracion=request.POST.get("duracion", "").strip(),
            color=request.POST.get("color") or "#c2703d",
        )
    return redirect("index")
