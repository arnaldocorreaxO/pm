import datetime
from config.utils import *
from core.base.models import ModeloBase, Sucursal
from django.db import models
from django.forms.models import model_to_dict
from crum import get_current_user

'''DEPENDENCIAS'''
class Dependencia(ModeloBase):	
	sucursal = models.ForeignKey(Sucursal,on_delete=models.PROTECT)
	dependencia_padre = models.ForeignKey('self',null=True,blank=True,on_delete=models.PROTECT)
	denominacion = models.CharField(max_length=100)
	denom_corta = models.CharField(verbose_name='Denom. Corta',max_length=25,unique=True,blank=True,null=True)
		
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
	def __str__(self):
		return f"{self.denominacion}"
	
	def nombre_corto(self):
		return f"{self.denom_corta}"

	class Meta:
	# ordering = ['1',]
		# db_table = 'as_marcacion'
		verbose_name = 'Dependencia'
		verbose_name_plural = 'Dependencias'

'''DEPENDENCIAS'''
class Destino(ModeloBase):	
	denominacion = models.CharField(max_length=100,unique=True)
			
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
	def __str__(self):
		return f"{self.denominacion}"

	class Meta:
	# ordering = ['1',]
		# db_table = 'as_marcacion'
		verbose_name = 'Destino'
		verbose_name_plural = 'Destinos'


'''PEDIDOS DE MATERIALES Y/O BIENES'''
class Movimiento(ModeloBase):	
	ESTADO_PEDIDO=(
		(' ','PENDIENTE'),
		('P','PARCIAL CUMPLIDO'),
		('C','CUMPLIDO'),
		('A','ADJUDICADO'),
		('L','LICITACION'),		
	)		
	sucursal = models.ForeignKey(Sucursal,on_delete=models.PROTECT)	
	nro_pedido = models.IntegerField() 
	fecha= models.DateField()
	anho = models.IntegerField(default=0)
	solicitante = models.ForeignKey(Dependencia,on_delete=models.PROTECT,related_name='solicitante') #Gerencia, Direccion o Departamento Solicitante 
	area_solicitante = models.ForeignKey(Dependencia,on_delete=models.PROTECT,related_name='area_solicitante',null=True) #El Area Solicitante
	descripcion = models.CharField(max_length=250)	
	destino = models.CharField(max_length=250,null=True,blank=True)	
	# destino = models.ForeignKey(Destino,on_delete=models.PROTECT)
	situacion = models.CharField(max_length=2,choices=ESTADO_PEDIDO,null=True,blank=True)
	ref_doc_asociado = models.TextField(null=True,blank=True) #Remisiones, Contrato, Ordenes de Compra
	ref_ped_anterior = models.CharField(max_length=100,null=True,blank=True) #Referencia Pedido Anterior
	nro_expediente = models.CharField(max_length=10,null=True,blank=True)
	url = models.URLField(null=True,blank=True)

	def toJSON(self):
		# Para obtener valor del choice 
		# Opcion 1
		# test = [("hi", 1), ("there", 2)]
		# test = dict(test)
		# print test["hi"] # prints 1
		# Opcion 2
		# [tup for tup in a if tup[0] == 1]
		estado_pedido = dict(self.ESTADO_PEDIDO)
		item = model_to_dict(self)
		item['fecha'] = self.fecha.strftime('%d/%m/%Y') if self.fecha else None
		item['solicitante_denom_corta'] = self.solicitante.nombre_corto() if self.solicitante else None
		item['area_solicitante_denom_corta'] = self.area_solicitante.nombre_corto() if self.area_solicitante else None
		item['situacion'] = estado_pedido[self.situacion] if self.situacion else None
		# item['situacion'] = [tup[1] for tup in self.ESTADO_PEDIDO if tup[0] == self.situacion] if self.situacion else None
		return item
	
	def __str__(self):
		return f"{self.nro_pedido} - {str(self.fecha)} -  {str(self.destino)}"

	# '''SAVE'''
	# def save(self, *args, **kwargs):
	# 	import datetime
	# 	user = get_current_user()
	# 	# print(user)
	# 	if user and not user.pk:
	# 		user = None
	# 	# print(dir(self))
	# 	if not self.usu_insercion_id:
	# 		self.usu_insercion = user
	# 	self.usu_modificacion = user
	# 	self.anho = int(datetime.datetime.strftime(self.fecha,'%Y'))
	# 	super(Movimiento, self).save(*args, **kwargs)

	class Meta:
	# ordering = ['1',]
		# db_table = 'as_marcacion'
		verbose_name = 'Solicitud'
		verbose_name_plural = 'Solicitudes'
		unique_together = ['sucursal','anho','nro_pedido']
