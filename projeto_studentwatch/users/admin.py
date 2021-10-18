from django.contrib import admin
from .models import Curso, ProfessorProfile, EstudanteProfile, User

admin.site.register(Curso)
admin.site.register(ProfessorProfile)
admin.site.register(EstudanteProfile)
admin.site.register(User)