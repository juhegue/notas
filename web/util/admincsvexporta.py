# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import csv
import base64

from django.http import HttpResponse
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db import models


class CsvExporta(object):
    """
    Exportación de modelos en admin

    Si no se define fields_csv se exportan todos los campos del modelo

    fields_csv es un list compuesto de nombre_campo, titulo_campo:
        Ej: fields_csv = [("nif", "NIF"), ("nombre", "Nombre")]
    """
    def __init__(self, modeladmin, request, queryset):
        self.modeladmin = modeladmin
        self.request = request
        self.queryset = queryset
        self._response = HttpResponse(content_type='text/csv')

        fichero = modeladmin.model._meta.object_name
        self._response['Content-Disposition'] = 'attachment; filename="%s.csv"' % fichero
        self._exporta(self._response)

    @property
    def response(self):
        """
        Retorna el response del csv
        :return: HttpResponse
        """
        return self._response

    @staticmethod
    def _get_foreinkey(model_rel, model, id):
        for field in model._meta.fields:
            if field.get_internal_type() == "ForeignKey":
                if field.related_model == model_rel or \
                        field.related_model == model_rel._meta.proxy_for_model:
                    name = field.name
                    return {name: id}

    @staticmethod
    def _get_fields(modeladmin, prefijo=None):
        fields = list()
        if getattr(modeladmin, "fields_csv", None) is None:
            for field in modeladmin.model._meta._get_fields():
                if not isinstance(field, ManyToOneRel):
                    name = field.name
                    title = getattr(field, "verbose_name", None) or name
                    if prefijo:
                        title = "%s_%s" % (prefijo, title)
                    fields.append((name, title))

        else:
            for name, title in modeladmin.fields_csv:
                if prefijo:
                    title = "%s_%s" % (prefijo, title)
                fields.append((name, title))

        return fields

    @staticmethod
    def _getitem(query, name):
        obj = query
        for n in name.split("__"):
            obj = getattr(obj, n, None)

        return obj

    def _exporta(self, csvfile):

        def get_row(valores, titles):
            resul = dict()
            longi = len(valores) - 1
            for n, title in enumerate(titles):
                if n > longi:
                    resul[title] = ""
                else:
                    resul[title] = valores[n]
            return resul

        titles = list()
        for name, title in self._get_fields(self.modeladmin, self.modeladmin.model._meta.object_name):
            titles.append(title)

        def title_inline(modeladmin_inlines):
            for inline in modeladmin_inlines:
                for name, title in self._get_fields(inline, inline.model._meta.object_name):
                    titles.append(title)

                title_inline(inline.inlines)

        title_inline(self.modeladmin.inlines)

        writer = csv.DictWriter(csvfile, fieldnames=titles)

        writer.writeheader()

        for query in self.queryset:
            valores = list()
            for name, title in self._get_fields(self.modeladmin):
                valor = self._getitem(query, name)
                if isinstance(valor, models.fields.files.FieldFile):
                    valor = base64.b64encode(valor.file.read()).decode()
                valores.append(valor or "")

            row = get_row(valores, titles)

            def valor_inline(row, modeladmin, query_id):
                con_inline = False
                for inline in modeladmin.inlines:
                    foreinkey = self._get_foreinkey(modeladmin.model, inline.model, query_id)
                    if foreinkey:
                        for iquery in inline.model.objects.filter(**foreinkey):
                            con_inline = True
                            for name, title in self._get_fields(inline, inline.model._meta.object_name):
                                valor = self._getitem(iquery, name)
                                if isinstance(valor, models.fields.files.FieldFile):
                                    row[title] = base64.b64encode(valor.file.read()).decode()
                                else:
                                    row[title] = valor

                            valor_inline(row.copy(), inline, iquery.id)

                if not con_inline:
                    writer.writerow(row)

            valor_inline(row, self.modeladmin, query.id)










