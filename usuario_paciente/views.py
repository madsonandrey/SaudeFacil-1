from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from usuario_paciente.form import UserForm, FormPaciente
from usuario_profissional.models import Usuario_profissional
from .models import Usuario_paciente


def home(request):

    return render(request, '../templates/home.html')

def login_paciente(request):
    if request.method != 'POST':
        return render(request, 'login_paciente.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'login_paciente.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('menu_paciente')

@login_required(redirect_field_name='login_paciente.html', login_url='login_paciente.html')

def menu_paciente(request):
    current_user = request.user.id
    usuario_paciente = get_object_or_404(Usuario_paciente, usuario_paciente_id=current_user)
    contexto = {'usuario_paciente': usuario_paciente}

    return render(request, 'menu_paciente.html', contexto)

def logout_paciente(request):
    auth.logout(request)
    return redirect('login_paciente')

def cadastrar_paciente(request):
    form1 = UserForm(request.POST or None)
    form2 = FormPaciente(request.POST or None)

    if request.method != 'POST':
        form1 = UserForm()
        form2 = FormPaciente()
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

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
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe')
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    # CPF

    if len(cpf) != 11:
        messages.error(request, 'CPF inválido')
        form1 = UserForm()
        form2 = FormPaciente()
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormPaciente()
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormPaciente()
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    # E-MAIL
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        if form2.is_valid():
            usuario_paciente = form2.save(commit=False)
            usuario_paciente.usuario_paciente = user
            form1.save()
            form2.save()
            return redirect('login_paciente')

    return render(request, 'cadastro_paciente.html', {'form1': form1, 'form2': form2})

def editar_paciente(request, usuario_paciente_id):
    obj = get_object_or_404(Usuario_paciente, id=usuario_paciente_id)

    user = request.POST.get('usuario')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')

    form1 = UserForm(request.POST or None, instance=obj.usuario_paciente)
    form2 = FormPaciente(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = FormPaciente()
            return render(request, 'editar_paciente.html', {'form1': form1, 'form2': form2})

        if len(cpf) != 11:
            messages.error(request, 'CPF inválido')
            form1 = UserForm()
            form2 = FormPaciente()
            return render(request, 'editar_paciente.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            usuario_paciente = form2.save(commit=False)
            usuario_paciente.usuario_paciente = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return redirect('menu_paciente')

    return render(request, 'editar_paciente.html', {'form1': form1, 'form2': form2})

def lista_profissionais(request):
    usuario_profissional = Usuario_profissional.objects.order_by('id')

    return render(request, 'lista_profissionais.html', {'usuario_profissional': usuario_profissional})

def deletar_paciente(request, usuario_paciente_id):
    usuario_paciente = get_object_or_404(Usuario_paciente, id=usuario_paciente_id)

    if request.method == "GET":
        usuario_paciente.delete()
        messages.success(request, 'Usuário apagado com sucesso')
        return redirect('home')

    return render(request, "delete_paciente.html")