from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('PROF', 'Professor'),
        ('CAPNES', 'CAPNES'),
    ]

    cargo = models.CharField(max_length=30, choices=TIPO_USUARIO)

class Aluno(models.Model):
    SEXO = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outros')
    ]

    nome = models.CharField(max_length=50, null=False)
    cpf = models.CharField(max_length=16, null=False, unique=True)
    foto = models.ImageField(upload_to="imagens/fotos")
    idade = models.IntegerField(null=False)  # Removido max_length=3
    sexo = models.CharField(max_length=30, choices=SEXO, null=False)
    contato = models.CharField(max_length=11, null=False)

    def __str__(self):
        return self.nome

class Pei(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, null=False, blank=False)
    ativo = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Diagnosticos(models.Model):

    pei = models.ForeignKey(Pei, on_delete=models.CASCADE)
    laudo = models.BooleanField(default=False)
    diagnostico = models.TextField(max_length=300)
    ano = models.DateField()

class Procedimento(models.Model):

    diagnostico = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE)
    atendimento = models.CharField(max_length=30)
    prioridade = models.CharField(max_length=30)

class Observacao(models.Model):

    professor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING)

    materia = models.CharField(max_length=30, null=False, blank=False)
    observacao = models.TextField(max_length=1000)
    data = models.DateTimeField(auto_now_add=True)

