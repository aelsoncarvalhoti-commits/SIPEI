from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Aluno, Diagnosticos, Procedimento, Pei, Observacao
# Register your models here.


@admin.register(Observacao)
class ObservacaoAdmin(admin.ModelAdmin):
    list_display = (
        'professor',
        'aluno'
    )

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'cpf',
        'idade',
        'sexo',
        'contato',
    )

    search_fields = (
        'nome',
        'cpf',
    )

    list_filter = (
        'sexo',
    )

    ordering = ('nome',)


@admin.register(Pei)
class PeiAdmin(admin.ModelAdmin):
    list_display = (
        'aluno',
        'ativo',
        'data_criacao',
    )

    search_fields = (
        'aluno__nome',
        'aluno__cpf',
    )

    list_filter = (
        'ativo',
    )

    ordering = ('-data_criacao',)


@admin.register(Diagnosticos)
class DiagnosticosAdmin(admin.ModelAdmin):
    list_display = (
        'pei',
        'diagnostico',
        'laudo',
        'ano',
    )

    search_fields = (
        'diagnostico',
        'pei__aluno__nome',
        'pei__aluno__cpf',
    )

    list_filter = (
        'laudo',
        'ano',
    )

    ordering = ('-ano',)


@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = (
        'diagnostico',
        'atendimento',
        'prioridade',
    )

    search_fields = (
        'atendimento',
        'prioridade',
        'diagnostico__diagnostico',
        'diagnostico__pei__aluno__nome',
    )

    list_filter = (
        'atendimento',
        'prioridade',
    )

    ordering = ('prioridade',)

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