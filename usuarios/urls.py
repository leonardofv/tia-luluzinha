from django.urls import path
from . import views

urlpatterns = [
    path("docentes/", views.login, name="login"),
    path("docentes/cadastro", views.cadastro, name="cadastro"),
    path("alunos/", views.login, name="login"),
    path("alunos/cadastro", views.cadastro, name="cadastro"),
]