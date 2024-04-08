from django.urls import path
from . import views

urlpatterns = [
    path('listar_turma/', views.listar_turma, name ="listar_turma"),
]