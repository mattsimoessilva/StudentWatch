from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


#CUSTOM USER MODEL
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    tipo = models.CharField(max_length=100)


#USER PROFILES
class CoordenadorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='coordenador_profile')
    campoextra = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='professor_profile')
    campoextra = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


#SOME CLASSES
class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500)
    coordenador = models.ForeignKey(CoordenadorProfile, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.nome

class Turno(models.Model):
    nome = models.CharField(max_length=50)
    inicio = models.TimeField(auto_now=False, auto_now_add=False)
    fim = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.DO_NOTHING, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('disciplina-detail', kwargs={'pk': self.pk})

class Dia_semana(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Aula(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.DO_NOTHING, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.DO_NOTHING, null=True)
    dia_semana = models.ForeignKey(Dia_semana, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.disciplina.nome


#USER PROFILE
class EstudanteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='estudante_profile')
    matricula = models.CharField(max_length=20, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.user.username

#MORE CLASSES
class Presenca(models.Model):
    estudante = models.ForeignKey(EstudanteProfile, on_delete=models.DO_NOTHING, null=True)
    data = models.DateField()
    aula = models.ForeignKey(Aula, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return str(self.estudante)

class Professor_curso(models.Model):
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.DO_NOTHING, null=True) 
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return str(self.curso)  

class Coordenador_curso(models.Model):
    coordenador = models.ForeignKey(CoordenadorProfile, on_delete=models.DO_NOTHING, null=True) 
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return str(self.curso)  
        

#SIGNAL STUFF TO ASSOCIATE THE USER MODEL WITH THE USER PROFILES
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.tipo == "Estudante":
		EstudanteProfile.objects.get_or_create(user = instance)
	elif instance.tipo == "Professor":
		ProfessorProfile.objects.get_or_create(user = instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	if instance.tipo == "Estudante":
		instance.estudante_profile.save()
	elif instance.tipo == "Professor":
		instance.professor_profile.save()



