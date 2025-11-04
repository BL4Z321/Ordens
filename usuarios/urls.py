from django.urls import path
from django.contrib import admin
from usuarios import views


urlpatterns = [
    path('login/', views.login_view, name='login'),    
    path('sair/', views.sair, name='sair'),    
    path('gestor/', views.painel_gestor , name='gestor'),
    path('operador/', views.painel_operador, name='operador'),
    path('viewer/', views.painel_viewer, name='viewer'),

]
