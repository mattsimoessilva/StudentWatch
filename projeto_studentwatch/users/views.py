from django.shortcuts import render
from .forms import CursoForm, ProfessorForm
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