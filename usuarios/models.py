from django.db import models

from django.db import models

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
        ('Perú', 'Perú'),
        ('Colombia', 'Colombia'),
    ]
        Genero_Choices = [
        ('', 'Select'),
        ('HOMBRE', 'Hombre'),
        ('MUJER', 'Mujer'),
    ]
        documento_identidad = models.CharField(max_length=100, blank=True, unique=True)
        nombre = models.CharField(max_length=60)
        email = models.EmailField(unique=True)
        genero = models.CharField(max_length=40, blank=True, choices= Genero_Choices)
        telefono = models.CharField(max_length=60)
        edad = models.PositiveIntegerField(blank=True, null=True)
        pais = models.CharField(max_length=100, blank=True, choices=Pais_Choices)
        region = models.CharField(max_length=40, blank=True)
        comuna = models.CharField(max_length=70, blank=True)
        contraseña_hash = models.CharField(max_length=256)

        def __str__(self):
             return self.nombre 
