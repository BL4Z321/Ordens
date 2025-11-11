from django.urls import path
from ordens_producao import views

urlpatterns = [
    path('gestor/dashboard/', views.dashboard, name='dashboard'),
    
    # URLs do CRUD das ordens - OK
    path('gestor/ordens/listar_ordens/', views.listar_ordens, name='listar_ordens'),
    path('gestor/ordens/criar_ordem/', views.criar_ordem, name='criar_ordem'),
    path('gestor/ordens/editar_ordem/<int:pk>/', views.editar_ordem, name='geditar_ordem'),
    path('gestor/ordens/excluir_ordem/<int:pk>/', views.excluir_ordem, name='gexcluir_ordem'),
]
