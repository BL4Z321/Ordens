from django.urls import path
from modelos_customizados import views

urlpatterns = [
    path('gestor/listar_modelos/', views.listar_modelos, name='listar_modelos'),
    
]
