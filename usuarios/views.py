from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.messages import constants
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
