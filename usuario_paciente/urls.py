from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_paciente/', views.cadastrar_paciente, name='cadastro_paciente'),
    path('login_paciente/', views.login_paciente, name='login_paciente'),
    path('logout_paciente/', views.logout_paciente, name='logout_paciente'),
    path('menu_paciente/', views.menu_paciente, name='menu_paciente'),
    path('lista_profissionais/', views.lista_profissionais, name='lista_profissionais'),
    path('editar_paciente/<int:usuario_paciente_id>', views.editar_paciente, name='editar_paciente'),
    path('deletar_paciente/<int:usuario_paciente_id>', views.deletar_paciente, name='deletar_paciente'),
]