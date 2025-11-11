from django.shortcuts import render

# Create your views here.
def listar_modelos(request):
    return render(request, 'gestor/modelos.html')