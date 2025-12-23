from django.urls import path
from django.contrib import admin
from usuarios import views


urlpatterns = [
    path('login/', views.login_view, name='login'),    
    path('sair/', views.sair, name='sair'),    
    path('operador/dashboard', views.dashboard_operador, name='dash_operador'),
    # path('viewer/', views.painel_viewer, name='viewer'),
    path('gestor/dashboard/', views.dashboard_gestor, name='dashboard'),

]
