''' 
=============================
===    FORM DE BUSQUEDA   ===
============================= '''


from django import forms
from config.utils import choiceAnho

from core.pedido.models import Movimiento

#Sobre-escribimos el metodo label_form_instance para representar otro valor distinto a al metodo __str__
class ModelChoiceFieldAnho(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.anho

class DashboardForm(forms.Form):  
    qs = Movimiento.objects.filter(activo__exact=True).order_by(
        '-anho').distinct('anho')
    max_anho = qs[0]
    anho = ModelChoiceFieldAnho(queryset=qs, to_field_name='anho',initial=max_anho, empty_label="(Todos)")
    # ANHO_CHOICES = choiceAnho()
    # anho = forms.ChoiceField(choices=ANHO_CHOICES)
    anho.widget.attrs.update(
        {'class': 'form-control select'})
