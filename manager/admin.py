from django.contrib import admin
from .models import (
    Disciplina,
    Aula,
    Turno,
    Presenca,
    Dia_semana,
    Professor_curso,
    Coordenador_curso,
    Curso
)

admin.site.register(Disciplina)
admin.site.register(Aula)
admin.site.register(Turno)
admin.site.register(Presenca)
admin.site.register(Dia_semana)
admin.site.register(Professor_curso)
admin.site.register(Coordenador_curso)
admin.site.register(Curso)
