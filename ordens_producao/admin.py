from django.contrib import admin
from .models import OrdemProducao, OPInsumo

# Register your models here.
class OPInsumoPrevistoInline(admin.TabularInline):
    model = OPInsumo
    extra = 0
    readonly_fields = ('insumo', 'qtd_necessaria_por_unidade', 'qt_total_prevista')

@admin.register(OrdemProducao)
class OrdemProducaoAdmin(admin.ModelAdmin):
    list_display = ('cod_op', 'cliente', 'status', 'prioridade', 'modelo', 'qtd_pedida', 'data_criacao')
    list_filter = ('status', 'prioridade', 'modelo')
    inlines = [OPInsumoPrevistoInline]
