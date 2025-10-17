from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RoleEnum(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    GESTOR = 'gestor', 'Gestor'
    OPERADOR = 'operador', 'Operador'
    VIEWER = 'viewer', 'Viewer'

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=RoleEnum.choices, default=RoleEnum.OPERADOR)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    