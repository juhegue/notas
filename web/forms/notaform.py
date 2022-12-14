# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import forms
from dal import autocomplete
from ..models import Nota
from .emailmultiple import EmailMultipleField


class NotaForm(forms.ModelForm):
    uuid_id = forms.CharField(required=False, widget=forms.TextInput(attrs={"style": "display:none;"}))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        libro = kwargs.pop("libro", None)
        super(NotaForm, self).__init__(*args, **kwargs)

        if libro:
            data = self.data.copy()         # actualiza data ya que libro al estar disabled no lo envia la página
            data.update({'libro': libro})   # y al ser requerido da error
            self.data = data
            self.fields['libro'].widget.attrs['disabled'] = True

    def clean_nombre(self):
        cleaned_data = super(NotaForm, self).clean()
        nombre = cleaned_data.get("nombre")
        if not nombre:
            raise forms.ValidationError(_("¡El campo es obligatorio!"))

        return nombre

    class Meta:
        model = Nota
        exclude = ['user', 'creado', 'modificado']

        widgets = {
            'libro': autocomplete.Select2(attrs={'class': 'form-control', 'required': 'true'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', "style": "display:none;"}),
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




