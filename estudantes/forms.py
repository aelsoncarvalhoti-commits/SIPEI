from django import forms

from .models import (
    Acompanhamento, Adaptacao, ComponenteCurricular, Diagnostico, Estudante,
    PerfilAprendizagem, PlanejamentoPedagogico,
)

INPUT = 'form-control'


class EstudanteForm(forms.ModelForm):
    class Meta:
        model = Estudante
        fields = [
            'nome_completo', 'data_nascimento', 'matricula', 'curso', 'turma', 'campus',
            'telefone', 'email', 'responsavel_nome', 'responsavel_telefone', 'foto',
            'necessidade_especifica', 'descricao_necessidade', 'professor_responsavel', 'ativo',
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': INPUT}),
            'data_nascimento': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'matricula': forms.TextInput(attrs={'class': INPUT}),
            'curso': forms.TextInput(attrs={'class': INPUT}),
            'turma': forms.TextInput(attrs={'class': INPUT}),
            'campus': forms.TextInput(attrs={'class': INPUT}),
            'telefone': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
            'responsavel_nome': forms.TextInput(attrs={'class': INPUT}),
            'responsavel_telefone': forms.TextInput(attrs={'class': INPUT}),
            'foto': forms.ClearableFileInput(attrs={'class': INPUT}),
            'necessidade_especifica': forms.Select(attrs={'class': INPUT}),
            'descricao_necessidade': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
            'professor_responsavel': forms.Select(attrs={'class': INPUT}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import Usuario
        self.fields['professor_responsavel'].queryset = Usuario.objects.filter(
            perfil=Usuario.Perfil.PROFESSOR, ativo=True,
        )
        self.fields['professor_responsavel'].required = False
        self.fields['professor_responsavel'].empty_label = 'Não atribuído'


class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['cid', 'data_diagnostico', 'profissional_responsavel', 'descricao', 'observacoes', 'laudo_medico']
        widgets = {
            'cid': forms.TextInput(attrs={'class': INPUT}),
            'data_diagnostico': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'profissional_responsavel': forms.TextInput(attrs={'class': INPUT}),
            'descricao': forms.Textarea(attrs={'class': INPUT, 'rows': 4}),
            'observacoes': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
            'laudo_medico': forms.ClearableFileInput(attrs={'class': INPUT}),
        }


class PerfilAprendizagemForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendizagem
        fields = ['pontos_fortes', 'dificuldades', 'estilo_aprendizagem', 'interesses', 'observacoes']
        widgets = {f: forms.Textarea(attrs={'class': INPUT, 'rows': 3}) for f in fields}


class AdaptacaoForm(forms.ModelForm):
    class Meta:
        model = Adaptacao
        fields = ['tipo', 'disciplina', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={'class': INPUT}),
            'disciplina': forms.TextInput(attrs={'class': INPUT}),
            'descricao': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
        }


class ComponenteCurricularForm(forms.ModelForm):
    class Meta:
        model = ComponenteCurricular
        fields = ['disciplina', 'professor', 'carga_horaria', 'adaptacoes_necessarias']
        widgets = {
            'disciplina': forms.TextInput(attrs={'class': INPUT}),
            'professor': forms.Select(attrs={'class': INPUT}),
            'carga_horaria': forms.NumberInput(attrs={'class': INPUT}),
            'adaptacoes_necessarias': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import Usuario
        self.fields['professor'].queryset = Usuario.objects.filter(
            perfil=Usuario.Perfil.PROFESSOR, ativo=True,
        )
        self.fields['professor'].required = False
        self.fields['professor'].empty_label = 'Não atribuído'


class PlanejamentoForm(forms.ModelForm):
    class Meta:
        model = PlanejamentoPedagogico
        fields = ['disciplina', 'objetivo', 'estrategia', 'meta', 'prazo', 'status']
        widgets = {
            'disciplina': forms.TextInput(attrs={'class': INPUT}),
            'objetivo': forms.Textarea(attrs={'class': INPUT, 'rows': 2}),
            'estrategia': forms.Textarea(attrs={'class': INPUT, 'rows': 2}),
            'meta': forms.Textarea(attrs={'class': INPUT, 'rows': 2}),
            'prazo': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': INPUT}),
        }


class AcompanhamentoForm(forms.ModelForm):
    class Meta:
        model = Acompanhamento
        fields = ['data', 'observacao', 'estrategias_aplicadas', 'adaptacoes_realizadas']
        widgets = {
            'data': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'observacao': forms.Textarea(attrs={'class': INPUT, 'rows': 4}),
            'estrategias_aplicadas': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
            'adaptacoes_realizadas': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
        }
