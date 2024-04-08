from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.http import HttpRequest

from .models import Aluno, Boletim 
from .models import BoletimDisciplina, NotaEtapa

admin.site.register(Aluno)
 

class NotaEtapaInline(admin.TabularInline):
    model = NotaEtapa
    extra = 0

class BoletimDisciplinaAdmin(admin.ModelAdmin):
    inlines = [NotaEtapaInline] 
 
admin.site.register(Boletim)
admin.site.register(BoletimDisciplina, BoletimDisciplinaAdmin)

