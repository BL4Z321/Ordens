from expedicao.models import Expedicao, ExpedicaoEnum
from insumos.models import Insumo
from modelos_customizados.models import Modelo
from ordens_producao.models import OrdemProducao, PrioridadeOPEnum, StatusOPEnum, OPInsumo, OPProduto
from produtos.models import Produto
from usuarios.models import RoleEnum, Usuario

from django.core.exceptions import ValidationError
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def criar_ordem(request):
    usuario = Usuario.objects.get(user=request.user)
    modelos = Modelo.objects.all()

    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})

    if request.method == 'POST':
        cod_op = request.POST.get('cod_op')
        qtd_pedida = request.POST.get('qtd_pedida')
        cliente = request.POST.get('cliente')
        data_entrega = request.POST.get('data_entrega')
        prioridade = request.POST.get('prioridade')
        observacoes = request.POST.get('obs')
        modelo_id = request.POST.get('modelo')

        if not all([cod_op, qtd_pedida, cliente, data_entrega, prioridade, modelo_id]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios!')
            return redirect('criar_ordem')

        modelo = Modelo.objects.get(id=modelo_id)

        status_inicial = StatusOPEnum.PENDENTE
        try:
            OrdemProducao.objects.create(
                cod_op=cod_op,
                qtd_pedida=qtd_pedida,
                cliente=cliente,
                data_entrega=data_entrega,
                status=status_inicial,
                prioridade=prioridade,
                observacoes=observacoes,
                modelo=modelo,
            )
            messages.add_message(request, constants.SUCCESS, f'Ordem {cod_op} criada com sucesso!')

        except ValidationError as ve:
            messages.add_message(request, constants.ERROR, ve.message)
            return redirect('listar_ordens')

        return redirect('listar_ordens')

    contexto = {
        'modelos': modelos,
        'prioridades': PrioridadeOPEnum.choices,
        'status': StatusOPEnum.choices,
        'hoje': date.today().isoformat()
    }
    return render(request, 'gestor/nova_ordem.html', contexto)

@login_required
def listar_ordens(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})
    
    query = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    prioridade_filtro =request.GET.get('prioridade', '')

    ordens = OrdemProducao.objects.all().order_by('-data_criacao')

    if query:
        ordens = ordens.filter(
            Q(cod_op__icontains=query) |
            Q(cliente__icontains=query) |
            Q(modelo__nome__icontains=query)
        )
    
    if status_filtro:
        ordens = ordens.filter(status=status_filtro)
    
    if prioridade_filtro:
        ordens = ordens.filter(prioridade=prioridade_filtro)

    paginator = Paginator(ordens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'ordens': page_obj,
        'page_obj': page_obj,
        'query': query,
        'status_filtro': status_filtro,
        'prioridade_filtro': prioridade_filtro,
        'status': StatusOPEnum.choices,
        'prioridade': PrioridadeOPEnum.choices
    }
    return render(request, 'gestor/ordens.html', contexto)

@login_required
def editar_ordem(request, pk):
    ordem = get_object_or_404(OrdemProducao, pk=pk)
    modelos = Modelo.objects.all()

    if request.method == 'POST':
        ordem.qtd_pedida = request.POST.get('qtd_pedida')
        ordem.cliente = request.POST.get('cliente')
        ordem.data_entrega = request.POST.get('data_entrega')
        ordem.status = request.POST.get('status')
        ordem.prioridade = request.POST.get('prioridade')
        ordem.observacoes = request.POST.get('obs')
        ordem.modelo_id = request.POST.get('modelo')

        try:
            ordem.save()
            messages.add_message(request, constants.SUCCESS, f'Ordem {ordem.cod_op} atualizada com sucesso!')
            return redirect('listar_ordens')

        except ValidationError as ve:
            messages.add_message(request, constants.ERROR, ve.message)
            return redirect('listar_ordens')

    contexto = {
        'ordem': ordem,
        'status': StatusOPEnum.choices,
        'prioridade': PrioridadeOPEnum.choices,
        'modelos': modelos,
        'hoje': date.today().isoformat()
    }

    return render(request, 'gestor/editar_ordem.html', contexto)

@login_required
def excluir_ordem(request, pk):
    ordem = get_object_or_404(OrdemProducao, pk=pk)

    if request.method == 'POST':
        ordem.delete()
        messages.add_message(request, constants.SUCCESS, 'Ordem de Produção excluída com sucesso!')
        return redirect('listar_ordens')

    return render(request, 'gestor/excluir_ordem.html', {'ordem': ordem})

@login_required
def detalhes_ordem(request, pk):
    op = OrdemProducao.objects.get(id=pk)
    insumos = OPInsumo.objects.filter(op=op).select_related('insumo')
    op_produtos = OPProduto.objects.filter(op=op).select_related('produto')
    historico = op.historicoop_set.all().order_by('-data_criacao') if hasattr(op, 'historicoop_set') else []

    contexto = {
        'op': op,
        'insumos': insumos,
        'op_produtos': op_produtos,
        'historico': historico,
    }
    return render(request, 'gestor/detalhes_ordem.html', contexto)

@login_required
def producao_ordens(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.OPERADOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})

    query = request.GET.get('q', '')
    status_filtro = request.GET.get('status', '')
    prioridade_filtro = request.GET.get('prioridade', '')

    ordens = OrdemProducao.objects.all().order_by('-data_criacao')

    if query:
        ordens = ordens.filter(
            Q(cod_op__icontains=query) |
            Q(cliente__icontains=query) |
            Q(modelo__nome__icontains=query)
        )

    if status_filtro:
        ordens = ordens.filter(status=status_filtro)

    if prioridade_filtro:
        ordens = ordens.filter(prioridade=prioridade_filtro)

    paginator = Paginator(ordens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'ordens': page_obj,
        'page_obj': page_obj,
        'query': query,
        'status_filtro': status_filtro,
        'prioridade_filtro': prioridade_filtro,
        'status': StatusOPEnum.choices,
        'prioridade': PrioridadeOPEnum.choices
    }

    return render(request, 'operador/producao_ordens.html', contexto)

@login_required
def producao_editar(request, pk):
    usuarios = Usuario.objects.all()
    ordem = get_object_or_404(OrdemProducao, pk=pk)

    if request.method == 'POST':
        ordem.status = request.POST.get('status')
        responsavel_id = request.POST.get('responsavel')
        ordem.responsavel = Usuario.objects.get(id=responsavel_id)

        try:
            ordem.save()
            messages.add_message(request, constants.SUCCESS, f'Ordem {ordem.cod_op} atualizada com sucesso!')
            return redirect('producao_ordens')

        except ValidationError as ve:
            messages.add_message(request, constants.ERROR, ve.message)
            return redirect('producao_ordens')

    contexto = {
        'ordem': ordem,
        'usuarios': usuarios,
        'status': StatusOPEnum.choices,
    }

    return render(request, 'operador/producao_editar.html', contexto)

@login_required
def producao_detalhes(request, pk):
    op = OrdemProducao.objects.get(id=pk)
    insumos = OPInsumo.objects.filter(op=op).select_related('insumo')
    op_produtos = OPProduto.objects.filter(op=op).select_related('produto')
    historico = op.historicoop_set.all().order_by('-data_criacao') if hasattr(op, 'historicoop_set') else []

    contexto = {
        'op': op,
        'insumos': insumos,
        'op_produtos': op_produtos,
        'historico': historico,
    }
    return render(request, 'operador/producao_detalhes.html', contexto)