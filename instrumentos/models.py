from django.db import models
Paises_Choices=[
    ('Select',''),
    ('Chile', 'Chile'),
    ('Perú', 'Perú'),
    ('Colombia', 'Colombia'),
]


class Mercado(models.Model):
    nombre = models.CharField(max_length=30)
    codigo_mercado = models.CharField(max_length=20, blank=True, choices=Paises_Choices)

    def __str__(self):
        return self.nombre
    

class Instrumento(models.Model):
    mercado = models.ForeignKey(Mercado, on_delete= models.CASCADE)
    codigo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    tipo_instrumento = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre
