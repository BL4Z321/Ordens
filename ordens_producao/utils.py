from django.db.models import Sum
from decimal import Decimal
from estoque.models import ModeloInsumo
from ordens_producao.models import OPProduto, OPInsumo

def desbloqueio(op):
    produto = op.modelo.produto_id

    total_produto = OPProduto.objects.filter(
        produto=produto
    ).exclude(op=op).aggregate(
        total=Sum('qtd_total')
    )['total'] or 0

    if total_produto + op.qtd_pedida > produto.qtd_estoque_atual:
        return False

    estrutura = ModeloInsumo.objects.filter(modelo=op.modelo)

    for item in estrutura:
        insumo = item.insumo

        if insumo.unidade_medida == 'metro':
            qtd_por_un = Decimal('0.15')
        else:
            qtd_por_un = Decimal(str(item.qtd_por_unidade or 0))

        qtd_op = qtd_por_un * Decimal(op.qtd_pedida)

        total_insumo =  OPInsumo.objects.filter(
            insumo=insumo
        ).exclude(op=op).aggregate(
            total=Sum('qt_total_prevista')
        )['total'] or Decimal('0')

        if total_insumo + qtd_op > Decimal(insumo.estoque_atual):
            return False

    return True
