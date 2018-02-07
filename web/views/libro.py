# coding=utf-8

from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from web.models import Libro
from web.forms.libroform import LibroForm


class LibroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'web/libro/editar.html'
    model = Libro
    form_class = LibroForm
    success_message = u"Libro creado correctamente."

    def dispatch(self, request, *args, **kwargs):
        return super(LibroCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LibroCreateView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(LibroCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            f = form.save(commit=False)
            f.user = self.request.user
            f.save()
        return super(LibroCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listanota', kwargs={'libro': self.object.id})
