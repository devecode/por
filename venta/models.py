import decimal
from django.db import models
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum
#Models Producto
from inv.models import Producto
#from cliente.models import Cliente

class VentaGeneral(models.Model):
    METODO = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TARJETA', 'TARJETA'),
        ('MIXTO', 'MIXTO'),
    ]
    
    articulo_total = models.BigIntegerField(default=0, editable=False)
    metodo_pago = models.CharField('METODO', choices=METODO, default='EFECTIVO', max_length=100, blank=True)
    fc = models.DateTimeField(auto_now_add=True)
    #hc = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.FloatField(default=0, editable=False)
    subtotal_descuento =  models.FloatField(default=0, editable=False)
    descuento = models.FloatField(default=0, editable=False)
    total = models.DecimalField(max_digits=50, decimal_places=2,default=0, editable=False)
    total_efectivo = models.FloatField(default=0, editable=False)
    total_tarjeta = models.FloatField(default=0, editable=False)
    cliente = models.ForeignKey("cliente.Cliente", on_delete=models.CASCADE, related_name="cliente_nombre" ,null=True, blank=True)
    resto = models.DecimalField(max_digits=50, decimal_places=2,default=0,null=True, blank=True, editable=False)
    resto_total = models.DecimalField(max_digits=50, decimal_places=2,default=0,null=True, blank=True, editable=False)
    status = models.BooleanField(default=True,null=True, blank=True)


    #objects = VentaGeneralManager()

    def __str__(self):
        return '{}'.format(self.pk)
    
    def save(self):
        if self.resto_total == 0:
            self.status = False
        else:
            self.status = True
            
        self.descuento = self.sub_total - self.subtotal_descuento
        self.total = (self.subtotal_descuento)
        super(VentaGeneral,self).save()

    class Meta:
        verbose_name_plural = "Ventas Generales"


class VentaProducto(models.Model):
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(Producto, related_name='producto_nombre',  on_delete=models.CASCADE)
    venta = models.FloatField(default=0, editable=False)
    importe = models.FloatField(default=0, editable=False)
    descuento = models.FloatField(default=0, editable=False)
    importe_descuento = models.FloatField(default=0, editable=False)
    num_venta = models.ForeignKey(VentaGeneral, on_delete=models.CASCADE)
    ga = models.FloatField(default=0, editable=False, blank=True)


    def __str__(self):
        return '{}'.format(self.pk)
    
    def save(self):
    
        self.venta = self.producto.precio_venta
        self.descuento = self.producto.precio_descuento
        self.importe = self.cantidad * self.venta
        self.importe_descuento = self.cantidad * self.descuento
        self.ga = self.cantidad * self.producto.ganancia
        super(VentaProducto,self).save()

@receiver(post_save, sender=VentaGeneral)
def update_deuda(sender, instance, **kwargs):
    if instance.cliente:
        instance.cliente.deuda += (decimal.Decimal(instance.total))
        instance.cliente.save()


@receiver(post_save, sender=VentaProducto)
def detalle_fac_guardar(sender,instance,**kwargs):
    num_venta_id = instance.num_venta.id
    producto_id = instance.producto.id

    vg = VentaGeneral.objects.get(pk=num_venta_id)
    if vg:
        cantidad = VentaProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(cantidad=Sum('cantidad')) \
            .get('cantidad',0.00)
        importe = VentaProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(importe=Sum('importe')) \
            .get('importe',0.00)
        importe_descuento =  VentaProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(importe_descuento=Sum('importe_descuento')) \
            .get('importe_descuento',0.00)
        

        vg.subtotal_descuento = importe_descuento
        vg.sub_total = importe
        vg.articulo_total = cantidad 
        vg.save()

    prod=Producto.objects.filter(pk=producto_id).first()
    
    if prod:
        cantidad = int(prod.stock_inicial) - int(instance.cantidad)
        prod.stock_inicial = cantidad
        prod.stock_final = cantidad
        prod.save()
    
