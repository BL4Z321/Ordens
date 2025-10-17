from django.db import models

# Create your models here.
class TipoInsumoEnum(models.TextChoices):
    CASE = 'case', 'Case'
    FIO = 'fio', 'Fio'
    COMPONENTE = 'componente', 'Componente'
    MODULO = 'modulo', 'Módulo'

class Insumo(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TipoInsumoEnum.choices)
    estoque_atual = models.IntegerField(default=0)
    unidade_medida = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    