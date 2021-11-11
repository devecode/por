from django.db import models
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from django.contrib.auth.models import User

class Compra(models.Model):
    fc = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    importe = models.FloatField(default=0, editable=False)
    image_producto = models.ImageField(null=True, blank=True,  upload_to='pedido/compras')

    def __str__(self):
        return '{}'.format(self.descripcion)
    
    def save(self):
        self.importe = self.cantidad * self.precio
        super(Compra, self).save()
