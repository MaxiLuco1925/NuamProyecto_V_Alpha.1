from django import forms
from usuarios.models import Usuario
import re
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm    

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
        fields = ['documento_identidad', 'nombre', 'email', 'telefono', 'genero', 'edad', 'region', 'comuna']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class' : 'form-input'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-input'}),
            'telefono' : forms.TextInput(attrs={'class' : 'form-input'}),
            'genero' : forms.Select(attrs={'class' : 'form-input'}, choices=[
                ('', 'Select'), ('Hombre', 'Hombre'), ('Mujer', 'Mujer')
            ]),
            'documento_identidad' : forms.TextInput(attrs={'class' : 'form-input'}),
            'edad' : forms.NumberInput(attrs={'class' : 'form-input'}),
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
        
        if contraseña1:
            try:
                validate_password(contraseña1, self.instance)
            except DjangoValidationError as error:
                self.add_error('password1', error)
                
                
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


class UsuarioRolForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'})
        }



class ResetearContraseñaForm(PasswordResetForm):
    email = forms.EmailField(
        label = ('Email'),
        max_length=256,
        widget=forms.EmailInput(attrs={
            'autocomplete' : 'email',
            'class' : 'form-control',
            'placeholder' : 'Ingresa tu correo'
        })
    )

    def get_users(self, email):
        active_users = Usuario._default_manager.filter(
            email__iexact = email,
            is_active = True
        )
        return active_users
    
class CustomContraseñaForm(SetPasswordForm):
        new_password1 = forms.CharField(
            label=("Nueva Contraseña"),
            widget= forms.PasswordInput(attrs={
                'autocomplete' : 'new-password',
                'class' : 'form-control',
                'placeholder' : 'Ingresa tu nueva contraseña'
            }),
            strip=False,
        )
        new_password2 = forms.CharField(
            label=("Confirmar nueva contraseña"),
            strip= False,
            widget=forms.PasswordInput(attrs={
                'autocomplete' : 'new-password',
                'class' : 'form-control',
                'placeholder' : 'Repite tu nueva contraseña'
            }),
        )