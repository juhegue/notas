# -*- coding: utf-8 -*-

import logging
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetForm
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from web.models import User
from web.middleware import get_request

logger = logging.getLogger(__name__)


class RestablecerClaveForm(PasswordResetForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )


class RestablecerClave(PasswordResetView):
    form_class = RestablecerClaveForm
    template_name = 'resetpassword/password_reset_form.html'
    subject_template_name = 'resetpassword/password_reset_subject.txt'
    email_template_name = 'resetpassword/password_reset_message.txt'
    html_email_template_name = 'resetpassword/password_reset_email.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            extra_mail_context = dict()
            email = form.cleaned_data.get('email')
            usuario = User.objects.filter(email=email).first()
            if usuario:
                extra_mail_context['nombre'] = usuario.first_name
                self.extra_email_context = extra_mail_context
                super().form_valid(form)
                messages.add_message(self.request, messages.SUCCESS,
                                     _('Compruebe su bandeja de entrada y siga los pasos para restablecer la contraseña.'),
                                     )
            else:
                messages.error(self.request, _('Usuario no registrado.'))
            return redirect('login')

        return super().form_valid(form)


# class RestablecerClaveConfirmarPassword(PasswordResetConfirmView):
#     pass
#     template_name='core/password_reset_new_password.html'
#     success_url = reverse_lazy('login_portal')

#     def form_valid(self, form):
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             url = get_host(self.request)
#             titulo = 'Restablecer contraseña'
#             super().form_valid(form)
#             messages.add_message(self.request, messages.SUCCESS,
#                                      'Nueva Contraseña restablecida correctamente.',
#                                      )
#             return redirect('login_portal')

#         return super().form_valid(form)

def envia_correo_restablecer_clave(usuario, request=None):
    if not request:
        request = get_request()

    if request:
        extra_mail_context = dict()
        extra_mail_context['nombre'] = usuario.first_name
        email = usuario.email

        form_reset = PasswordResetForm({'email': email})
        form_reset.is_valid()
        form_reset.save(request=request,
                        email_template_name='resetpassword/password_reset_message.txt',
                        html_email_template_name='resetpassword/password_reset_email.html',
                        subject_template_name='resetpassword/password_reset_subject.txt',
                        extra_email_context=extra_mail_context,
                        use_https=request.is_secure()
                        )
    else:
        logger.error('envia_correo_restablecer_clave: sin request')
