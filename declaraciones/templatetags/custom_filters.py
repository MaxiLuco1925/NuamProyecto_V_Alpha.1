from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Divide un string por el separador especificado
    Uso: {{ "8,9,10"|split:"," }}
    """
    return value.split(arg)

@register.filter
def get_factor(factores, numero):
    """
    Obtiene un factor específico por su número
    Uso: {{ cal.factormensual_set.all|get_factor:8 }}
    """
    try:
        num = int(numero)
        for factor in factores:
            if factor.numero_factor == num:
                return factor
        return None
    except (ValueError, AttributeError, TypeError):
        return None