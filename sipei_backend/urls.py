from django.urls import path
from .views.public_views import paginaInicial, listar_estudantes
from .views.authenticated_view import cadastrar_aluno

urlpatterns = [
    path('', paginaInicial, name="home"),
    path('estudantes/', listar_estudantes, name="estudantes"),
    path('aluno/cadastro/', cadastrar_aluno, name="cadastrar_aluno"),
]