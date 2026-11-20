from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone

from accounts.decorators import coordenacao_required
from estudantes.models import Acompanhamento, Estudante
from pei.models import PEI
from django.shortcuts import render

CORES_GRAFICO = ['#227a45', '#7c6fe0', '#f2b705', '#3b82c4', '#d1453b', '#a2ada7', '#14432b']


def _build_pie(itens):
    """Recebe lista de dicts com 'total' e devolve com 'cor' e um CSS conic-gradient pronto."""
    total_geral = sum(i['total'] for i in itens) or 1
    partes = []
    acumulado = 0
    for i, item in enumerate(itens):
        cor = CORES_GRAFICO[i % len(CORES_GRAFICO)]
        item['cor'] = cor
        item['percentual'] = round(item['total'] * 100 / total_geral)
        fatia = item['total'] * 100 / total_geral
        inicio = acumulado
        acumulado += fatia
        partes.append(f"{cor} {inicio:.2f}% {acumulado:.2f}%")
    gradiente = 'conic-gradient(' + ', '.join(partes) + ')' if partes else '#e3e9e5'
    return itens, gradiente


@login_required
def home(request):
    if request.user.is_coordenacao:
        return _home_coordenacao(request)
    return _home_professor(request)


def _home_coordenacao(request):
    estudantes = Estudante.objects.filter(ativo=True)
    total_estudantes = estudantes.count()

    por_necessidade = list(
        estudantes.values('necessidade_especifica').annotate(total=Count('id')).order_by('-total')
    )
    necessidade_labels = dict(Estudante.Necessidade.choices)
    for item in por_necessidade:
        item['label'] = necessidade_labels.get(item['necessidade_especifica'], item['necessidade_especifica'])
    por_necessidade, grafico_css = _build_pie(por_necessidade)

    hoje = timezone.localdate()
    limite = hoje + timezone.timedelta(days=30)
    peis_vencendo = PEI.objects.select_related('estudante').filter(
        data_validade__isnull=False, data_validade__gte=hoje, data_validade__lte=limite,
    ).order_by('data_validade')[:6]

    total_peis_ativos = PEI.objects.filter(status=PEI.Status.VIGENTE).count()
    total_pendentes_revisao = PEI.objects.filter(
        status__in=[PEI.Status.RASCUNHO, PEI.Status.EM_ELABORACAO],
    ).count()
    total_concluidos = PEI.objects.filter(status=PEI.Status.CONCLUIDO).count()

    return render(request, 'dashboard/home_coordenacao.html', {
        'total_estudantes': total_estudantes,
        'por_necessidade': por_necessidade,
        'grafico_css': grafico_css,
        'peis_vencendo': peis_vencendo,
        'total_peis_ativos': total_peis_ativos,
        'total_pendentes_revisao': total_pendentes_revisao,
        'total_concluidos': total_concluidos,
    })


def _home_professor(request):
    estudantes = Estudante.objects.filter(professor_responsavel=request.user, ativo=True)
    hoje = timezone.localdate()
    limite = hoje + timezone.timedelta(days=30)
    peis_vencendo = PEI.objects.select_related('estudante').filter(
        estudante__professor_responsavel=request.user,
        data_validade__isnull=False, data_validade__gte=hoje, data_validade__lte=limite,
    ).order_by('data_validade')[:6]
    ultimos_acompanhamentos = Acompanhamento.objects.select_related('estudante').filter(
        professor=request.user,
    ).order_by('-data')[:6]

    return render(request, 'dashboard/home_professor.html', {
        'estudantes': estudantes,
        'total_estudantes': estudantes.count(),
        'peis_vencendo': peis_vencendo,
        'ultimos_acompanhamentos': ultimos_acompanhamentos,
    })


@login_required
def ajuda(request):
    return render(request, 'dashboard/ajuda.html')


@coordenacao_required
def relatorios(request):
    estudantes = Estudante.objects.filter(ativo=True)
    por_necessidade = list(
        estudantes.values('necessidade_especifica').annotate(total=Count('id')).order_by('-total')
    )
    necessidade_labels = dict(Estudante.Necessidade.choices)
    for item in por_necessidade:
        item['label'] = necessidade_labels.get(item['necessidade_especifica'], item['necessidade_especifica'])
    por_necessidade, grafico_necessidade_css = _build_pie(por_necessidade)

    por_status_pei = list(PEI.objects.values('status').annotate(total=Count('id')).order_by('-total'))
    status_labels = dict(PEI.Status.choices)
    for item in por_status_pei:
        item['label'] = status_labels.get(item['status'], item['status'])
    por_status_pei, grafico_status_css = _build_pie(por_status_pei)

    por_campus = list(estudantes.values('campus').annotate(total=Count('id')).order_by('-total'))
    por_professor = list(
        estudantes.exclude(professor_responsavel__isnull=True)
        .values('professor_responsavel__first_name', 'professor_responsavel__last_name')
        .annotate(total=Count('id')).order_by('-total')
    )

    return render(request, 'dashboard/relatorios.html', {
        'total_estudantes': estudantes.count(),
        'total_com_pei': estudantes.filter(pei__isnull=False).count(),
        'total_sem_pei': estudantes.filter(pei__isnull=True).count(),
        'por_necessidade': por_necessidade,
        'grafico_necessidade_css': grafico_necessidade_css,
        'por_status_pei': por_status_pei,
        'grafico_status_css': grafico_status_css,
        'por_campus': por_campus,
        'por_professor': por_professor,
    })
