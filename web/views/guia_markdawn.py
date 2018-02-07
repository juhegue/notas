# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class GuiaMarkdownView(TemplateView):
    template_name = "web/guia_markdown/guia.html"

