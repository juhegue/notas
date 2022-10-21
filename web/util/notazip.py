# coding=utf-8

import os
from io import BytesIO
import logging
import tempfile
import zipfile
from xhtml2pdf import pisa
from tomd import Tomd
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from web.models import Nota

TEMPLATE_HTML = """
<!doctype html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="author" content="Juhegue">
        <title>%s</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">    
    </head>
    <body>
        %s
    </body>
</html>                        
""" 

logger = logging.getLogger(__name__)


class NotaZip(object):
    def __init__(self, nota_id, list_adjuntos=None):
        self.nota = Nota.objects.get(pk=nota_id)
        self.list_adjuntos = list_adjuntos
        
    def _crea(self, tmp):
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as archive:
            html = TEMPLATE_HTML % (self.nota.nombre, self.nota.texto)

            nombre = "nota_%s.html" % self.nota.id
            archive.writestr(nombre, html)

            result = BytesIO()
            try:
                pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
                if not pdf.err:
                    nombre = "nota_%s.pdf" % self.nota.id
                    archive.writestr(nombre, result.getvalue())
                else:
                    logger.debug("ERROR al crear PDF (1) %s" % pdf.err)

            except Exception as e:
                logger.debug("ERROR al crear PDF %s" % e)

            md = Tomd(html).markdown
            nombre = "nota_%s.md" % self.nota.id
            archive.writestr(nombre, md)

            adjuntos = self.list_adjuntos if self.list_adjuntos else self.nota.adjunto_set.all()

            for a in adjuntos:
                try:
                    archive.write(a.fichero.file.name, a.nombre)
                except Exception as e:
                    logger.debug("ERROR al comprimir adjunto %s" % e)

            archive.close()

        length = tmp.tell()
        # Reset file pointer
        tmp.seek(0)
        return length

    def response(self):
        with tempfile.SpooledTemporaryFile() as tmp:
            length = self._crea(tmp)
            wrapper = FileWrapper(tmp)
            response = HttpResponse(wrapper, content_type="application/zip")
            response["Content-Disposition"] = "attachment; filename=nota_%s.zip" % self.nota.id
            response["Content-Length"] = length
            response.set_cookie("fileDownload", "true", max_age=6660, path="/")
            return response

    def file(self):
        nombre = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))
        with open(nombre, "wb") as tmp:
            self._crea(tmp)
        return nombre
