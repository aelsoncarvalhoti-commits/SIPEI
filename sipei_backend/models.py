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