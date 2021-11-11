from django import forms

from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {'nombre':"Nombre"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','categoria','img', 'lote', 'caducidad', 'descuento',
                    'precio_compra', 'precio_venta', 'stock_inicial', 'stock_final','codigo_barra']
        labels = {'nombre':"Nombre", 'categoria':"Categoría",
                    'img':"Imagen", 'lote':"Lote", 'caducidad':"Caducidad",
                    'descuento':"Descuento",
                    'precio_compra':"Precio de Compra", 'precio_venta':"Precio de Venta", 'stock_inicial':"Stock Inicial",
                    'stock_final':"Stock Final", 'codigo_barra':"Código de Barra"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })