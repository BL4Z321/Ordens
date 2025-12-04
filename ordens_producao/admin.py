from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.contrib.messages import constants

from .models import OrdemProducao, OPInsumo, StatusOPEnum


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

    def save_model(self, request, obj, form, change):
        try:
            if not obj.pk and obj.status == StatusOPEnum.EM_PRODUCAO:
                raise ValidationError('Não é permitido criar uma ordem já em produção!')
            super().save_model(request, obj, form, change)

        except ValidationError as ve:
            messages.add_message(request, constants.ERROR, ve.message)
