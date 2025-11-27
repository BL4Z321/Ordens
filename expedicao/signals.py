from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from ordens_producao.models import OrdemProducao, StatusOPEnum
from .models import Expedicao, ExpedicaoEnum


# Guarda o status antigo antes do save
@receiver(pre_save, sender=OrdemProducao)
def salvar_status_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


# Ação principal após salvar OP
@receiver(post_save, sender=OrdemProducao)
def gerenciar_expedicao(sender, instance, created, **kwargs):

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    # (1) Criar expedição quando virar CONCLUÍDA
    if new_status == StatusOPEnum.CONCLUIDA:
        if not Expedicao.objects.filter(ordem=instance).exists():
            Expedicao.objects.create(
                ordem=instance,
                status=ExpedicaoEnum.PENDENTE,
                data_entrega=instance.data_entrega,
                qtd_enviada=instance.qtd_produzida,
                observacoes=instance.observacoes,
            )
        return

    # (2) Excluir expedição quando SAIR de CONCLUÍDA
    if old_status == StatusOPEnum.CONCLUIDA and new_status != StatusOPEnum.CONCLUIDA:
        exp = Expedicao.objects.filter(ordem=instance).first()
        if exp:
            exp.delete()
