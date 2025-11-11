from django.urls import path
from produtos import views

urlpatterns = [
      # URLs do CRUD dos produtos - Em desenvolvimento
    path('gestor/listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('gestor/criar_produto/', views.criar_produto, name='criar_produto'),
    path('gestor/editar_produto/<int:pk>/', views.editar_produto, name='geditar_produto'),
    path('gestor/excluir_produto/<int:pk>/', views.excluir_produto, name='gexcluir_produto'),
]
