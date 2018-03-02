# -*- coding: utf-8 -*-

import re


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
        (<font\scolor=\'red\'\sstyle=\'background-color:yellow;\'>)   # Bloque 2, busca valor constante (los '\s' es porque con VERBOSE no puede contener espacios
        ([a-z]+)    # Bloque 3, busca cualquier caracter
        (</font>) #   # Bloque 4
        """, re.VERBOSE)

    return re.sub(patron, r'\1\3', nueva)  # El resultado es el bloque 1 y el 3
