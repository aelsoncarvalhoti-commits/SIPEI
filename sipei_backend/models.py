from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Usuario(AbstractUser):

    TIPO_USUARIO = [
        ('PROF', 'Professor'),
        ('CAPNES', 'CAPNES'),
    ]

    cargo = models.CharField(max_length= 30, choices=TIPO_USUARIO)

# Create your models here.
class Aluno(models.Model):

    SEXO = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outros')
    ]

    nome = models.CharField(max_length=50, null=False)
    cpf = models.CharField(max_length=16, null=False, unique=True)
    foto = models.ImageField(upload_to="imagens/fotos")
    idade = models.IntegerField(max_length=3, null=False)
    sexo = models.CharField(max_length=30, choices=SEXO, null=False)
    contato = models.CharField(max_length=11, null=False)