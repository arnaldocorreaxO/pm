import math

from django.db import connection
from core.pedido.models import Dependencia
from core.reports.jasperbase import JasperReportBase
from datetime import date, datetime
from core.reports.forms import ReportForm
import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from core.pedido.forms import Movimiento, MovimientoForm, SearchForm
from core.security.mixins import PermissionMixin

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import permission_required

class MovimientoListView(PermissionMixin, FormView):	
	# model = Movimiento
	template_name = 'pedido/movimiento/list.html'
	permission_required = 'view_movimiento'
	form_class = SearchForm
 
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		# print(request.POST)
		try:
			if action == 'search_area_solicitante_id':
				data = [{'id': '', 'text': '------------'}]
				print(request.POST)
				id = request.POST.getlist('id') if 'id' in request.POST else '0'		
				id= ",".join(id) if id!=[''] else None

				_where = "1 = 1"
				if id:
					_where += f" AND pedido_dependencia.dependencia_padre_id IN ({id})"
				
				qs = Dependencia.objects.filter(activo__exact=True)\
										.extra(where=[_where])\
									    .order_by('denominacion')	
				# print(qs.query)
				for i in qs:
					# data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
					data.append({'id': i.id, 'text': i.denominacion})	
			elif action == 'search':
				data = []
				term = request.POST['term']
				start_date = request.POST['start_date']
				end_date = request.POST['end_date']
				anho = request.POST.getlist('anho') if 'anho' in request.POST else None				
				solicitante = request.POST.getlist('solicitante') if 'solicitante' in request.POST else None
				area_solicitante = request.POST.getlist('area_solicitante') if 'area_solicitante' in request.POST else None

				anho = ",".join(anho) if anho!=[''] else None
				solicitante = ",".join(solicitante) if solicitante!=[''] else None
				area_solicitante = ",".join(area_solicitante) if area_solicitante!=[''] else None

				_start = request.POST['start']
				_length = request.POST['length']
				_search = request.POST['search[value]']
								
				# _order = ['barrio','manzana','nro_casa'] debe enviarse ya el orden desde el datatable para default
				_order = []
				# print(request.POST)
				#range(start, stop, step)
				for i in range(9): 
					_column_order = f'order[{i}][column]'
					# print('Column Order:',_column_order)
					if _column_order in request.POST:					
						_column_number = request.POST[_column_order]
						# print('Column Number:',_column_number)
						if _column_number == '9': #Hacemos esto por que en el datatable edad es un campo calculado
							_order.append('fecha_nacimiento')
						elif _column_number == '2': #Hacemos esto por que en el datatable fullname es un campo calculado
							pass
							# _order.append('apellido')
							# _order.append('nombre')
						else:			
							_order.append(request.POST[f'columns[{_column_number}][data]'].split(".")[0])
					if f'order[{i}][dir]' in request.POST:
						_dir = request.POST[f'order[{i}][dir]']
						if (_dir=='desc'):
							_order[i] = f"-{_order[i]}"
				# print('Order:', _order)
				if len(term):
					_search = term
				

				_where = "'' = %s"
				# _where = "nro_pedido = 1000"
				if len(_search):
					if _search.isnumeric():
						_where = " nro_pedido = %s"
					else:
						_search = '%' + _search.replace(' ', '%') + '%'
						_where = " upper(descripcion||' '|| destino) LIKE upper(%s)"			

				if anho:
					_where += f" AND pedido_movimiento.anho IN ({anho})"
				if solicitante:
					_where += f" AND pedido_movimiento.solicitante_id IN ({solicitante})"
				if area_solicitante:
					_where += f" AND pedido_movimiento.area_solicitante_id IN ({area_solicitante})"
				# if len(pasoxpc):
				# 	_where += f" AND COALESCE(electoral_movimiento.pasoxpc,'N') = '{pasoxpc}'"
				# if len(pasoxmv):
				# 	_where += f" AND COALESCE(electoral_movimiento.tipo_voto_id,0) <> 11 \
				# 				 AND COALESCE(electoral_movimiento.pasoxmv,'N') = '{pasoxmv}'"
				
				qs = Movimiento.objects\
								.filter()\
								.extra(where=[_where], params=[_search])\
								.order_by(*_order)

				#Pedidos del Año
				if len(start_date) and len(end_date):
					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					qs = qs.filter(fecha__range=(start_date,end_date))
								   
				total = qs.count()
				# print(qs.query)
				
				if _start and _length:
					start = int(_start)
					length = int(_length)
					page = math.ceil(start / length) + 1
					per_page = length
				
				if _length== '-1':
					qs = qs[start:]
				else:
					qs = qs[start:start + length]

				position = start + 1
				for i in qs:
					item = i.toJSON()
					item['position'] = position					
					data.append(item)
					position += 1
				# print(data)
				data = {'data': data,
						'page': page,  # [opcional]
						'per_page': per_page,  # [opcional]
						'recordsTotal': total,
						'recordsFiltered': total, }
			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url'] = reverse_lazy('movimiento_create')
		context['title'] = 'Listado de Movimientos'
		return context

class MovimientoCreateView(PermissionMixin, CreateView):
	model = Movimiento
	template_name = 'pedido/movimiento/create.html'
	form_class = MovimientoForm
	success_url = reverse_lazy('movimiento_list')
	permission_required = 'add_movimiento'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def validate_data(self):
		data = {'valid': True}
		try:			
			type = self.request.POST['type']
			obj = self.request.POST['obj'].strip()            
			if type == 'nro_pedido':                
				if Movimiento.objects.filter(nro_pedido__exact=obj):
					data['valid'] = False
			if type == 'no_denominacion':
				if Movimiento.objects.filter(denominacion__iexact=obj):
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
	
	# Este usamos para el modal 	
	def get(self, request, *args, **kwargs):
		data = {}				
		try:	
			if request.user.has_perm('pedido.add_movimiento'):			
				# pk = kwargs['pk']
				# elector = get_object_or_404(Movimiento, pk=pk)
				form = self.get_form()
				self.template_name = 'pedido/movimiento/create_modal.html'
				# context =self.get_context_data(**kwargs)
				context={}				
				context['form'] = form				
				context['class_form'] = 'js-create-form'
				context['action_url'] = reverse_lazy('movimiento_create')
				context['list_url'] = self.success_url
				context['title'] = 'Nuevo registro de un Pedido'
				context['action'] = 'add'
				data['html_form'] = render_to_string(self.template_name, context, request=request)
			else:
				data['error'] = 'No tiene permisos para editar'
		
		except Exception as e:
			print(str(e))
			data['error'] = str(e)
		# print(data['html_form'])
		return HttpResponse(json.dumps(data), content_type='application/json')
		#return  JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['list_url'] = self.success_url
		context['title'] = 'Nuevo registro de un Pedido'
		context['action'] = 'add'
		return context

class MovimientoUpdateView(PermissionMixin, UpdateView):
	model = Movimiento
	template_name = 'pedido/movimiento/create.html'
	form_class = MovimientoForm
	success_url = reverse_lazy('movimiento_list')	
	permission_required = 'change_movimiento'

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
			if type == 'no_descripcion':
				if Movimiento.objects.filter(name__iexact=obj).exclude(id=id):
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
			elif action == 'search_area_solicitante_id':
				data = [{'id': '', 'text': '------------'}]
				for i in Dependencia.objects.filter(dependencia_padre_id=request.POST['id']):
					# data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
					data.append({'id': i.id, 'text': i.denominacion})
			else:
				data['error'] = 'No ha seleccionado ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')
	
	# Este usamos para el modal 	
	def get(self, request, *args, **kwargs):
		data = {}				
		try:	
			if request.user.has_perm('pedido.change_movimiento'):			
				pk = kwargs['pk']
				elector = get_object_or_404(Movimiento, pk=pk)
				form = MovimientoForm(instance=elector)
				self.template_name = 'pedido/movimiento/create_modal.html'
				context = self.get_context_data(**kwargs)
				context['form'] = form				
				context['class_form'] = 'js-update-form'
				context['action_url'] = reverse_lazy('movimiento_update', kwargs={'pk': pk})
				data['html_form'] = render_to_string(self.template_name, context, request=request)
			else:
				data['error'] = 'No tiene permisos para editar'
		
		except Exception as e:
			data['error'] = str(e)
		# print(data['html_form'])
		return HttpResponse(json.dumps(data), content_type='application/json')
		#return  JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['list_url'] = self.success_url
		context['title'] = 'Edición de un Pedido'
		context['action'] = 'edit'
		return context


# class MovimientoDeleteView(PermissionMixin, DeleteView):
# 	model = Movimiento
# 	template_name = 'pedido/movimiento/delete.html'
# 	success_url = reverse_lazy('movimiento_list')
# 	permission_required = 'delete_movimiento'

# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super().dispatch(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		data = {}
# 		try:
# 			self.get_object().delete()
# 		except Exception as e:
# 			data['error'] = str(e)
# 		return HttpResponse(json.dumps(data), content_type='application/json')

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['title'] = 'Notificación de eliminación'
# 		context['list_url'] = self.success_url
# 		return context


# def test_reporte(request):
# 	# debemos obtener nuestro objeto classroom haciendo la consulta a la base de datos
# 	report = JasperReportBase()
# 	report.report_name ='rpt_001'
# 	return report.render_to_response()
