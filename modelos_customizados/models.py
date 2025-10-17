from django.db import models
from insumos.models import Insumo
from produtos.models import Produto

# Create your models here.
class ModeloEnum(models.TextChoices):
    T1000 = 'T1000'
    T1000C = 'T1000C'
    T1000E = 'T1000E'
    T1000G = 'T1000G'
    T1000M = 'T1000M'
    T1000S = 'T1000S'
    T1000X = 'T1000X'

class Modelo(models.Model):
    nome = models.CharField(max_length=20, choices=ModeloEnum.choices)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='modelos_customizados')
    
    def __str__(self):
        return self.nome
