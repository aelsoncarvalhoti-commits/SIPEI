from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Perfil(models.TextChoices):
        COORDENACAO = 'coordenacao', 'Coordenação CAPNE'
        PROFESSOR = 'professor', 'Professor'

    perfil = models.CharField(
        max_length=20, choices=Perfil.choices, default=Perfil.PROFESSOR,
    )
    registro = models.CharField(
        'Matrícula/SIAPE', max_length=30, blank=True,
    )
    campus = models.CharField(max_length=100, blank=True, default='Porto Seguro')
    telefone = models.CharField(max_length=20, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_coordenacao(self):
        return self.perfil == self.Perfil.COORDENACAO
