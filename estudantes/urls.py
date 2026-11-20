from django.urls import path

from . import views

app_name = 'estudantes'

urlpatterns = [
    path('', views.estudante_list, name='list'),
    path('novo/', views.estudante_create, name='create'),
    path('<int:pk>/', views.estudante_detail, name='detail'),
    path('<int:pk>/editar/', views.estudante_update, name='update'),

    path('<int:pk>/diagnostico/', views.diagnostico_update, name='diagnostico_update'),
    path('<int:pk>/perfil-aprendizagem/', views.perfil_aprendizagem_update, name='perfil_update'),

    path('<int:pk>/adaptacoes/nova/', views.adaptacao_create, name='adaptacao_create'),
    path('<int:pk>/adaptacoes/<int:filho_pk>/editar/', views.adaptacao_update, name='adaptacao_update'),
    path('<int:pk>/adaptacoes/<int:filho_pk>/excluir/', views.adaptacao_delete, name='adaptacao_delete'),

    path('<int:pk>/componentes/novo/', views.componente_create, name='componente_create'),
    path('<int:pk>/componentes/<int:filho_pk>/editar/', views.componente_update, name='componente_update'),
    path('<int:pk>/componentes/<int:filho_pk>/excluir/', views.componente_delete, name='componente_delete'),

    path('<int:pk>/planejamentos/novo/', views.planejamento_create, name='planejamento_create'),
    path('<int:pk>/planejamentos/<int:filho_pk>/editar/', views.planejamento_update, name='planejamento_update'),
    path('<int:pk>/planejamentos/<int:filho_pk>/excluir/', views.planejamento_delete, name='planejamento_delete'),

    path('<int:pk>/acompanhamentos/novo/', views.acompanhamento_create, name='acompanhamento_create'),
    path('acompanhamentos/historico/', views.acompanhamento_historico, name='acompanhamento_historico'),
]
