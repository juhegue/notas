# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from .select2es import *
from ..models import Libro
from ..models import Nota
from .select2es import Select2Es
from .emailmultiple import EmailMultipleField


class NotaForm(forms.ModelForm):

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
        exclude = ['user', 'creado', 'modificado']

        widgets = {
            'libro': Select2Es(attrs={'class': 'form-control', 'required': 'true'}),
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

    mensaje = forms.CharField(label=_("Mensaje"),
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
            self.fields['mensaje'].initial = nota.nombre




