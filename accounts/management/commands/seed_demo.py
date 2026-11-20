import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Usuario
from estudantes.models import (
    Acompanhamento, Adaptacao, ComponenteCurricular, Diagnostico, Estudante,
    PerfilAprendizagem, PlanejamentoPedagogico,
)
from pei.models import PEI


class Command(BaseCommand):
    help = 'Cria usuários e estudantes de exemplo para demonstração do SIPEI.'

    def handle(self, *args, **options):
        coordenadora, criado = Usuario.objects.get_or_create(
            username='coordenacao',
            defaults=dict(
                first_name='Alaine', last_name='Santos',
                email='capne@ifba.edu.br', perfil=Usuario.Perfil.COORDENACAO,
                is_staff=True, is_superuser=True, campus='Porto Seguro',
            ),
        )
        if criado:
            coordenadora.set_password('capne@2026')
            coordenadora.save()
            self.stdout.write(self.style.SUCCESS('Usuário "coordenacao" criado (senha: capne@2026)'))

        professor, criado = Usuario.objects.get_or_create(
            username='professor',
            defaults=dict(
                first_name='Aelson', last_name='Fernandes',
                email='professor@ifba.edu.br', perfil=Usuario.Perfil.PROFESSOR,
                campus='Porto Seguro',
            ),
        )
        if criado:
            professor.set_password('professor@2026')
            professor.save()
            self.stdout.write(self.style.SUCCESS('Usuário "professor" criado (senha: professor@2026)'))

        hoje = timezone.localdate()
        exemplos = [
            dict(nome_completo='João Victor dos Santos', matricula='2024001', curso='Informática',
                 turma='2ºA', necessidade_especifica=Estudante.Necessidade.TEA, dias_validade=7),
            dict(nome_completo='Maria Eduarda Melo', matricula='2024002', curso='Administração',
                 turma='3ºB', necessidade_especifica=Estudante.Necessidade.BAIXA_VISAO, dias_validade=10),
            dict(nome_completo='Pedro Henrique Costa', matricula='2024003', curso='Edificações',
                 turma='1ºC', necessidade_especifica=Estudante.Necessidade.DEFICIENCIA_FISICA, dias_validade=45),
            dict(nome_completo='Ana Beatriz Souza', matricula='2024004', curso='Informática',
                 turma='2ºA', necessidade_especifica=Estudante.Necessidade.DEFICIENCIA_INTELECTUAL, dias_validade=None),
        ]

        for dados in exemplos:
            dias_validade = dados.pop('dias_validade')
            estudante, criado = Estudante.objects.get_or_create(
                matricula=dados['matricula'],
                defaults=dict(
                    nome_completo=dados['nome_completo'], curso=dados['curso'], turma=dados['turma'],
                    necessidade_especifica=dados['necessidade_especifica'],
                    data_nascimento=datetime.date(2007, 5, 12),
                    professor_responsavel=professor, criado_por=coordenadora,
                ),
            )
            if not criado:
                continue

            Diagnostico.objects.create(
                estudante=estudante, cid='—',
                descricao=f'Laudo de acompanhamento — {estudante.get_necessidade_especifica_display()}.',
                profissional_responsavel='Equipe multiprofissional CAPNE',
            )
            PerfilAprendizagem.objects.create(
                estudante=estudante,
                pontos_fortes='Boa memória visual e participação em atividades práticas.',
                dificuldades='Dificuldade de concentração em atividades longas.',
                estilo_aprendizagem='Aprendizagem visual e prática.',
            )
            Adaptacao.objects.create(
                estudante=estudante, tipo=Adaptacao.Tipo.AVALIATIVA, disciplina='Geral',
                descricao='Tempo adicional para realização de avaliações.', criado_por=coordenadora,
            )
            ComponenteCurricular.objects.create(
                estudante=estudante, disciplina='Matemática', professor=professor, carga_horaria=4,
                adaptacoes_necessarias='Material com fonte ampliada.',
            )
            PlanejamentoPedagogico.objects.create(
                estudante=estudante, disciplina='Matemática',
                objetivo='Desenvolver autonomia na resolução de problemas.',
                meta='Concluir 80% das atividades propostas.',
                status=PlanejamentoPedagogico.Status.EM_ANDAMENTO, criado_por=coordenadora,
            )
            Acompanhamento.objects.create(
                estudante=estudante, professor=professor, data=hoje - datetime.timedelta(days=3),
                observacao='Estudante participou ativamente da aula, com uso das adaptações previstas.',
                estrategias_aplicadas='Uso de material visual complementar.',
            )

            data_validade = (hoje + datetime.timedelta(days=dias_validade)) if dias_validade else None
            PEI.objects.create(
                estudante=estudante,
                status=PEI.Status.VIGENTE if data_validade else PEI.Status.RASCUNHO,
                data_elaboracao=hoje - datetime.timedelta(days=60),
                data_validade=data_validade,
                responsavel_elaboracao=coordenadora,
                objetivos_gerais='Garantir acesso pleno ao currículo com as adaptações necessárias.',
            )
            self.stdout.write(self.style.SUCCESS(f'Estudante "{estudante.nome_completo}" criado.'))

        self.stdout.write(self.style.SUCCESS('Dados de demonstração prontos.'))
