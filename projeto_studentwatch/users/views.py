from django.shortcuts import render
from .forms import CursoForm, ProfessorForm, EstudanteForm
from django.contrib import messages


def cadastrarCurso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            nome = form.cleaned_data.get('nome')
            messages.success(request, f"Curso '{nome}' cadastrado")
            form = CursoForm()
    else:
        form = CursoForm()
    return render(request, 'users/cadastrar-curso.html', {'form': form})

def cadastrarProfessor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            nome = form.cleaned_data.get('nome')
            messages.success(request, f"Professor '{nome}' cadastrado")
            form = ProfessorForm()
    else:
        form = ProfessorForm()
    return render(request, 'users/cadastrar-professor.html', {'form': form})

def cadastrarEstudante(request):
    if request.method == 'POST':
        form = EstudanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            nome = form.cleaned_data.get('nome')
            messages.success(request, f"Estudante '{nome}' cadastrado")
            form = EstudanteForm()
    else:
        form = EstudanteForm()
    return render(request, 'users/cadastrar-estudante.html', {'form': form})