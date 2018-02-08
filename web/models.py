# -*- coding: utf-8 -*-

import os
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .managers import MyUserManager
from .modelsmixin import ActualizaMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('apellido1'), max_length=30, blank=True)
    apellido2 = models.CharField(_('apellido2'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.last_name, self.apellido2)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class UserMixin(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Libro(ActualizaMixin, UserMixin):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Nota(ActualizaMixin, UserMixin):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, default='', null=True, blank=True)
    texto = models.TextField(default='', null=True, blank=True)
    html = models.TextField(default='', null=True, blank=True)
    activa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


def adjunto_upload_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    nombre_fichero = '%s%s' % (uuid.uuid4().hex, filename_ext.lower())

    instance.nombre = filename

    return os.path.join('adjuntos', nombre_fichero)


class Adjunto(ActualizaMixin, UserMixin):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
    fichero = models.FileField(upload_to=adjunto_upload_to)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


@receiver(pre_delete)
def delete_repo(sender, instance, **kwargs):
    if sender == Adjunto:
        try:
            os.unlink(instance.fichero.file.name)
        except:
            pass

