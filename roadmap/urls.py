from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="roadmap/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("item/nuevo/global/", views.crear_item_global, name="crear_item_global"),
    path("item/<int:pk>/alternar/", views.alternar_item, name="alternar_item"),
    path("item/<int:pk>/borrar/", views.borrar_item, name="borrar_item"),
    path("etapa/<int:etapa_pk>/item/nuevo/", views.crear_item, name="crear_item"),
    path("etapa/nueva/", views.crear_etapa, name="crear_etapa"),
]
