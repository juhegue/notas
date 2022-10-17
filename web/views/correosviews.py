# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.test.client import Client
from django.conf import settings

from web.models import User


class EnviaCorreoBienvenidaView(LoginRequiredMixin, TemplateView):
    template_name = "web/correos/correo_bienvenida.html"
    usuario = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            id_usuario = kwargs.get('pk', '0')
            usuario = get_object_or_404(User, pk=id_usuario)
            self.usuario = usuario

            self.envia_correo_completar_registro(request, usuario)
        else:
            raise Http404

        return super(EnviaCorreoBienvenidaView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(EnviaCorreoBienvenidaView, self).get_context_data(**kwargs)

        context['usuario'] = self.usuario
        return context

    @staticmethod
    def envia_correo_completar_registro(request, user):
        if not request:
            client = Client(SERVER_NAME="%s" % settings.SERVER_NAME_PARA_CORREOS)
            response = client.get('/')
            request = response.wsgi_request

        form_reset = PasswordResetForm({'email': user.email})
        form_reset.is_valid()
        form_reset.save(request=request,
                        email_template_name='web/password/completar_registro_email.txt',
                        html_email_template_name='web/password/completar_registro_email.html',
                        subject_template_name='web/password/completar_registro_subject.txt')
