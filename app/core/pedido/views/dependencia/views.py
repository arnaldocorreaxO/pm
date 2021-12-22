import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.base.models import Sucursal

from core.pedido.models import Dependencia
from core.pedido.forms import DependenciaForm
from config.utils import print_info
from core.user.models import User

class DependenciaListView(PermissionRequiredMixin, ListView):
    model = Dependencia
    template_name = 'pedido/dependencia/list.html'
    permission_required = 'pedido.view_dependencia'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Funciona así tambien para modificar un atributo de la clase
        # self.usuario = User.objects.filter(id=self.request.user.id).first()
        self.usuario = request.user
        return super().dispatch(request, *args, **kwargs)    
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('dependencia_create')
        context['title'] = 'Listado de Dependencias '
        context['object_list'] = Dependencia.objects.filter(sucursal=self.usuario.sucursal)
        return context


class DependenciaCreateView(PermissionRequiredMixin, CreateView):
    model = Dependencia
    template_name = 'pedido/dependencia/create.html'
    form_class = DependenciaForm
    success_url = reverse_lazy('dependencia_list')
    permission_required = 'pedido.add_dependencia'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.filter(id=self.request.user.id).first()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if Dependencia.objects.filter(sucursal=self.usuario.sucursal,denominacion__iexact=obj):
                    data['valid'] = False
            elif type == 'denom_corta':                
                if Dependencia.objects.filter(sucursal=self.usuario.sucursal,denominacion__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de Dependencias '
        context['action'] = 'add'
        return context


class DependenciaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Dependencia
    template_name = 'pedido/dependencia/create.html'
    form_class = DependenciaForm
    success_url = reverse_lazy('dependencia_list')
    permission_required = 'pedido.change_dependencia'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'denominacion':
                if Dependencia.objects.filter(sucursal=self.usuario.sucursal,denominacion__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Dependencias '
        context['action'] = 'edit'
        return context


class DependenciaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dependencia
    template_name = 'pedido/dependencia/delete.html'
    success_url = reverse_lazy('dependencia_list')
    permission_required = 'pedido.delete_dependencia'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context