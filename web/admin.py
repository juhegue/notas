# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf.locale.es import formats as es_fotmats
import nested_admin

from .models import User
from .models import Libro
from .models import Nota
from .models import Adjunto
from .models import AdjuntoTemporal
from .models import AgendaEvento
from .models import AgendaEventoColor
from .models import AgendaEventoPredefinido

from .util.admincsvexporta import CsvExporta
from .util.adminmesfilter import MesFilter
from .util.notificacionfcm import NotificacionFcm
from .views.resetpassword import envia_correo_restablecer_clave

es_fotmats.DATETIME_FORMAT = 'd-m-y H:i'
es_fotmats.DATE_FORMAT = 'd-m-y'


class Color:
    def _color(self, obj):
        return mark_safe(f'<div class="color" style="background-color:{obj.color};"></div>')

    class Media:
        css = {
             'all': ('css/admin.css',)
        }


def reenviar_correo_restablecer_clave(modeladmin, request, queryset):
    for usuario in queryset:
        envia_correo_restablecer_clave(usuario, request)


def notifica_fcm_demo(modeladmin, request, queryset):
    for q in queryset:
        n = NotificacionFcm(q)
        n.demo()


def privado_si(modeladmin, request, queryset):
    for q in queryset:
        q.privado = True
        q.save()


def privado_no(modeladmin, request, queryset):
    for q in queryset:
        q.privado = False
        q.save()


def activo_si(modeladmin, request, queryset):
    for q in queryset:
        q.activo = True
        q.save()


def activo_no(modeladmin, request, queryset):
    for q in queryset:
        q.activo = False
        q.save()


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
        'editor',
        'is_active',
        'is_staff',
    )
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'editor')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'apellido2')}),
        (_('Propertie'), {'fields': ('propiedades', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups', 'fcm_token')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'apellido2', 'editor')

    def get_object(self, request, object_id, from_field=None):
        obj = super(UserAdminExtended, self).get_object(request, object_id)
        return obj

    def save_model(self, request, obj, form, change):
        obj.save()

    actions = [notifica_fcm_demo, reenviar_correo_restablecer_clave]


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'nombre',
        'activo',
        'privado',
        'user',
        'creado',
        'modificado'
    )
    actions = [exportar_csv, activo_si, activo_no, privado_si, privado_no]
    field_date_filter = 'creado'
    list_filter = ['user', 'activo', MesFilter]


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    search_fields = ('libro__nombre', 'nombre', 'texto', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'libro',
        'activo',
        'privado',
        'nombre',
        'user',
        'creado',
        'modificado',
    )
    actions = [exportar_csv, activo_si, activo_no, privado_si, privado_no]
    field_date_filter = 'creado'
    list_filter = ['user', 'activo', MesFilter]


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
    actions = [exportar_csv]
    field_date_filter = 'creado'
    list_filter = ['user', MesFilter]


@admin.register(AdjuntoTemporal)
class AdjuntoTemporal(admin.ModelAdmin):
    pass


class LibroNotaAdjunto(Libro):
    class Meta:
        proxy = True


class AdjuntoInline(nested_admin.NestedStackedInline):
    model = Adjunto
    readonly_fields = ('creado', 'modificado')


class NotaInline(nested_admin.NestedStackedInline):
    model = Nota
    readonly_fields = ('creado', 'modificado')
    inlines = [AdjuntoInline]


class LibroAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('creado', 'modificado')
    search_fields = (
        'nombre',
    )
    list_display = (
        'nombre', 'user', 'creado',
    )
    inlines = [
        NotaInline,
    ]
    actions = [exportar_csv]
    field_date_filter = 'creado'
    list_filter = ['user', MesFilter]


admin.site.register(LibroNotaAdjunto, LibroAdmin)


class AgendaEventoAdmin(admin.ModelAdmin, Color):
    list_display = ('id', 'usuario', '_color', 'dia_completo', 'aviso_email', 'aviso_movil', 'inicio', 'fin', 'email_enviado','movil_enviado', 'titulo')
    ordering = ('usuario', '-inicio')
    search_fields = ('usuario', 'color', 'inicio', 'fin', 'titulo')
    field_date_filter = 'creado'
    list_filter = ['usuario', MesFilter]


admin.site.register(AgendaEvento, AgendaEventoAdmin)


class AgendaEventoColorAdmin(admin.ModelAdmin, Color):
    list_display = ('usuario', '_color')
    ordering = ('usuario', 'color')
    search_fields = ('usuario', 'color')
    field_date_filter = 'creado'
    list_filter = ['usuario', MesFilter]


admin.site.register(AgendaEventoColor, AgendaEventoColorAdmin)


class AgendaEventoArrastrarAdmin(admin.ModelAdmin, Color):
    list_display = ('usuario', '_color', 'inicio', 'duracion', 'titulo')
    ordering = ('usuario', 'duracion')
    search_fields = ('usuario', 'color', 'duracion', 'titulo')
    field_date_filter = 'creado'
    list_filter = ['usuario', MesFilter]


admin.site.register(AgendaEventoPredefinido, AgendaEventoArrastrarAdmin)
