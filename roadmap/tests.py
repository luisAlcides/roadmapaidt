from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Etapa, Item


class ModeloTests(TestCase):
    def setUp(self):
        self.etapa = Etapa.objects.create(orden=0, titulo="Nivelación")
        self.item = Item.objects.create(etapa=self.etapa, titulo="Curso de Git")
        Item.objects.create(etapa=self.etapa, titulo="Curso de SQL")

    def test_alternar_marca_y_desmarca(self):
        self.assertTrue(self.item.alternar())
        self.item.refresh_from_db()
        self.assertTrue(self.item.completado)
        self.assertIsNotNone(self.item.completado_en)

        self.assertFalse(self.item.alternar())
        self.item.refresh_from_db()
        self.assertIsNone(self.item.completado_en)

    def test_porcentaje_de_etapa(self):
        self.assertEqual(self.etapa.porcentaje, 0)
        self.item.alternar()
        self.assertEqual(self.etapa.porcentaje, 50)
        self.assertFalse(self.etapa.completa)

    def test_etapa_vacia_no_divide_por_cero(self):
        vacia = Etapa.objects.create(orden=9, titulo="Vacía")
        self.assertEqual(vacia.porcentaje, 0)
        self.assertFalse(vacia.completa)


class VistaTests(TestCase):
    def setUp(self):
        self.etapa = Etapa.objects.create(orden=0, titulo="Nivelación")
        self.item = Item.objects.create(etapa=self.etapa, titulo="Curso de Git")
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_index_renderiza(self):
        respuesta = self.client.get(reverse("index"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Curso de Git")

    def test_alternar_devuelve_json_para_fetch(self):
        respuesta = self.client.post(
            reverse("alternar_item", args=[self.item.pk]),
            headers={"x-requested-with": "fetch"},
        )
        datos = respuesta.json()
        self.assertTrue(datos["completado"])
        self.assertEqual(datos["global_porcentaje"], 100)

    def test_alternar_sin_fetch_redirige(self):
        respuesta = self.client.post(reverse("alternar_item", args=[self.item.pk]))
        self.assertRedirects(respuesta, reverse("index"))

    def test_alternar_rechaza_get(self):
        respuesta = self.client.get(reverse("alternar_item", args=[self.item.pk]))
        self.assertEqual(respuesta.status_code, 405)

    def test_crear_item(self):
        self.client.post(
            reverse("crear_item", args=[self.etapa.pk]),
            {"titulo": "Curso de Docker", "tipo": "curso", "fuente": "Platzi"},
        )
        nuevo = Item.objects.get(titulo="Curso de Docker")
        self.assertEqual(nuevo.etapa, self.etapa)
        self.assertEqual(nuevo.orden, 1)

    def test_crear_item_sin_titulo_no_crea_nada(self):
        self.client.post(reverse("crear_item", args=[self.etapa.pk]), {"titulo": "   "})
        self.assertEqual(self.etapa.items.count(), 1)

    def test_borrar_item(self):
        self.client.post(reverse("borrar_item", args=[self.item.pk]))
        self.assertEqual(Item.objects.count(), 0)

    def test_crear_etapa_se_ubica_al_final(self):
        self.client.post(reverse("crear_etapa"), {"titulo": "Etapa nueva"})
        nueva = Etapa.objects.get(titulo="Etapa nueva")
        self.assertEqual(nueva.orden, 1)


class RutaEnfocadaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user("alcides", password="clave-larga-123")
        self.client.login(username="alcides", password="clave-larga-123")
        call_command("cargar_ruta_enfocada", verbosity=0)
        call_command("cargar_biblioteca", verbosity=0)

    def test_es_la_unica_ruta_y_vive_en_la_raiz(self):
        respuesta = self.client.get("/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["ruta"], Etapa.Ruta.ENFOCADA)
        self.assertFalse(Etapa.objects.filter(ruta=Etapa.Ruta.COMPLETO).exists())

    def test_el_progreso_es_del_plan_no_de_la_biblioteca(self):
        """La barra de arriba mide los 12 meses; los libros tienen la suya."""
        plan = Item.objects.filter(etapa__oculta=False).count()

        respuesta = self.client.get("/")

        self.assertEqual(respuesta.context["total"], plan)
        self.assertGreater(respuesta.context["libros_total"], plan)

    def test_la_biblioteca_no_se_dibuja_en_el_mapa(self):
        etapas = self.client.get("/").context["etapas"]

        self.assertEqual(len(etapas), 6)
        self.assertTrue(Etapa.objects.filter(oculta=True).exists())

    def test_tiene_una_etapa_en_paralelo(self):
        paralelas = Etapa.objects.filter(ruta=Etapa.Ruta.ENFOCADA, paralela=True)
        self.assertEqual(paralelas.count(), 1)

    def test_todo_curso_trae_enlace(self):
        sin_enlace = Item.objects.filter(
            etapa__ruta=Etapa.Ruta.ENFOCADA, tipo=Item.Tipo.CURSO, url=""
        )
        # Solo la práctica de inglés diaria no tiene a dónde apuntar.
        self.assertLessEqual(sin_enlace.count(), 1)

    def test_la_ruta_enfocada_no_tiene_libros_propios(self):
        """Los libros viven una sola vez, en la biblioteca compartida."""
        propios = Item.objects.filter(
            etapa__ruta=Etapa.Ruta.ENFOCADA, tipo=Item.Tipo.LIBRO
        )
        self.assertFalse(propios.exists())

    def test_la_biblioteca_entera_es_visible_y_con_enlace(self):
        libros = Item.objects.filter(tipo=Item.Tipo.LIBRO)

        respuesta = self.client.get("/")

        self.assertEqual(respuesta.context["libros_total"], libros.count())
        self.assertGreater(libros.count(), 250)
        self.assertFalse(libros.filter(url="").exists())

    def test_marcar_un_libro_no_mueve_la_barra_del_plan(self):
        libro = Item.objects.filter(tipo=Item.Tipo.LIBRO).first()

        respuesta = self.client.post(
            f"/item/{libro.pk}/alternar/", headers={"x-requested-with": "fetch"}
        )

        datos = respuesta.json()
        self.assertEqual(datos["libros_hechos"], 1)
        self.assertEqual(datos["global_hechos"], 0)

    def test_es_idempotente(self):
        total = Item.objects.count()
        call_command("cargar_ruta_enfocada", verbosity=0)
        self.assertEqual(Item.objects.count(), total)

    def test_quitar_deja_la_biblioteca_en_pie(self):
        libros = Item.objects.filter(tipo=Item.Tipo.LIBRO).count()

        call_command("cargar_ruta_enfocada", "--quitar", verbosity=0)

        self.assertEqual(Etapa.objects.filter(oculta=False).count(), 0)
        self.assertEqual(Item.objects.filter(tipo=Item.Tipo.LIBRO).count(), libros)

    def test_alternar_devuelve_el_total_del_plan(self):
        item = Item.objects.filter(etapa__oculta=False).first()

        respuesta = self.client.post(
            f"/item/{item.pk}/alternar/", headers={"x-requested-with": "fetch"}
        )

        datos = respuesta.json()
        self.assertEqual(
            datos["global_total"], Item.objects.filter(etapa__oculta=False).count()
        )


class PodarCatalogoTests(TestCase):
    def setUp(self):
        call_command("cargar_roadmap", verbosity=0)
        call_command("cargar_ruta_enfocada", verbosity=0)

    def test_rescata_los_libros_y_borra_el_resto(self):
        libros = Item.objects.filter(tipo=Item.Tipo.LIBRO).count()
        self.assertGreater(libros, 0)

        call_command("podar_catalogo", "--si", verbosity=0)

        self.assertFalse(Etapa.objects.filter(ruta=Etapa.Ruta.COMPLETO).exists())
        self.assertEqual(Item.objects.filter(tipo=Item.Tipo.LIBRO).count(), libros)
        self.assertTrue(Etapa.objects.filter(oculta=True).exists())

    def test_conserva_lo_que_ya_estaba_leido(self):
        libro = Item.objects.filter(tipo=Item.Tipo.LIBRO).first()
        libro.alternar()

        call_command("podar_catalogo", "--si", verbosity=0)

        libro.refresh_from_db()
        self.assertTrue(libro.completado)

    def test_correrlo_dos_veces_no_rompe_nada(self):
        call_command("podar_catalogo", "--si", verbosity=0)
        libros = Item.objects.filter(tipo=Item.Tipo.LIBRO).count()

        call_command("podar_catalogo", "--si", verbosity=0)

        self.assertEqual(Item.objects.filter(tipo=Item.Tipo.LIBRO).count(), libros)
