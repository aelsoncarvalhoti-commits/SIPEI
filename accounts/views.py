from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import coordenacao_required
from .forms import UsuarioCreateForm, UsuarioUpdateForm
from .models import Usuario


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha inválidos.')
        return super().form_invalid(form)


class LogoutView(auth_views.LogoutView):
    next_page = 'accounts:login'


@coordenacao_required
def usuario_list(request):
    usuarios = Usuario.objects.all()
    perfil = request.GET.get('perfil')
    if perfil:
        usuarios = usuarios.filter(perfil=perfil)
    busca = request.GET.get('q')
    if busca:
        usuarios = usuarios.filter(first_name__icontains=busca) | usuarios.filter(
            last_name__icontains=busca) | usuarios.filter(username__icontains=busca)
    usuarios = list(usuarios)
    return render(request, 'accounts/usuario_list.html', {
        'usuarios': usuarios,
        'perfis': Usuario.Perfil.choices,
        'total_usuarios': len(usuarios),
    })


@coordenacao_required
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuário "{usuario}" cadastrado com sucesso.')
            return redirect('accounts:usuario_list')
    else:
        form = UsuarioCreateForm()
    return render(request, 'accounts/usuario_form.html', {'form': form, 'novo': True})


@coordenacao_required
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário "{usuario}" atualizado com sucesso.')
            return redirect('accounts:usuario_list')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'accounts/usuario_form.html', {'form': form, 'novo': False, 'usuario_obj': usuario})


@coordenacao_required
def usuario_toggle_ativo(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.ativo = not usuario.ativo
        usuario.is_active = usuario.ativo
        usuario.save(update_fields=['ativo', 'is_active'])
        estado = 'ativado' if usuario.ativo else 'desativado'
        messages.success(request, f'Usuário "{usuario}" {estado}.')
    return redirect('accounts:usuario_list')


@login_required
def perfil(request):
    return render(request, 'accounts/perfil.html')
