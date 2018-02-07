# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class IframeView(TemplateView):
    template_name = "web/iframe/iframe_tinymce.html"
    template_name = "web/iframe/iframe_SimpleMDE.html"
    template_name = "web/iframe/iframe_bootstrap-markdown.html"

    def dispatch(self, request, *args, **kwargs):
        nota_id = kwargs.get("id")
        return super(IframeView, self).dispatch(request, *args, **kwargs)
