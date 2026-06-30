from django.shortcuts import render
from ..sevices.pdf_service import *
from ..models import Aluno

def cadastrar_aluno(request):

    if request.method == 'POST':
        nome = request.POST.get("nome")
        cpf = request.POST.get("cpf")
        idade = request.POST.get("idade")
        sexo = request.POST.get("sexo")
        contato = request.POST.get("contato")

        aluno = Aluno(nome=nome, cpf = cpf, idade = idade, sexo = sexo, contato = contato)
        aluno.save()

    return render(request, "authenticated/cadastroaluno.html")

def gerar_pdf_aluno(request, aluno_id):

    gerar_pdf(request, aluno_id)