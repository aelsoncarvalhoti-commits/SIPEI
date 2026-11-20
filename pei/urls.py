from django.urls import path

from . import views

app_name = 'pei'

urlpatterns = [
    path('', views.pei_list, name='list'),
    path('<int:pk>/', views.pei_detail, name='detail'),
    path('<int:pk>/editar/', views.pei_update, name='update'),
    path('<int:pk>/pdf/', views.pei_pdf, name='pdf'),
]
