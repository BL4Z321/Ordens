from django.urls import path
from insumos import views

urlpatterns = [
    path('gestor/listar_insumos', views.listar_insumos, name='listar_insumos'),
    path('gestor/novo_insumo', views.criar_insumo, name='criar_insumo'),
    path('gestor/editar_insumo/<int:pk>', views.editar_insumo, name='editar_insumo'),
    path('gestor/excluir_insumo/<int:pk>', views.excluir_insumo, name='excluir_insumo'),

]