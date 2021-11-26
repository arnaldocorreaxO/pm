from django.urls import path
from core.pedido.views.dependencia.views import *
from core.pedido.views.destino.views import *
from core.pedido.views.movimiento.views import *


urlpatterns = [
    # Dependencia
    path('dependencia', DependenciaListView.as_view(), name='dependencia_list'),
    path('dependencia/add/', DependenciaCreateView.as_view(), name='dependencia_create'),
    path('dependencia/update/<int:pk>/', DependenciaUpdateView.as_view(), name='dependencia_update'),
    path('dependencia/delete/<int:pk>/', DependenciaDeleteView.as_view(), name='dependencia_delete'),
    # Destino
    path('destino', DestinoListView.as_view(), name='destino_list'),
    path('destino/add/', DestinoCreateView.as_view(), name='destino_create'),
    path('destino/update/<int:pk>/', DestinoUpdateView.as_view(), name='destino_update'),
    path('destino/delete/<int:pk>/', DestinoDeleteView.as_view(), name='destino_delete'),
    # Pedido
    path('movimiento', MovimientoListView.as_view(), name='movimiento_list'),
    path('movimiento/add/', MovimientoCreateView.as_view(), name='movimiento_create'),
    path('movimiento/update/<int:pk>/', MovimientoUpdateView.as_view(), name='movimiento_update'),
    path('movimiento/delete/<int:pk>/', MovimientoListView.as_view(), name='movimiento_delete'),    
   ]