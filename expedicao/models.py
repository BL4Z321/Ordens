from django.db import models
from ordens_producao.models import OrdemProducao

# Create your models here.
class ExpedicaoEnum(models.TextChoices):
    EM_TRANSPORTE = 'em_transporte', 'Em tranporte'
    ENTREGUE = 'entregue', 'Entregue'
    RETORNADO = 'retornado', 'Retornado'
    ENVIADO = 'enviado', 'Enviado'
    PENDENTE = 'pendente', 'Pendente'

class Expedicao(models.Model):
    data_envio = models.DateField()
    destino = models.CharField(max_length=255)
    transportadora = models.CharField(max_length=100)
    cod_rastreio = models.CharField(max_length=100, blank=True, null=True)
    qtd_enviada = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ExpedicaoEnum.choices, default=ExpedicaoEnum.PENDENTE)
    observacoes = models.TextField(null=True, blank=True)
    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name='expedicoes')

    def __str__(self):
        return f'Expedição {self.id} - {self.status}'
    