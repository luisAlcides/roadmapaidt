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


class CargarRoadmapTests(TestCase):
    def test_carga_el_plan_del_pdf(self):
        call_command("cargar_roadmap", verbosity=0)
        self.assertEqual(Etapa.objects.count(), 5)
        self.assertEqual(Item.objects.count(), 65)

    def test_es_idempotente_y_conserva_el_progreso(self):
        call_command("cargar_roadmap", verbosity=0)
        item = Item.objects.first()
        item.alternar()

        call_command("cargar_roadmap", verbosity=0)

        self.assertEqual(Item.objects.count(), 65)
        item.refresh_from_db()
        self.assertTrue(item.completado)

    def test_reset_borra_todo(self):
        call_command("cargar_roadmap", verbosity=0)
        Item.objects.first().alternar()

        call_command("cargar_roadmap", "--reset", verbosity=0)

        self.assertEqual(Item.objects.count(), 65)
        self.assertEqual(Item.objects.filter(completado=True).count(), 0)


class CargarExtrasTests(TestCase):
    def setUp(self):
        call_command("cargar_roadmap", verbosity=0)

    def test_agrega_contenido_y_lo_marca_como_generado(self):
        call_command("cargar_extras", verbosity=0)

        generados = Item.objects.filter(generado=True)
        self.assertEqual(generados.count(), Item.objects.count() - 65)
        self.assertEqual(Etapa.objects.count(), 7)
        # Lo del PDF queda intacto.
        self.assertEqual(Item.objects.filter(generado=False).count(), 65)

    def test_es_idempotente(self):
        call_command("cargar_extras", verbosity=0)
        total = Item.objects.count()

        call_command("cargar_extras", verbosity=0)

        self.assertEqual(Item.objects.count(), total)

    def test_quitar_deja_solo_el_pdf(self):
        call_command("cargar_extras", verbosity=0)
        call_command("cargar_extras", "--quitar", verbosity=0)

        self.assertEqual(Item.objects.count(), 65)
        self.assertEqual(Etapa.objects.count(), 5)

    def test_quitar_conserva_el_progreso_del_pdf(self):
        call_command("cargar_extras", verbosity=0)
        item = Item.objects.filter(generado=False).first()
        item.alternar()

        call_command("cargar_extras", "--quitar", verbosity=0)

        item.refresh_from_db()
        self.assertTrue(item.completado)

    def test_sin_roadmap_previo_no_hace_nada(self):
        Etapa.objects.all().delete()
        call_command("cargar_extras", verbosity=0)
        self.assertEqual(Item.objects.count(), 0)
