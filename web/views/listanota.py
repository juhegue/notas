# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View
from django.http import JsonResponse

from ..forms.listanotaform import ListaNotaForm
from ..models import Nota
from ..util.util import marca_texto


class ListaNotaView(LoginRequiredMixin, FormView):
    template_name = "web/listanota.html"
    form_class = ListaNotaForm

    def dispatch(self, request, *args, **kwargs):
        return super(ListaNotaView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ListaNotaView, self).get_initial()
        initial["libro"] = self.request.user.get_propiedad("libro")
        return initial

    def get_form_kwargs(self):
        kwargs = super(ListaNotaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ListaNotaView, self).get_context_data(**kwargs)
        return context


class NotasView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        sort = self.request.GET.get("sort")
        order = self.request.GET.get("order")
        search = self.request.GET.get("search")
        limit = int(self.request.GET.get("limit"))
        offset = int(self.request.GET.get("offset"))

        libro = self.request.GET.get("libro")
        request.user.set_propiedad("libro", libro)

        if sort:
            sort = sort if order == "asc" else "-%s" % sort
            query = Nota.objects.filter(activa=True).order_by(sort)
        else:
            query = Nota.objects.filter(activa=True)

        if libro:
            query = query.filter(libro=libro)

        if search:
            for s in search.split(","):
                s = s.strip()
                query = query.filter(nombre__icontains=s) | \
                    query.filter(texto__icontains=s) | \
                    query.filter(adjunto__nombre__icontains=s)

        count = query.count()

        if offset or limit:
            query = query[offset:offset+limit]

        rows = list()
        for q in query:
            rows.append({
                "id": q.id,
                "nombre": marca_texto(search, q.nombre),
                "modificado": q.modificado.strftime("%d/%m/%Y %H:%M"),
                "texto": marca_texto(search, q.texto),
                "adjunto_html_sin_borrar": marca_texto(search, q.adjunto_html_sin_borrar()),
            })

        resul = {"total": count, "rows": rows}
        return JsonResponse(resul, safe=False)

