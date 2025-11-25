from django.urls import path
from estoque import views

urlpatterns = [
    path('gestor/listar_estoque', views.listar_estoque, name='listar_estoque'),
    path('gestor/criar_ordem', views.criar_estoque, name='criar_estoque'),
    path('gestor/editar_estoque/<int:pk>', views.editar_estoque, name='editar_estoque'),
    path(' gestor/excluir_estoque/<int:pk>', views.excluir_estoque, name='excluir_estoque'),
]