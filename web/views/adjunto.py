# coding=utf-8

import os
import mimetypes
import urllib
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse
from django.template import Template
from django.template import Context
from django.conf import settings

from ..models import AdjuntoTemporal
from ..models import Adjunto
from ..models import Nota

logger = logging.getLogger(__name__)


def adjunto_html(uuid_id):
    html = ""
    for adj in AdjuntoTemporal.objects.filter(uuid_id=uuid_id).all():
        link_download = "<a href='/adjunto_bajar_temporal/%s/'>%s</a>" % (adj.id, adj.nombre)
        href_baja = "javascript:borraAdjuntoTemporal(%s);" % adj.id
        html += """
            <tr>
                <td class="wrappable">%s</td>
                <td class="text-center">
                    <a href="%s" class="text-danger" role="button"><span class="fa fw fa-trash"></span></a>
                </td>                
            </tr>            
    """ % (link_download, href_baja)

    return "" if not html else """
        <div class="panel panel-default">
        <table class='table' style='width:100%%'>
          %s
        </table>
        </div>                
        """ % html


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


class AdjuntoBajar(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        adj_id = kwargs.get("adj_id")
        try:
            adj = Adjunto.objects.get(id=adj_id)
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


class AdjuntoBajarTemporal(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        adj_id = kwargs.get("adj_id")
        try:
            adj = AdjuntoTemporal.objects.get(id=adj_id)
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
    def dispatch(self, request, *args, **kwargs):
        nota_id = request.POST.get("nota_id")
        try:
            nota = Nota.objects.get(id=nota_id)
            for fichero in request.FILES.getlist("files", []):
                try:
                    adj = Adjunto()
                    adj.user = request.user
                    adj.nota = nota
                    adj.fichero = fichero
                    adj.save()
                except Exception as e:
                    logger.error(e)
            html = nota.adjunto_html()
        except ValueError:
            for fichero in request.FILES.getlist("files", []):
                try:
                    adj = AdjuntoTemporal()
                    adj.uuid_id = nota_id
                    adj.fichero = fichero
                    adj.save()
                except Exception as e:
                    logger.error(e)
            html = adjunto_html(nota_id)
        return HttpResponse(html)


