from django.urls import path
from ordens_producao import views

urlpatterns = [
    path('gestor/listar_ordens/', views.listar_ordens, name='listar_ordens'),
    path('gestor/criar_ordem/', views.criar_ordem, name='criar_ordem'),
    path('gestor/editar_ordem/<int:pk>/', views.editar_ordem, name='geditar_ordem'),
    path('gestor/excluir_ordem/<int:pk>/', views.excluir_ordem, name='gexcluir_ordem'),
]
