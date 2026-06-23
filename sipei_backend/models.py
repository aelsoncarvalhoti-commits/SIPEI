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
    pass