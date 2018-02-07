# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ActualizaMixin(models.Model):
    creado = models.DateTimeField(_('Creado'), editable=False)
    modificado = models.DateTimeField(_('Actualizado'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.creado = timezone.now()
        self.modificado = timezone.now()
        return super(ActualizaMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True

