# -*- coding: utf-8 -*-

from markdown import markdown

from ..models import Nota


def run(*args):
    """
    Cambia nota.texto de formato markdawn a html
    """
    for nota in Nota.objects.all():
        html = markdown(nota.texto, extensions=["markdown.extensions.tables"])
        nota.texto = html
        nota.save()


#   python manage.py  runscript nota_texto2html --settings notas.settings_jh



