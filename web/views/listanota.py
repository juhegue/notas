# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.utils import timezone

from ..forms.listanotaform import ListaNotaForm, get_qlibros
from ..models import Nota
from ..models import Libro
from ..util.utiles import marca_texto


class ListaNotaView(LoginRequiredMixin, FormView):
    template_name = "web/listanota.html"
    form_class = ListaNotaForm
    del_cookie = None

    def dispatch(self, request, *args, **kwargs):
        self.del_cookie = kwargs.get("del_cookie")
        return super(ListaNotaView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ListaNotaView, self).get_initial()
        libro_id = self.request.user.get_propiedad("libro", 0)
        query = get_qlibros(self.request)
        libro = query.filter(id=libro_id).first()
        initial["libro"] = libro.id if libro else 0
        return initial

    def get_form_kwargs(self):
        kwargs = super(ListaNotaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ListaNotaView, self).get_context_data(**kwargs)
        libro_id = self.request.user.get_propiedad("libro", 0)
        query = get_qlibros(self.request)
        libro = query.filter(id=libro_id).first()
        context["del_cookie"] = self.del_cookie
        context["libro"] = libro
        context["hidden"] = True
        context["nav_activa"] = "notas"
        return context


class NotasView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        sort = self.request.GET.get("sort")
        order = self.request.GET.get("order")
        search = self.request.GET.get("search")
        limit = int(self.request.GET.get("limit"))
        offset = int(self.request.GET.get("offset"))

        libro = int(self.request.GET.get("libro"))
        # TODO:: si la url contiene ?todos=true se muestra todo
        todos = True if self.request.GET.get("todos") == 'true' else False

        request.user.set_propiedad("libro", libro)

        if todos:
            query = Nota.objects.all()
        else:
            query = get_qlibros(request)
            query = Nota.objects.filter(libro__in=query, activo=True)

        if sort:
            if todos:
                if order == "asc":
                    query = query.order_by("-libro__nombre", sort)
                else:
                    query = query.order_by("libro__nombre", sort)
            else:
                sort = sort if order == "asc" else "-%s" % sort
                query = query.order_by(sort)
        else:
            query = query.order_by("-modificado")

        if libro and not todos:
            query = query.filter(libro=libro)

        if search:
            for s in search.split(","):
                s = s.strip()
                query = query.filter(nombre__icontains=s) | \
                    query.filter(texto__icontains=s) | \
                    query.filter(adjunto__nombre__icontains=s)
            query = query.distinct()
        count = query.count()

        if offset or limit:
            query = query[offset:offset+limit]

        hoy = timezone.now().date()

        rows = list()
        for q in query:
            modificado = timezone.localtime(q.modificado)
            modi = modificado.strftime("%H:%M") if hoy == modificado.date() else modificado.strftime("%d/%m/%Y")

            adjuntos = list()
            for adj in q.adjuntos():
                adj["nombre"] = marca_texto(search, adj["nombre"])
                adjuntos.append(adj)

            libro = q.libro.nombre if q.libro.activo else f'[{q.libro.nombre}]'
            nota = q.nombre if q.activo else f'[{q.nombre}]'
            nombre = f'{libro}: {nota}' if todos else q.nombre
            
            rows.append({
                "id": q.id,
                "nombre": marca_texto(search, nombre),
                "modificado": modi,
                "texto": marca_texto(search, q.texto),
                "adjuntos": adjuntos,
                "privado": q.privado
            })

        resul = {"total": count, "rows": rows}
        return JsonResponse(resul, safe=False)

