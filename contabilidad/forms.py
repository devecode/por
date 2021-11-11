from django import forms

from .models import  Corte

class CorteForm(forms.ModelForm):
    class Meta:
        model = Corte
        fields = ['fechaCorte','usuario', 'efectivo']
        labels = {'fechaCorte':"Fecha de Corte",'usuario':"Usuario",
               "efectivo":"Efectivo"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })