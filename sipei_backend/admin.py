from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {
            'fields': ('cargo',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações adicionais', {
            'fields': ('cargo',)
        }))