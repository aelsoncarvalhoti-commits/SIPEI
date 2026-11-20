from django.conf import settings
from django.db import models
from django.urls import reverse


class Estudante(models.Model):
    class Necessidade(models.TextChoices):
        DEFICIENCIA_INTELECTUAL = 'deficiencia_intelectual', 'Deficiência Intelectual'
        DEFICIENCIA_FISICA = 'deficiencia_fisica', 'Deficiência Física'
        BAIXA_VISAO = 'baixa_visao', 'Baixa Visão'
        CEGUEIRA = 'cegueira', 'Cegueira'
        SURDEZ = 'surdez', 'Surdez/Deficiência Auditiva'
        TEA = 'tea', 'Transtorno do Espectro Autista (TEA)'
        TDAH = 'tdah', 'TDAH'
        ALTAS_HABILIDADES = 'altas_habilidades', 'Altas Habilidades/Superdotação'
        OUTROS = 'outros', 'Outros'

    nome_completo = models.CharField('Nome completo', max_length=150)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    matricula = models.CharField('Matrícula', max_length=30, unique=True)
    curso = models.CharField('Curso', max_length=150, blank=True)
    turma = models.CharField('Turma', max_length=50, blank=True)
    campus = models.CharField('Campus', max_length=100, default='Porto Seguro')

    telefone = models.CharField('Telefone do estudante', max_length=20, blank=True)
    email = models.EmailField('E-mail do estudante', blank=True)
    responsavel_nome = models.CharField('Nome do responsável', max_length=150, blank=True)
    responsavel_telefone = models.CharField('Telefone do responsável', max_length=20, blank=True)

    foto = models.ImageField('Foto', upload_to='estudantes/fotos/', null=True, blank=True)

    necessidade_especifica = models.CharField(
        'Necessidade específica', max_length=30, choices=Necessidade.choices,
        default=Necessidade.OUTROS,
    )
    descricao_necessidade = models.TextField('Descrição da necessidade', blank=True)

    professor_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='estudantes_responsavel', verbose_name='Professor(a) AEE responsável',
    )

    ativo = models.BooleanField('Ativo', default=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='estudantes_cadastrados',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    def get_absolute_url(self):
        return reverse('estudantes:detail', args=[self.pk])

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        from datetime import date
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )


class Diagnostico(models.Model):
    estudante = models.OneToOneField(
        Estudante, on_delete=models.CASCADE, related_name='diagnostico',
    )
    cid = models.CharField('CID', max_length=20, blank=True)
    data_diagnostico = models.DateField('Data do diagnóstico', null=True, blank=True)
    profissional_responsavel = models.CharField('Profissional responsável', max_length=150, blank=True)
    descricao = models.TextField('Descrição do diagnóstico', blank=True)
    observacoes = models.TextField('Observações médicas', blank=True)
    laudo_medico = models.FileField('Laudo médico (arquivo)', upload_to='estudantes/laudos/', null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'

    def __str__(self):
        return f'Diagnóstico de {self.estudante.nome_completo}'


class PerfilAprendizagem(models.Model):
    estudante = models.OneToOneField(
        Estudante, on_delete=models.CASCADE, related_name='perfil_aprendizagem',
    )
    pontos_fortes = models.TextField('Pontos fortes', blank=True)
    dificuldades = models.TextField('Principais dificuldades', blank=True)
    estilo_aprendizagem = models.TextField('Estilo de aprendizagem', blank=True)
    interesses = models.TextField('Interesses e preferências', blank=True)
    observacoes = models.TextField('Observações gerais', blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de aprendizagem'
        verbose_name_plural = 'Perfis de aprendizagem'

    def __str__(self):
        return f'Perfil de aprendizagem de {self.estudante.nome_completo}'


class Adaptacao(models.Model):
    class Tipo(models.TextChoices):
        CURRICULAR = 'curricular', 'Curricular'
        AVALIATIVA = 'avaliativa', 'Avaliativa'
        ESTRUTURAL = 'estrutural', 'Estrutural/Física'
        COMUNICACIONAL = 'comunicacional', 'Comunicacional'
        TECNOLOGICA = 'tecnologica', 'Tecnológica/Recursos'

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='adaptacoes')
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.CURRICULAR)
    disciplina = models.CharField('Componente curricular', max_length=100, blank=True)
    descricao = models.TextField('Descrição da adaptação')
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Adaptação'
        verbose_name_plural = 'Adaptações'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.estudante.nome_completo}'


class ComponenteCurricular(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='componentes')
    disciplina = models.CharField('Componente curricular', max_length=100)
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='componentes_lecionados',
    )
    carga_horaria = models.PositiveIntegerField('Carga horária semanal', null=True, blank=True)
    adaptacoes_necessarias = models.TextField('Adaptações necessárias', blank=True)

    class Meta:
        verbose_name = 'Componente curricular'
        verbose_name_plural = 'Componentes curriculares'
        ordering = ['disciplina']

    def __str__(self):
        return f'{self.disciplina} — {self.estudante.nome_completo}'


class PlanejamentoPedagogico(models.Model):
    class Status(models.TextChoices):
        PLANEJADO = 'planejado', 'Planejado'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        CONCLUIDO = 'concluido', 'Concluído'

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='planejamentos')
    disciplina = models.CharField('Componente curricular', max_length=100, blank=True)
    objetivo = models.TextField('Objetivo pedagógico')
    estrategia = models.TextField('Estratégia/metodologia', blank=True)
    meta = models.TextField('Meta esperada', blank=True)
    prazo = models.DateField('Prazo', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANEJADO)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Planejamento pedagógico'
        verbose_name_plural = 'Planejamentos pedagógicos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Planejamento — {self.estudante.nome_completo}'


class Acompanhamento(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='acompanhamentos')
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='acompanhamentos_registrados',
    )
    data = models.DateField('Data do registro')
    observacao = models.TextField('Observação pedagógica')
    estrategias_aplicadas = models.TextField('Estratégias aplicadas', blank=True)
    adaptacoes_realizadas = models.TextField('Adaptações realizadas', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro de acompanhamento'
        verbose_name_plural = 'Registros de acompanhamento'
        ordering = ['-data', '-criado_em']

    def __str__(self):
        return f'Acompanhamento de {self.estudante.nome_completo} em {self.data}'
