from django import forms

from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['vendedor', 'cantidad', 'descripcion', 'precio', 'image_producto']
        labels = {'vendedor':"Vendedor", 'cantidad':"Cantidad", 'descripcion':"Descripción",
                    'precio':"Precio", 'image_producto':"Imagen del Producto"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })