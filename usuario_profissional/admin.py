from django.contrib import admin
from .models import Usuario_profissional, User


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_display_links = ('first_name',)


admin.site.register(Usuario_profissional)