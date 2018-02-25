# -*- coding: utf-8 -*-


def marca_texto(busca, cadena, template="<font color='red' style='background-color:yellow;'>%s</font>", ind=0):
    if not busca:
        return cadena

    ind = cadena.lower().find(busca.lower(), ind)
    if ind < 0:
        return cadena

    valor = template % cadena[ind:ind + len(busca)]
    cadena = cadena[:ind] + valor + cadena[ind + len(busca):]
    return marca_texto(busca, cadena, template, ind + len(valor) + 1)

