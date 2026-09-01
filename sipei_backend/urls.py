from django.urls import path
from .views.public_views import paginaInicial, listar_estudantes, login_view, logout_view
from .views.authenticated_view import cadastrar_aluno

urlpatterns = [
    path('', paginaInicial, name="home"),
    path('estudantes/', listar_estudantes, name="estudantes"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('aluno/cadastro/', cadastrar_aluno, name="cadastrar_aluno"),
]