# coding=utf-8

import uuid
from html2text import html2text
from post_office import mail

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect

from web.models import Nota
from web.models import Adjunto
from web.models import AdjuntoTemporal
from web.forms.notaform import NotaForm
from web.forms.notaform import NotaEnviarForm

from ..util.notazip import NotaZip


class NotaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'web/nota/editar.html'
    model = Nota
    form_class = NotaForm
    success_message = "Nota creada."
    libro_id = 0
    uuid_id = None

    def dispatch(self, request, *args, **kwargs):
        self.libro_id = kwargs.get("libro", 0)
        return super(NotaCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(NotaCreateView, self).get_form_kwargs()
        kwargs["libro"] = self.libro_id
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super(NotaCreateView, self).get_initial()
        self.uuid_id = uuid.uuid4()
        initial["libro"] = self.libro_id
        initial["uuid_id"] = self.uuid_id
        return initial

    def get_context_data(self, **kwargs):
        context = super(NotaCreateView, self).get_context_data(**kwargs)
        context["create_view"] = True
        context["libro"] = self.libro_id
        context["uuid_id"] = self.uuid_id
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            f = form.save(commit=False)
            f.user = self.request.user
            f.activa = True
            f.save()
            uuid_id = data.get("uuid_id")
            for adj in AdjuntoTemporal.objects.filter(uuid_id=uuid_id).all():
                Adjunto(nota=f, fichero=adj.fichero, nombre=adj.nombre).save()

        return super(NotaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listanota')


class NotaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'web/nota/editar.html'
    model = Nota
    form_class = NotaForm
    success_message = "Nota modificada."

    def get_form_kwargs(self):
        kwargs = super(NotaUpdateView, self).get_form_kwargs()
        kwargs["libro"] = self.object.libro.id
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaUpdateView, self).get_context_data(**kwargs)
        context["libro"] = self.object.libro.id
        context["adjunto_html"] = self.object.adjunto_html()
        context["uuid_id"] = None
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            f = form.save(commit=False)
            # f.user = self.request.user
            f.activa = True
            f.save()
        return super(NotaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('listanota')


class NotaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'web/nota/eliminar.html'
    model = Nota
    success_message = "Nota eliminada."

    def get_success_url(self):
        return reverse('listanota')

    def delete(self, *args, **kwargs):
        object = self.get_object()
        if not self.request.user.is_staff:
            if object.user.email != self.request.user.email:
                return HttpResponseForbidden("Esta nota pertenece al usuario '%s'" % self.object.user.email)

        return super(NotaDeleteView, self).delete(*args, **kwargs)


class NotaDownloadZip(LoginRequiredMixin, SuccessMessageMixin, View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        return NotaZip(pk).response()


class NotaEnviarView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'web/nota/enviar.html'
    form_class = NotaEnviarForm
    id_nota = None

    def dispatch(self, request, *args, **kwargs):
        self.id_nota = kwargs.get("pk")
        return super(NotaEnviarView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(NotaEnviarView, self).get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["id_nota"] = self.id_nota
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NotaEnviarView, self).get_context_data(**kwargs)
        context["nota"] = Nota.objects.get(id=self.id_nota)
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            adj = NotaZip(self.id_nota).file()
            try:
                mail.send(
                    recipients=data.get("para", ""),
                    subject=data.get("asunto", ""),
                    message=html2text(data.get("texto", "")),
                    html_message=data.get("texto", ""),
                    attachments={"nota_%s.zip" % self.id_nota: adj}
                )
                messages.success(self.request, "Correo enviado.")
            except Exception as e:
                messages.error(self.request, "Error al enviar correo. (%s)" % e)

            return redirect("listanota")

        return super(NotaEnviarView, self).form_valid(form)

