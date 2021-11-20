from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import FiltrarDisciplinaForm, CursoForm
from .models import Disciplina


@login_required
@permission_required("users.view_disciplina", raise_exception=True)
def gerenciarDisciplina(request):
    if request.method=='POST':
        form = FiltrarDisciplinaForm(request.POST, user = request.user)
        if form.is_valid():
            dados = form.cleaned_data
            curso = dados.get('curso')

            disciplinas = []
            lista_disciplinas = Disciplina.objects.all()

            for x in range(len(lista_disciplinas)-1, -1, -1):
                if(lista_disciplinas[x].curso.nome == str(curso)):
                    disciplinas.append(lista_disciplinas[x])
                   
            if(disciplinas == []):
                disciplinas = None
                messages.warning(request, f"Não há disciplinas")

            context = {
                'disciplinas': disciplinas,
                'curso': curso
            }
    else:
        return redirect('filtrarDisciplina')
    
    return render(request, 'manager/gerenciar-disciplina.html', context)

@login_required
@permission_required("users.view_disciplina", raise_exception=True)
def filtrarDisciplina(request):
    form = FiltrarDisciplinaForm(user=request.user)
    return render(request, 'manager/filtrar-disciplina.html', {'form': form})

def load_disciplinas(request):
    curso_id = request.GET.get('curso')
    disciplinas = Disciplina.objects.filter(curso_id=curso_id)
    return render(request, 'manager/disciplina_dropdown.html', {'disciplinas': disciplinas})


class DisciplinaDetailView(LoginRequiredMixin, DetailView):
    model = Disciplina

class DisciplinaCreateView(LoginRequiredMixin, CreateView):
    model = Disciplina
    fields = ['nome', 'professor', 'curso']

class DisciplinaUpdateView(LoginRequiredMixin, UpdateView):
    model = Disciplina
    fields = ['nome', 'professor', 'curso']

class DisciplinaDeleteView(LoginRequiredMixin, DeleteView):
    model = Disciplina
    success_url = '/'


@login_required
@permission_required("users.add_curso", raise_exception=True)
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
    return render(request, 'manager/cadastrar-curso.html', {'form': form})
