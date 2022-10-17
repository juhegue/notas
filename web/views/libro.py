# coding=utf-8

from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.http.response import HttpResponseForbidden
from django.http import HttpResponseRedirect

from web.models import Libro
from web.forms.libroform import LibroForm
from web.forms.listanotaform import get_qlibros


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
            f.activo = True
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
            f.activo = True
            f.save()
        return super(LibroUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("listanota")


class LibroDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "web/libro/eliminar.html"
    model = Libro
    success_message = "Libro eliminado."

    def form_valid(self, form):
        object = self.get_object()
        if not self.request.user.is_staff:
            if object.user.email != self.request.user.email:
                return HttpResponseForbidden("Esta libro pertenece al usuario '%s'" % self.object.user.email)

        # TODO:: No se borra, solo se marca no ctivo
        success_url = self.get_success_url()
        object.activo = False
        object.save()
        return HttpResponseRedirect(success_url)
        #  return super(LibroDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self):
        object = self.get_object()
        libro = get_qlibros(self.request).exclude(id=object.id).first()
        libro_id = libro.id if libro else 0
        self.request.user.set_propiedad("libro", libro_id)
        messages.success(self.request, self.success_message)
        return reverse("listanota")

