from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from accounts.decorators import coordenacao_required
from estudantes.models import Estudante

from .forms import PEIForm
from .models import PEI


def _pode_acessar(request, estudante):
    return request.user.is_coordenacao or estudante.professor_responsavel_id == request.user.id


@login_required
def pei_list(request):
    peis = PEI.objects.select_related('estudante', 'responsavel_elaboracao')
    if not request.user.is_coordenacao:
        peis = peis.filter(estudante__professor_responsavel=request.user)
    status = request.GET.get('status')
    if status:
        peis = peis.filter(status=status)
    busca = request.GET.get('q')
    if busca:
        peis = peis.filter(estudante__nome_completo__icontains=busca)
    return render(request, 'pei/pei_list.html', {
        'peis': peis,
        'status_choices': PEI.Status.choices,
        'filtro_status': status or '',
        'busca': busca or '',
    })


@login_required
def pei_detail(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if not _pode_acessar(request, estudante):
        messages.error(request, 'Você não tem acesso a este estudante.')
        return redirect('estudantes:list')
    pei = getattr(estudante, 'pei', None)
    return render(request, 'pei/pei_detail.html', {
        'estudante': estudante,
        'pei': pei,
        'diagnostico': getattr(estudante, 'diagnostico', None),
        'perfil_aprendizagem': getattr(estudante, 'perfil_aprendizagem', None),
        'adaptacoes': estudante.adaptacoes.all(),
        'planejamentos': estudante.planejamentos.all(),
    })


@coordenacao_required
def pei_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    instance = getattr(estudante, 'pei', None)
    if request.method == 'POST':
        form = PEIForm(request.POST, instance=instance)
        if form.is_valid():
            pei = form.save(commit=False)
            pei.estudante = estudante
            if not pei.responsavel_elaboracao_id:
                pei.responsavel_elaboracao = request.user
            pei.save()
            messages.success(request, 'PEI salvo com sucesso.')
            return redirect('pei:detail', pk=pk)
    else:
        form = PEIForm(instance=instance)
    return render(request, 'pei/pei_form.html', {'form': form, 'estudante': estudante, 'novo': instance is None})


@login_required
def pei_pdf(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    if not _pode_acessar(request, estudante):
        messages.error(request, 'Você não tem acesso a este estudante.')
        return redirect('estudantes:list')
    pei = getattr(estudante, 'pei', None)
    if pei is None:
        messages.error(request, 'Este estudante ainda não possui um PEI elaborado.')
        return redirect('estudantes:detail', pk=pk)

    from xhtml2pdf import pisa

    html = render_to_string('pei/pei_pdf.html', {
        'estudante': estudante,
        'pei': pei,
        'diagnostico': getattr(estudante, 'diagnostico', None),
        'perfil_aprendizagem': getattr(estudante, 'perfil_aprendizagem', None),
        'adaptacoes': estudante.adaptacoes.all(),
        'componentes': estudante.componentes.all(),
        'planejamentos': estudante.planejamentos.all(),
    })

    response = HttpResponse(content_type='application/pdf')
    nome_arquivo = f"PEI_{estudante.nome_completo.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{nome_arquivo}"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF do PEI.', status=500)
    return response
