from django.db import models

from venta.models import VentaGeneral


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum


class Cliente(models.Model):
    nombre = models.CharField(max_length=500)
    telefono = models.CharField(max_length=500)
    direccion = models.CharField(max_length=500)
    deuda = models.DecimalField(max_digits=50, decimal_places=2,default=0)

    def __str__(self):
        return '{}'.format(self.nombre)


class Abono(models.Model):
    nombre = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    num_venta = models.ForeignKey(VentaGeneral, on_delete=models.CASCADE)
    abono = models.DecimalField(max_digits=50, decimal_places=2,default=0)
    fa = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.nombre)
    




@receiver(post_save, sender=Abono)
def update_resto(sender, instance, **kwargs):
    instance.num_venta.resto += instance.abono
    instance.num_venta.resto_total =  instance.num_venta.total - instance.num_venta.resto
    instance.num_venta.save()


@receiver(post_save, sender=Abono)
def update_stock(sender, instance, **kwargs):
    instance.nombre.deuda = instance.nombre.deuda - instance.abono
    instance.nombre.save()