from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Corte
from .forms import  CorteForm

@login_required(login_url = "contabilidad:login")
def home(request):
    from venta.models import VentaGeneral, VentaProducto
    from inv.models import Producto
    from django.db.models import Count, Sum, Max, Min, F, FloatField
    from datetime import date, datetime, timedelta

 
    fecha = str(date.today())

    venta = VentaGeneral.objects.count()
    venta_oct = VentaGeneral.objects.filter(fc__month='10').aggregate(total=Sum('total'))
    ingreso = VentaGeneral.objects.all().aggregate(Sum('total'))
    producto = Producto.objects.count()
    pro_total = Producto.objects.values('stock_inicial').aggregate(total=Sum('stock_inicial'))

    inversion = Producto.objects.aggregate(total=Sum(F('stock_inicial') * F('precio_compra'), output_field=FloatField()))

    ing_dia = VentaGeneral.objects.filter(fc__gte=fecha).aggregate(Sum('total'))

    oct= VentaProducto.objects.select_related('producto__nombre').values('producto__nombre').filter(num_venta__fc__month='10').aggregate(total=Sum('ga'))

    ga_dia = VentaProducto.objects.select_related('producto__nombre').values('producto__nombre').filter(num_venta__fc__gte=fecha).aggregate(total=Sum('ga'))
    ga_mes = VentaProducto.objects.select_related('producto__nombre').values('producto__nombre').filter(num_venta__fc__month='10').aggregate(total=Sum('ga'))
    

    pro = VentaProducto.objects.select_related('producto__nombre').values('producto__nombre').annotate(masimo=Sum('cantidad')).order_by("-masimo").first()
    pro_mas = VentaProducto.objects.select_related('producto__nombre').filter(num_venta__fc__gte=fecha).values('producto__nombre').annotate(total=Sum('cantidad')).order_by("-total").first()
    pro_men = VentaProducto.objects.select_related('producto__nombre').filter(num_venta__fc__gte=fecha).values('producto__nombre').annotate(total=Sum('cantidad')).order_by("-total").last()
    v_dia = VentaGeneral.objects.filter(fc__gte=fecha).count()




    return render(request, 'contabilidad/inicio.html', {'venta': venta, 'pro_mas': pro_mas, 'pro_men': pro_men,
                            'v_dia': v_dia, 'ingreso': ingreso, 'producto': producto, 'pro': pro, 'ing_dia': ing_dia, 'ga_dia': ga_dia, 'ga_mes': ga_mes,
                             'oct': oct , 'pro_total':pro_total, 'inversion': inversion, 'venta_oct': venta_oct})


class CorteList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Corte
    permission_required='contabilidad.view_corte'
    template_name = 'contabilidad/corte_list.html'
    context_object_name = 'obj'

class CorteNew(SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="contabilidad.add_corte"
    model=Corte
    template_name="contabilidad/corte_form.html"
    context_object_name = "obj"
    form_class=CorteForm
    success_url=reverse_lazy("contabilidad:cortes")
    success_message="corte Creado Satisfactoriamente"