# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from ..util.utiles import marca_texto, codehex
from ..models import EDITOR_CHOICES

register = template.Library()


@register.filter(name='colorea_busca', is_safe=True)
def colorea_busca(valor, arg):
    if arg:
        for busca in arg.split(","):
            busca = busca.strip()
            valor = marca_texto(busca, valor)
        return mark_safe(valor)

    return valor


@register.simple_tag(takes_context=True)
def editor_choices(context):
    url = context.request.get_full_path()
    urlhex = codehex(url)

    resul = list()
    for editor in EDITOR_CHOICES:
        resul.append({
            "url": urlhex,
            "disabled": True if context.request.user.editor == editor[0] else False,
            "key": editor[0],
            "name": editor[1]
        })
    return resul


@register.simple_tag
def param_settings(param):
    if hasattr(settings, param):
        return getattr(settings, param)

