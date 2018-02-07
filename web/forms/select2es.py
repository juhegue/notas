# https://www.javascripting.com/view/select2
# https://github.com/yourlabs/django-autocomplete-light/issues/731

from dal_select2.widgets import *


class Select2EsWidgetMixin(Select2WidgetMixin):
    class Media:
        """Automatically include static files for the admin."""

        css = {
            'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.css',
                'autocomplete_light/select2.css',
            )
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/vendor/select2/dist/js/select2.full.js',
            'autocomplete_light/select2.js',
            # Provide an additional i18 js.
            'autocomplete_light/vendor/select2/dist/js/i18n/es.js',
        )

    def build_attrs(self, *args, **kwargs):
        attrs = super(Select2EsWidgetMixin, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-language', 'es')
        attrs.setdefault('class', 'form-control')
        return attrs


class Select2Es(Select2EsWidgetMixin, Select):
    pass


class Select2EsMultiple(Select2EsWidgetMixin, SelectMultiple):
    pass


class ModelSelect2Es(QuerySetSelectMixin,
                     Select2EsWidgetMixin,
                     forms.Select):
    pass


class ModelSelect2EsMultiple(QuerySetSelectMixin,
                             Select2EsWidgetMixin,
                             forms.SelectMultiple):
    pass
