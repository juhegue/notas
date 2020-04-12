# -*- coding: utf-8 -*-

import sys
import traceback
import os
import logging
import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic.edit import View

from ..models import Adjunto
from ..models import AdjuntoTemporal
from web.views.adjunto import adjunto_html

logger = logging.getLogger(__name__)


class Datos(object):
    def __init__(self, **kargs):
        self.request = kargs.get("request", None)
        self.error = False

    def adjunto_borra(self, adj_id):
        adj = Adjunto.objects.get(id=adj_id)
        nota = adj.nota
        if not self.request.user.is_staff:
            if adj.user.email != self.request.user.email:
                self.error = "Esta nota pertenece al usuario '%s'" % adj.user.email
                return
        adj.delete()
        return {"data": nota.adjunto_html()}

    @staticmethod
    def adjunto_borra_temporal(adj_id):
        adj = AdjuntoTemporal.objects.get(id=adj_id)
        adj.delete()
        return {"data": adjunto_html(adj.uuid_id)}


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

            logger.error(error)

            #  TODO:: Comentado para que muestre siempre el error
            #  if not settings.DEBUG:
            #      error = "Error de comunicación con el servidor."

            resul = {"err": error, "param": {}}
            return JsonResponse(resul)
