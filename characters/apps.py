from django.apps import AppConfig


class CharactersAppConfig(AppConfig):
    name = 'characters'

    def ready(self):
        import characters.signals
