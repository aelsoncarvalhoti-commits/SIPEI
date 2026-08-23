from django.shortcuts import render
from sipei_backend.models import Aluno  

def paginaInicial(request):
    return render(request, 'public/paginainicial.html')

def listar_estudantes(request):
    alunos = Aluno.objects.all()
    return render(request, 'public/estudantes.html', {'alunos': alunos})