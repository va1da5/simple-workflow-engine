from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "flows.core"

    def ready(self):
        from . import signals, tasks