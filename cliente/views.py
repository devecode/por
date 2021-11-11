from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Cliente, Abono
from .forms import ClienteForm, AbonoForm

class AbonoList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Abono
    permission_required='cliente.view_abono'
    template_name = 'cliente/abono_list.html'
    context_object_name = 'obj'

class AbonoNew(SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="cliente.add_abono"
    model=Abono
    template_name="cliente/abono_form.html"
    context_object_name = "obj"
    form_class=AbonoForm
    success_url=reverse_lazy("cliente:abono")

class ClienteList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = Cliente
    permission_required='cliente.view_cliente'
    template_name = 'cliente/cliente_list.html'
    context_object_name = 'obj'

class ClienteNew(SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="cliente.add_cliente"
    model=Cliente
    template_name="cliente/cliente_form.html"
    context_object_name = "obj"
    form_class=ClienteForm
    success_url=reverse_lazy("cliente:cliente")

class ClienteEdit(LoginRequiredMixin, generic.UpdateView):
    model = Cliente
    template_name = "cliente/cliente_form.html"
    context_object_name = 'obj'
    form_class = ClienteForm
    success_url = reverse_lazy("cliente:cliente")
    permission_required = "cliente.change_cliente"
