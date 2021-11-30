from django.urls import path
from . import views

from .views import (
    #GERENCIAMENTO DE DISCIPLINAS
    DisciplinaDetailView,
    DisciplinaCreateView,
    DisciplinaUpdateView,
    DisciplinaDeleteView,

    #GERENCIAMENTO DE AULAS
    AulaDetailView,
    AulaCreateView,
    AulaUpdateView,
    AulaDeleteView,

    #GERENCIAMENTO DE CURSOS
    CursoDetailView,
    CursoCreateView,
    CursoUpdateView,
    CursoDeleteView,

    #GERENCIAMENTO DE ESTUDANTES
    EstudanteDetailView,
    EstudanteDeleteView,
    EstudanteCreateView,
    EstudanteUpdateView,

    #GERENCIAMENTO DE PROFESSORES
    ProfessorDetailView,
    ProfessorDeleteView,
    ProfessorCreateView,
    ProfessorUpdateView,

    #GERENCIAMENTO DE COORDENADORES
    CoordenadorDetailView,
    CoordenadorDeleteView,
    CoordenadorCreateView,
    CoordenadorUpdateView
)

urlpatterns = [
    #GERECIAMENTO DE DISCIPLINAS
    path('filtrarDisciplina/', views.filtrarDisciplina, name='filtrarDisciplina'),
    path('gerenciarDisciplina/<int:pk>/', views.gerenciarDisciplina, name='gerenciarDisciplina'),
    path('disciplina/<int:pk>/', DisciplinaDetailView.as_view(), name='disciplina-detail'),
    path('disciplina/<int:pk>/delete/', DisciplinaDeleteView.as_view(), name='disciplina-delete'),
    path('disciplina/<int:pk>/new/', DisciplinaCreateView.as_view(), name='disciplina-create'),
    path('disciplina/<int:pk>/update/', DisciplinaUpdateView.as_view(), name='disciplina-update'),

    #GERENCIAMENTO DE AULAS
    path('filtrarAula/', views.filtrarAula, name='filtrarAula'),
    path('gerenciarAula/<int:pk>/', views.gerenciarAula, name='gerenciarAula'),
    path('aula/<int:pk>/', AulaDetailView.as_view(), name='aula-detail'),
    path('aula/<int:pk>/delete/', AulaDeleteView.as_view(), name='aula-delete'),
    path('aula/<int:pk>/new/', AulaCreateView.as_view(), name='aula-create'),
    path('aula/<int:pk>/update/', AulaUpdateView.as_view(), name='aula-update'),

    #GERENCIAMENTO DE CURSOS
    path('gerenciarCurso/', views.gerenciarCurso, name='gerenciarCurso'),
    path('curso/<int:pk>/', CursoDetailView.as_view(), name='curso-detail'),
    path('curso/<int:pk>/delete/', CursoDeleteView.as_view(), name='curso-delete'),
    path('curso/new/', CursoCreateView.as_view(), name='curso-create'),
    path('curso/<int:pk>/update/', CursoUpdateView.as_view(), name='curso-update'),

    #GERENCIAMENTO DE ESTUDANTES
    path('filtrarEstudante/', views.filtrarEstudante, name='filtrarEstudante'),
    path('gerenciarEstudante/<int:pk>/', views.gerenciarEstudante, name='gerenciarEstudante'),
    path('estudante/<int:pk>/', EstudanteDetailView.as_view(), name='estudante-detail'),
    path('estudante/<int:pk>/delete/', EstudanteDeleteView.as_view(), name='estudante-delete'),
    path('estudante/new/', EstudanteCreateView.as_view(), name='estudante-create'),
    path('estudante/<int:pk>/update/', EstudanteUpdateView.as_view(), name='estudante-update'),

    #GERENCIAMENTO DE PROFESSORES
    path('filtrarProfessor/', views.filtrarProfessor, name='filtrarProfessor'),
    path('gerenciarProfessor/<int:curso_id>/', views.gerenciarProfessor, name='gerenciarProfessor'),
    path('professor/<int:curso_id>/<int:professor_id>/', ProfessorDetailView.as_view(), name='professor-detail'),
    path('professor/<int:curso_id>/<int:professor_id>/delete/', ProfessorDeleteView.as_view(), name='professor-delete'),
    path('professor/<int:curso_id>/new/', ProfessorCreateView.as_view(), name='professor-create'),
    path('professor/<int:curso_id>/<int:professor_id>/update/', ProfessorUpdateView.as_view(), name='professor-update'),

    #GERENCIAMENTO DE COORDENADORES
    path('filtrarCoordenador/', views.filtrarCoordenador, name='filtrarCoordenador'),
    path('gerenciarCoordenador/<int:curso_id>/', views.gerenciarCoordenador, name='gerenciarCoordenador'),
    path('coordenador/<int:curso_id>/<int:coordenador_id>/', CoordenadorDetailView.as_view(), name='coordenador-detail'),
    path('coordenador/<int:curso_id>/<int:coordenador_id>/delete/', CoordenadorDeleteView.as_view(), name='coordenador-delete'),
    path('coordenador/<int:curso_id>/new/', CoordenadorCreateView.as_view(), name='coordenador-create'),
    path('coordenador/<int:curso_id>/<int:coordenador_id>/update/', CoordenadorUpdateView.as_view(), name='coordenador-update'),

    path('ajax/load-disciplinas-estudante/', views.load_disciplinas_estudante, name='ajax_load_disciplinas_estudante'),
]
