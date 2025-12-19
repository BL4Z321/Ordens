from django.apps import AppConfig


class InsumosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insumos'

    def ready(self):
        import insumos.signals.insumo_signals