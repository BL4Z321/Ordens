from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.messages import constants

from expedicao.models import Expedicao, ExpedicaoEnum
from insumos.models import Insumo
from modelos_customizados.models import Modelo
from ordens_producao.models import OrdemProducao, StatusOPEnum
from produtos.models import Produto
from usuarios.models import RoleEnum, Usuario

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                usuario = Usuario.objects.get(user=user)
            except Usuario.DoesNotExist:
                messages.add_message(request, constants.ERROR, 'Usuario não cadastrado.')
                return redirect('login')
            if usuario.ativo:
                login(request, user)
                messages.add_message(request, constants.SUCCESS, f'Bem-vindo, {user.username}')
                
                if usuario.role == RoleEnum.ADMIN:
                    if not user.is_staff:
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()

                    return redirect('/admin/')
                
                elif usuario.role == RoleEnum.GESTOR:
                    return redirect('dashboard')
                
                elif usuario.role == RoleEnum.OPERADOR:
                    return redirect('operador')
                
                else:
                    return redirect('viewer')
                
            else:
                messages.add_message(request, constants.ERROR, 'Usuário inativo. Contate o administrador.')
                return redirect('login')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inváidos.')
            return redirect('login')
        
    return render(request, 'login.html')
    
@login_required
def sair(request):
    logout(request)
    messages.add_message(request, constants.INFO, 'Você saiu do sistema!')
    return redirect('login')

@login_required
def painel_gestor(request):
    return render(request, 'ordens/gestor/dashboard')

@login_required
def painel_operador(request):
    return render(request, 'operador.html')

@login_required
def painel_viewer(request):
    return render(request, 'viewer.html')


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