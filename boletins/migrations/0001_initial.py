# Generated by Django 4.1 on 2024-04-07 20:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("turmas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aluno",
            fields=[
                ("nome", models.CharField(max_length=100)),
                ("cpf", models.CharField(max_length=11, unique=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "matricula",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                (
                    "turma",
                    models.ManyToManyField(related_name="alunos", to="turmas.turma"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Boletim",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="boletins.aluno"
                    ),
                ),
                (
                    "ano_letivo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="turmas.anoletivo",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BoletimDisciplina",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "boletim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="boletins.boletim",
                    ),
                ),
                (
                    "disciplina",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="turmas.disciplina",
                    ),
                ),
            ],
            options={
                "ordering": ["boletim"],
            },
        ),
        migrations.CreateModel(
            name="NotaEtapa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nota1",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "nota2",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "extra",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(3),
                        ],
                    ),
                ),
                ("falta", models.IntegerField()),
                (
                    "media_faltas",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=3, null=True
                    ),
                ),
                (
                    "media_notas",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "boletim_disciplina",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="boletins.boletimdisciplina",
                    ),
                ),
                (
                    "etapa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="turmas.etapa"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="boletimdisciplina",
            name="etapas",
            field=models.ManyToManyField(
                through="boletins.NotaEtapa", to="turmas.etapa"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="boletimdisciplina",
            unique_together={("disciplina", "boletim")},
        ),
    ]
