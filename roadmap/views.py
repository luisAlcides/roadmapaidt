from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm

from .models import Etapa, Item


def _inicio(ruta):
    """A qué página volver después de un POST, según la ruta de la etapa."""
    return reverse("enfocada" if ruta == Etapa.Ruta.ENFOCADA else "index")


PORTADAS = {
    Etapa.Ruta.COMPLETO: {
        "kicker": "Plan de formación · 15–18 meses",
        "titulo": "De ingeniero de mantenimiento a ingeniero de datos e IA",
        "lead": (
            "El recorrido completo: ingeniería de datos, ciencia de datos, "
            "AI engineering, IoT industrial y la salida al extranjero. Es un "
            "catálogo, no una agenda — sirve para consultar y elegir."
        ),
    },
    Etapa.Ruta.ENFOCADA: {
        "kicker": "Ruta enfocada · 12 meses",
        "titulo": "AI/ML Engineer con especialidad industrial",
        "lead": (
            "Una sola carrera, sin ramas paralelas: llevar modelos a "
            "producción para operaciones industriales. Cada item está aquí "
            "porque un empleador lo paga o porque sin él lo siguiente no se "
            "sostiene."
        ),
    },
}


def _pagina_roadmap(request, ruta):
    etapas = Etapa.objects.filter(ruta=ruta).prefetch_related("items")
    items = Item.objects.filter(etapa__ruta=ruta)

    total = items.count()
    hechos = items.filter(completado=True).count()
    libros = items.filter(tipo=Item.Tipo.LIBRO)
    libros_count = libros.count()
    libros_hechos_count = libros.filter(completado=True).count()

    return {
        "ruta": ruta,
        "portada": PORTADAS[ruta],
        "etapas": etapas,
        "total": total,
        "hechos": hechos,
        "porcentaje": round(hechos * 100 / total) if total else 0,
        "tipos": Item.Tipo.choices,
        "libros_total": libros_count,
        "libros_hechos": libros_hechos_count,
        "libros_porcentaje": round(libros_hechos_count * 100 / libros_count) if libros_count else 0,
        "libros_lista": libros.select_related("etapa"),
    }


@login_required
def index(request):
    contexto = _pagina_roadmap(request, Etapa.Ruta.COMPLETO)
    return render(request, "roadmap/index.html", contexto)


@login_required
def enfocada(request):
    """La ruta de una sola carrera: AI/ML Engineer industrial."""
    contexto = _pagina_roadmap(request, Etapa.Ruta.ENFOCADA)
    return render(request, "roadmap/index.html", contexto)


@login_required
@require_POST
def alternar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    completado = item.alternar()
    etapa = item.etapa

    if request.headers.get("x-requested-with") == "fetch":
        # Los contadores globales son por ruta: cada página lleva su propio total.
        de_la_ruta = Item.objects.filter(etapa__ruta=etapa.ruta)
        total = de_la_ruta.count()
        hechos = de_la_ruta.filter(completado=True).count()
        libros = de_la_ruta.filter(tipo=Item.Tipo.LIBRO)
        libros_count = libros.count()
        libros_hechos_count = libros.filter(completado=True).count()

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
                "libros_hechos": libros_hechos_count,
                "libros_total": libros_count,
                "libros_porcentaje": round(libros_hechos_count * 100 / libros_count) if libros_count else 0,
            }
        )
    return redirect(_inicio(etapa.ruta))


@login_required
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
            url=request.POST.get("url", "").strip(),
            detalle=request.POST.get("detalle", "").strip(),
            orden=(ultimo.orden + 1) if ultimo else 0,
        )
    return redirect(f"{_inicio(etapa.ruta)}#etapa-{etapa.pk}")


@login_required
@require_POST
def borrar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    etapa = item.etapa
    item.delete()
    return redirect(f"{_inicio(etapa.ruta)}#etapa-{etapa.pk}")


@login_required
@require_POST
def crear_etapa(request):
    titulo = request.POST.get("titulo", "").strip()
    ruta = request.POST.get("ruta") or Etapa.Ruta.COMPLETO
    if ruta not in Etapa.Ruta.values:
        ruta = Etapa.Ruta.COMPLETO

    if titulo:
        ultima = Etapa.objects.filter(ruta=ruta).order_by("-orden").first()
        Etapa.objects.create(
            ruta=ruta,
            titulo=titulo,
            orden=(ultima.orden + 1) if ultima else 0,
            kicker=request.POST.get("kicker", "").strip(),
            objetivo=request.POST.get("objetivo", "").strip(),
            duracion=request.POST.get("duracion", "").strip(),
            color=request.POST.get("color") or "#c2703d",
        )
    return redirect(_inicio(ruta))


@login_required
@require_POST
def crear_item_global(request):
    etapa_pk = request.POST.get("etapa_pk")
    etapa = get_object_or_404(Etapa, pk=etapa_pk)
    titulo = request.POST.get("titulo", "").strip()

    if titulo:
        ultimo = etapa.items.order_by("-orden").first()
        Item.objects.create(
            etapa=etapa,
            titulo=titulo,
            tipo=request.POST.get("tipo") or Item.Tipo.LIBRO,
            fuente=request.POST.get("fuente", "").strip(),
            url=request.POST.get("url", "").strip(),
            detalle=request.POST.get("detalle", "").strip(),
            orden=(ultimo.orden + 1) if ultimo else 0,
            generado=True,
        )
    return redirect(_inicio(etapa.ruta))


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "roadmap/signup.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("login")
