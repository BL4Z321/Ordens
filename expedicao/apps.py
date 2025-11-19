from django.apps import AppConfig


class ExpedicaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expedicao'

    def ready(self):
        import expedicao.signals