from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

from estoque.models import ModeloInsumo
from insumos.models import TipoInsumoEnum, Insumo
from modelos_customizados.models import ModeloEnum, Modelo
from usuarios.models import Usuario, RoleEnum

# Create your views here.
@login_required
def listar_estoque(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

    modelo_filtro = request.GET.get('modelo', '')
    insumo_filtro = request.GET.get('insumo', '')

    estoques = ModeloInsumo.objects.all().order_by('-modelo')
    insumos = Insumo.objects.all()
    modelos = Modelo.objects.all()

    if modelo_filtro:
        estoques = estoques.filter(modelo=modelo_filtro)

    if insumo_filtro:
        estoques = estoques.filter(insumo=insumo_filtro)

    contexto = {
        'estoques': estoques,
        'modelo_filtro': modelo_filtro,
        'modelos': modelos,
        'insumo_filtro': insumo_filtro,
        'insumos': insumos,
    }

    return render(request, 'gestor/estoques.html', contexto)

@login_required
def criar_estoque(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.role != RoleEnum.GESTOR:
        return render(request, 'login.html', {'mensagem': 'Acesso restrito ao gestor!'})

    modelos = Modelo.objects.all()
    insumos = Insumo.objects.all()

    if request.method == 'POST':
        modelo_id = request.POST.get('modelo')
        insumo_id = request.POST.get('insumo')
        qtd = request.POST.get('qtd')

        if not all([modelo_id, insumo_id, qtd]):
            messages.add_message(request, constants.ERROR, 'Preencha os campos obrigatórios!')
            return redirect('criar_estoque')

        modelo = Modelo.objects.get(id=modelo_id)
        insumo = Insumo.objects.get(id=insumo_id)

        ModeloInsumo.objects.create(
            modelo=modelo,
            insumo=insumo,
            qtd_por_unidade=qtd,
        )
        messages.add_message(request, constants.SUCCESS, f'Estoque {modelo} criado com sucesso!')
        return redirect('listar_estoque')

    contexto = {
        'modelos': modelos,
        'insumos': insumos,
    }

    return render(request, 'gestor/novo_estoque.html', contexto)

@login_required
def editar_estoque(request, pk):
    estoque = get_object_or_404(ModeloInsumo, pk=pk)
    modelos = Modelo.objects.all()
    insumos = Insumo.objects.all()

    if request.method == 'POST':
        estoque.modelo = request.POST.get('modelo')
        estoque.insumo = request.POST.get('insumo')
        estoque.qtd_por_unidade = request.POST.get('qtd_por_unidade')

        estoque.save()
        messages.add_message(request, constants.SUCCESS, f'Estoque {estoque.modelo} editado com sucesso!')
        return redirect('listar_estoque')

    contexto = {
        'estoque': estoque,
        'modelos': modelos,
        'insumos': insumos
    }

    return render(request, 'gestor/editar_estoque.html', contexto)

@login_required
def excluir_estoque(request, pk):
    estoque = get_object_or_404(ModeloInsumo, pk=pk)

    if request.method == 'POST':
        estoque.delete()
        messages.add_message(request, constants.SUCCESS, f'Estoque excluido com sucesso!')
        return redirect('listar_estoque')

    return render(request, 'gestor/excluir_estoque.html', {'estoque': estoque})