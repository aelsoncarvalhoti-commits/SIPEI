from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from sipei_backend.models import Aluno, Pei

def paginaInicial(request):

    alunos = Aluno.objects.all()
    peis = Pei.objects.all()
    peisrevisao = Pei.objects.filter(ativo=False)
    peisconcluidos = Pei.objects.filter(ativo=True)
    return render(request, 'public/paginainicial.html', {'alunos': alunos, 'peis':peis, 'peisrevisao':peisrevisao, 'peisconcluidos':peisconcluidos})

def listar_estudantes(request):
    alunos = Aluno.objects.all()
    return render(request, 'public/estudantes.html', {'alunos': alunos})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('home')

        return render(request, 'public/login.html', {
            'erro': 'Usuário ou senha inválidos.'
        })

    return render(request, 'public/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')