from django.urls import path
from ordens_producao import views

urlpatterns = [
    path('gestor/dashboard/', views.dashboard, name='dashboard'),
    
    # URLs do CRUD das ordens - OK
    path('gestor/ordens/listar_ordens/', views.listar_ordens, name='listar_ordens'),
    path('gestor/ordens/criar_ordem/', views.criar_ordem, name='criar_ordem'),
    path('gestor/ordens/editar_ordem/<int:pk>/', views.editar_ordem, name='geditar_ordem'),
    path('gestor/ordens/excluir_ordem/<int:pk>/', views.excluir_ordem, name='gexcluir_ordem'),

    # URLs do CRUD dos produtos - Em desenvolvimento
    path('gestor/produtos/listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('gestor/produtos/criar_produto/', views.criar_produto, name='criar_produto'),
    path('gestor/produtos/editar_produto/<int:pk>/', views.editar_produto, name='geditar_produto'),
    path('gestor/produtos/excluir_produto/<int:pk>/', views.excluir_produto, name='gexcluir_produto'),
]
