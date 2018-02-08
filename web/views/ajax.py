# -*- coding: utf-8 -*-

import sys
import traceback
import os
import logging
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic.edit import View
from django.conf import settings

from ..models import Adjunto
from ..models import Nota
from ..models import Libro

logger = logging.getLogger(__name__)


class Datos(object):
    def __init__(self, **kargs):
        self.request = kargs.get("request", None)

    def adjunto_borra(self, adj_id):
        adj = Adjunto.objects.get(id=adj_id)
        adj.delete()
        return {"data": self.adjunto_html(adj.nota.id), "nota_id": adj.nota.id}

    def adjunto_html(self, nota_id):
        html = ""
        for adj in Adjunto.objects.filter(nota=nota_id).order_by("nombre"):
            link_download = "<a href='/adjunto_bajar/%s/'>%s</a>" % (adj.id, adj.nombre)
            href_baja = "javascript:borraAdjunto(%s);" % adj.id
            html += """
                <tr>
                    <td class="wrappable">%s</td>
                    <td class="text-center">
                        <a href="%s" class="text-danger" role="button"><span class="glyphicon glyphicon-trash"></span></a>
                    </td>                
                </tr>            
        """ % (link_download, href_baja)

        if not html:
            return ""

        return """
            <div class="panel panel-default">
            <table class='table' style='width:100%%'>
              %s
            </table>
            </div>                
            """ % html

    def lee_nota(self, nota_id):
        nota = Nota.objects.filter(id=nota_id).first()
        resul = dict()
        resul["texto"] = nota.texto if nota else ""
        resul["html"] = nota.html if nota else ""
        return resul

    def graba_nota_texto(self, nota_id, texto, html):
        nota = Nota.objects.get(id=nota_id)
        nota.texto = texto
        nota.html = html
        nota.save()

    def nueva_nota(self, libro_id):
        nota = Nota()
        nota.user = self.request.user
        nota.libro = Libro.objects.get(id=libro_id)
        nota.save()
        return nota.id


class AjaxView(View, Datos):
    def dispatch(self, request, *args, **kwargs):
        self.request = request

        try:
            if self.request.GET:
                param = self.request.GET
                funcion = args[0]

                r = getattr(self, funcion)(**param)
                return HttpResponse("false") if r else HttpResponse("true")

            if self.request.POST:
                param = request.POST["param"]
                param = json.loads(param)
                funcion = args[0]

                r = getattr(self, funcion)(**param)
                resul = {"err": False, "param": r}
                return JsonResponse(resul)

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc = traceback.format_exception(exc_type, exc_value, exc_traceback)
            error = os.linesep.join(exc)

            logger.debug(error)
            print(error)

            #  TODO:: Comentado para que muestre siempre el error
            #  if not settings.DEBUG:
            #      error = "Error de comunicación con el servidor."

            resul = {"err": error, "param": {}}
            return JsonResponse(resul)
