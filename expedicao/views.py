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

    query = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')

    expedicoes = Expedicao.objects.all().order_by('-criado_em')

    if query:
        expedicoes = expedicoes.filter(
            Q(destino__icontains=query)
        )

    if status_filtro:
        expedicoes = expedicoes.filter(status=status_filtro)

    contexto = {
        'expedicoes': expedicoes,
        'query': query,
        'status_filtro': status_filtro,
        'status':  ExpedicaoEnum.choices,
    }

    return render(request, 'gestor/expedicoes.html', contexto)