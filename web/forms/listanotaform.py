# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Lower
from django import forms
from dal import autocomplete
from ..models import Libro


class ListaNotaForm(forms.Form):
    libro = forms.ChoiceField(label=_("Libro"),
                              widget=autocomplete.Select2(
                                  attrs={"class": "form-control",
                                         "data-placeholder": "Seleccione ...",
                                         }),
                              required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ListaNotaForm, self).__init__(*args, **kwargs)

        choices = list()
        for libro in Libro.objects.all().order_by(Lower("nombre")):
            choices.append((libro.id, libro.nombre.title))

        self.fields["libro"].choices = choices
