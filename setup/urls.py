import django
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("usuarios.urls")),
    path("boletins/", include("boletins.urls")),
    path("turmas/", include("turmas.urls"))
    #path("boletins/", boletim_disciplina_lista, name='boletim_lista'),
]


