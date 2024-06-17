from django.apps import AppConfig


class AfficheConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'affiche'


class AfficheConfig(AppConfig):
    name = 'affiche'

    def ready(self):
        from . import scheduler
        scheduler.start()