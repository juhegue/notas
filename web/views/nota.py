# coding=utf-8

from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http.response import HttpResponseForbidden


from web.models import Nota
from web.forms.notaform import NotaForm


class NotaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'web/nota/editar.html'
    model = Nota
    form_class = NotaForm
    success_message = u"Nota creada correctamente."
    libro_id = 0

    def dispatch(self, request, *args, **kwargs):
        self.libro_id = kwargs.get("libro", 0)
        return super(NotaCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(NotaCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["libro"] = self.libro_id
        return kwargs

    def get_initial(self):
        initial = super(NotaCreateView, self).get_initial()
        initial["libro"] = self.libro_id
        return initial

    def get_context_data(self, **kwargs):
        context = super(NotaCreateView, self).get_context_data(**kwargs)
        context["libro"] = self.libro_id
        context["create_view"] = True
        context["nota_id"] = "000000"
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            f = form.save(commit=False)
            f.user = self.request.user
            f.save()
        return super(NotaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('nota_editar', kwargs={'pk': self.object.id})


class NotaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'web/nota/editar.html'
    model = Nota
    form_class = NotaForm
    success_message = "Éxito al modificar nota."

    def get_context_data(self, **kwargs):
        context = super(NotaUpdateView, self).get_context_data(**kwargs)
        context["nota_id"] = "%06d" % self.object.id
        return context

    def form_valid(self, form):
        if form.is_valid():
            f = form.save(commit=False)
            # f.user = self.request.user
            f.activa = True
            f.save()
        return super(NotaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listanota', kwargs={'libro': self.object.libro.id})


class NotaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'web/nota/elimina.html'
    model = Nota
    success_message = "Éxito al eliminar nota."

    def get_success_url(self):
        return reverse('listanota', kwargs={'libro': self.object.libro.id})

    def delete(self, *args, **kwargs):
        object = self.get_object()
        if not self.request.user.is_staff:
            if object.user.email != self.request.user.email:
                return HttpResponseForbidden("Esta nota pertenece al usuario '%s'" % self.object.user.email)

        return super(NotaDeleteView, self).delete(*args, **kwargs)