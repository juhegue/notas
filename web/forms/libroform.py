# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django import forms
from web.models import Libro


class LibroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(LibroForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        cleaned_data = super(LibroForm, self).clean()
        nombre = cleaned_data.get("nombre")

        if self.instance:
            if Libro.objects.filter(nombre=nombre).exclude(pk=self.instance.pk).first():
                raise forms.ValidationError(_("¡Ya existe un libro con ese mismo nombre!"))
        else:
            if Libro.objects.filter(nombre=nombre).first():
                raise forms.ValidationError(_("¡Ya existe un libro con ese mismo nombre!"))

        return nombre

    # def clean(self):
    #     cleaned_data = super(LibroForm, self).clean()
    #     nombre = cleaned_data.get("nombre")
    #
    #     if Libro.objects.filter(nombre=nombre).first():
    #         self.add_error("nombre", _("¡Ya existe un libro con ese mismo nombre!"))
    #
    #     return cleaned_data

    class Meta:
        model = Libro
        exclude = ['user', 'creado', 'modificado']
        help_texts = {
            'privado': 'Marcar para hacer el libro no visible para los demás usuarios.',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'required': 'true',
                                             "autofocus": "autofocus"
                                             }),
            'privado': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }
