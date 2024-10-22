from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Publicacion

# Vista para listar publicaciones
class VistaListaBlog(ListView):
    model = Publicacion
    template_name = 'inicio.html'

# Vista para ver detalles de una publicación
class VistaDetalleBlog(DetailView):
    model = Publicacion
    template_name = 'detalle_pub.html'

# Vista para crear una nueva publicación
class VistaCrearBlog(CreateView):
    model = Publicacion
    template_name = 'nueva_pub.html'
    fields = ['titulo', 'autor', 'cuerpo']

# Vista para editar una publicación existente
class VistaEditarBlog(UpdateView):
    model = Publicacion
    template_name = 'editar_pub.html'
    fields = ['titulo', 'cuerpo']

    # Método para redirigir después de una edición exitosa
    def get_success_url(self):
        return reverse_lazy('detalle_pub', kwargs={'pk': self.object.pk})

class VistaEliminarBlog(DeleteView):
    model = Publicacion
    template_name = 'eliminar_pub.html'
    success_url = reverse_lazy('inicio')  # Redirigir al inicio después de eliminar