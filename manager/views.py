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
from .forms import FiltrarDisciplinaForm, CursoForm, FiltrarAulaForm
from .models import Disciplina, Aula, Curso


#GERENCIAMENTO DE DISCIPLINAS
@login_required
@permission_required("manager.view_disciplina", raise_exception=True)
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
@permission_required("manager.view_disciplina", raise_exception=True)
def filtrarDisciplina(request):
    form = FiltrarDisciplinaForm(user=request.user)
    return render(request, 'manager/filtrar-disciplina.html', {'form': form})

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



#GERENCIAMENTO DE AULAS
@login_required
@permission_required("manager.view_aula", raise_exception=True)
def gerenciarAula(request):
    if request.method=='POST':
        form = FiltrarAulaForm(request.POST, user = request.user)
        if form.is_valid():
            dados = form.cleaned_data
            curso = dados.get('curso')

            aulas = []
            lista_aulas = Aula.objects.all()

            for x in range(len(lista_aulas)-1, -1, -1):
                if(lista_aulas[x].disciplina.curso.nome == str(curso)):
                    print("macaco")
                    aulas.append(lista_aulas[x])

            if(aulas == []):
                aulas = None
                messages.warning(request, f"Não há aulas")

            context = {
                'aulas': aulas,
                'curso': curso
            }
    else:
        return redirect('filtrarAula')
    
    return render(request, 'manager/gerenciar-aula.html', context)


@login_required
@permission_required("users.view_aula", raise_exception=True)
def filtrarAula(request):
    form = FiltrarAulaForm(user=request.user)
    return render(request, 'manager/filtrar-aula.html', {'form': form})

class AulaDetailView(LoginRequiredMixin, DetailView):
    model = Aula

class AulaCreateView(LoginRequiredMixin, CreateView):
    model = Aula
    fields = ['turno', 'disciplina', 'dia_semana']

class AulaUpdateView(LoginRequiredMixin, UpdateView):
    model = Aula
    fields = ['turno', 'disciplina', 'dia_semana']

class AulaDeleteView(LoginRequiredMixin, DeleteView):
    model = Aula
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

#GERENCIAMENTO DE CURSOS
@login_required
@permission_required("manager.view_aula", raise_exception=True)
def gerenciarCurso(request):
    cursos = Curso.objects.all()

    if(cursos == []):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/gerenciar-curso.html', context)

class CursoDetailView(LoginRequiredMixin, DetailView):
    model = Curso

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    fields = ['nome', 'descricao', 'coordenador']

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    fields = ['nome', 'descricao', 'coordenador']

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    success_url = '/'