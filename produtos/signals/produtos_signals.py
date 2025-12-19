from django.db.models.signals import post_save
from django.dispatch import receiver

from ordens_producao.models import OrdemProducao, StatusOPEnum
from ordens_producao.utils import desbloqueio
from produtos.models import Produto


@receiver(post_save, sender=Produto)
def tentar_desbloquear_ops_por_produto(sender, instance, **kwargs):
    ops_bloqueadas = OrdemProducao.objects.filter(
        status = StatusOPEnum.BLOQUEADA,
        modelo__produto_id=instance,
    )

    for op in ops_bloqueadas:
        if desbloqueio(op):
            op.status = StatusOPEnum.PENDENTE
            op.save(update_fields=['status'])