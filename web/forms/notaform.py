# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from .select2es import *
from ..models import Libro
from ..models import Nota


class NotaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        libro = kwargs.pop("libro", None)
        super(NotaForm, self).__init__(*args, **kwargs)

        choices = list()
        for libro in Libro.objects.all().order_by("nombre"):
            choices.append((libro.id, libro.nombre))

        self.fields["libro"].choices = choices
        if libro:
            # al ser el campo requerido en el template, antes del submit, hay que habilitarlo
            self.fields['libro'].widget.attrs['disabled'] = True

    def clean_nombre(self):
        cleaned_data = super(NotaForm, self).clean()
        nombre = cleaned_data.get("nombre")

        if not nombre:
            raise forms.ValidationError(_("¡El camop es obligatorio!"))

        return nombre

    class Meta:
        model = Nota
        exclude = ['user', 'creado', 'modificado']

        widgets = {
            'libro': Select2Es(attrs={'class': 'form-control', 'required': 'true'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', "style": "display:none;"}),
        }

