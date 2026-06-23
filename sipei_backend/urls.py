from django.urls import path
from .views.public_views import *

urlpatterns = [
    path('', paginaInicial, name="paginainicial")
]