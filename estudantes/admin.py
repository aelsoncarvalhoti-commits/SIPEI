from django.contrib import admin

from .models import (
    Acompanhamento, Adaptacao, ComponenteCurricular, Diagnostico, Estudante,
    PerfilAprendizagem, PlanejamentoPedagogico,
)


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'matricula', 'curso', 'necessidade_especifica', 'professor_responsavel', 'ativo']
    list_filter = ['necessidade_especifica', 'ativo', 'campus']
    search_fields = ['nome_completo', 'matricula']


admin.site.register(Diagnostico)
admin.site.register(PerfilAprendizagem)
admin.site.register(Adaptacao)
admin.site.register(ComponenteCurricular)
admin.site.register(PlanejamentoPedagogico)
admin.site.register(Acompanhamento)
