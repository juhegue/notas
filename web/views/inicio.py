# -*- coding: utf-8 -*-

import logging
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class Index(LoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("listanota", del_cookie=1)

        messages.add_message(request, messages.ERROR, "Usuario no registrado")
        logger.error("Usuario no registrado")
        return redirect("login")


