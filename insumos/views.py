from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from insumos.models import Insumo, TipoInsumoEnum
from usuarios.models import Usuario, RoleEnum


# Create your views here.
@login_required
def listar_insumos(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

    query = request.GET.get('q', '')
    tipo_filtro = request.GET.get('tipo', '')
    ativo_filtro = request.GET.get('ativo', '')

    insumos = Insumo.objects.all().order_by('nome')
    if query:
        insumos = insumos.filter(
            Q(nome__icontains=query)
        )

    if tipo_filtro:
        insumos = insumos.filter(tipo=tipo_filtro)

    if ativo_filtro:
        insumos = insumos.filter(ativo=ativo_filtro)

    paginator = Paginator(insumos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'insumos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'tipo_filtro': tipo_filtro,
        'tipo': TipoInsumoEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')]
    }

    return render(request, 'gestor/insumos.html', contexto)

@login_required
def criar_insumo(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        estoque_atual = request.POST.get('qtd')
        unidade_medida = request.POST.get('um')
        ativo = request.POST.get('ativo')

        if not all([nome, tipo, estoque_atual, unidade_medida]):
            messages.add_message(request, constants.WARNING, 'Preencha todos os campos obrigatorios!')
            return redirect('criar_insumo')

        Insumo.objects.create(
            nome=nome,
            tipo=tipo,
            estoque_atual=estoque_atual,
            unidade_medida=unidade_medida,
            ativo=ativo
        )

        messages.add_message(request, constants.SUCCESS, f'Insumo {nome} criado com sucesso!')
        return redirect('listar_insumos')

    contexto = {
        'tipos': TipoInsumoEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')]
    }
    return render(request, 'gestor/novo_insumo.html', contexto)

@login_required
def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)

    if request.method == 'POST':
        insumo.nome = request.POST.get('nome')
        insumo.tipo = request.POST.get('tipo')
        insumo.estoque_atual = request.POST.get('qtd')
        insumo.unidade_medida = request.POST.get('um')
        insumo.ativo = request.POST.get('ativo')

        insumo.save()
        messages.add_message(request, constants.SUCCESS, f'Insumo {insumo.nome} atualizado com sucesso!')
        return redirect('listar_insumos')

    contexto = {
        'insumo': insumo,
        'tipos': TipoInsumoEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')]
    }

    return render(request, 'gestor/editar_insumo.html', contexto)

@login_required
def excluir_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)

    if request.method == 'POST':
        insumo.delete()
        messages.add_message(request, constants.SUCCESS, 'Produto excluido com sucesso!')
        return redirect('listar_insumos')

    return render(request, 'gestor/excluir_insumo.html', {'insumo': insumo})

