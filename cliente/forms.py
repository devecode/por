from django import forms

from .models import Cliente, Abono

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['nombre', 'num_venta', 'abono']
        labels = {'nombre':"Nombre", 'num_venta':"Número de Venta", 'abono':"Abono"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'direccion']
        labels = {'nombre':"Nombre", 'telefono':"Telefono", 'direccion':"Direccion"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })