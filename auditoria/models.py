from django.db import models
from datetime import datetime
from instrumentos.models import Instrumento 
from usuarios.models import Usuario
from declaraciones.models import DeclaracionJurada
from declaraciones.models import CargaArchivo

class CalificacionTributaria(models.Model):

    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE, blank= True, null=True)
    declaracion = models.ForeignKey(DeclaracionJurada, on_delete=models.CASCADE, null=True, blank=True)
    fecha_pago = models.DateTimeField()
    descripcion = models.TextField()
    secuencia_evento = models.IntegerField()
    dividendo = models.FloatField()
    valor_historico = models.FloatField()
    año_tributario = models.IntegerField()
    isfut = models.BooleanField(default=False)
    origen = models.ForeignKey(CargaArchivo, on_delete= models.SET_NULL, null = True, blank= True, help_text= "Carga de archivo que originó esta calificación")
    estado_tributario = models.CharField(max_length=50, default="Manual")
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE, blank= True )

    def __str__(self):
        return self.instrumento.nombre





class FactorMensual(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.TextField(blank = True, null = True)
    valor_factor = models.FloatField()
    fecha_factor = models.DateField()
    carga_origen = models.ForeignKey(CargaArchivo, on_delete=models.SET_NULL, null=True, blank=True)
    numero_factor = models.IntegerField(default = 0)
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.SET_NULL, null=True, blank=True,)

    class Meta:
        ordering = ['numero_factor']


    def __str__(self):
        return f"Factor {self.numero_factor} : {self.descripcion}"


class Reportes(models.Model):
    Estado_Choices = [
        ('pendiente' , 'Pendiente'),
        ('revisado', 'Revisado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(help_text="Detalles del error encontrado")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reportes_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    area_afectada = models.CharField(max_length=90, default="Panel de calificacion")
    estado = models.CharField(max_length=20, choices= Estado_Choices, default='pendiente')
    imagen = models.FileField(upload_to='reportes_evidencias/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    


class AuditoriaLog(models.Model):
    tablaAfectada = models.CharField(max_length=100)
    accion = models.CharField(max_length=50)
    descripcion = models.TextField()
    usuario = models.CharField(max_length=100)
    fecha = models.DateTimeField()

    class Meta:
        managed = False  #esto es para que no cree la tabla o la trate de migrar
        db_table = 'auditoria_log'

    



