
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.messages import constants
from usuarios.models import Usuario

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            usuario = Usuario.objects.get(user=user)
            if usuario.ativo:
                login(request, user)
                messages.add_message(request, constants.SUCCESS , f'Bem-vindo, {user.username}')
                
                match usuario:
                    case 'admin':
                        return redirect('login.html')
                    
                    case 'gestor':
                        return redirect('gestor.html')
                    
                    case 'operador':
                        return redirect('operador.html')
                    
                    case 'viewer':
                        return redirect('viewer.html')
            else:
                messages.add_message(request, constants.ERROR, 'Usuário inativo. Contate o administrador.')
        else:
            messages.error(request, constants.ERROR, 'Usuário ou senha inváidos.')
        
        return render(request, 'login.html')
    
@login_required
def sair(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema!')
    return redirect('login')
