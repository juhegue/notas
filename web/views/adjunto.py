# coding=utf-8

import os
import mimetypes
import urllib

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse
from django.template import Template
from django.template import Context
from django.conf import settings

from .ajax import Datos
from ..models import Adjunto
from ..models import Nota


class AdjuntoBajar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        adj_id = kwargs.get("adj_id")
        try:
            adj = Adjunto.objects.get(id=adj_id)
            response = self.fichero_response(request, adj.fichero.name, adj.nombre)
        except IOError as e:
            t = Template("<br><h3>I/O ERROR {{ errno }}: {{ strerror }}:</h3><p>{{ fichero }}</p>")
            html = t.render(Context({'fichero': adj.nombre, 'errno': e.errno, 'strerror': e.strerror}))
            return HttpResponse(html, status=404)
        except Exception as e:
            t = Template("<br><h3>ERROR: {{ error }}")
            html = t.render(Context({'error': e}))
            return HttpResponse(html, status=404)
        return response

    def fichero_response(self, request, fichero, nombre_destino):
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
            filename_header = 'filename=%s' % nombre_destino.encode('utf-8')
        elif u'MSIE' in request.META['HTTP_USER_AGENT']:
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL, so we do the trick via routing rules.
            filename_header = ''
        else:
            # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
            filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(nombre_destino.encode('utf-8'))

        # if type == 'application/pdf':
        #     response['Content-Disposition'] = 'attachment; ' + filename_header      # Para forzar la descarga
        # else:
        #     if type == 'application/xml':
        #         response['Content-Disposition'] = 'attachment; ' + filename_header  # Para forzar la descarga
        #     else:
        #         response['Content-Disposition'] = 'inline; ' + filename_header      # Para abrir en el navegador
        response['Content-Disposition'] = 'attachment; ' + filename_header
        return response
    

class AdjuntoSubir(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        nota_id = request.POST.get("nota_id")
        nota = Nota.objects.get(id=nota_id)

        for fichero in request.FILES.getlist("files", []):
            try:
                adj = Adjunto()
                adj.user = request.user
                adj.nota = nota
                adj.fichero = fichero
                adj.save()
            except Exception as e:
                print(e)

        html = Datos().adjunto_html(nota_id)
        return HttpResponse(html)

