from django.apps import AppConfig


class WebConfig(AppConfig):
    name = 'web'

    def ready(self):
        from . import updater
        updater.start()
