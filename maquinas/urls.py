from django.urls import path

from . import views

app_name = 'maquinas'

urlpatterns = [
    path('', views.lista_maquinas, name='lista'),
    path('maquinas/<int:pk>/atualizar/', views.atualizar_maquina, name='atualizar'),
    path('maquinas/<int:pk>/excluir/', views.excluir_maquina, name='excluir'),
]
