# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
import nested_admin

from .models import User
from .models import Libro
from .models import Nota
from .models import Adjunto
from .models import AdjuntoTemporal

from .util.admincsvexporta import CsvExporta


def exportar_csv(modeladmin, request, queryset):
    return CsvExporta(modeladmin, request, queryset).response


class NotaActivaFilter(SimpleListFilter):
    title = _("activa")
    parameter_name = "activa"

    def lookups(self, request, modeladmin):
        return [(True, "activa"), (False, "desactiva")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(activa=self.value())

    def value(self):
        value = super(NotaActivaFilter, self).value()
        return value


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
    readonly_fields = ()
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'editor')}),
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
    search_fields = ('email', 'first_name', 'last_name', 'apellido2', 'editor')

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


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    search_fields = ('libro__nombre', 'nombre', 'texto', 'user__email')
    readonly_fields = ('creado', 'modificado')
    list_display = (
        'libro',
        'nombre',
        'user',
        'creado',
        'modificado',
        'activa',
    )
    actions = [exportar_csv]
    list_filter = (NotaActivaFilter,)


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


@admin.register(AdjuntoTemporal)
class AdjuntoTemporal(admin.ModelAdmin):
    pass


class LibroNotaAdjunto(Libro):
    class Meta:
        proxy = True


class AdjuntoInline(nested_admin.NestedStackedInline):
    model = Adjunto
    readonly_fields = ("creado", "modificado")


class NotaInline(nested_admin.NestedStackedInline):
    model = Nota
    readonly_fields = ("creado", "modificado")
    inlines = [AdjuntoInline]


class LibroAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ("creado", "modificado")
    search_fields = (
        "nombre",
    )
    list_display = (
        "nombre",
    )
    inlines = [
        NotaInline,
    ]
    actions = [exportar_csv]


admin.site.register(LibroNotaAdjunto, LibroAdmin)

