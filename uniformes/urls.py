from django.urls import path

from . import views

app_name = 'uniformes'

urlpatterns = [
    path('', views.lista_uniformes, name='lista'),
    path('<int:pk>/atualizar/', views.atualizar_uniforme, name='atualizar'),
    path('<int:pk>/excluir/', views.excluir_uniforme, name='excluir'),
]
