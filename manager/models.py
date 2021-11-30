from django.db import models
from users.models import EstudanteProfile, ProfessorProfile, CoordenadorProfile
from django.urls import reverse


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500)
    coordenador = models.ForeignKey(CoordenadorProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('curso-detail', kwargs={'pk': self.pk})

class Turno(models.Model):
    nome = models.CharField(max_length=50)
    inicio = models.TimeField(auto_now=False, auto_now_add=False)
    fim = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('gerenciarDisciplina', kwargs={'pk': self.curso.id})

class Dia_semana(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Aula(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True)
    dia_semana = models.ForeignKey(Dia_semana, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.disciplina.nome

    def get_absolute_url(self):
        return reverse('gerenciarAula', kwargs={'pk': self.disciplina.curso.id})

class Presenca(models.Model):
    estudante = models.ForeignKey(EstudanteProfile, on_delete=models.CASCADE, null=True)
    data = models.DateField()
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, null=True)

    def __str__(self):
        presenca = str(self.estudante)+" | "+str(self.aula)+" | "+str(self.data)+" | "+str(self.aula.turno)
        return presenca

class Professor_curso(models.Model):
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, null=True) 
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.curso)  

class Estudante_disciplina(models.Model):
    estudante = models.ForeignKey(EstudanteProfile, on_delete=models.CASCADE, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.disciplina) 