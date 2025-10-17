from django.db import models
from insumos.models import Insumo
from modelos_customizados.models import Modelo

# Create your models here.
class ModeloInsumo(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='modelos')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='insumo')
    qtd_por_unidade = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.modelo.nome} - {self.insumo.nome}'