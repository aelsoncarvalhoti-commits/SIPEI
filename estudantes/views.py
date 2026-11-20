from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import coordenacao_required
from .forms import (
    AcompanhamentoForm, AdaptacaoForm, ComponenteCurricularForm, DiagnosticoForm,
    EstudanteForm, PerfilAprendizagemForm, PlanejamentoForm,
)
from .models import (
    Acompanhamento, Adaptacao, ComponenteCurricular, Diagnostico, Estudante,
    PerfilAprendizagem, PlanejamentoPedagogico,
)


def _visible_estudantes(user):
    qs = Estudante.objects.all()
    if user.is_coordenacao:
        return qs
    return qs.filter(professor_responsavel=user)


@login_required
def estudante_list(request):
    estudantes = _visible_estudantes(request.user)
    necessidade = request.GET.get('necessidade')
    if necessidade:
        estudantes = estudantes.filter(necessidade_especifica=necessidade)
    busca = request.GET.get('q')
    if busca:
        estudantes = estudantes.filter(nome_completo__icontains=busca)
    status = request.GET.get('status', 'ativos')
    if status == 'ativos':
        estudantes = estudantes.filter(ativo=True)
    elif status == 'inativos':
        estudantes = estudantes.filter(ativo=False)
    return render(request, 'estudantes/estudante_list.html', {
        'estudantes': estudantes.select_related('pei'),
        'necessidades': Estudante.Necessidade.choices,
        'filtro_necessidade': necessidade or '',
        'filtro_status': status,
        'busca': busca or '',
    })


@coordenacao_required
def estudante_create(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES)
        if form.is_valid():
            estudante = form.save(commit=False)
            estudante.criado_por = request.user
            estudante.ativo = True
            estudante.save()
            messages.success(request, f'Estudante "{estudante.nome_completo}" cadastrado com sucesso.')
            return redirect('estudantes:detail', pk=estudante.pk)
    else:
        form = EstudanteForm()
    return render(request, 'estudantes/estudante_form.html', {'form': form, 'novo': True})


@coordenacao_required
def estudante_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES, instance=estudante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do estudante atualizados.')
            return redirect('estudantes:detail', pk=estudante.pk)
    else:
        form = EstudanteForm(instance=estudante)
    return render(request, 'estudantes/estudante_form.html', {'form': form, 'novo': False, 'estudante': estudante})


TABS = ['identificacao', 'diagnostico', 'perfil', 'adaptacoes', 'componentes', 'planejamentos', 'acompanhamentos']


@login_required
def estudante_detail(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if not request.user.is_coordenacao and estudante.professor_responsavel_id != request.user.id:
        messages.error(request, 'Você não tem acesso a este estudante.')
        return redirect('estudantes:list')

    tab = request.GET.get('tab', 'identificacao')
    if tab not in TABS:
        tab = 'identificacao'

    diagnostico = getattr(estudante, 'diagnostico', None)
    perfil_aprendizagem = getattr(estudante, 'perfil_aprendizagem', None)
    pei = getattr(estudante, 'pei', None)

    return render(request, 'estudantes/estudante_detail.html', {
        'estudante': estudante,
        'tab': tab,
        'diagnostico': diagnostico,
        'perfil_aprendizagem': perfil_aprendizagem,
        'pei': pei,
        'adaptacoes': estudante.adaptacoes.all(),
        'componentes': estudante.componentes.all(),
        'planejamentos': estudante.planejamentos.all(),
        'acompanhamentos': estudante.acompanhamentos.all()[:20],
    })


@coordenacao_required
def diagnostico_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    instance = getattr(estudante, 'diagnostico', None)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.estudante = estudante
            diagnostico.save()
            messages.success(request, 'Diagnóstico atualizado.')
            return redirect(f"/estudantes/{pk}/?tab=diagnostico")
    else:
        form = DiagnosticoForm(instance=instance)
    return render(request, 'estudantes/subform.html', {
        'form': form, 'estudante': estudante, 'titulo': 'Diagnóstico', 'tab': 'diagnostico',
    })


@coordenacao_required
def perfil_aprendizagem_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    instance = getattr(estudante, 'perfil_aprendizagem', None)
    if request.method == 'POST':
        form = PerfilAprendizagemForm(request.POST, instance=instance)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.estudante = estudante
            perfil.save()
            messages.success(request, 'Perfil de aprendizagem atualizado.')
            return redirect(f"/estudantes/{pk}/?tab=perfil")
    else:
        form = PerfilAprendizagemForm(instance=instance)
    return render(request, 'estudantes/subform.html', {
        'form': form, 'estudante': estudante, 'titulo': 'Perfil de aprendizagem', 'tab': 'perfil',
    })


def _crud_filho(request, pk, model, form_class, campo_pk, titulo, tab, template='estudantes/subform.html'):
    estudante = get_object_or_404(Estudante, pk=pk)
    instance = get_object_or_404(model, pk=campo_pk, estudante=estudante) if campo_pk else None
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.estudante = estudante
            if hasattr(obj, 'criado_por') and not obj.pk:
                obj.criado_por = request.user
            obj.save()
            messages.success(request, f'{titulo} salvo(a) com sucesso.')
            return redirect(f"/estudantes/{pk}/?tab={tab}")
    else:
        form = form_class(instance=instance)
    return render(request, template, {'form': form, 'estudante': estudante, 'titulo': titulo, 'tab': tab})


@coordenacao_required
def adaptacao_create(request, pk):
    return _crud_filho(request, pk, Adaptacao, AdaptacaoForm, None, 'Adaptação', 'adaptacoes')


@coordenacao_required
def adaptacao_update(request, pk, filho_pk):
    return _crud_filho(request, pk, Adaptacao, AdaptacaoForm, filho_pk, 'Adaptação', 'adaptacoes')


@coordenacao_required
def adaptacao_delete(request, pk, filho_pk):
    get_object_or_404(Adaptacao, pk=filho_pk, estudante_id=pk).delete()
    messages.success(request, 'Adaptação removida.')
    return redirect(f"/estudantes/{pk}/?tab=adaptacoes")


@coordenacao_required
def componente_create(request, pk):
    return _crud_filho(request, pk, ComponenteCurricular, ComponenteCurricularForm, None, 'Componente curricular', 'componentes')


@coordenacao_required
def componente_update(request, pk, filho_pk):
    return _crud_filho(request, pk, ComponenteCurricular, ComponenteCurricularForm, filho_pk, 'Componente curricular', 'componentes')


@coordenacao_required
def componente_delete(request, pk, filho_pk):
    get_object_or_404(ComponenteCurricular, pk=filho_pk, estudante_id=pk).delete()
    messages.success(request, 'Componente curricular removido.')
    return redirect(f"/estudantes/{pk}/?tab=componentes")


@coordenacao_required
def planejamento_create(request, pk):
    return _crud_filho(request, pk, PlanejamentoPedagogico, PlanejamentoForm, None, 'Planejamento pedagógico', 'planejamentos')


@coordenacao_required
def planejamento_update(request, pk, filho_pk):
    return _crud_filho(request, pk, PlanejamentoPedagogico, PlanejamentoForm, filho_pk, 'Planejamento pedagógico', 'planejamentos')


@coordenacao_required
def planejamento_delete(request, pk, filho_pk):
    get_object_or_404(PlanejamentoPedagogico, pk=filho_pk, estudante_id=pk).delete()
    messages.success(request, 'Planejamento removido.')
    return redirect(f"/estudantes/{pk}/?tab=planejamentos")


@login_required
def acompanhamento_create(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if not request.user.is_coordenacao and estudante.professor_responsavel_id != request.user.id:
        messages.error(request, 'Você não tem acesso a este estudante.')
        return redirect('estudantes:list')
    if request.method == 'POST':
        form = AcompanhamentoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.estudante = estudante
            registro.professor = request.user
            registro.save()
            messages.success(request, 'Registro de acompanhamento salvo com sucesso.')
            return redirect(f"/estudantes/{pk}/?tab=acompanhamentos")
    else:
        form = AcompanhamentoForm(initial={'data': timezone.localdate()})
    return render(request, 'estudantes/acompanhamento_form.html', {'form': form, 'estudante': estudante})


@login_required
def acompanhamento_historico(request):
    registros = Acompanhamento.objects.select_related('estudante', 'professor')
    if not request.user.is_coordenacao:
        registros = registros.filter(professor=request.user)
    estudante_id = request.GET.get('estudante')
    if estudante_id:
        registros = registros.filter(estudante_id=estudante_id)
    return render(request, 'estudantes/acompanhamento_historico.html', {
        'registros': registros,
        'estudantes': _visible_estudantes(request.user),
    })
