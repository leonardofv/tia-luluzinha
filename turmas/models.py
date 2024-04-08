from datetime import datetime
from django.db import models

class AnoLetivo(models.Model):

    TIPOS_ETAPA = [
        ('BIM', 'Bimestre'),
        ('SEM', 'Semestre'),
        ]
    
    id = models.AutoField(primary_key=True)
    ano = models.IntegerField(null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_ETAPA, verbose_name='etapas', null=True)

    def __str__(self):
        return f"Ano Letivo {self.ano} - {self.get_tipo_display()}"
    
class Etapa(models.Model):
    ano_letivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE, related_name='etapas')
    numero = models.PositiveIntegerField(verbose_name='Etapa')
    data_inicio = models.DateField(verbose_name='Data de Início', default=datetime.now)
    data_termino = models.DateField(verbose_name='Data de Término', default=datetime.now) 

    class Meta:
        unique_together = ['ano_letivo', 'numero']  

    def __str__(self) -> str:
        return f"{self.ano_letivo} - {self.numero}"

class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=10, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.nome
    
class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.nome
    
class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=10, null=False, blank=False, unique=True)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20, null=False, blank=False)
    carga_horaria = models.IntegerField(null=False, blank=False)
    series= models.ManyToManyField(Serie, related_name="disciplinas")

    def __str__(self) -> str:
        return self.nome
    
class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    disciplinas = models.ManyToManyField(Disciplina, through='ProfessorDisciplina', related_name='professores')

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self) -> str:
        return self.nome
    
class ProfessorDisciplina(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ['professor', 'disciplina']

    def __str__(self) -> str:
        return f'{self.professor} - {self.disciplina}'
    
class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=10, null=False, blank=False, unique=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    anoLetivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    vagas = models.IntegerField(null=False, blank=False)
    professores_disciplinas = models.ManyToManyField(ProfessorDisciplina, related_name='turmas')
    # Define se a turma já finalizou o ano letivo ou se ainda está em andamento.
    status= models.BooleanField(default=False) 

    def __str__(self) -> str:
        return self.nome