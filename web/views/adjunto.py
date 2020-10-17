# coding=utf-8
import json
import os
import mimetypes
import urllib
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.template import Template
from django.template import Context
from django.conf import settings

from ..models import AdjuntoTemporal
from ..models import Adjunto
from ..models import Nota

logger = logging.getLogger(__name__)


def fichero_response(request, fichero, nombre_destino):
    fichero = os.path.join(settings.MEDIA_ROOT, fichero)
    fp = open(fichero, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    type, encoding = mimetypes.guess_type(fichero)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(fichero).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % nombre_destino
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(nombre_destino)

    # if type == 'application/pdf':
    #     response['Content-Disposition'] = 'attachment; ' + filename_header      # Para forzar la descarga
    # else:
    #     if type == 'application/xml':
    #         response['Content-Disposition'] = 'attachment; ' + filename_header  # Para forzar la descarga
    #     else:
    #         response['Content-Disposition'] = 'inline; ' + filename_header      # Para abrir en el navegador
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def adjuntos(nota_id, uuid_id):
    resul = list()
    nota = Nota.objects.filter(id=nota_id).first()
    if nota:
        resul = nota.adjuntos(uuid_id)

    for tmp in AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id=0):
        resul.append({
            "id": tmp.id,
            "nombre": tmp.nombre,
            "tmp": True
        })

    return resul


class AdjuntoBajar(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tipo = kwargs.get("tipo")
        adjunto_id = kwargs.get("adjunto_id")
        try:
            adj = Adjunto.objects.get(id=adjunto_id) if tipo == 1 else AdjuntoTemporal.objects.get(id=adjunto_id)
            response = fichero_response(request, adj.fichero.name, adj.nombre)
        except IOError as e:
            t = Template("<br><h3>I/O ERROR {{ errno }}: {{ strerror }}:</h3><p>{{ fichero }}</p>")
            html = t.render(Context({'fichero': adj.nombre, 'errno': e.errno, 'strerror': e.strerror}))
            return HttpResponse(html, status=404)
        except Exception as e:
            t = Template("<br><h3>ERROR: {{ error }}")
            html = t.render(Context({'error': e}))
            return HttpResponse(html, status=404)
        return response


class AdjuntoSubir(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        nota_id = request.POST.get("nota_id") or 0
        uuid_id = request.POST.get("uuid_id")
        for fichero in request.FILES.getlist("files", []):
            adj = AdjuntoTemporal()
            adj.uuid_id = uuid_id
            adj.fichero = fichero
            adj.save()

        adjs = adjuntos(nota_id, uuid_id)
        return JsonResponse(adjs, safe=False)


class AdjuntoBorrar(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get("tipo")
        adjunto_id = request.POST.get("adjunto_id")
        nota_id = request.POST.get("nota_id")
        uuid_id = request.POST.get("uuid_id")
        if tipo == "0":
            AdjuntoTemporal.objects.get(id=adjunto_id).delete()
        else:
            adj = AdjuntoTemporal()
            adj.uuid_id = uuid_id
            adj.adjunto_borrado_id = adjunto_id
            adj.fichero = None
            adj.save()

        adjs = adjuntos(nota_id, uuid_id)
        return JsonResponse(adjs, safe=False)


