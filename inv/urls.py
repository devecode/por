from django.urls import path
from .views import CategoriaList, CategoriaNew,  ProductoList, ProductoEdit
from django.conf.urls.static import static
from inv import views as vistas
from pos import settings

MEDIA_URL = '/media'
MEDIA_ROOT = '/media/'

urlpatterns = [
    path('categoria',CategoriaList.as_view(), name='categoria'),
    path('categoria/nueva',CategoriaNew.as_view(), name='categoria_nueva'),
    path('producto',ProductoList.as_view(), name='producto'),
    path('producto/nuevo',vistas.subir_imagen, name='producto_nuevo'),
    path('producto/edit/<int:pk>', ProductoEdit.as_view(), name="producto_edit"),
    path('producto/codigoBarras/<str:pk>', vistas.generar_barras, name='generar_barras'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)