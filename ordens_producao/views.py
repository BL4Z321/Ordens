from expedicao.models import Expedicao, ExpedicaoEnum
from insumos.models import Insumo
from modelos_customizados.models import Modelo
from ordens_producao.models import OrdemProducao, PrioridadeOPEnum, StatusOPEnum
from produtos.models import Produto
from usuarios.models import RoleEnum, Usuario

from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
@login_required
def dashboard(request):
    usuario = Usuario.objects.get(user=request.user)

    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})
    
    total_ordens = OrdemProducao.objects.count()
    ordens_ativas = OrdemProducao.objects.filter(status=StatusOPEnum.EM_PRODUCAO).count()
    ordens_concluidas = OrdemProducao.objects.filter(status=StatusOPEnum.CONCLUIDA).count()
    ordens_pendentes = OrdemProducao.objects.filter(status=StatusOPEnum.PENDENTE).count()
    ordens_canceladas = OrdemProducao.objects.filter(status=StatusOPEnum.CANCELADA).count()
    
    produtos_disponiveis = Produto.objects.count()
    
    modelos_custom = Modelo.objects.count()
    
    insumos_baixos = Insumo.objects.filter(estoque_atual__lt=5).count()
    
    expedicao = Expedicao.objects.count()
    expedi_transporte = Expedicao.objects.filter(status=ExpedicaoEnum.EM_TRANSPORTE).count()
    expedi_entregue = Expedicao.objects.filter(status=ExpedicaoEnum.ENTREGUE).count()
    expedi_retornado = Expedicao.objects.filter(status=ExpedicaoEnum.RETORNADO).count()
    expedi_enviado = Expedicao.objects.filter(status=ExpedicaoEnum.ENVIADO).count()
    expedi_pendente = Expedicao.objects.filter(status=ExpedicaoEnum.PENDENTE).count()

    contexto = {
        'usuario': usuario,
        'total_ordens': total_ordens,
        'ordens_ativas': ordens_ativas,
        'ordens_concluidas': ordens_concluidas,
        'ordens_pendentes': ordens_pendentes, 
        'ordens_canceladas': ordens_canceladas,
        'produtos_disponiveis': produtos_disponiveis,
        'modelos_custom': modelos_custom,
        'insumos_baixos': insumos_baixos,
        'expedicao': expedicao,
        'expedi_transporte': expedi_transporte,
        'expedi_entregue': expedi_entregue,
        'expedi_retornado': expedi_retornado,
        'expedi_enviado': expedi_enviado,
        'expedi_pendente': expedi_pendente,
    }

    return render(request, 'gestor/dashboard.html', contexto)

# CRUD das Ordens
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
        status = request.POST.get('status')
        prioridade = request.POST.get('prioridade')
        observacoes = request.POST.get('obs')
        modelo_id = request.POST.get('modelo')

        if not all([cod_op, qtd_pedida, cliente, data_entrega, status, prioridade, modelo_id]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios!')
            return redirect('criar_ordem')

        modelo = Modelo.objects.get(id=modelo_id)

        OrdemProducao.objects.create(
            cod_op=cod_op,
            qtd_pedida=qtd_pedida,
            cliente=cliente,
            data_entrega=data_entrega,
            status=status,
            prioridade=prioridade,
            observacoes=observacoes,
            modelo=modelo,
        )
        messages.add_message(request, constants.SUCCESS, f'Ordem {cod_op} criada com sucesso!')
        return redirect('listar_ordens')
    
    contexto = {
        'modelos': modelos,
        'prioridades': PrioridadeOPEnum.choices,
        'status': StatusOPEnum.choices,
        'hoje': date.today().isoformat()
    }
    return render(request, 'gestor/nova_ordem.html', contexto)
    
@login_required
def ordens(request):
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

        ordem.save()
        messages.add_message(request, constants.SUCCESS, f'Ordem {ordem.cod_op} atualizada com sucesso!')
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
