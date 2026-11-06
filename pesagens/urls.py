from django.urls import path

from . import views

app_name = 'pesagens'

urlpatterns = [
    path('', views.lista_pesagens, name='lista'),
    path('pesagens/<int:pk>/editar/', views.editar_pesagem, name='editar'),
    path('pesagens/<int:pk>/excluir/', views.excluir_pesagem, name='excluir'),
]
