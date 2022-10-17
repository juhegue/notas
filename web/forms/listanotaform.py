# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django import forms
#from dal import autocomplete
from ..models import Libro


def get_qlibros(request):
    return Libro.objects.filter(activo=True, privado=False) | \
           Libro.objects.filter(activo=True, user=request.user)


class ListaNotaForm(forms.Form):
    libro = forms.ChoiceField(label=_("Libro"),
                              widget=forms.Select(
                                  attrs={"class": "form-control choice-select2",
                                         "data-placeholder": "Seleccione ...",
                                         }),
                              required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ListaNotaForm, self).__init__(*args, **kwargs)

        choices = list()
        for libro in get_qlibros(request).order_by(Lower("nombre")):
            choices.append((libro.id, libro.nombre.title()))

        self.fields["libro"].choices = choices
