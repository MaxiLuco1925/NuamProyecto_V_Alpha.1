from django import forms
from usuarios.models import Usuario
import re
from django.contrib.auth.hashers import make_password, check_password    

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label = 'Contraseña',
        widget= forms.PasswordInput(attrs= {'class' : 'form-input'}) 
    )
    password2 = forms.CharField(
        label = "Confirmar Conteraseña",
        widget= forms.PasswordInput(attrs={'class' : 'form-input'})
    )

    class Meta:
        model = Usuario
        fields = ['documento_identidad', 'nombre', 'email', 'telefono', 'genero', 'edad', 'pais', 'region', 'comuna']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class' : 'form-input'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-input'}),
            'telefono' : forms.TextInput(attrs={'class' : 'form-input'}),
            'genero' : forms.Select(attrs={'class' : 'form-input'}, choices=[
                ('', 'Select'), ('Hombre', 'Hombre'), ('Mujer', 'Mujer')
            ]),
            'documento_identidad' : forms.TextInput(attrs={'class' : 'form-input'}),
            'edad' : forms.NumberInput(attrs={'class' : 'form-input'}),
            'pais' : forms.Select(attrs={'class' : 'form-input'}, choices=[
                ('', 'Select'), ('Chile', 'Chile'), ('Perú', 'Perú'), ('Colombia', 'Colombia')
            ]),
            'region' : forms.TextInput(attrs={'class' : 'form-input'}),
            'comuna' : forms.TextInput(attrs={'class' : 'form-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        pais = cleaned_data.get('pais')
        documento = cleaned_data.get('documento_identidad')

        if not (pais and documento):
            return cleaned_data
        
        reglas ={
            'Chile' : {
                'patron' : r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$',
                'mensaje' : 'El RUT Chileno debe contener verse de la siguiente manera 9.000.000-4, 10.000.000-6 o con un digito K'
            },
            'Perú':{
                'patron' : r'^\d{8}$',
                'mensaje' : 'El DNI peruano debe tener 8 dígitos númericos !!'
            },
            'Colombia':{
                'patron' : r'^\d{5,10}$',
                'mensaje' : 'La Cédula Colombiana debe tener entre 5 y 10 dígitos !!!'
            }
        }

        if pais in reglas:
            regla = reglas[pais]
            if not re.match(regla['patron'], documento):
                self.add_error('documento_identidad', regla['mensaje'])
        return cleaned_data
    
    def clean_password2(self):
        contraseña1 = self.cleaned_data.get('password1')
        contraseña2 = self.cleaned_data.get('password2')

        if contraseña1 and contraseña2 and contraseña1 != contraseña2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return contraseña2


    def save(self, commit = True):
        usuario = super().save(commit=False)
        usuario.contraseña_hash = make_password(self.cleaned_data['password1'])

        if commit:
            usuario.save()

        return usuario
    
class InicioSesionForm(forms.Form):
    documento_identidad = forms.CharField(
        label="RUT",
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-input'})
    )
    contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class':  'form-input'})
    )

    
    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get("documento_identidad")
        contraseña = cleaned_data.get("contraseña")

        if documento and contraseña:
            try:
                usuario = Usuario.objects.get(documento_identidad=documento)
            except Usuario.DoesNotExist:
                raise forms.ValidationError("RUT ingresado no existe")
            if not check_password(contraseña,usuario.contraseña_hash):
                raise forms.ValidationError("Contraseña incorrecta")
        return cleaned_data