from django import template

register = template.Library()

TITULOS = {
    "Curso": "Cursos",
    "Libro": "Lecturas de esta etapa",
    "Entregable": "Entregable",
    "Nota": "Ojo con esto",
}


@register.filter
def titulo_grupo(nombre_tipo):
    """Convierte el nombre del tipo de item en el encabezado del grupo."""
    return TITULOS.get(nombre_tipo, nombre_tipo)
