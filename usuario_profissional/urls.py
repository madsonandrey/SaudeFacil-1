from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_pro/', views.login_pro, name='login_pro'),
    path('logout_pro/', views.logout_pro, name='logout_pro'),
    path('cadastro_pro/', views.cadastrar_pro, name='cadastro_pro'),
    path('editar_pro/<int:usuario_profissional_id>', views.editar_pro, name='editar_pro'),
    path('menu_pro/', views.menu_user, name='menu_user'),
    path('listar_pro/', views.listar_pro, name='listar_pro'),
    path('deletar_profissional/<int:usuario_profissional_id>', views.deletar_profissional, name='deletar_profissional'),
]
