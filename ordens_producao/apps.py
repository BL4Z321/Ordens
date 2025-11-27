from django.apps import AppConfig


class OrdensProducaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordens_producao'

    def ready(self):
        import ordens_producao.signals.op_signals