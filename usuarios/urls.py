from django.urls import path
from usuarios import views


urlpatterns = [
    path('login/', views.login_view, name='login'),    
    path('logout/', views.sair, name='logout'),
]
