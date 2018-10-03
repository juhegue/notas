# -*- coding: utf-8 -*-

import urllib
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from ..util.util import marca_texto, codehex
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


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag(takes_context=True)
def editor_choices(context):
    url = context.request.get_full_path()
    urlhex = codehex(url)
    menu = ""
    for n, editor in enumerate(EDITOR_CHOICES):
        if context.request.user.editor == editor[0]:
            menu += '<li class="disabled"><a href="#/cambia_editor/%s/%s/">' \
                    '<i class="glyphicon glyphicon-ok"></i> %s</a></li>' % (urlhex, editor[0], editor[1])
        else:
            menu += '<li><a href="/cambia_editor/%s/%s/">&nbsp;&nbsp;&nbsp;&nbsp;%s</a></li>' % \
                    (urlhex, editor[0], editor[1])
    if menu:
        menu += '<li role="separator" class="divider">'

    menu += '<li><a href="/logout/"><i class="fa fa-sign-out"></i>Salir</a></li>'

    return mark_safe(menu)

