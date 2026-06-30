from django.urls import path
from .views.public_views import *
from .views.authenticated_view import *

urlpatterns = [
    path('', paginaInicial, name="paginainicial"),
    path('aluno/cadastro', cadastrar_aluno, name="cadastrar_aluno")
]