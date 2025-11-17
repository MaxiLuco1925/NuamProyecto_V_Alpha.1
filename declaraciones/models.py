from django.db import models
from usuarios.models import Usuario

class DeclaracionJurada(models.Model):
    tipo_declaración = models.CharField(max_length=100)
    fecha_extraccion = models.DateTimeField()
    estado_declaracion = models.CharField(max_length=60)

    def __str__(self):
        return self.tipo_declaración


class CargaArchivo(models.Model):
    TIPO_CHOICES = [
        ('montos:dj1948', 'Montos - DJ1948'),
        ('factores', 'Factores Tributarios'),
    ]

    ESTADO_CHOICES = [
        ('procesando', 'Procesando'),
        ('completa', 'Completa'),
        ('fallida', 'Fallida'),
    ]

    archivo = models.FileField(upload_to='cargas/')
    tipo_carga = models.CharField(max_length=30, choices=TIPO_CHOICES)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    cargado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='procesando')
    total_registros = models.IntegerField(default=0)
    registros_exitosos = models.IntegerField(default=0)
    mensaje_error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Carga #{self.id} - {self.tipo_carga} - {self.archivo.name if self.archivo else 'sin archivo'}"


