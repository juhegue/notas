# -*- coding: utf-8 -*-

import re
import binascii
import uuid
from bs4 import BeautifulSoup
#  from lxml.html.clean import Cleaner


def marca_texto(busca, cadena):
    """
    Reemplaza busca en cadena obviando los href
    """
    if not busca:
        return cadena

    for s in busca.split(","):
        s = s.strip()

        # obtiene los href
        soup = BeautifulSoup(cadena, "html.parser")
        href = {str(uuid.uuid4()): link['href'] for link in soup.findAll('a')}

        # reemplaza los href por uuid
        for k, v in href.items():
            cadena = cadena.replace(v, k)

        # Colorea la cadena buscada
        patron = re.compile(r"(" + s + ")", re.IGNORECASE)
        cadena = re.sub(patron, r"<font color='red' style='background-color:yellow;'>\1</font>", cadena)

        # restaura los uuid por los href
        for k, v in href.items():
            cadena = cadena.replace(k, v)

    return cadena


def clean_html(texto_html):
    return texto_html

    # TODO: Anulado ya que quita los 'style' del html  (se realiza con HtmlSanitizer.js)
    if texto_html:
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = False  # This is True because we want to activate the styles & stylesheet filter
        html_sin = cleaner.clean_html(texto_html)
        return html_sin
    else:
        return ""


def codehex(key):    # simple, pero funcional :)
    if key:
        b = key.encode()
        h = binascii.hexlify(b)
        return h.decode("utf8")
    return ""


def decodehex(key):
    if key:
        b = key.encode()
        s = binascii.unhexlify(b)
        return s.decode("utf8")
    return ""


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
