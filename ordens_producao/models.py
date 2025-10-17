from django.db import models
from modelos_customizados.models import Modelo
from usuarios.models import Usuario

# Create your models here.
class StatusOPEnum(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    EM_PRODUCAO = 'em_producao', 'Em Produção'
    CONCLUIDA = 'concluida', 'Concluída'
    CANCELADA = 'cancelada', 'Cancelada'

class PrioridadeOPEnum(models.TextChoices):
    BAIXA = 'baixa', 'Baixa'
    MEDIA = 'media', 'Media'
    ALTA = 'alta', 'Alta'
    URGENTE = 'urgente', 'Urgente'

class OrdemProducao(models.Model):
    cod_op = models.CharField(max_length=50, unique=True)
    qtd_pedida = models.IntegerField(default=1)
    qtd_produzida = models.IntegerField(default=0)
    cliente = models.CharField(max_length=100)
    data_criacao = models.DateField(auto_now_add=True)
    data_inicio = models.DateField(null=False, blank=False)
    data_conclusao = models.DateField(null=False, blank=False)
    data_entrega = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=StatusOPEnum.choices, default=StatusOPEnum.PENDENTE)
    prioridade = models.CharField(max_length=20, choices=PrioridadeOPEnum.choices, default=PrioridadeOPEnum.MEDIA)
    observacoes = models.TextField(null=True, blank=True)
    responsavel = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ordens')
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='ordens')

    def __str__(self):
        return f'OP {self.cod_op} - {self.modelo.nome}'
    