from django.contrib import admin
from .models import (
    Aula,
    CoordenadorProfile,
    Curso, Dia_semana,
    Disciplina, Presenca,
    Professor_curso,
    ProfessorProfile,
    EstudanteProfile,
    User,
    Turno,
    Coordenador_curso
    )
from django.contrib.auth.models import Permission

admin.site.register(Curso)
admin.site.register(ProfessorProfile)
admin.site.register(EstudanteProfile)
admin.site.register(User)
admin.site.register(Turno)
admin.site.register(CoordenadorProfile)
admin.site.register(Aula)
admin.site.register(Disciplina)
admin.site.register(Dia_semana)
admin.site.register(Presenca)
admin.site.register(Permission)
admin.site.register(Professor_curso)
admin.site.register(Coordenador_curso)