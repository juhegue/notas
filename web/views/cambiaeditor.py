# -*- coding: utf-8 -*-

from django.views.generic.edit import View
from django.shortcuts import redirect
from ..util.utiles import decodehex


class CambiaEditorView(View):
    def dispatch(self, request, *args, **kwargs):
        request.user.editor = kwargs.get("editor")
        request.user.save()

        url_hex = kwargs.get("url_origen")
        url = decodehex(url_hex)
        return redirect(url)
