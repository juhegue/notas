# -*- coding: utf-8 -*-

import json
import os
import uuid
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import MyUserManager
from .util.util import clean_html


EDITOR_CHOICES = (
    ("summernote", "Summernote"),
    ("ckeditor",  "Ckeditor"),
    ("froala",  "Froala"),
    ("trumbowyg",  "Trumbowyg"),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('apellido1'), max_length=30, blank=True)
    apellido2 = models.CharField(_('apellido2'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    propiedades = models.TextField(_('propiedades'), blank=True, null=True)
    editor = models.CharField(_('editor'), max_length=30, choices=EDITOR_CHOICES, default="summernote")

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

    def set_propiedad(self, nombre, valor):
        p = json.loads(self.propiedades or "{}")
        p[nombre] = valor
        self.propiedades = json.dumps(p)
        self.save()

    def get_propiedad(self, nombre, defecto=None):
        p = json.loads(self.propiedades or "{}")
        return p.get(nombre) or defecto


class UserMixin(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


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


class Libro(ActualizaMixin, UserMixin):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Nota(ActualizaMixin, UserMixin):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, default='', null=True, blank=True)
    texto = models.TextField(default='', null=True, blank=True)
    activa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def adjuntos(self, uuid_id=None):
        borrados = list()
        if uuid_id:
            borrados = AdjuntoTemporal.objects.filter(uuid_id=uuid_id, adjunto_borrado_id__gt=0)\
                .values_list('adjunto_borrado_id', flat=True)

        resul = list()
        for adj in self.adjunto_set.all().exclude(id__in=borrados):
            resul.append({
                "id": adj.id,
                "nombre": adj.nombre
            })
        return resul

    def save(self, *args, **kwargs):
        self.texto = clean_html(self.texto)
        return super(Nota, self).save(*args, **kwargs)


def adjunto_upload_to(instance, filename):
    nombre_fichero = '%s_%s' % (filename, uuid.uuid4().hex)
    instance.nombre = filename

    if isinstance(instance, AdjuntoTemporal):
        return os.path.join('adjuntos', 'tmp', nombre_fichero)

    return os.path.join('adjuntos', nombre_fichero)


class Adjunto(ActualizaMixin, UserMixin):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
    fichero = models.FileField(upload_to=adjunto_upload_to)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class AdjuntoTemporal(models.Model):
    uuid_id = models.UUIDField(db_index=True)
    fichero = models.FileField(upload_to=adjunto_upload_to)
    nombre = models.CharField(max_length=200)
    adjunto_borrado_id = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def mueve_a_adjuntos(self):
        path = os.path.basename(self.fichero.path)
        des = os.path.join(settings.MEDIA_ROOT, "adjuntos", path)
        os.replace(self.fichero.path, des)
        self.fichero = os.path.join("adjuntos", path)

    class Meta:
        verbose_name_plural = "AdjuntosTemporal"


@receiver(pre_delete)
def delete_repo(sender, instance, **kwargs):
    if sender == Adjunto or sender == AdjuntoTemporal:
        try:
            os.unlink(instance.fichero.file.name)
        except:
            pass

