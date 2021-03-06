from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class StarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stark'

    def ready(self):
        print("start load")
        autodiscover_modules('stark')
