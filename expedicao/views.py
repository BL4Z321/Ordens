from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from expedicao.models import Expedicao, ExpedicaoEnum
from ordens_producao.models import OrdemProducao, StatusOPEnum
from usuarios.models import Usuario, RoleEnum

@login_required
def listar_expedicao(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

# Create your views here.
