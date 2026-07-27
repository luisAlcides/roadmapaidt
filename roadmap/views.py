from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm

from .models import Etapa, Item


PORTADA = {
    "kicker": "Ruta enfocada · 12 meses",
    "titulo": "AI/ML Engineer con especialidad industrial",
    "lead": (
        "Una sola carrera, sin ramas paralelas: llevar modelos a producción "
        "para operaciones industriales. Cada item está aquí porque un "
        "empleador lo paga o porque sin él lo siguiente no se sostiene."
    ),
}


def _pagina_roadmap(request, ruta):
    etapas = Etapa.objects.filter(ruta=ruta, oculta=False).prefetch_related("items")
    items = Item.objects.filter(etapa__ruta=ruta, etapa__oculta=False)

    total = items.count()
    hechos = items.filter(completado=True).count()
    # La biblioteca es una sola para las dos rutas: un libro leído lo está en
    # ambas páginas. El plan de cada ruta sí es suyo.
    libros = Item.objects.filter(tipo=Item.Tipo.LIBRO)
    libros_count = libros.count()
    libros_hechos_count = libros.filter(completado=True).count()

    return {
        "ruta": ruta,
        "portada": PORTADA,
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
    """La única página: la ruta enfocada de AI/ML Engineer industrial."""
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
        de_la_ruta = Item.objects.filter(
            etapa__ruta=etapa.ruta, etapa__oculta=False
        )
        total = de_la_ruta.count()
        hechos = de_la_ruta.filter(completado=True).count()
        libros = Item.objects.filter(tipo=Item.Tipo.LIBRO)
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
    return redirect(reverse("index"))


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
    return redirect(f"{reverse('index')}#etapa-{etapa.pk}")


@login_required
@require_POST
def borrar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    etapa = item.etapa
    item.delete()
    return redirect(f"{reverse('index')}#etapa-{etapa.pk}")


@login_required
@require_POST
def crear_etapa(request):
    titulo = request.POST.get("titulo", "").strip()
    ruta = request.POST.get("ruta") or Etapa.Ruta.ENFOCADA
    if ruta not in Etapa.Ruta.values:
        ruta = Etapa.Ruta.ENFOCADA

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
    return redirect(reverse("index"))


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
    return redirect(reverse("index"))


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
