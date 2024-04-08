from django.shortcuts import render

from boletins.models import Boletim, BoletimDisciplina

def boletim_disciplina_lista(request):
    boletim_disciplina = BoletimDisciplina.objects.all()
    return render(request, 'boletins/boletim_lista.html', {'boletim_disciplina': boletim_disciplina})




