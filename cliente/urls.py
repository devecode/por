from django.urls import path
from .views import ClienteList, ClienteNew, ClienteEdit, AbonoList, AbonoNew


urlpatterns = [
    path('abono/',AbonoList.as_view(), name='abono'),
    path('abono/nuevo',AbonoNew.as_view(), name='abono_nuevo'),

    path('cliente/',ClienteList.as_view(), name='cliente'),
    path('cliente/nuevo',ClienteNew.as_view(), name='cliente_nuevo'),
    path('cliente/edit/<int:pk>', ClienteEdit.as_view(), name="cliente_edit"),


]