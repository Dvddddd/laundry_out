from django.urls import path

from . import views

app_name = 'contas'

urlpatterns = [
    path('entrar/', views.EntrarView.as_view(), name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/<int:pk>/editar/', views.editar_usuario, name='editar'),
    path('cadastro/<int:pk>/excluir/', views.excluir_usuario, name='excluir'),
    path('sair/', views.sair, name='logout'),
]
