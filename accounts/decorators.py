from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def coordenacao_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_coordenacao:
            messages.error(request, 'Acesso restrito à Coordenação CAPNE/AEE.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return _wrapped
