from django.contrib import admin
from .models import Insumo

# Register your models here.
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade_medida', 'estoque_atual', 'ativo')
    list_filter = ('unidade_medida', 'ativo')
    search_fields = ('nome',)