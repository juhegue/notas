# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import User
from .models import Libro
from .models import Nota
from .models import Adjunto

from .util.admincsvexporta import CsvExporta


def exportar_csv(modeladmin, request, queryset):
    return CsvExporta(modeladmin, request, queryset).response


# Custom Admin User
@admin.register(User)
class UserAdminExtended(UserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'apellido2',
        'is_active',
        'is_staff',
    )
    readonly_fields = ()
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'apellido2')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'apellido2')

    def get_object(self, request, object_id, from_field=None):
        obj = super(UserAdminExtended, self).get_object(request, object_id)
        return obj

    def save_model(self, request, obj, form, change):
        obj.save()


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'nombre',
        'user',
        'creado',
        'modificado'
    )
    actions = [exportar_csv]
    fields_csv = [('nombre', 'Nombre'),
                  ('user', 'Usuario'),
                  ('creado', 'Creado'),
                  ('modificado', 'Modificado'),
                  ]


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    search_fields = ('libro__nombre', 'nombre', 'texto', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'libro',
        'nombre',
        'user',
        'creado',
        'modificado'
    )
    actions = [exportar_csv]
    fields_csv = [('libro', 'Libro'),
                  ('nombre', 'Nombre'),
                  ('user', 'Usuario'),
                  ('creado', 'Creado'),
                  ('modificado', 'Modificado'),
                  ]


@admin.register(Adjunto)
class AdjuntoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'fichero', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'nombre',
        'fichero',
        'user',
        'creado',
    )
