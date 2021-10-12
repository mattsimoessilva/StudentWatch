from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    senha = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.nome

class ProfessorCurso(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.DO_NOTHING)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

class Estudante(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    periodo = models.CharField(max_length=6)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
    professor = models.ForeignKey(Professor, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome

class DisciplinaEstudante(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.DO_NOTHING)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.DO_NOTHING)

class Coordenador(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome

