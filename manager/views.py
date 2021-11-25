from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.views.generic import(
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from users.models import CoordenadorProfile, EstudanteProfile
from .forms import CursoForm, EscolherCursoForm, ProfessorCursoForm
from .models import Disciplina, Aula, Curso, Professor_curso
from users.models import User, EstudanteProfile, ProfessorProfile
from users.forms import UserForm, EstudanteProfileForm, ProfessorProfileForm

#GERENCIAMENTO DE DISCIPLINAS
@login_required
@permission_required("manager.view_disciplina", raise_exception=True)
def gerenciarDisciplina(request):
    if request.method=='POST':
        form = EscolherCursoForm(request.POST, user = request.user)
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
    form = EscolherCursoForm(user=request.user)
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
        form = EscolherCursoForm(request.POST, user = request.user)
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
    form = EscolherCursoForm(user=request.user)
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
@permission_required("manager.view_curso", raise_exception=True)
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

#GERENCIAMENTO DE ESTUDANTES
@login_required
@permission_required("manager.view_estudante_profile", raise_exception=True)
def gerenciarEstudante(request):
    if request.method=='POST':
        form = EscolherCursoForm(request.POST, user = request.user)
        if form.is_valid():
            dados = form.cleaned_data
            curso = dados.get('curso')
        
            estudantes = []
            lista_estudanteprofile = EstudanteProfile.objects.all()

            for x in range(len(lista_estudanteprofile)-1, -1, -1):
                if(lista_estudanteprofile[x].curso.nome == str(curso)):
                    print("novo macaco")
                    estudantes.append(lista_estudanteprofile[x])

            if(estudantes == []):
                estudantes = None
                messages.warning(request, f"Não há estudantes")

            context = {
                'estudantes': estudantes,
                'curso': curso
            }
    else:
        return redirect('filtrarEstudante')
    
    return render(request, 'manager/gerenciar-estudante.html', context)


@login_required
@permission_required("users.view_estudante_profile", raise_exception=True)
def filtrarEstudante(request):
    form = EscolherCursoForm(user=request.user)
    return render(request, 'manager/filtrar-estudante.html', {'form': form})

class EstudanteDetailView(LoginRequiredMixin, DetailView):
    model = EstudanteProfile
    template_name = "manager/estudante_detail.html"

class EstudanteDeleteView(DeleteView):
    model = EstudanteProfile
    template_name = "manager/estudante_confirm_delete.html"
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        estudanteprofile_id = self.kwargs['pk']

        lista_estudanteprofile = EstudanteProfile.objects.all()

        for x in range(len(lista_estudanteprofile)-1, -1, -1):
            if(lista_estudanteprofile[x].id == estudanteprofile_id):
                user_id = lista_estudanteprofile[x].user.id

        user = User.objects.filter(id=user_id)
        user.delete()

        return HttpResponseRedirect(reverse('gerenciarEstudante'))


class EstudanteUpdateView(UpdateView):
    template_name = "manager/estudante_form.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        estudanteprofile_id = self.kwargs['pk']

        lista_estudanteprofile = EstudanteProfile.objects.all()

        for x in range(len(lista_estudanteprofile)-1, -1, -1):
            if(lista_estudanteprofile[x].id == estudanteprofile_id):
                user_id = lista_estudanteprofile[x].user.id

        user = User.objects.get(id=user_id)
        estudanteprofile = EstudanteProfile.objects.get(id=estudanteprofile_id)

        return render(request, self.template_name, {
                                                    'user_form': UserForm(instance=user, prefix='UF'),
                                                    'profile_form': EstudanteProfileForm(instance=estudanteprofile, prefix='PF'),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        estudanteprofile_id = self.kwargs['pk']

        lista_estudanteprofile = EstudanteProfile.objects.all()

        for x in range(len(lista_estudanteprofile)-1, -1, -1):
            if(lista_estudanteprofile[x].id == estudanteprofile_id):
                user_id = lista_estudanteprofile[x].user.id

        user = User.objects.get(id=user_id)
        estudanteprofile = EstudanteProfile.objects.get(id=estudanteprofile_id)

        user_form = UserForm(request.POST, instance=user, prefix='UF')
        profile_form = EstudanteProfileForm(request.POST, instance=estudanteprofile, prefix='PF')

        # Check form validation
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return HttpResponseRedirect(reverse('estudante-detail', kwargs={'pk': estudanteprofile_id}))
            

#GERENCIAMENTO DE PROFESSORES
@login_required
@permission_required("manager.view_professor_profile", raise_exception=True)
def gerenciarProfessor(request):
    if request.method=='POST':
        form = EscolherCursoForm(request.POST, user = request.user)
        if form.is_valid():
            dados = form.cleaned_data
            curso = dados.get('curso')
            
            lista_curso = Curso.objects.all()
            for x in range(len(lista_curso)-1, -1, -1):
                if(lista_curso[x].nome == str(curso)):
                    curso_id = lista_curso[x].id

            professores = []
            lista_professor_curso = Professor_curso.objects.all()

            for x in range(len(lista_professor_curso)-1, -1, -1):
                if(lista_professor_curso[x].curso.nome == str(curso)):
                    print("teste")
                    professores.append(lista_professor_curso[x].professor)

            if(professores == []):
                professores = None
                messages.warning(request, f"Não há professores")

            context = {
                'professores': professores,
                'curso': curso,
                'curso_id': curso_id,
            }
    else:
        return redirect('filtrarProfessor')
    
    return render(request, 'manager/gerenciar-professor.html', context)


@login_required
@permission_required("users.view_professor_profile", raise_exception=True)
def filtrarProfessor(request):
    form = EscolherCursoForm(user=request.user)
    return render(request, 'manager/filtrar-professor.html', {'form': form})

class ProfessorDetailView(LoginRequiredMixin, DetailView):
    model = ProfessorProfile
    template_name = "manager/professor_detail.html"

class ProfessorDeleteView(DeleteView):
    model = ProfessorProfile
    template_name = "manager/professor_confirm_delete.html"
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        professorprofile_id = self.kwargs['pk']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.filter(id=user_id)
        user.delete()

        return HttpResponseRedirect(reverse('gerenciarProfessor'))


class ProfessorUpdateView(UpdateView):
    template_name = "manager/professor_form_update.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        professorprofile_id = self.kwargs['pk']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.get(id=user_id)
        professorprofile = ProfessorProfile.objects.get(id=professorprofile_id)

        return render(request, self.template_name, {
                                                    'user_form': UserForm(instance=user, prefix='UF'),
                                                    'profile_form': ProfessorProfileForm(instance=professorprofile, prefix='PF'),
                                                    'curso_form': ProfessorCursoForm(prefix="CF"),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        professorprofile_id = self.kwargs['pk']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.get(id=user_id)
        professorprofile = ProfessorProfile.objects.get(id=professorprofile_id)

        user_form = UserForm(request.POST, instance=user, prefix='UF')
        profile_form = ProfessorProfileForm(request.POST, instance=professorprofile, prefix='PF')
        curso_form = ProfessorCursoForm(request.POST, prefix='CF')

        # Check form validation
        if user_form.is_valid() and profile_form.is_valid() and curso_form.is_valid():
            user_form.save()
            profile_form.save()

            Professor_curso.objects.filter(professor=professorprofile).delete()

            cursos = curso_form.cleaned_data.get('curso')
            for x in range(0, len(cursos), 1):
                curso = Curso.objects.get(id=cursos[x])
                professor_curso = Professor_curso(professor=professorprofile, curso=curso)
                professor_curso.save()

        return HttpResponseRedirect(reverse('professor-detail', kwargs={'pk': professorprofile_id}))

class ProfessorCreateView(CreateView):
    template_name = "manager/professor_form_create.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
                                                    'user_form': UserForm(prefix='UF'),
                                                    'profile_form': ProfessorProfileForm(prefix='PF'),
                                                    'curso_form': ProfessorCursoForm(prefix="CF"),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = ProfessorProfileForm(request.POST, prefix='PF')
        curso_form = ProfessorCursoForm(request.POST, prefix='CF')

        # Check form validation
        if user_form.is_valid() and profile_form.is_valid() and curso_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo = "Professor"
            user.save()

            user.professor_profile.campoextra = profile_form.cleaned_data.get('campoextra')
            user.professor_profile.save()
            permission = Permission.objects.get(codename='view_presenca')
            permission2 = Permission.objects.get(codename='view_aula')
            user.user_permissions.add(permission, permission2)

            professor = user.professor_profile
            cursos = curso_form.cleaned_data.get('curso')
            for x in range(0, len(cursos), 1):
                curso = Curso.objects.get(id=cursos[x])
                professor_curso = Professor_curso(professor=professor, curso=curso)
                professor_curso.save()

        return HttpResponseRedirect(reverse('gerenciarProfessor'))


#GERENCIAMENTO DE COORDENADORES
@login_required
@permission_required("manager.view_coordenador", raise_exception=True)
def gerenciarCoordenador(request):
    coordenadores = CoordenadorProfile.objects.all()

    if(coordenadores == []):
        coordenadores = None
        messages.warning(request, f"Não há coordenadores")

    context = {
        'coordenadores': coordenadores,
    }
    
    return render(request, 'manager/gerenciar-coordenador.html', context)