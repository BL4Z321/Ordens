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
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidade_medida = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)

    def get_unidade_abreviada(self):
        if self.unidade_medida in ['metros', 'metro']:
            return 'm'
        elif self.unidade_medida in ['gramas', 'grama']:
            return 'g'
        elif self.unidade_medida in ['unidades', 'unidade']:
            return 'unid.'
        return ''

    def __str__(self):
        return self.nome
    