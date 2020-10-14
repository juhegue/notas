# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class Index(LoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("listanota", del_cookie=1)

        return redirect("login")


