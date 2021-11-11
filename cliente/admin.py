from django.contrib import admin

from .models import Cliente, Abono


class AbonoAdmin( admin.ModelAdmin):
    list_display = ['nombre', 'num_venta', 'abono', 'fa']
    search_fields = ['nombre']


admin.site.register(Abono, AbonoAdmin)
admin.site.register(Cliente)
