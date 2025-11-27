from django.contrib import admin
from estoque.models import ModeloInsumo
from .models import Modelo

# Register your models here.
class ModeloInsumoInline(admin.TabularInline):
    model = ModeloInsumo
    extra = 1

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao', 'ativo', 'produto_id')
    search_fields = ('nome', )
    inlines = [ModeloInsumoInline]
