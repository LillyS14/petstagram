from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "petstagram.accounts"

    def ready(self):
        import petstagram.accounts.signals
