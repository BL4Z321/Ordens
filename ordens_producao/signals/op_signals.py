from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum
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

        if item.insumo.unidade_medida == 'metro':
            qtd = Decimal('0.15')  # 15 cm em metros
            total = qtd * Decimal(instance.qtd_pedida)

        OPInsumo.objects.create(
            op=instance,
            insumo=item.insumo,
            qtd_necessaria_por_unidade=qtd,
            qt_total_prevista=total,
            qtd_baixada=0
        )

@receiver(pre_save, sender=OrdemProducao)
def validar_estoque_insumos(sender, instance, **kwargs):
    if instance.pk:
        return

    estrutura = ModeloInsumo.objects.filter(modelo=instance.modelo)

    for item in estrutura:
        insumo = item.insumo

        if insumo.unidade_medida == 'metro':
            qtd_por_un = Decimal('0.15')
        else:
            qtd_por_un = Decimal(str(item.qtd_por_unidade or 0))

        qtd_nova_op = qtd_por_un * Decimal(instance.qtd_pedida)

        total_reservado = OPInsumo.objects.filter(
            insumo=insumo
        ).aggregate(total=Sum('qt_total_prevista'))['total'] or Decimal('0')

        estoque = Decimal(str(insumo.estoque_atual))
        total_requirido = total_reservado + qtd_nova_op

        if  total_requirido > estoque:
            instance.status = StatusOPEnum.BLOQUEADA
            return

@receiver(pre_save, sender=OrdemProducao)
def validar_estoque_antes_de_iniciar(sender, instance, **kwargs):
    if not instance.pk:
        return

    estado_anterior = OrdemProducao.objects.get(pk=instance.pk)

    if estado_anterior.status == instance.status:
        return

    if instance.status == StatusOPEnum.EM_PRODUCAO:
        if estado_anterior.status == StatusOPEnum.BLOQUEADA:
            raise  ValidationError(
                'OP bloqueada por falta de estoque. Regularize antes de iniciar a produção.'
            )

        if estado_anterior.status in [StatusOPEnum.CANCELADA, StatusOPEnum.CONCLUIDA]:
            raise ValidationError(
                'Não é possível iniciar produção para esta OP.'
            )

        for item in instance.insumos_previstos.all():
            if item.insumo.estoque_atual < item.qt_total_prevista:
                raise ValidationError(
                    f'Insumo "{item.insumo.nome}" não possui estoque suficiente '
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

    total_em_ops = OPProduto.objects.filter(
        produto=produto
    ).aggregate(total=Sum('qtd_total'))['total'] or 0

    qtd_nova = int(instance.qtd_pedida)
    estoque = int(produto.qtd_estoque_atual)

    total_requerido = total_em_ops + qtd_nova

    if total_requerido > estoque:
       instance.status = StatusOPEnum.BLOQUEADA

@receiver(post_save, sender=OrdemProducao)
def criar_op_produto(sender, instance, created, **kwargs):
    if created:

        produto = instance.modelo.produto_id

        OPProduto.objects.create(
            op=instance,
            produto=produto,
            qtd_necessaria=1,
            qtd_total=instance.qtd_pedida
        )

@receiver(post_save, sender=OrdemProducao)
def baixar_produto_estoque(sender, instance, created, **kwargs):
    if created:
        return

    if instance.status == StatusOPEnum.CONCLUIDA:
        op_produto = instance.op_produto.first()
        produto = op_produto.produto

        produto.qtd_estoque_atual -= op_produto.qtd_total
        produto.save()