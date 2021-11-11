from django.http.response import HttpResponseBadRequest
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm
from inv import models as modelsInv

from django.http import FileResponse
from barcode import EAN13
from barcode.writer import ImageWriter
from io import BytesIO
import io
from barcode import generate
from PIL import Image

class CategoriaList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Categoria
    permission_required='inv.view_categoria'
    template_name = 'inv/categoria_list.html'
    context_object_name = 'obj'

class CategoriaNew(SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="inv.add_categoria"
    model=Categoria
    template_name="inv/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("inv:categoria")
    success_message="Categoria Creada Satisfactoriamente"


class ProductoList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Producto
    permission_required='inv.view_producto'
    template_name = 'inv/producto_list.html'
    context_object_name = 'obj'


@login_required(login_url='bases:login')
def subir_imagen(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.img = request.FILES['img']
            producto.save()
            return redirect("inv:producto")

    context = {"form": form,}
    return render(request, 'inv/producto_form.html', context)

class ProductoEdit(LoginRequiredMixin, generic.UpdateView):
    model = Producto
    template_name = "inv/producto_form.html"
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy("inv:producto")
    success_message = "Producto Editado Correctamente"
    permission_required = "inv.change_producto"

@login_required(login_url='admin:login')
def generar_barras(request,pk):
    producto = modelsInv.Producto.objects.filter(id=pk).exists()
    attachment = False #False si solo se quiere visualizar
    ancho = 500
    alto =  250
    if producto:
        try:
            producto = modelsInv.Producto.objects.get(id=pk)
            codigo = producto.codigo_barra
            fp = BytesIO()
            generate('EAN13', codigo, writer=ImageWriter(), output=fp)
            fp.seek(io.SEEK_SET)
            img = Image.open(io.BytesIO(fp.read()))
            image = img.resize((ancho, alto), Image.ANTIALIAS)
            output = BytesIO()
            image.save(output, format="png", optimize=True)
            name = str(producto.id) + ".png"
            output.seek(io.SEEK_SET)
            response = FileResponse(output, as_attachment=attachment, filename=name)
            return response 
        except:
            return HttpResponseBadRequest("Error al generar el código de barras")
    else:
        return HttpResponseBadRequest("El producto buscado no existe")