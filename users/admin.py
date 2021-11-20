from django.contrib import admin
from .models import (
    CoordenadorProfile,
    ProfessorProfile,
    EstudanteProfile,
    User
    )
from django.contrib.auth.models import Permission

admin.site.register(ProfessorProfile)
admin.site.register(EstudanteProfile)
admin.site.register(User)
admin.site.register(CoordenadorProfile)
admin.site.register(Permission)