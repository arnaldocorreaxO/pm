
from django.conf import UserSettingsHolder
from django.contrib.auth.models import User
from core.base.forms import *
from django import forms
# from django.forms import *

from .models import *

''' 
=============================
===    DEPENDENCIA        ===
============================= '''
class DependenciaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Dependencia
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'cod': forms.TextInput(attrs={'placeholder': 'Ingrese Dependencia'}),
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese Denominacion'}),
            'denom_corta': forms.TextInput(attrs={'placeholder': 'Ingrese Denominacion Corta'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
=============================
===    DESTINO        ===
============================= '''
class DestinoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Destino
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese Denominacion'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
''' 
=============================
===    MOVIMIENTO        ===
============================= '''
class MovimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # self.user = user
        super().__init__(*args, **kwargs)       
        # self.fields['sucursal'] = self.request.user
        self.fields['solicitante'].queryset = Dependencia.objects.filter(activo__exact=True,dependencia_padre__isnull=True).order_by('denominacion')
        self.fields['area_solicitante'].queryset = Dependencia.objects.filter(activo__exact=True,dependencia_padre__isnull=False)
        # self.fields['nro_pedido'].widget.attrs['autofocus'] = True

    class Meta:
        model = Movimiento
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;','disabled': True,}),
            'nro_pedido': forms.TextInput(attrs={'placeholder': 'Ingrese Nro SOLPED'}),  
            'fecha' : forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control','autocomplete': 'off'}),
            'nro_expediente': forms.TextInput(attrs={'placeholder': 'Ingrese Nro Expediente','required': True}),
            'anho': forms.TextInput(attrs={'readonly':'readonly'}),
            'solicitante': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'area_solicitante': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'descripcion': forms.Textarea(attrs={'rows':2,'placeholder': 'Ingrese la Descripcion del Pedido','required': True}),
            'destino': forms.Textarea(attrs={'rows':2,'placeholder': 'Ingrese el Destino del Pedido','required': True}),
            'ref_doc_asociado': forms.Textarea(attrs={'rows':4,'placeholder': 'Ingrese Ref. Documentos Asociados al Pedido, Contratos, Ordenes de Compra, Remisiones, etc'}),
            'ref_ped_anterior': forms.TextInput(attrs={'placeholder': 'Ingrese Referencia de Pedidos Anteriores'}),
        }
        # label ={
        #     "sucursal":"Frente de Servicios",
        # }

    def clean(self):
        import datetime
        cd = super().clean() #CLEANED_DATA
        fecha = cd.get('fecha')
        cd['anho'] = int(datetime.datetime.strftime(fecha,'%Y'))
        return cd

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


#Sobre-escribimos el metodo label_form_instance para representar otro valor distinto a al metodo __str__
class ModelChoiceFieldAnho(forms.ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.anho
    

''' 
=============================
===    FORM DE BUSQUEDA   ===
============================= '''

class SearchForm(forms.Form):    
    solicitante = None
    def __init__(self,*args, **kwargs):
        usuario = kwargs.pop('user', None)
        print_info('FORM')
        print(usuario)
        super(SearchForm, self).__init__(*args, **kwargs)
        if usuario:
            self.fields['solicitante'].queryset= Dependencia.objects.filter(sucursal=usuario.sucursal,dependencia_padre__isnull=True, activo__exact=True).order_by('denominacion')                  
          

    # Extra Fields
    # Rango de fechas
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    # Termino de busqueda 
    term = forms.CharField()

    habilita_fecha = forms.BooleanField(initial=False,required=False)

    choiceSituacion = Movimiento().SITUACION_PEDIDO
    choiceSituacion = choiceSituacion + (('','(Todos)'),)

    anho = ModelChoiceFieldAnho(queryset=Movimiento.objects.filter(activo__exact=True).order_by(
        '-anho').distinct('anho'), to_field_name='anho', empty_label="(Todos)")
    situacion = forms.ChoiceField(choices=choiceSituacion)
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.filter(activo__exact=True).order_by('denominacion'), empty_label="(Todos)")  
    solicitante = forms.ModelChoiceField(queryset=None, empty_label="(Todos)")    
    area_solicitante = forms.ModelChoiceField(queryset=Dependencia.objects.filter(
        dependencia_padre__isnull=False, activo__exact=True).order_by('denominacion'), empty_label="(Todos)")
    # producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo__exact=True).order_by('denominacion'), empty_label="(Todos)")
    # vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(activo__exact=True).order_by('matricula'), empty_label="(Todos)")
    # chofer = forms.ModelChoiceField(queryset=Chofer.objects.filter(activo__exact=True).order_by('nombre','apellido'), empty_label="(Todos)")
    
    term.widget.attrs.update({'class': 'form-control'})
    anho.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    situacion.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    sucursal.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    solicitante.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    area_solicitante.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    habilita_fecha.widget.attrs.update({'class': 'form-control'})