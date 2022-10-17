# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import EMPTY_VALUES, EmailValidator
from django.core.exceptions import ValidationError
from django.forms.fields import Field


class EmailMultipleField(Field):
    description = _("E-mail address(es)")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ";")
        super(EmailMultipleField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):

        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(_("This field is required."))

        for email in value:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError as e:

                raise forms.ValidationError(_("%s: No es una dirección de correo electrónico válida.") % email)

        return value