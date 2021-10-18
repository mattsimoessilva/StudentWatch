from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.nome

#USER AUTHENTICATION STUFF
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_estudante = models.BooleanField(default=True)

class EstudanteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='estudante_profile')
    matricula = models.CharField(max_length=20, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.user.username

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='professor_profile')
    campoextra = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_estudante:
		EstudanteProfile.objects.get_or_create(user = instance)
	else:
		ProfessorProfile.objects.get_or_create(user = instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	# print(instance.internprofile.matricula, instance.estudanteprofile.curso)
	if instance.is_estudante:
		instance.estudante_profile.save()
	else:
		instance.professor_profile.save()



