from django import forms
from auditoria.models import Reportes
class ReporteForm(forms.Form):
    titulo = forms.CharField(
        label='Título',
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control'})
        )
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        )
    area_afectada = forms.CharField(
        label='Área Afectada',
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    
    class Meta:
        model = Reportes
        fields = ['titulo', 'descripcion', 'fecha', 'area_afectada', 'usuario']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'area_afectada': forms.TextInput(attrs={'class': 'form-control'}),
        }