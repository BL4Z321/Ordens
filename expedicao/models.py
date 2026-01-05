from django.db import models
from ordens_producao.models import OrdemProducao

# Create your models here.
class ExpedicaoEnum(models.TextChoices):
    EM_TRANSPORTE = 'em_transporte', 'Em Transporte'
    ENTREGUE = 'entregue', 'Entregue'
    RETORNADO = 'retornado', 'Retornado'
    ENVIADO = 'enviado', 'Enviado'
    PENDENTE = 'pendente', 'Pendente'

class Expedicao(models.Model):
    ordem = models.OneToOneField(OrdemProducao, on_delete=models.CASCADE, related_name='expedicao')
    status = models.CharField(max_length=20, choices=ExpedicaoEnum.choices, default=ExpedicaoEnum.PENDENTE)
    destino = models.CharField(max_length=255, null=True, blank=True)
    data_envio = models.DateField(blank=True, null=True)
    data_entrega = models.DateField(blank=True, null=True)
    transportadora = models.CharField(max_length=100, blank=True, null=True)
    cod_rastreio = models.CharField(max_length=100, blank=True, null=True)
    qtd_enviada = models.IntegerField(default=0, blank=True, null=True)
    observacoes = models.TextField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Expedição {self.ordem.id} - {self.status}'
    