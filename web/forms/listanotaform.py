# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from .select2es import *
from ..models import Libro


class ListaNotaForm(forms.Form):
    libro = forms.ChoiceField(label=_("Libro"),
                              widget=Select2Es(
                                  attrs={"class": "form-control",
                                         "data-placeholder": "Seleccione ...",
                                         }),
                              required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ListaNotaForm, self).__init__(*args, **kwargs)

        choices = list()
        for libro in Libro.objects.all().order_by("nombre"):
            choices.append((libro.id, libro.nombre))

        self.fields["libro"].choices = choices
