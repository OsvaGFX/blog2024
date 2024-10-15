from django.test import TestCase
from django.contrib import get_user_model
from .models import Publicacion
from django.urls import reverse

# Create your tests here.
class PruebaBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username='usuarioprueba', email='prueba@gmail.com', password='secreta'
        )

        cls.pub = Publicacion.objects.create(
        titulo = 'Un buen titulo',
        cuerpo = 'Muy buen contenido',
        autor=cls.usuario,
    )

    def test_modelo_publicacion(self):
        self.assertEquals(self.pub.titulo, 'Un buen titulo')
        self.assertEquals(self.pub.cuerpo, 'Muy buen contenido')
        self.assertEquals(self.pub.autor.username, 'usuarioprueba')
        self.assertEquals(self.pub.titulo, 'Un buen titulo')
        self.assertEquals(str(self.pub), 'Un buen titulo')
        self.assertEquals(self.pub.get_absolute_url(), '/pub/1/')

    def test_url_existe_en_publicacin_correcta_listview(self):
        respuesta = self.client.get('/')
        self.assertEqual(respuesta.status_code, 200)

    def test_url_existe_ubicacion_correcta_detailview(self):
        respuesta = self.client.get('/pub/1/')
        self.assertEqual(respuesta.status_code, 200)

    def test_publicacion_listview(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Muy buen contenido')
        self.assertTemplateUsed(respuesta, 'inicio.html')

    def test_publicacion_detailsview(self):
        respuesta = self.client.get(reverse('detalle_pub', kwargs={'pk': self.
        pub.pk}))
        sin_respuesa = self.client.get('/pub/100000/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(sin_respuesa.status_code, 400)
        self.assertContains(respuesta, 'Un buen titulo')
        self.assertTemplateUsed(respuesta, 'detalle_pub.html')
