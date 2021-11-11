from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Compra
from .forms import CompraForm

class CompraList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Compra
    permission_required='pedido.view_compra'
    template_name = 'pedido/compra_list.html'
    context_object_name = 'obj'

@login_required(login_url="bases:login")
def compraNew(request):
    form = CompraForm()
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.image_producto = request.FILES['image_producto']
            img.save()
            return redirect("pedido:compra")

    context = {'form': form}
    return render(request, "pedido/compra_form.html", context)


