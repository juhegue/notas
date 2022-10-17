# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django import forms
from ..models import Nota
from .emailmultiple import EmailMultipleField


class NotaForm(forms.ModelForm):
    uuid_id = forms.CharField(required=False, widget=forms.TextInput(attrs={"style": "display:none;"}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(NotaForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        cleaned_data = super(NotaForm, self).clean()
        nombre = cleaned_data.get("nombre")
        if not nombre:
            raise forms.ValidationError(_("¡El campo es obligatorio!"))

        return nombre

    class Meta:
        model = Nota
        exclude = ['user', 'creado', 'modificado', 'libro']
        help_texts = {
            'privado': 'Marcar para hacer la nota no visible para los demás usuarios.',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', "style": "display:none;"}),
            'privado': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }


class NotaEnviarForm(forms.Form):
    para = EmailMultipleField(label=_("Para"),
                              widget=forms.TextInput(attrs={"class": "form-control"}),
                              required=True,
                              help_text="Separar por ; para indicar más de un correo."
                             )

    asunto = forms.CharField(label=_("Asunto"),
                             widget=forms.TextInput(attrs={"class": "form-control"}),
                             required=True
                             )

    texto = forms.CharField(label=_("Mensaje"),
                            widget=forms.TextInput(attrs={"style": "display:none;"}),
                            required=False
                            )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        nota_id = kwargs.pop('id_nota', None)
        super(NotaEnviarForm, self).__init__(*args, **kwargs)

        nota = Nota.objects.get(id=nota_id)
        if nota:
            self.fields['asunto'].initial = "%s (%s)" % (nota.nombre, nota.libro)
            self.fields['texto'].initial = nota.nombre




