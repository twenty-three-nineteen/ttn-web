from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'account'

    def ready(self):
        from account import signals
