from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

from ordens_producao.models import OrdemProducao, OPInsumo, StatusOPEnum, OPProduto
from estoque.models import ModeloInsumo
from insumos.models import Insumo

@receiver(post_save, sender=OrdemProducao)
def gerar_insumos_automaticos(sender, instance, created, **kwargs):
    if not created:
        return

    estrutura = ModeloInsumo.objects.filter(modelo=instance.modelo)
    for item in estrutura:
        qtd = Decimal(str(item.qtd_por_unidade or 0))
        total = qtd * Decimal(instance.qtd_pedida)

        OPInsumo.objects.create(
            op=instance,
            insumo=item.insumo,
            qtd_necessaria_por_unidade=qtd,
            qt_total_prevista=total,
            qtd_baixada=0
        )

@receiver(pre_save, sender=OrdemProducao)
def validar_estoque_antes_de_iniciar(sender, instance, **kwargs):
    # Só valida se a ordem já existe
    if not instance.pk:
        return

    estado_anterior = OrdemProducao.objects.get(pk=instance.pk)

    # Só checa quando está tentando mudar para EM_PRODUCAO
    if estado_anterior.status != StatusOPEnum.EM_PRODUCAO and instance.status == StatusOPEnum.EM_PRODUCAO:
        for item in instance.insumos_previstos.all():
            if item.insumo.estoque_atual < item.qt_total_prevista:
                raise ValidationError(
                    f'Insumo "{item.insumo.nome}" não possui estoque suficiente'
                    f"({item.insumo.estoque_atual} disponível / {item.qt_total_prevista} necessário)."
                )

        instance.data_inicio = timezone.now()

@receiver(pre_save, sender=OrdemProducao)
def baixar_insumos_ao_concluir(sender, instance, **kwargs):
    if not instance.pk:
        return

    estado_anterior = OrdemProducao.objects.get(pk=instance.pk)

    if estado_anterior.status != StatusOPEnum.CONCLUIDA and instance.status == StatusOPEnum.CONCLUIDA:
        for item in instance.insumos_previstos.all():
            if item.qtd_baixada > 0:
                continue

            insumo = item.insumo

            insumo.estoque_atual -= item.qt_total_prevista
            insumo.save()

            item.qtd_baixada = item.qt_total_prevista
            item.save()

        instance.data_conclusao = timezone.now()

@receiver(pre_save, sender=OrdemProducao)
def estornar_insumos_se_reabrir(sender, instance, **kwargs):
    if not instance.pk:
        return

    estado_anterior = OrdemProducao.objects.get(pk=instance.pk)
    if estado_anterior.status == StatusOPEnum.CONCLUIDA and instance.status != StatusOPEnum.CONCLUIDA:
        if instance.status == StatusOPEnum.CANCELADA:
            return

        for item in instance.insumos_previstos.all():
            if item.qtd_baixada > 0:

                qtd_estornar = Decimal(str(item.qtd_baixada))

                insumo = item.insumo
                insumo.estoque_atual = Decimal(str(insumo.estoque_atual)) + qtd_estornar
                insumo.save()

                item.qtd_baixada = 0
                item.save()

        instance.data_conclusao = None

@receiver(pre_save, sender=OrdemProducao)
def verificar_estoque_produto(sender, instance, **kwargs):
    if instance.pk:
        return

    produto = instance.modelo.produto_id

    estoque = produto.qtd_estoque_atual
    necessario = instance.qtd_pedida

    if necessario > estoque:
        raise ValueError(
            f'Estoque insuficiente do produto {produto.modelo}. '
            f'Necessário: {necessario}, Disponível: {estoque}.'
        )

@receiver(post_save, sender=OrdemProducao)
def criar_op_produto(sender, instance, created, **kwargs):
    if created:
        produto = instance.modelo.produto_id

        OPProduto.objects.create(
            op=instance,
            produto=produto,
            qtd_necessaria=1,
            qtd_total=instance.qtd_pedida,
        )

@receiver(post_save, sender=OrdemProducao)
def baixar_produto_estoque(sender, instance, created, **kwargs):
    if created:
        return

    if instance.status == StatusOPEnum.CONCLUIDA:
        op_prod = instance.op_produto
        produto = op_prod.produto

        produto.qtd_estoque_atual -= op_prod.qtd_total
        produto.save()
