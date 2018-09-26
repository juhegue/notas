# -*- coding: utf-8 -*-

import json
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
from .util.util import clean_html


EDITOR_CHOICES = (
    ("summernote", "Summernote"),
    ("ckeditor",  "Ckeditor"),
    ("froala",  "Froala"),
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

    def get_propiedad(self, nombre):
        p = json.loads(self.propiedades or "{}")
        return p.get(nombre)


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
    activa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def adjunto_html(self):
        html = ""
        for adj in self.adjunto_set.all():
            link_download = "<a href='/adjunto_bajar/%s/'>%s</a>" % (adj.id, adj.nombre)
            href_baja = "javascript:borraAdjunto(%s);" % adj.id
            html += """
                <tr>
                    <td class="wrappable">%s</td>
                    <td class="text-center">
                        <a href="%s" class="text-danger" role="button"><span class="glyphicon glyphicon-trash"></span></a>
                    </td>                
                </tr>            
        """ % (link_download, href_baja)

        return "" if not html else """
            <div class="panel panel-default">
            <table class='table' style='width:100%%'>
              %s
            </table>
            </div>                
            """ % html

    def adjunto_html_sin_borrar(self):
        html = ""
        for adj in self.adjunto_set.all():
            link_download = "<a href='/adjunto_bajar/%s/'>%s</a>" % (adj.id, adj.nombre)
            html += '<tr><td class="wrappable">%s</td></tr>' % link_download

        return "" if not html else """
            <div class="panel panel-default">
            <table class='table' style='width:100%%'>
              %s
            </table>
            </div>                
            """ % html

    def save(self, *args, **kwargs):
        self.texto = clean_html(self.texto)
        return super(Nota, self).save(*args, **kwargs)


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

