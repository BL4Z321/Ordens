from django.urls import path
from ordens_producao import views

urlpatterns = [
    path('gestor/dashboard/', views.dashboard, name='dashboard'),
    
    # URLs do CRUD das ordens
    path('gestor/listar/', views.ordens, name='listar_ordens'),
    path('gestor/ordens/nova/', views.criar_ordem, name='criar_ordem'),
    path('gestor/editar/<int:pk>/', views.editar_ordem, name='geditar_ordem'),
    path('gestor/excluir/<int:pk>/', views.excluir_ordem, name='gexcluir_ordem'),

    
]
