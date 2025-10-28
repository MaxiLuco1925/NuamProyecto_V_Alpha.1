from django.db import models
from datetime import datetime
from instrumentos.models import Instrumento 
from usuarios.models import Usuario
from declaraciones.models import DeclaracionJurada
from declaraciones.models import CargaArchivo

class CalificacionTributaria(models.Model):

    Estado_validacion_Choices = [
    ('Pendiente', 'Pendiente'),
    ('Validado', 'Validado'),
    ('Rechazado', 'Rechazado'),
]
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    declaracion = models.ForeignKey(DeclaracionJurada, on_delete=models.CASCADE)
    factor = models.ForeignKey('auditoria.FactorMensual', on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField()
    descripcion = models.TextField()
    secuencia_evento = models.IntegerField()
    dividendo = models.FloatField()
    valor_historico = models.FloatField()
    año_tributario = models.IntegerField()
    isfut = models.BooleanField(default=False)
    origen = models.ForeignKey(CargaArchivo, on_delete= models.SET_NULL, null = True, blank= True, help_text= "Carga de archivo que originó esta calificación")
    estado_tributario = models.CharField(max_length=50, default="Activo")
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE, null = True, blank= True )

    def __str__(self):
        return self.instrumento.nombre
2




class FactorMensual(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor_factor = models.FloatField()
    fecha_factor = models.DateField()
    regimen = models.CharField(max_length=200)
    carga_origen = models.ForeignKey(CargaArchivo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.valor_factor


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
    estado = models.CharField(max_length=20, choices= Estado_Choices, default='pendiente')

    def __str__(self):
        return self.titulo
    
