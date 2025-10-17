from django.urls import path

from ordens_producao import views

urlpatterns = [
    path('', views.teste, name='teste')
]
