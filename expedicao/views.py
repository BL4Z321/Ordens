from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, get_object_or_404, redirect
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

@login_required
def editar_expedicao(request, pk):
    expedicao = get_object_or_404(Expedicao, pk=pk)

    if request.method == 'POST':
        expedicao.status = request.POST.get('status')
        expedicao.destino = request.POST.get('destino')
        expedicao.data_envio = request.POST.get('data_envio')
        expedicao.data_entrega = request.POST.get('data_entrega')
        expedicao.transportadora = request.POST.get('transportadora')
        expedicao.cod_rastreio = request.POST.get('cod_rastreio')
        expedicao.observacoes = request.POST.get('obs')

        expedicao.save()
        messages.add_message(request, constants.SUCCESS, f'Expedição {expedicao.ordem.cod_op} atualizado com sucesso!')
        return redirect('listar_expedicoes')

    contexto = {
        'expedicao': expedicao,
        'status': ExpedicaoEnum.choices,
    }

    return render(request, 'gestor/editar_expedicao.html', contexto)
