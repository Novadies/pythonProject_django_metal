from django.apps import AppConfig


class SomethingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metal'
    verbose_name = 'Метал'
