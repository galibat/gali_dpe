# galidpe/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate

class GalidpeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'galidpe'

    def ready(self):
        import galidpe.signals  # active le signal
        

