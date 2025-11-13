import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as text

class ValidadorMayusculas(object):
    def validate(self, password, user = None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                text("La Contraseña debe contener al menos una letra mayúscua!!."),
                code = 'password_no_uppercase',

            )
    def get_help_text(self):
        return text("Tu contraseña debe contener al menos una letra mayúscula.")
    
class ValidadordeNumeros(object):
    def validate(self, password, user = None):
        if not re.findall('[0-9]', password):
            raise ValidationError(
                text("La contraseña debe contener al menos un número.!!!"),
                code='password_no_number'
            )
    def get_help_text(self):
        return text("Tu contraseña debe contenrr al menos un número.")

class ValidadorCaracteresEspeciales(object):
    def __init__(self, allowed_chars=''):
        self.allowed_chars = allowed_chars

    def validate(self, password, user = None):
        if not any(c in self.allowed_chars for c in password):
            raise ValidationError(
                text("La contaseña debe contener al menos un carácter especial como : %(chars).s !!") % {'chars' : self.allowed_chars},
                     code = 'password_no_special',
                     params = {'allowed_chars' : self.allowed_chars},
                     )
    def get_help_text(self):
        return text("Tu contraseña debe contener al menos un carácter espcial.")    
               
        

