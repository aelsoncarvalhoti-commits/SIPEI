from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario


TEXT_WIDGET = forms.TextInput(attrs={'class': 'form-control'})


class UsuarioCreateForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'perfil', 'registro', 'campus', 'telefone',
        ]
        widgets = {
            'username': TEXT_WIDGET,
            'first_name': TEXT_WIDGET,
            'last_name': TEXT_WIDGET,
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'registro': TEXT_WIDGET,
            'campus': TEXT_WIDGET,
            'telefone': TEXT_WIDGET,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UsuarioUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email',
            'perfil', 'registro', 'campus', 'telefone', 'ativo',
        ]
        widgets = {
            'first_name': TEXT_WIDGET,
            'last_name': TEXT_WIDGET,
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'registro': TEXT_WIDGET,
            'campus': TEXT_WIDGET,
            'telefone': TEXT_WIDGET,
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
