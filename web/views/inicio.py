# -*- coding: utf-8 -*-

import logging
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class Index(LoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #  return render(request, "web/index.html")
            return redirect("listanota")
        return super(Index, self).dispatch(request, *args, **kwargs)


