from django.contrib import admin

from .models import VentaGeneral, VentaProducto


class VentaGeneralAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fc', 'vendedor', 'articulo_total', 'sub_total', 'subtotal_descuento', 
                    'descuento', 'total','total_efectivo','total_tarjeta', 'metodo_pago',
                    'cliente', 'resto', 'status', 'resto_total']

admin.site.register(VentaGeneral, VentaGeneralAdmin)
admin.site.register(VentaProducto)
