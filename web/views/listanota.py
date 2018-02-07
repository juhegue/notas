# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView

from ..forms.listanotaform import ListaNotaForm
from ..models import Nota


class ListaNotaView(LoginRequiredMixin, FormView):
    template_name = "web/listanota.html"
    form_class = ListaNotaForm
    libro_id = None

    def dispatch(self, request, *args, **kwargs):
        self.libro_id = int(kwargs.get("libro", 0) or request.COOKIES.get('libro', 0))
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
        queryset = Nota.objects.filter(libro=self.libro_id, activa=True).order_by("-modificado")
        context["nota_list"] = queryset
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            self.libro_id = data.get("libro", None)
        return super(ListaNotaView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listanota', kwargs={"libro": self.libro_id})
