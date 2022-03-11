import locale
import datetime
from django.db.models.aggregates import Count

from django.db.models.fields import FloatField
from django.db.models.query_utils import Q
from core.dashboard.forms import DashboardForm

from core.pedido.models import Dependencia, Movimiento
from core.base.models import Empresa, Sucursal
from core.security.models import Dashboard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView
from core.user.models import User
from django.db.models.functions import Coalesce
locale.setlocale(locale.LC_TIME, '')


class DashboardView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.filter(id=self.request.user.id).first()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtcpanel.html'
        return 'hztpanel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            anho = int(request.POST['anho'])
            # anho = int(datetime.datetime.today().strftime('%Y'))
            if action == 'get_graph_1':
                info = []                
                qs = Movimiento.objects.values('situacion') \
                        .filter(sucursal=self.usuario.sucursal,fecha__year=anho)\
                        .exclude(activo=False)\
                        .annotate(total=Count('id')) \
                        .order_by('-total')
                for i in qs:
                    SITUACION_PEDIDO = dict(Movimiento().SITUACION_PEDIDO )
                    info.append([SITUACION_PEDIDO[i['situacion']],
                                                  i['total']])
                data = {
                    'name': 'Situacion Pedido',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_2':
                info = []                
                qs = Movimiento.objects.values('situacion') \
                        .filter(sucursal=self.usuario.sucursal,fecha__year= anho - 1)\
                        .exclude(activo=False)\
                        .annotate(total=Count('id')) \
                        .order_by('-total')
                for i in qs:
                    SITUACION_PEDIDO = dict(Movimiento().SITUACION_PEDIDO )
                    info.append([SITUACION_PEDIDO[i['situacion']],
                                                  i['total']])
                data = {
                    'name': 'Situacion Pedido',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_3':
                info = []                
                qs = Movimiento.objects.values('situacion') \
                        .filter(sucursal=self.usuario.sucursal,fecha__year=anho - 2)\
                        .exclude(activo=False)\
                        .annotate(total=Count('id')) \
                        .order_by('-total')
                for i in qs:
                    SITUACION_PEDIDO = dict(Movimiento().SITUACION_PEDIDO )
                    info.append([SITUACION_PEDIDO[i['situacion']],
                                                  i['total']])
                data = {
                    'name': 'Situacion Pedido',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_4':
                info = []
                for i in Movimiento.objects.values('solicitante__denominacion') \
                                        .filter(sucursal=self.usuario.sucursal,fecha__year=anho,activo=True)\
                                        .annotate(ctd_pedidos=Count(True)) \
                                        .order_by('-ctd_pedidos'):
                                        info.append({'name' : i['solicitante__denominacion'],
                                                     'data' : [float(i['ctd_pedidos']),]})
                data = info
                # print(data)
            elif action == 'get_graph_5':
                info = []
                for i in Movimiento.objects.values('area_solicitante__denominacion') \
                                        .filter(sucursal=self.usuario.sucursal,fecha__year=anho,activo=True)\
                                        .annotate(ctd_pedidos=Count(True)) \
                                        .order_by('-ctd_pedidos'):
                                        info.append({'name' : i['area_solicitante__denominacion'],
                                                     'data' : [float(i['ctd_pedidos']),]})
                data = info   
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        import datetime
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['fecha_actual'] = datetime.datetime.today().strftime("%d/%m/%Y")
        context['fecha_hora_actual'] = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        context['mes_actual'] = datetime.datetime.today().strftime("%B").capitalize()
        # context['anho_actual'] = str(int(datetime.datetime.today().strftime("%Y")) - 1)
        context['anho_actual'] = datetime.datetime.today().strftime("%Y")
        context['empresa'] = Empresa.objects.first()
        context['sucursales'] = Sucursal.objects.filter(activo=True).count()
        context['dependencias'] = Dependencia.objects.filter(sucursal=self.usuario.sucursal,activo=True).count()
        context['pedidos'] = Movimiento.objects.filter(sucursal=self.usuario.sucursal,fecha__year=datetime.datetime.today().strftime("%Y")).count()
        context['movimientos'] = Movimiento.objects.filter(sucursal=self.usuario.sucursal).order_by('-fecha','-nro_pedido')[0:10]
        context['usuario'] = self.usuario
        context['form'] = DashboardForm()
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
