from django.db import models
from django.contrib.auth.models import User




class Rol(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    

class Permiso(models.Model):
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.descripcion
    

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')


class Usuario(models.Model):
        Pais_Choices =[
        ('', 'Select'),
        ('Chile', 'Chile'),

    ]
        Genero_Choices = [
        ('', 'Select'),
        ('HOMBRE', 'Hombre'),
        ('MUJER', 'Mujer'),
    ]
        documento_identidad = models.CharField(max_length=100, blank=True, unique=True)
        nombre = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        genero = models.CharField(max_length=40, blank=True, choices= Genero_Choices)
        telefono = models.CharField(max_length=60)
        edad = models.PositiveIntegerField(blank=True, null=True)
        pais = models.CharField(max_length=100, blank=True, choices=Pais_Choices)
        region = models.CharField(max_length=40, blank=True)
        comuna = models.CharField(max_length=70, blank=True)
        contraseña_hash = models.CharField(max_length=256)
        rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, blank= True, null=True)
        estado = models.CharField(max_length=20, null = True, blank= True)
        verificado = models.BooleanField(default=False)



        def __str__(self):
             return self.nombre 
        


class AuditoriaSesion(models.Model):
    TIPOS_EVENTO = [
         ('LOGIN', 'Inicio de Sesisón'),
         ('LOGOUT', 'Cierre de Sesión'),
         ('LOGIN_FALLIDO', 'Intento fallido'),
         ('INYECCION_SQL', 'Intento de Inyección SQL'),
         ('XSS', 'Intento de Cross-Site Scripting'),
         ('CSRF', 'Intento CSRF'),
         ('ACCESO_DENEGADO', 'Acceso Denegado'),
         ('FUERZA_BRUTA', 'Ataque Fuerza Bruta'),    
    ]

    NIVEL_AMENAZA = [
         ('BAJO', 'Bajo'),
         ('MEDIO', 'Medio'),
         ('ALTO', 'Alto'),
         ('CRITICO', 'Critico')

    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    documento_intentado = models.CharField(max_length=100, blank=True)
    exito = models.BooleanField()
    rol = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)#auto_now_add=True sirve para asignar la fecha y hora de manera automatica
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO, default='LOGIN')
    nivel_amenaza = models.CharField(max_length=10, choices=NIVEL_AMENAZA, default='BAJO')
    ip_adress = models.GenericIPAddressField(null= True, blank= True)
    user_agent = models.TextField(blank= True)
    detalles = models.TextField(blank= True)
    ruta_accedida = models.CharField(max_length=10, blank= True)
    metodo_http = models.CharField(max_length=10, blank= True)
    payload_intentado = models.TextField(blank= True)
    parametro_afectado = models.CharField(max_length=100, blank=True)
    tipo_ataque = models.CharField(max_length=50, blank=True)

    def __str__(self):
        estado = "Éxito" if self.exito else "Fallido"
        return f"{self.documento_intentado} - {estado} - {self.fecha}"
    


