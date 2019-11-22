from decimal import Decimal
from django import template

register = template.Library()

# Creacion de custom tag para poder usarlos en los templates


@register.filter
def index(List, i):
    try:
        return List[int(i)]
    except IndexError:
        return None


@register.filter
def numberformat(value):
    if value:
        return "{:,}".format(value).replace(',', '.')
    return str()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def multiply(value, arg):
    return int(value * arg)


@register.filter
def multiplydecimal(value, arg):
    return round(Decimal(value * arg), 0)


@register.filter
def discount(value, arg):
    discount = round((value * arg) / 100, 2)
    return discount


@register.filter
def rutformat(value):
    actual = value.replace("/^0+/", "")
    if actual is not '' and len(actual) > 1:
        rut_sin_formato = actual.replace(r"/\./g", "")
        actual_limpio = rut_sin_formato.replace("/-/g", "")
        inicio = actual_limpio[0:-1]
        rut_formateado = ""
        i = 0
        j = 1
        for i in reversed(inicio):
            rut_formateado = i + rut_formateado
            if j % 3 == 0 and j <= len(inicio) - 1:
                rut_formateado = "." + rut_formateado
            j = j + 1

        dv = actual_limpio[-1]
        rut_formateado = rut_formateado + "-" + dv

        return rut_formateado
    return value
