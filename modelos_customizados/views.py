from modelos_customizados.models import Modelo, ModeloEnum
from produtos.models import Produto
from usuarios.models import RoleEnum, Usuario
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def listar_modelos(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})
    
    query = request.GET.get('q', '')
    ativo_filtro = request.GET.get('ativo', '')

    modelos = Modelo.objects.all().order_by('nome')
    
    if query:
        modelos = modelos.filter(
            Q(nome__icontains=query)
        )
    
    if ativo_filtro:
        modelos = modelos.filter(ativo=(ativo_filtro == 'True'))

    paginator = Paginator(modelos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'modelos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'ativo_filtro': ativo_filtro,
        'nome': ModeloEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')]
    }

    return render(request, 'gestor/modelos.html', contexto)

@login_required
def editar_modelo(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)
    produtos = Produto.objects.all()

    if request.method == 'POST':
        modelo.nome = request.POST.get('nome')
        modelo.descricao = request.POST.get('descricao')
        modelo.ativo = request.POST.get('ativo')
        modelo.produto = request.POST.get('produto')

        modelo.save()
        messages.add_message(request, constants.SUCCESS, f'Modelo {modelo.nome} atualizado com sucesso!')
        return redirect('listar_modelos')

    contexto = {
        'modelo': modelo,
        'nome': ModeloEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')],
        'produtos': produtos,
    }

    return render(request, 'gestor/editar_modelo.html', contexto)

@login_required
def excluir_modelo(request, pk):
    modelo = get_object_or_404(Modelo, pk=pk)

    if request.method == 'POST':
        modelo.delete()
        messages.add_message(request, constants.SUCCESS, f'Modelo {modelo.nome} excluido com sucesso!')
        return redirect('listar_modelos')

    return render(request, 'gestor/excluir_modelo.html', {'modelo': modelo})

@login_required
def criar_modelo(request):
    usuario = Usuario.objects.get(user=request.user)
    produtos = Produto.objects.all()

    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        ativo = request.POST.get('ativo')
        produto_id = request.POST.get('produto')

        if not all([nome, ativo, produto_id]):
            messages.add_message(request,constants.ERROR, 'Preencha todos os campos obrigatórios!')
            return redirect('listar_modelos')

        produto = Produto.objects.get(id=produto_id)

        Modelo.objects.create(
            nome=nome,
            descricao=descricao,
            ativo=ativo,
            produto_id=produto
        )
        messages.add_message(request, constants.SUCCESS, f'Modelo {nome} criado com sucesso!')
        return redirect('listar_modelos')

    contexto = {
        'produtos': produtos,
        'nome': ModeloEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')]
    }

    return render(request, 'gestor/novo_modelo.html', contexto)