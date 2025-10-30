from django import forms
from auditoria.models import CalificacionTributaria, DeclaracionJurada
from instrumentos.models import Mercado, Instrumento
from auditoria.models import FactorMensual
from datetime import date

class IngresoCalificacionManualForm(forms.ModelForm):
    mercado = forms.ModelChoiceField(
        queryset=Mercado.objects.all(),
        label = "Mercado",
        empty_label= "Seleccione un mercado",
        widget=forms.Select(attrs= {'class' : 'form-control'})
    )
    instrumento = forms.ModelChoiceField(
        queryset= Instrumento.objects.all(),
        empty_label= "Seleccione un instrumento",
        widget=forms.Select(attrs={'class' : 'form-control'})
    )

    factor_valor = forms.FloatField(
        label= "Factor de Actualizacion",
        min_value=0.0,
        widget=forms.NumberInput(attrs={'class' : 'form-control', 'step' : '0.0001'})
    )


    class Meta:
        model = CalificacionTributaria
        fields = [
            'descripcion', 'fecha_pago', 'secuencia_evento', 'dividendo',
            'valor_historico', 'año_tributario'
        ]
        widgets = {
            'descripcion' : forms.TextInput(attrs={'class' : 'form-control'}),
            'fecha_pago' : forms.DateInput(attrs={'type' : 'date', 'class' : 'form.control'}),
            'secuencia_evento' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'dividendo' : forms.NumberInput(attrs= {'class' : 'form-control', 'step' : '0.01'}),
            'valor_historico' : forms.NumberInput(attrs={'class' : 'form-control', 'step' : '0.01'}),
            'año_tributario' : forms.NumberInput(attrs= {'class' : 'form-control', 'min' : 2020, 'max ': 2100}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if 'mercado' in self.data:
                try:
                    mercado_id = int(self.data.get('mercado'))
                    self.fields['instrumento'].queryset = Instrumento.objects.filter(mercado_id = mercado_id)
                except(ValueError, TypeError):
                    print("Instrumento no valido dentro del mercado")
            else:
                self.fields['instrumento'].queryset = Instrumento.objects.none()

        def save(self, user = None, commit = True):
            declaracion = DeclaracionJurada.objects.get_or_create(
                tipo_declaracion = "Anual",
                fecha_extraccion = date.today(),
                estado_declaracion = "Pendiente"

            )

            factor = FactorMensual.objects.create(
                usuario = user,
                valor_factor = self.cleaned_data['factor_valor'],
                fecha_factor = date.today(),
                regimen = "Manual"
            )

            calificacion = super().save(commit=False)
            calificacion.instrumento = self.cleaned_data = ['instrumento']
            calificacion.declaracion = declaracion
            calificacion.factor = factor
            calificacion.isfut = self.cleaned_data_data.get('isfut', False)
            calificacion.origen = "Manual"

            if commit:
                calificacion.save()
            return calificacion


    
    
