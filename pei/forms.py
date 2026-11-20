from django import forms

from .models import PEI

INPUT = 'form-control'


class PEIForm(forms.ModelForm):
    class Meta:
        model = PEI
        fields = ['status', 'data_elaboracao', 'data_validade', 'objetivos_gerais', 'observacoes_gerais']
        widgets = {
            'status': forms.Select(attrs={'class': INPUT}),
            'data_elaboracao': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'data_validade': forms.DateInput(attrs={'class': INPUT, 'type': 'date'}, format='%Y-%m-%d'),
            'objetivos_gerais': forms.Textarea(attrs={'class': INPUT, 'rows': 4}),
            'observacoes_gerais': forms.Textarea(attrs={'class': INPUT, 'rows': 4}),
        }
