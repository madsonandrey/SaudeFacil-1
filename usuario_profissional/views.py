from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth, messages
from usuario_profissional.form import UserForm, FormUsuario
from .models import Usuario_profissional

def home(request):
    return render(request, '../templates/home.html')


def login_pro(request):
    if request.method != 'POST':
        return render(request, 'usuario/login_pro.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'usuario/login_pro.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('menu_user')

@login_required(redirect_field_name='login_pro', login_url='login_pro')

def menu_user(request):
    current_user = request.user.id
    usuario_profissional = get_object_or_404(Usuario_profissional, usuario_profissional_id=current_user)
    contexto = {'usuario_profissional': usuario_profissional}

    return render(request, 'usuario/menu_pro.html', contexto)

def logout_pro(request):
    auth.logout(request)
    return redirect('login_pro')


def cadastrar_pro(request):
    form1 = UserForm(request.POST or None)
    form2 = FormUsuario(request.POST or None)
    if request.method != 'POST':
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    username = request.POST.get('username')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')

    # Validações

    # USUÁRIO

    if not username or not senha or not confirmar_senha or not first_name or not last_name or not cpf or not email:
        messages.error(request, 'Todos os campos devem ser preenchidos')
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe')
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    # CPF

    if len(cpf) != 11:
        messages.error(request, 'CPF inválido')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    # E-MAIL
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        # user.is_staff = True
        # user.is_superuser = True
        form1.save()
        # user.groups.add(1)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario_profissional = user
            form1.save()
            form2.save()
            return redirect('login_pro')

    return render(request, 'usuario/cadastro_pro.html', {'form1': form1, 'form2': form2})

def listar_pro(request):
    usuario_profissional = Usuario_profissional.objects.order_by('-id')

    return render(request, 'lista_pro', {
        'usuario_profissional': usuario_profissional
    })


def editar_pro(request, usuario_profissional_id):
    obj = get_object_or_404(Usuario_profissional, id=usuario_profissional_id)

    user = request.POST.get('usuario')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')

    form1 = UserForm(request.POST or None, instance=obj.usuario_profissional)
    form2 = FormUsuario(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_pro.html', {'form1': form1, 'form2': form2})

        if len(cpf) != 11:
            messages.error(request, 'CPF inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_pro.html.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            usuario_profissional = form2.save(commit=False)
            usuario_profissional.usuario_profissional = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return redirect('menu_user')

    return render(request, 'usuario/editar_pro.html', {'form1': form1, 'form2': form2})


def deletar_profissional(request, usuario_profissional_id):
    usuario_profissional = get_object_or_404(Usuario_profissional, id=usuario_profissional_id)

    if request.method == "GET":
        usuario_profissional.delete()
        messages.success(request, 'Usuário apagado com sucesso')
        return redirect('home')

    return render(request, "../templates/home.html")