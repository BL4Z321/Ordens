from django.urls import path
from modelos_customizados import views

urlpatterns = [
    path('gestor/listar_modelos/', views.listar_modelos, name='listar_modelos'),
    path('gestor/editar_modelo/<int:pk>', views.editar_modelo, name='editar_modelos'),
    path('gestor/excluir_modelo/<int:pk>', views.excluir_modelo, name='excluir_modelo'),
    path('gestor/criar_modelo/', views.criar_modelo, name='criar_modelo')
]
