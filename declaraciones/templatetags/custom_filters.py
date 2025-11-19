from django import template

register = template.Library()

@register.filter
def split(value, arg):

    return value.split(arg)

@register.filter
def get_factor(factores, numero):

    try:
        num = int(numero)
        for factor in factores:
            if factor.numero_factor == num:
                return factor
        return None
    except (ValueError, AttributeError, TypeError):
        return None
    
@register.filter
def get_item_by_factor(diccionario, factor):
    try:
        return diccionario.get(factor)
    except Exception:
        return None
    
@register.filter
def get_item_by_factor(factors, numero):
    return factors.filter(numero_factor=numero).first()