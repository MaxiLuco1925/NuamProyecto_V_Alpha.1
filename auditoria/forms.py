# forms.py
from django import forms
from auditoria.models import Reportes
from declaraciones.models import CargaArchivo


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['titulo', 'descripcion', 'area_afectada', 'imagen']  
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



class CargaArchivoForm(forms.Form):
    archivo = forms.FileField(
        label='Archivo CSV',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    tipo_carga = forms.ChoiceField(
        choices=CargaArchivo.TIPO_CHOICES,
        widget=forms.HiddenInput()
    )