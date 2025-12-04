from django.db import models
from fornecedores.models import Fornecedore

# Create your models here.
class TipoProdutoEnum(models.TextChoices):
    RASTREADOR = 'rastreador', 'Rastreador'
    ISCA = 'isca', 'Isca'

class TecnologiaProdutoEnum(models.TextChoices):
    G2 = '2G', '2G'
    G4 = '4G', '4G'

class Produto(models.Model):
    modelo = models.CharField(max_length=100, unique=True,)
    tipo = models.CharField(max_length=20, choices=TipoProdutoEnum.choices)
    tecnologia = models.CharField(max_length=20, choices=TecnologiaProdutoEnum.choices)
    descricao = models.TextField(null=True, blank=True)
    qtd_estoque_atual = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    fornecedor_id = models.ForeignKey(Fornecedore, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return f'{self.modelo} - ({self.tecnologia})'
