from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<int:pk>/alternar/", views.alternar_item, name="alternar_item"),
    path("item/<int:pk>/borrar/", views.borrar_item, name="borrar_item"),
    path("etapa/<int:etapa_pk>/item/nuevo/", views.crear_item, name="crear_item"),
    path("etapa/nueva/", views.crear_etapa, name="crear_etapa"),
]
