from django.shortcuts import render

from turmas.models import Turma

def listar_turma(request):
    if request.method == "GET":
        turmas = Turma.objects.all()
        return render(request, "listar_turma.html", {'turmas': turmas})
