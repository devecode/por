from django.urls import path
from .views import VentaGeneralList, CodigoBarrasSearch, apliacionVenta, get_ticket, VentaG
 

urlpatterns = [
    path('ventas-generales',VentaG.as_view(), name='ventas_generales'),

    path('ventas',VentaGeneralList.as_view(), name='ventas'),
    path('codigoBarras/<str:bar_id>/',CodigoBarrasSearch, name='busqueda'),
    path('aplicacionVenta',apliacionVenta, name='venta'),
    path('ticketVenta/<str:pk>/',get_ticket, name='ticket'),
]