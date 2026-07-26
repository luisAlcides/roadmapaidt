from django.db import models
from django.utils import timezone


class Etapa(models.Model):
    """Un nivel del roadmap. El orden define el recorrido del mapa."""

    orden = models.PositiveIntegerField(unique=True)
    kicker = models.CharField(max_length=80, blank=True)
    titulo = models.CharField(max_length=120)
    subtitulo = models.CharField(max_length=200, blank=True)
    objetivo = models.TextField(blank=True)
    duracion = models.CharField(max_length=60, blank=True)
    horas = models.CharField(max_length=60, blank=True)
    color = models.CharField(max_length=7, default="#c2703d")

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "Etapas"

    def __str__(self):
        return f"{self.orden} · {self.titulo}"

    @property
    def total(self):
        return self.items.count()

    @property
    def hechos(self):
        return self.items.filter(completado=True).count()

    @property
    def porcentaje(self):
        total = self.total
        return round(self.hechos * 100 / total) if total else 0

    @property
    def completa(self):
        return self.total > 0 and self.hechos == self.total


class Item(models.Model):
    """Cualquier cosa que se tacha: un curso, un libro, un entregable, una nota."""

    class Tipo(models.TextChoices):
        CURSO = "curso", "Curso"
        LIBRO = "libro", "Libro"
        ENTREGABLE = "entregable", "Entregable"
        NOTA = "nota", "Nota"

    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name="items")
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.CURSO)
    titulo = models.CharField(max_length=250)
    fuente = models.CharField(
        max_length=80, blank=True, help_text="Platzi, Udemy, autor del libro…"
    )
    detalle = models.TextField(blank=True)
    etiqueta = models.CharField(
        max_length=40, blank=True, help_text="Hábitos, Ficción, Foco…"
    )
    en_ingles = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)
    completado_en = models.DateTimeField(null=True, blank=True)
    orden = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["etapa__orden", "orden", "id"]

    def __str__(self):
        return self.titulo

    def alternar(self):
        self.completado = not self.completado
        self.completado_en = timezone.now() if self.completado else None
        self.save(update_fields=["completado", "completado_en"])
        return self.completado
