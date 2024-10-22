from django.test import TestCase
from django.contrib.auth import get_user_model
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
            titulo='Un buen titulo',
            cuerpo='Muy buen contenido',
            autor=cls.usuario,
        )

    def test_modelo_publicacion(self):
        self.assertEquals(self.pub.titulo, 'Un buen titulo')
        self.assertEquals(self.pub.cuerpo, 'Muy buen contenido')
        self.assertEquals(self.pub.autor.username, 'usuarioprueba')
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
        respuesta = self.client.get(reverse('detalle_pub', kwargs={'pk': self.pub.pk}))
        sin_respuesta = self.client.get('/pub/100000/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(sin_respuesta.status_code, 404)  # Código de error corregido
        self.assertContains(respuesta, 'Un buen titulo')
        self.assertTemplateUsed(respuesta, 'detalle_pub.html')

    def test_vista_crear_publicacion(self):
        respuesta = self.client.post(
            reverse('nueva_pub'), {
                "titulo": "Nuevo titulo",
                "cuerpo": "Nuevo cuerpo",
                "autor": self.usuario.id  # Corregido a self.usuario
            })
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Publicacion.objects.last().titulo, "Nuevo titulo")
        self.assertEqual(Publicacion.objects.last().cuerpo, "Nuevo cuerpo")

    def test_vista_editar(self):
        respuesta = self.client.post(
            reverse('editar_pub', args=[1]),  # args necesita ser una lista o tupla
            {
                'titulo': 'titulo modificado',
                'cuerpo': 'cuerpo modificado', 
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Publicacion.objects.last().titulo, 'titulo modificado')
        self.assertEqual(Publicacion.objects.last().cuerpo, 'cuerpo modificado')
            
    def test_vista_eliminar(self):
        respuesta = self.client.post(reverse('eliminar_pub', args=[1]))  # args necesita ser una lista o tupla
        self.assertEqual(respuesta.status_code, 302)
