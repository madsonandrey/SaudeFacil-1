from usuario_paciente.models import Usuario_paciente
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    senha = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class FormPaciente(forms.ModelForm):
    class Meta:
        model = Usuario_paciente
        exclude = ('data_criacao', 'usuario_paciente')

