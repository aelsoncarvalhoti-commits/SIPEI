from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('ajuda/', views.ajuda, name='ajuda'),
    path('relatorios/', views.relatorios, name='relatorios'),
]
