from django.urls import path
from . import views

urlpatterns = [
    path('', views.boletim_disciplina_lista , name ="boletim-disciplina"),
]