from django.db import models
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from barcode import EAN13
from barcode.writer import ImageWriter
from barcode import get_barcode

def generaCodigoBarra(idProducto):
    codigo = str(idProducto).zfill(12)  
    cod = get_barcode('EAN13', codigo, writer=ImageWriter())
    return cod



class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        help_text='Descripción de la Categoría',
        unique=True
    )
    def __str__(self):
        return '{}'.format(self.nombre)
    
    def save(self):
        self.nombre = self.nombre.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural= "Categorias"



class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='inv/fotos', blank=True)
    caducidad = models.DateField(blank=True)
    lote = models.CharField(max_length=200, blank=True)
    codigo_barra = models.CharField(max_length=200, blank=True)
    descuento = models.FloatField(default=0)
    precio_descuento = models.FloatField(default=0, editable=False)
    precio_compra = models.FloatField(default=0)
    precio_venta = models.FloatField(default=0)
    stock_inicial = models.IntegerField(default=0)
    stock_final = models.IntegerField(default=0)
    ganancia = models.FloatField(default=0, editable=False, blank = True)

    def __str__(self):
        return '{}:{}'.format(self.nombre,self.codigo_barra)
    
    def save(self):
        self.precio_descuento = ((100 - self.descuento)*self.precio_venta)/100
        #self.descripcion = self.descripcion.upper()
        self.ganancia = (self.precio_descuento - self.precio_compra)
        super(Producto,self).save()
        self.codigo_barra = generaCodigoBarra(self.id) 
        super(Producto,self).save()
    
    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('nombre', 'codigo_barra')


 
