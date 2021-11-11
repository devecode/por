from django.db import models
from django.contrib.auth.models import User

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from datetime import datetime
import datetime
from venta.models import VentaGeneral
from pedido.models import Compra
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware


class Corte(models.Model):
    fechaCorte =  models.DateTimeField('Fecha de corte', null=False, blank=False)
    fechaCreacion =models.DateTimeField('Fecha de creación',auto_now_add=True)
    #hc =  models.TimeField('Horario de corte', auto_now_add=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    venta_efectivo = models.FloatField(default=0, null=True, editable=False)
    venta_tarjeta = models.FloatField(default=0, editable=False)
    egresos = models.FloatField(default=0, editable=False)
    efectivo = models.FloatField(default=0)
    total_efectivo = models.FloatField(default=0, editable=False)

    def _total_venta(self):
        sumaTotales= VentaGeneral.objects.filter(vendedor=self.usuario).filter(fc__date=self.fechaCorte.date()).aggregate(Sum('total'))
        total_venta = sumaTotales['total__sum'] or 0
        
        return format(total_venta, ".2f")
    total_venta = property(_total_venta)

    def _total_tarjeta(self):
        sumaTarjeta = VentaGeneral.objects.filter(vendedor=self.usuario).filter(fc__date=self.fechaCorte.date()).aggregate(Sum('total_tarjeta'))
        venta_tarjeta = sumaTarjeta['total_tarjeta__sum'] or 0 
        
        return format(venta_tarjeta, ".2f")
    venta_tarjeta = property(_total_tarjeta)

    def _total_efectivo(self):
        sumaEfectivo = VentaGeneral.objects.filter(vendedor=self.usuario).filter(fc__date=self.fechaCorte.date()).aggregate(Sum('total_efectivo'))
        venta_efectivo = sumaEfectivo['total_efectivo__sum'] or 0
        
        return format(venta_efectivo, ".2f")
    venta_efectivo = property(_total_efectivo)


    def _total_egresos(self):
        sumaEgresos = Compra.objects.filter(vendedor=self.usuario).filter(fc__date=self.fechaCorte.date()).aggregate(Sum('importe'))        
        egresos = sumaEgresos['importe__sum'] or 0
        
        return format(egresos, ".2f")
    egresos = property(_total_egresos)

    def clean(self):
        if Corte.objects.exclude(pk=self.pk).filter(usuario=self.usuario).filter(fechaCorte__date=self.fechaCorte.date()).exists():
            mensaje="El usuario {} ya cuenta con un corte para el día {}".format(self.usuario.username,self.fechaCorte.date())
            raise ValidationError(mensaje)
        
         
        if len(Corte.objects.filter(pk=self.pk)) != 0 :
            if (Corte.objects.get(pk=self.pk).efectivo != self.efectivo):
                mensaje="No puedes modificar el monto del efectivo una vez guardado el corte, el valor guardado fue: {}".format(Corte.objects.get(pk=self.pk).efectivo)
                raise ValidationError(mensaje)

    

    def __str__(self):
        return '{}'.format(self.usuario)
        

    def save(self):      
        self.total_efectivo = (float(self.venta_efectivo) - float(self.egresos))
        super(Corte, self).save()

