# coding=utf-8

from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.http.response import HttpResponseForbidden

from web.models import Libro
from web.forms.libroform import LibroForm


class LibroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "web/libro/editar.html"
    model = Libro
    form_class = LibroForm
    success_message = "Libro creado."

    def dispatch(self, request, *args, **kwargs):
        return super(LibroCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LibroCreateView, self).get_context_data(**kwargs)
        context["create_view"] = True
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
            self.request.user.set_propiedad("libro", f.id)
        return super(LibroCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("listanota")


class LibroUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "web/libro/editar.html"
    model = Libro
    form_class = LibroForm
    success_message = "Libro modificado."

    def get_form_kwargs(self):
        kwargs = super(LibroUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(LibroUpdateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            f = form.save(commit=False)
            f.save()
        return super(LibroUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("listanota")


class LibroDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "web/libro/eliminar.html"
    model = Libro
    success_message = "Libro eliminado."

    def delete(self, *args, **kwargs):
        object = self.get_object()
        if not self.request.user.is_staff:
            if object.user.email != self.request.user.email:
                return HttpResponseForbidden("Esta libro pertenece al usuario '%s'" % self.object.user.email)

        return super(LibroDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self):
        libro = Libro.objects.exclude(id=self.object.id).first()
        libro_id = libro.id if libro else 0
        self.request.user.set_propiedad("libro", libro_id)
        return reverse("listanota")

