from django.contrib import admin

from .models import PEI


@admin.register(PEI)
class PEIAdmin(admin.ModelAdmin):
    list_display = ['estudante', 'status', 'data_elaboracao', 'data_validade', 'responsavel_elaboracao']
    list_filter = ['status']
