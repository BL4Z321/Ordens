from fornecedores.models import Fornecedore
from produtos.models import Produto, TecnologiaProdutoEnum, TipoProdutoEnum
from usuarios.models import RoleEnum, Usuario
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# CRUD das Produtos - Em desenvolvimento
@login_required
def listar_produtos(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})
    
    query = request.GET.get('q', '')
    ativo_filtro = request.GET.get('ativo', '')

    produtos = Produto.objects.all().order_by('modelo')
    if query:
        produtos = produtos.filter(
            Q(modelo__icontains=query)
        )
        
    if ativo_filtro:
        produtos = produtos.filter(ativo=(ativo_filtro == 'True'))

    paginator = Paginator(produtos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'produtos': page_obj,
        'page_obj': page_obj,
        'query': query,
        'ativo_filtro': ativo_filtro,
        'tipo': TipoProdutoEnum.choices,
        'tecnologia': TecnologiaProdutoEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')],
    }

    return render(request, 'gestor/produtos.html', contexto)

@login_required
def criar_produto(request):
    usuario = Usuario.objects.get(user=request.user)
    fornecedores = Fornecedore.objects.all()

    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor.'})
    
    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        tipo = request.POST.get('tipo')
        tecnologia = request.POST.get('tecnologia')
        descricao = request.POST.get('descricao')
        qtd_estoque_atual = request.POST.get('qtd')
        ativo  = request.POST.get('ativo')
        fornecedor_id = request.POST.get('fornecedor')
        
        if not all([modelo, tipo, tecnologia, qtd_estoque_atual, ativo, fornecedor_id]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios!')
            return redirect('criar_produto')
        
        fornecedor = Fornecedore.objects.get(id=fornecedor_id)

        Produto.objects.create(
            modelo=modelo,
            tipo=tipo,
            tecnologia=tecnologia,
            descricao=descricao,
            qtd_estoque_atual=qtd_estoque_atual,
            ativo=ativo,
            fornecedor_id=fornecedor
        )

        messages.add_message(request, constants.SUCCESS, f'Produto {modelo} criado com sucesso!')
        return redirect('listar_produtos')
    
    contexto = {
        'fornecedores': fornecedores,
        'tipos': TipoProdutoEnum.choices,
        'tecnologias': TecnologiaProdutoEnum.choices,
        'ativos': [('True', 'Ativo'), ('False', 'Inativo')],
    }

    return render(request, 'gestor/novo_produto.html', contexto)

@login_required
def editar_produto(request, pk):
 produto = get_object_or_404(Produto, pk=pk)
 fornecedores = Fornecedore.objects.all()

 if request.method == 'POST':
     produto.modelo = request.POST.get('modelo')
     produto.tipo = request.POST.get('tipo')
     produto.tecnologia = request.POST.get('tecnologia')
     produto.descricao = request.POST.get('descricao')
     produto.qtd_estoque_atual = request.POST.get('qtd')
     produto.ativo = request.POST.get('ativo')
     produto.fornecedor = request.POST.get('fornecedor')
     
     produto.save()
     messages.add_message(request, constants.SUCCESS, f'Produto {produto.modelo} atualizado com sucesso!')
     return redirect('listar_produtos')
 
 contexto = {
     'produto': produto,
     'tipos': TipoProdutoEnum.choices,
     'tecnologias': TecnologiaProdutoEnum.choices,
     'ativos': [('True', 'Ativo'), ('False', 'Inativo')],
     'fornecedores': fornecedores
 }

 return render(request, 'gestor/editar_produto.html', contexto)

@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        produto.delete()
        messages.add_message(request, constants.SUCCESS, 'Produto excluido com sucesso!')
        return redirect('listar_produtos')
    
    return render(request, 'gestor/excluir_produto.html', {'produto': produto})