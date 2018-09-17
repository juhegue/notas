# -*- coding: utf-8 -*-

import re
from lxml.html.clean import Cleaner


def marca_texto(busca, cadena):
    if not busca:
        return cadena

    # Reemplaza
    patron = re.compile(r"(" + busca + ")", re.IGNORECASE)
    nueva = re.sub(patron, r"<font color='red' style='background-color:yellow;'>\1</font>", cadena)

    # Elimina lo marcado en los links, '<a href=..'
    patron = re.compile(r"""
        (<[\s]?     # Comienzo del 1º bloque busca '<' seguido de algún o ningún blanco
        a\s         # busca 'a' seguido de un o más blancos
        href[\s]?   # busca 'href' seguido de algún o ningún blanco
        =[\s]?      # busca '=' seguido de algún o ningún blanco
        ["]?        # busca '"' puede o no existir
        [a-z]+://)  # busca uno o más caracteres seguidos de '://' y Final del 1º bloque
        ([a-z]+)    # Bloque 2, busca cualquier caracter
        (<font\scolor=\'red\'\sstyle=\'background-color:yellow;\'>)   # Bloque 3, busca valor constante (los '\s' es porque con VERBOSE no puede contener espacios
        ([a-z]+)    # Bloque 4, busca cualquier caracter
        (</font>)   # Bloque 5, busca valor constante
        """, re.VERBOSE)

    return re.sub(patron, r'\1\2\4', nueva)  # El resultado son los bloques 1+2+4


def clean_html(texto_html):
    return texto_html

    # TODO: Anulado ya que quita los 'style' del html
    if texto_html:
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = False  # This is True because we want to activate the styles & stylesheet filter
        html_sin = cleaner.clean_html(texto_html)
        return html_sin
    else:
        return ""

