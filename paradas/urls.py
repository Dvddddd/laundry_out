from django.urls import path
from . import views

app_name = 'paradas'

urlpatterns = [
    path('paradas/', views.lista_paradas, name='lista'),
    path('paradas/<int:pk>/retorno/', views.registrar_retorno, name='retorno'),
    path('paradas/<int:pk>/excluir/', views.excluir_parada, name='excluir'),
]
