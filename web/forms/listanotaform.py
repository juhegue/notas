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
                                  attrs={"class": "form-control choice-simple-select2",
                                         "data-placeholder": "Seleccione ...",
                                         "data-url": "/libros/"
                                         }),
                              required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(ListaNotaForm, self).__init__(*args, **kwargs)

        libro_id = request.user.get_propiedad("libro", 0)
        query = get_qlibros(request)
        libro = query.filter(id=libro_id).first()

        choices = list()
        if libro:
            choices.append((libro.id, libro.nombre.title()))
        # carga el valor inicial
        self.fields["libro"].choices = choices
