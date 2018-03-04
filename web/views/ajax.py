# -*- coding: utf-8 -*-

import sys
import traceback
import os
import logging
import json
from markdown import markdown
from lxml.html.clean import Cleaner

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic.edit import View
from django.conf import settings

from ..util.util import marca_texto
from ..util.mk_delextension import DelExtension
from ..models import Adjunto
from ..models import Nota
from ..models import Libro

logger = logging.getLogger(__name__)


class Datos(object):
    def __init__(self, **kargs):
        self.request = kargs.get("request", None)
        self.error = False

    def adjunto_borra(self, adj_id):
        adj = Adjunto.objects.get(id=adj_id)
        if not self.request.user.is_staff:
            if adj.user.email != self.request.user.email:
                self.error = "Esta nota pertenece al usuario '%s'" % adj.user.email
                return

        adj.delete()
        return {"data": self.adjunto_html(adj.nota.id), "nota_id": adj.nota.id}

    def adjunto_html(self, nota_id, sin_borrar=None, busca=None):
        html = ""
        for adj in Adjunto.objects.filter(nota=nota_id).order_by("nombre"):
            nombre = marca_texto(busca, adj.nombre)
            link_download = "<a href='/adjunto_bajar/%s/'>%s</a>" % (adj.id, nombre)
            if sin_borrar:
                html += '<tr><td class="wrappable">%s</td></tr>' % link_download
                continue
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

    def lee_nota(self, nota_id, busca):
        nota = Nota.objects.filter(id=nota_id).first()
        resul = {"texto": "", "htnl": ""}
        if nota:
            resul["texto"] = nota.texto if nota else ""
            html = markdown(nota.texto, extensions=["markdown.extensions.tables",       # tables
                                                    "markdown.extensions.fenced_code",  # cambia <p><code> por <pre><code>
                                                    DelExtension()]
                            )
            if html:
                # elimina javascript y estilos
                cleaner = Cleaner()
                cleaner.javascript = True  # This is True because we want to activate the javascript filter
                cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
                html_sin = cleaner.clean_html(html)
                html_sin = marca_texto(busca, html_sin)
                resul["html"] = html_sin
        return resul

    def graba_nota_texto(self, nota_id, texto, html):
        nota = Nota.objects.get(id=nota_id)
        nota.texto = texto
        nota.save()

    def nueva_nota(self, libro_id):
        nota = Nota()
        nota.user = self.request.user
        nota.libro = Libro.objects.get(id=libro_id)
        nota.save()
        return nota.id


class AjaxView(View):
    def dispatch(self, request, *args, **kwargs):
        datos = Datos(request=request)

        try:
            if self.request.GET:
                param = self.request.GET
                funcion = args[0]

                r = getattr(datos, funcion)(**param)
                return HttpResponse("false") if r else HttpResponse("true")

            if self.request.POST:
                param = request.POST["param"]
                param = json.loads(param)
                funcion = args[0]

                r = getattr(datos, funcion)(**param)
                resul = {"err": datos.error, "param": r}
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
