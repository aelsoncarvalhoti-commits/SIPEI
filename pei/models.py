from django.conf import settings
from django.db import models
from django.utils import timezone


class PEI(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = 'rascunho', 'Rascunho'
        EM_ELABORACAO = 'em_elaboracao', 'Em elaboração'
        VIGENTE = 'vigente', 'Vigente'
        VENCIDO = 'vencido', 'Vencido'
        CONCLUIDO = 'concluido', 'Concluído'

    estudante = models.OneToOneField(
        'estudantes.Estudante', on_delete=models.CASCADE, related_name='pei',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RASCUNHO)
    data_elaboracao = models.DateField('Data de elaboração', default=timezone.localdate)
    data_validade = models.DateField('Válido até', null=True, blank=True)
    responsavel_elaboracao = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='peis_elaborados',
    )
    objetivos_gerais = models.TextField('Objetivos gerais do PEI', blank=True)
    observacoes_gerais = models.TextField('Observações gerais', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PEI'
        verbose_name_plural = 'PEIs'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f'PEI de {self.estudante.nome_completo}'

    @property
    def dias_para_vencer(self):
        if not self.data_validade:
            return None
        return (self.data_validade - timezone.localdate()).days

    @property
    def esta_vencido(self):
        dias = self.dias_para_vencer
        return dias is not None and dias < 0
