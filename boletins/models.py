from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from turmas.models import AnoLetivo, Disciplina, Etapa, Turma

'''
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
'''
   
class Aluno(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)
    email = models.EmailField()
    matricula = models.CharField(max_length=10, primary_key=True)
    turma = models.ManyToManyField(Turma, related_name="alunos")

    def __str__(self) -> str:
        return self.nome

class Boletim(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    ano_letivo = models.ForeignKey(AnoLetivo, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.aluno}, {self.ano_letivo}'

class BoletimDisciplina(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    boletim = models.ForeignKey(Boletim, on_delete=models.PROTECT)
    etapas = models.ManyToManyField(Etapa, through='NotaEtapa')

    class Meta:
        ordering = ['boletim']
        unique_together = ['disciplina', 'boletim']

    def __str__(self):
        return f'{self.disciplina}'
    
class NotaEtapa(models.Model):
    boletim_disciplina = models.ForeignKey(BoletimDisciplina, on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE)
    nota1 = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    nota2 = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)])
    extra = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(3)])

    falta = models.IntegerField()

    media_faltas = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    media_notas = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def calcular_media_notas(self):
        if self.nota1 is not None and self.nota2 is not None:
            self.media_notas =  (self.nota1 + self.nota2 + self.extra) / 2
        else:
            self.media_notas = None
        self.save()

    def calcular_media_notas(self):
        # Calcula a média do bimestre baseada nas notas 
        if self.nota1 is not None and self.nota2 is not None:
            self.media_notas =  (self.nota1 + self.nota2 + self.extra) / 2
        else:
            self.media_notas =None 
        self.save()
        
    def calcular_media_final(self):
        # Calcula a média final baseada na média dos bimestres
        if all(getattr(self, f'bim{i}') is not None for i in range(1, 5)):
            return (self.bim1 + self.bim2 + self.bim3 + self.bim4) / 4
        else:
            return None
        
    def __str__(self):
        return f'{self.boletim_disciplina} - {self.etapa}'
    




    