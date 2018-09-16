# coding=utf-8

from io import BytesIO
import tempfile
import zipfile
from xhtml2pdf import pisa

from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http.response import HttpResponseForbidden
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from web.models import Adjunto
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
        context["adjunto_html"] = self.object.adjunto_html()
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


class NotaDownloadZip(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        nota = Nota.objects.get(pk=pk)
        adj = Adjunto.objects.filter(nota=nota)
        return self.get_zip(nota, adj)

    @staticmethod
    def get_zip(nota, adj):
        with tempfile.SpooledTemporaryFile() as tmp:
            with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as archive:
                html = nota.texto
                nombre = "nota_%s.html" % nota.id
                archive.writestr(nombre, html)

                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                if not pdf.err:
                    nombre = "nota_%s.pdf" % nota.id
                    archive.writestr(nombre, result.getvalue())

                for a in adj:
                    archive.write(a.fichero.file.name, a.nombre)
                archive.close()

            length = tmp.tell()
            # Reset file pointer
            tmp.seek(0)

            wrapper = FileWrapper(tmp)
            response = HttpResponse(wrapper, content_type="application/zip")
            response["Content-Disposition"] = "attachment; filename=nota_%s.zip" % nota.id
            response["Content-Length"] = length
            return response

