from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_clinica/', views.login_clinica, name='login_clinica'),
    path('logout_clinica/', views.logout_clinica, name='logout_clinica'),
    path('cadastro_clinica/', views.cadastrar_clinica, name='cadastro_clinica'),
]