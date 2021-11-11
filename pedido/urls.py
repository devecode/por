from django.urls import path
from . import views
from .views import CompraList

urlpatterns = [
    path('compra',CompraList.as_view(), name='compra'),
    path('compra/nueva', views.compraNew, name='compra_nueva'),

]