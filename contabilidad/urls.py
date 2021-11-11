from django.urls import path
from django.contrib.auth import views as auth_views
from contabilidad import views as vistas
from .views import CorteList, CorteNew

urlpatterns = [
    path('',vistas.home, name='inicio'),
    path('login/',auth_views.LoginView.as_view(template_name='contabilidad/login.html'),
                name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='contabilidad/login.html'),
            name='logout'),
    path('cortes',CorteList.as_view(), name='cortes'),
    path('cortes/nuevo',CorteNew.as_view(), name='corte_nuevo'),

]