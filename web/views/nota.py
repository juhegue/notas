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
from django.http import HttpResponseRedirect

from web.models import Libro
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
    libro = None
    uuid_id = None

    def dispatch(self, request, *args, **kwargs):
        libro_id = kwargs.get("libro", 0)
        self.libro = Libro.objects.get(id=libro_id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        self.uuid_id = uuid.uuid4()
        initial["libro"] = self.libro
        initial["uuid_id"] = self.uuid_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view"] = True
        context["libro"] = self.libro
        context["uuid_id"] = self.uuid_id
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            uuid_id = data.get("uuid_id")
            f = form.save(commit=False)
            f.libro = self.libro
            f.user = self.request.user
            f.activo = True
            f.save()

            for adj in AdjuntoTemporal.objects.filter(uuid_id=uuid_id).all():
                adj.mueve_a_adjuntos()
                Adjunto(nota=f, fichero=adj.fichero, nombre=adj.nombre).save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listanota') + '?scrool=0'


class NotaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'web/nota/editar.html'
    model = Nota
    form_class = NotaForm
    success_message = "Nota modificada."
    uuid_id = None

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        self.uuid_id = uuid.uuid4()
        initial["uuid_id"] = self.uuid_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["libro"] = self.object.libro
        context["adjuntos"] = self.object.adjuntos()
        context["uuid_id"] = self.uuid_id
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            uuid_id = data.get("uuid_id")
            f = form.save(commit=False)
            f.activo = True
            f.save()

            for adj in AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id=0).all():
                adj.mueve_a_adjuntos()
                Adjunto(nota=f, fichero=adj.fichero, nombre=adj.nombre).save()

            borrados = AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id__gt=0)\
                .values_list('adjunto_borrado_id', flat=True)
            f.adjunto_set.filter(id__in=borrados).delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listanota') + '?scrool=0'


class NotaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'web/nota/eliminar.html'
    model = Nota
    success_message = "Nota eliminada."

    def form_valid(self, form):
        object = self.get_object()
        if not self.request.user.is_staff:
            if object.user.email != self.request.user.email:
                return HttpResponseForbidden("Esta nota pertenece al usuario '%s'" % self.object.user.email)

        # TODO:: No se borra, solo se marca no activo
        success_url = self.get_success_url()
        object.activo = False
        object.save()
        return HttpResponseRedirect(success_url)
        # return super().delete(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('listanota')


class NotaDownloadZip(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        return NotaZip(pk).response()


class NotaEnviarView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'web/nota/enviar.html'
    form_class = NotaEnviarForm
    id_nota = None
    uuid_id = None

    def dispatch(self, request, *args, **kwargs):
        self.id_nota = kwargs.get("pk")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["id_nota"] = self.id_nota
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        self.uuid_id = uuid.uuid4()
        initial["uuid_id"] = self.uuid_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nota = Nota.objects.get(id=self.id_nota)
        context["nota"] = nota
        context["adjuntos"] = nota.adjuntos()
        context["uuid_id"] = self.uuid_id
        context["create_view"] = True
        return context

    def form_valid(self, form):
        if form.is_valid():
            data = form.cleaned_data
            uuid_id = data.get("uuid_id")
            nota = Nota.objects.get(id=self.id_nota)

            adjuntos = {n.id: n for n in nota.adjunto_set.all()}

            for borrado_id in AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id__gt=0)\
                    .values_list('adjunto_borrado_id', flat=True):
                del adjuntos[borrado_id]

            list_adjuntos = list(adjuntos.values())

            for adj in AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id=0).all():
                list_adjuntos.append(adj)

            adj = NotaZip(self.id_nota, list_adjuntos).file()
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

        return super().form_valid(form)

