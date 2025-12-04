from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from usuarios.models import Usuario, RoleEnum


@receiver(post_save, sender=User)
def create_usuario(sender, instance, created, **kwargs):
    if created:
        role = RoleEnum.ADMIN if instance.is_superuser else RoleEnum.OPERADOR
        Usuario.objects.create(user=instance, role=role)