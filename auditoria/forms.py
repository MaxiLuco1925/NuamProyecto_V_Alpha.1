# forms.py
from django import forms
from auditoria.models import Reportes


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['titulo', 'descripcion', 'area_afectada', 'imagen']  # Sin fecha
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'area_afectada': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción del error encontrado',
            'area_afectada': 'Área Afectada',
            'imagen': 'Evidencia (Imagen/Archivo)',
        }