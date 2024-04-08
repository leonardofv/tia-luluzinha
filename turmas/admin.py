from django.contrib import admin

from turmas.models import AnoLetivo, Curso, Disciplina, Etapa, Professor, Serie, Turma, Turno


class EtapaInline(admin.TabularInline):
    model = Etapa
    extra = 0

class AnoLetivoAdmin(admin.ModelAdmin):
    inlines = [EtapaInline]

class ProfessorDisciplinaInline(admin.TabularInline):
    model = Professor.disciplinas.through
    extra = 1

class ProfessorAdmin(admin.ModelAdmin):
    inlines = (ProfessorDisciplinaInline,)  


admin.site.register(AnoLetivo, AnoLetivoAdmin)
admin.site.register(Etapa)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma) 
admin.site.register(Disciplina)
admin.site.register(Curso)
admin.site.register(Serie)
admin.site.register(Turno)
