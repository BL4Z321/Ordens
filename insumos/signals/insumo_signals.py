from django.db.models.signals import post_save
from django.dispatch import receiver
from insumos.models import Insumo
from ordens_producao.models import OrdemProducao, StatusOPEnum
from ordens_producao.utils import desbloqueio


@receiver(post_save, sender=Insumo)
def tentar_desbloquear_ops_por_insumo(sender, instance, **kwargs):
    ops_bloqueadas = OrdemProducao.objects.filter(
        status=StatusOPEnum.BLOQUEADA
    )

    for op in ops_bloqueadas:
        if desbloqueio(op):
            op.status = StatusOPEnum.PENDENTE
            op.save(update_fields=['status'])
