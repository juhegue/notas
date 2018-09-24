# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from ..util.util import marca_texto

register = template.Library()


@register.filter(name='colorea_busca', is_safe=True)
def colorea_busca(valor, arg):
    if arg:
        for busca in arg.split(","):
            busca = busca.strip()
            valor = marca_texto(busca, valor)
        return mark_safe(valor)

    return valor


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")