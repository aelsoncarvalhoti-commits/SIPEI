from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'perfil', 'campus', 'ativo', 'is_staff']
    list_filter = ['perfil', 'campus', 'ativo']
    fieldsets = UserAdmin.fieldsets + (
        ('Dados SIPEI', {'fields': ('perfil', 'registro', 'campus', 'telefone', 'ativo')}),
    )
