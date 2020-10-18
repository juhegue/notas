# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from ..forms.listanotaform import ListaNotaForm
from ..models import Nota
from ..models import Libro
from ..util.util import marca_texto


class ListaNotaView(LoginRequiredMixin, FormView):
    template_name = "web/listanota.html"
    form_class = ListaNotaForm
    del_cookie = None

    def dispatch(self, request, *args, **kwargs):
        self.del_cookie = kwargs.get("del_cookie")
        return super(ListaNotaView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ListaNotaView, self).get_initial()
        libro_id = self.request.user.get_propiedad("libro")
        if not libro_id or not Libro.objects.filter(id=libro_id).first():
            libro = Libro.objects.all().first()
            libro_id = libro.id if libro else 0
        initial["libro"] = libro_id
        return initial

    def get_form_kwargs(self):
        kwargs = super(ListaNotaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ListaNotaView, self).get_context_data(**kwargs)
        context["del_cookie"] = self.del_cookie
        context["libro"] = self.request.user.get_propiedad("libro", 0)
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
            query = Nota.objects.filter(activa=True).order_by("-modificado")

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

        hoy = timezone.now().date()

        rows = list()
        for q in query:
            modi = q.modificado.strftime("%H:%M") if hoy == q.modificado.date() else q.modificado.strftime("%d/%m/%Y")

            adjuntos = list()
            for adj in q.adjuntos():
                adj["nombre"] = marca_texto(search, adj["nombre"])
                adjuntos.append(adj)

            rows.append({
                "id": q.id,
                "nombre": marca_texto(search, q.nombre),
                "modificado": modi,
                "texto": marca_texto(search, q.texto),
                "adjuntos": adjuntos,
            })

        resul = {"total": count, "rows": rows}
        return JsonResponse(resul, safe=False)

