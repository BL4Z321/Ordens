from django.urls import path
from ordens_producao import views

urlpatterns = [
    path('gestor/listar_ordens/', views.listar_ordens, name='listar_ordens'),
    path('gestor/criar_ordem/', views.criar_ordem, name='criar_ordem'),
    path('gestor/editar_ordem/<int:pk>/', views.editar_ordem, name='geditar_ordem'),
    path('gestor/excluir_ordem/<int:pk>/', views.excluir_ordem, name='gexcluir_ordem'),
    path('gestor/detalhes_ordem/<int:pk>/', views.detalhes_ordem, name='detalhes_ordem'),

    path('operador/producao_ordens', views.producao_ordens, name='producao_ordens'),
    path('operador/producao_editar/<int:pk>/', views.producao_editar, name='producao_editar'),
    path('operador/producao_detalhes/<int:pk>/', views.producao_detalhes, name='producao_detalhes'),

]
