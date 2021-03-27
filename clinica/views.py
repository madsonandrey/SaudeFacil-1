from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from clinica.form import UserForm, FormClinica
from .models import Clinica

def home(request):

    return render(request, '../templates/home.html')

def login_clinica(request):

    if request.method != 'POST':
        return render(request, 'login_clinica.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'usuario ou senha incorretos')
        return render(request, 'login_clinica.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')

def logout_clinica(request):
    auth.logout(request)
    return redirect('login_clinica')

def cadastrar_clinica(request):
    form1 = UserForm(request.POST or None)
    form2 = FormClinica(request.POST or None)

    if request.method != 'POST':
        form1 = UserForm()
        form2 = FormClinica()
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    username = request.POST.get('username')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cnpj = request.POST.get('cnpj')
    email = request.POST.get('email')

    # Validações

    # USUÁRIO

    if not username or not senha or not confirmar_senha or not first_name or not last_name or not cnpj or not email:
        messages.error(request, 'Todos os campos devem ser preenchidos')
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe')
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    # CNPJ

    if len(cnpj) != 14:
        messages.error(request, 'CNPJ inválido')
        form1 = UserForm()
        form2 = FormClinica()
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormClinica()
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormClinica()
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    # E-MAIL
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        if form2.is_valid():
            clinica = form2.save(commit=False)
            clinica.clinica = user
            form1.save()
            form2.save()
            return redirect('login_clinica')

    return render(request, 'cadastro_clinica.html', {'form1': form1, 'form2': form2})