# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.db.models import Sum

from ..forms.listanotaform import ListaNotaForm
from ..models import Nota
from ..models import Adjunto


class Busca(object):
    busca = None
    libro_id = None

    def get_queryset_notas(self):
        notas = Nota.objects.filter(libro=self.libro_id, activa=True)
        if self.busca:
            for busca in self.busca.split(","):
                busca = busca.strip()
                nota_ids = notas.values_list("id", flat=True)

                nota_adj_ids = Adjunto.objects.filter(nombre__icontains=busca, nota__id__in=nota_ids).\
                    values_list("nota__id", flat=True)

                notas = Nota.objects.filter(id__in=nota_ids, nombre__icontains=busca) | \
                        Nota.objects.filter(id__in=nota_ids, texto__icontains=busca) | \
                        Nota.objects.filter(id__in=nota_adj_ids)

        notas = notas.order_by("-modificado")
        return notas


class ListaNotaView(LoginRequiredMixin, FormView, Busca):
    template_name = "web/listanota.html"
    form_class = ListaNotaForm

    def dispatch(self, request, *args, **kwargs):
        self.libro_id = int(kwargs.get("libro") or 0)
        if self.libro_id:
            request.user.set_propiedad("libro", self.libro_id)
        else:
            self.libro_id = request.user.get_propiedad("libro")

        self.busca = kwargs.get("busca")
        if self.busca:
            if self.busca == "__NULL__":
                self.busca = ""
            request.user.set_propiedad("busca", self.busca)
        else:
            self.busca = request.user.get_propiedad("busca")

        return super(ListaNotaView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ListaNotaView, self).get_initial()
        initial["libro"] = self.libro_id
        return initial

    def get_form_kwargs(self):
        kwargs = super(ListaNotaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ListaNotaView, self).get_context_data(**kwargs)
        context["nota_list"] = self.get_queryset_notas()
        context["busca"] = self.busca
        return context

