from django.db import models

from insumos.models import Insumo
from modelos_customizados.models import Modelo
from produtos.models import Produto
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
    qtd_pedida = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    qtd_produzida = models.IntegerField(default=0, null=True, blank=True)
    cliente = models.CharField(max_length=100)
    data_criacao = models.DateField(auto_now_add=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    data_entrega = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=StatusOPEnum.choices, default=StatusOPEnum.PENDENTE)
    prioridade = models.CharField(max_length=20, choices=PrioridadeOPEnum.choices, default=PrioridadeOPEnum.MEDIA)
    observacoes = models.TextField(null=True, blank=True)
    responsavel = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ordens', null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='ordens')

    def __str__(self):
        return f'OP {self.cod_op} - {self.modelo.nome}'

class OPInsumo(models.Model):
    op = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name='insumos_previstos')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    qtd_necessaria_por_unidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qt_total_prevista = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qtd_baixada = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'OP {self.op.cod_op} - {self.insumo.nome}'

class OPProduto(models.Model):
    op = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name='op_produto')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd_necessaria = models.IntegerField(default=1)
    qtd_total = models.IntegerField(default=0)

    def __str__(self):
        return f'OP {self.op.cod_op} - {self.produto.modelo}'