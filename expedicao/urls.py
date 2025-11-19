from django.urls import path
from expedicao import views

urlpatterns = [
    path('gestor/listar_expedicoes/', views.listar_expedicao, name='listar_expedicoes'),
    path('gestor/editar_expedicao/<int:pk>', views.editar_expedicao, name='editar_expedicao'),
]