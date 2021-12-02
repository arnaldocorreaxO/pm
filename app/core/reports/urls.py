from django.urls import path
from .views.pedido.views import *

urlpatterns = [    
    # REPORTES BASCULA    
    path('rpt_pedido001/', RptPedido001ReportView.as_view(), name='rpt_pedido001'),

]