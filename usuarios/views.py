from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.messages import constants
from django.db.models import Count, Sum
from django.views.decorators.csrf import csrf_protect

from estoque.models import ModeloInsumo
from expedicao.models import Expedicao, ExpedicaoEnum
from insumos.models import Insumo
from modelos_customizados.models import Modelo
from ordens_producao.models import OrdemProducao, StatusOPEnum
from produtos.models import Produto
from usuarios.models import RoleEnum, Usuario

import json

@csrf_protect
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
        return redirect('login')

    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
        return redirect('login')

    try:
        usuario = Usuario.objects.get(user=user)
    except Usuario.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
        return redirect('login')

    if not usuario.ativo:
        messages.add_message(request, constants.ERROR, 'Usuário inativo. Contate o administrador.')
        return redirect('login')

    login(request, user)

    if usuario.role == RoleEnum.ADMIN:
        return redirect('admin:index')
    elif usuario.role == RoleEnum.GESTOR:
        return redirect('dashboard')
    elif usuario.role == RoleEnum.OPERADOR:
        return redirect('dash_operador')
    elif usuario.role == RoleEnum.VIEWER:
        return redirect('viewer')

    return redirect('login')
    
@login_required
def sair(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_gestor(request):
    usuario = Usuario.objects.get(user=request.user)

    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao usuário.'})

    total_ordens = OrdemProducao.objects.count()
    ordens_ativas = OrdemProducao.objects.filter(status=StatusOPEnum.EM_PRODUCAO).count()
    ordens_concluidas = OrdemProducao.objects.filter(status=StatusOPEnum.CONCLUIDA).count()
    ordens_pendentes = OrdemProducao.objects.filter(status=StatusOPEnum.PENDENTE).count()
    ordens_canceladas = OrdemProducao.objects.filter(status=StatusOPEnum.CANCELADA).count()
    ordens_bloqueadas = OrdemProducao.objects.filter(status=StatusOPEnum.BLOQUEADA).count()

    produtos_disponiveis = Produto.objects.count()

    modelos_custom = Modelo.objects.count()

    insumos_baixos = Insumo.objects.filter(estoque_atual__lt=5).count()

    expedicao = Expedicao.objects.count()
    expedi_transporte = Expedicao.objects.filter(status=ExpedicaoEnum.EM_TRANSPORTE).count()
    expedi_entregue = Expedicao.objects.filter(status=ExpedicaoEnum.ENTREGUE).count()
    expedi_retornado = Expedicao.objects.filter(status=ExpedicaoEnum.RETORNADO).count()
    expedi_enviado = Expedicao.objects.filter(status=ExpedicaoEnum.ENVIADO).count()
    expedi_pendente = Expedicao.objects.filter(status=ExpedicaoEnum.PENDENTE).count()

    estoque = ModeloInsumo.objects.count()

    contexto = {
        'usuario': usuario,
        'total_ordens': total_ordens,
        'ordens_ativas': ordens_ativas,
        'ordens_concluidas': ordens_concluidas,
        'ordens_pendentes': ordens_pendentes,
        'ordens_canceladas': ordens_canceladas,
        'ordens_bloqueadas': ordens_bloqueadas,
        'produtos_disponiveis': produtos_disponiveis,
        'modelos_custom': modelos_custom,
        'insumos_baixos': insumos_baixos,
        'expedicao': expedicao,
        'expedi_transporte': expedi_transporte,
        'expedi_entregue': expedi_entregue,
        'expedi_retornado': expedi_retornado,
        'expedi_enviado': expedi_enviado,
        'expedi_pendente': expedi_pendente,
        'estoque': estoque,
    }

    return render(request, 'gestor/dashboard.html', contexto)

@login_required
def dashboard_operador(request):
    usuario = Usuario.objects.get(user=request.user)

    if usuario.role != RoleEnum.OPERADOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao usuário.'})

    total_ordens = OrdemProducao.objects.count()
    ordens_ativas = OrdemProducao.objects.filter(status=StatusOPEnum.EM_PRODUCAO).count()
    ordens_concluidas = OrdemProducao.objects.filter(status=StatusOPEnum.CONCLUIDA).count()
    ordens_pendentes = OrdemProducao.objects.filter(status=StatusOPEnum.PENDENTE).count()
    ordens_canceladas = OrdemProducao.objects.filter(status=StatusOPEnum.CANCELADA).count()
    ordens_bloqueadas = OrdemProducao.objects.filter(status=StatusOPEnum.BLOQUEADA).count()

    contexto = {
        'usuario': usuario,
        'total_ordens': total_ordens,
        'ordens_ativas': ordens_ativas,
        'ordens_concluidas': ordens_concluidas,
        'ordens_pendentes': ordens_pendentes,
        'ordens_canceladas': ordens_canceladas,
        'ordens_bloqueadas': ordens_bloqueadas,
    }

    return render(request, 'operador/dashboard.html', contexto)

@login_required
def dashboard_viewer(request):
    usuario = Usuario.objects.get(user=request.user)

    if usuario.role != RoleEnum.VIEWER:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao usuário.'})


    ordens_em_producao = OrdemProducao.objects.filter(status=StatusOPEnum.EM_PRODUCAO)

    total_ordens = OrdemProducao.objects.count()
    ordens_ativas = OrdemProducao.objects.filter(status=StatusOPEnum.EM_PRODUCAO).count()
    ordens_concluidas = OrdemProducao.objects.filter(status=StatusOPEnum.CONCLUIDA).count()
    ordens_pendentes = OrdemProducao.objects.filter(status=StatusOPEnum.PENDENTE).count()
    ordens_canceladas = OrdemProducao.objects.filter(status=StatusOPEnum.CANCELADA).count()
    ordens_bloqueadas = OrdemProducao.objects.filter(status=StatusOPEnum.BLOQUEADA).count()

    modelos = (
        OrdemProducao.objects
        .values("modelo__nome")
        .annotate(
        total_ordens=Count("id"),
        total_produzido=Sum("qtd_produzida")
        )
        .order_by("-total_ordens")
    )
    
    metrics = {
        'total_ordens': total_ordens,
        'ordens_ativas': ordens_ativas,
        'ordens_concluidas': ordens_concluidas,
        'ordens_pendentes': ordens_pendentes,
        'ordens_canceladas': ordens_canceladas,
        'ordens_bloqueadas': ordens_bloqueadas,
        'modelos': list(modelos),
    }

    contexto = {
        'usuario': usuario,
        'metrics_json': json.dumps(metrics),
        'metrics': metrics,
        'ordens_em_producao': ordens_em_producao,
    }

    return render(request, 'viewer/dashboard.html', contexto)
