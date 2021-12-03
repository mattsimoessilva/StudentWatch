from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
from .forms import EscolherCursoForm, ProfessorCursoForm, EstudanteDisciplinaForm, DisciplinaForm
from .models import Disciplina, Aula, Curso, Estudante_disciplina, Professor_curso
from users.models import User, EstudanteProfile, ProfessorProfile, CoordenadorProfile
from users.forms import UserForm, EstudanteProfileForm, ProfessorProfileForm, CoordenadorProfileForm

#GERENCIAMENTO DE DISCIPLINAS
@login_required
@permission_required("manager.view_disciplina", raise_exception=True)
def gerenciarDisciplina(request, pk):
    curso_id = pk
    curso = Curso.objects.get(id=curso_id)

    disciplinas = []
    lista_disciplinas = Disciplina.objects.all()

    for x in range(len(lista_disciplinas)-1, -1, -1):
        if(lista_disciplinas[x].curso.id == curso_id):
            disciplinas.append(lista_disciplinas[x])
                   
    if(disciplinas == []):
        disciplinas = None
        messages.warning(request, f"Não há disciplinas")

    context = {
        'disciplinas': disciplinas,
        'curso': curso
    }
    
    return render(request, 'manager/gerenciar-disciplina.html', context)

@login_required
@permission_required("manager.view_disciplina", raise_exception=True)
def filtrarDisciplina(request):

    if request.user.tipo == "Coordenador":
        cursos = Curso.objects.filter(coordenador = request.user.coordenador_profile.id)
    else:
        cursos = Curso.objects.all()

    if(cursos == [] or not cursos):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/filtrar-disciplina.html', context)


class DisciplinaDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'manager.view_disciplina'
    model = Disciplina

class DisciplinaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manager.add_disciplina'
    template_name = "manager/disciplina_form_create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
                                                    'disciplina_form': DisciplinaForm(),
                                                    }
                                                )

    def post(self, request, *args, **kwargs):
        curso_id = self.kwargs["pk"]
        disciplina_form = DisciplinaForm(request.POST)

        if disciplina_form.is_valid():
            disciplina = disciplina_form.save(commit=False)
            disciplina.save()

        return HttpResponseRedirect(reverse('gerenciarDisciplina', kwargs={'pk': curso_id}))



def load_professores(request):
    curso_id = request.GET.get('curso')
    if(curso_id == ''):
        professores = []
    else:
        professores = []
        lista_professor_curso = Professor_curso.objects.all()

        for x in range(0, len(lista_professor_curso), 1):
            if(lista_professor_curso[x].curso.id == int(curso_id)):
                professores.append(lista_professor_curso[x].professor)

    return render(request, 'manager/professor_dropdown.html', {'professores': professores})


class DisciplinaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'manager.change_disciplina'
    template_name = "manager/disciplina_form_update.html"

    def get(self, request, *args, **kwargs):
        disciplina_id = self.kwargs['pk']

        disciplina = Disciplina.objects.get(id=disciplina_id)

        return render(request, self.template_name, {
                                                    'disciplina_form': DisciplinaForm(instance=disciplina),
                                                    }
                                                )

    def post(self, request, *args, **kwargs):
        disciplina_id = self.kwargs['pk']

        disciplina = Disciplina.objects.get(id=disciplina_id)
        curso_id = disciplina.curso.id

        disciplina_form = DisciplinaForm(request.POST, instance=disciplina)

        if disciplina_form.is_valid():
            disciplina_form.save()

        return HttpResponseRedirect(reverse('gerenciarDisciplina', kwargs={'pk': curso_id}))


class DisciplinaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'manager.delete_disciplina'
    model = Disciplina
    template_name = "manager/disciplina_confirm_delete.html"

    def get_success_url(self):
        disciplina_id = self.kwargs["pk"]
        disciplina = Disciplina.objects.get(id=disciplina_id)
        curso_id = disciplina.curso.id
        return reverse("gerenciarDisciplina", kwargs={"pk": curso_id})



#GERENCIAMENTO DE AULAS
@login_required
@permission_required("manager.view_aula", raise_exception=True)
def gerenciarAula(request, pk):
    curso_id = pk
    curso = Curso.objects.get(id=curso_id)

    aulas = []
    lista_aulas = Aula.objects.all()

    for x in range(len(lista_aulas)-1, -1, -1):
        if(lista_aulas[x].disciplina.curso.id == curso_id):
            aulas.append(lista_aulas[x])
                   
    if(aulas == []):
        aulas = None
        messages.warning(request, f"Não há aulas")

    context = {
        'aulas': aulas,
        'curso': curso
    }
    
    return render(request, 'manager/gerenciar-aula.html', context)


@login_required
@permission_required("manager.view_aula", raise_exception=True)
def filtrarAula(request):

    if request.user.tipo == "Coordenador":
        cursos = Curso.objects.filter(coordenador = request.user.coordenador_profile.id)
    else:
        cursos = Curso.objects.all()

    if(cursos == [] or not cursos):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/filtrar-aula.html', context)

class AulaDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'manager.view_aula'
    model = Aula

class AulaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manager.add_aula'
    model = Aula
    fields = ['turno', 'disciplina', 'dia_semana']
    template_name = "manager/aula_form_create.html"

    def get_success_url(self):
        curso_id = self.kwargs["pk"]
        return reverse("gerenciarAula", kwargs={"pk": curso_id})

class AulaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'manager.change_aula'
    model = Aula
    fields = ['turno', 'disciplina', 'dia_semana']
    template_name = "manager/aula_form_update.html"

    def get_success_url(self):
        aula_id = self.kwargs["pk"]
        aula = Aula.objects.get(id=aula_id)
        curso_id = aula.disciplina.curso.id
        return reverse("gerenciarAula", kwargs={"pk": curso_id})

class AulaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'manager.delete_aula'
    model = Aula

    def get_success_url(self):
        aula_id = self.kwargs["pk"]
        aula = Aula.objects.get(id=aula_id)
        curso_id = aula.disciplina.curso.id
        return reverse("gerenciarAula", kwargs={"pk": curso_id})


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

class CursoDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'manager.view_curso'
    model = Curso

class CursoCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manager.add_curso'
    model = Curso
    fields = ['nome', 'descricao', 'coordenador']
    template_name = "manager/curso_form_create.html"

    def get_success_url(self):
        return reverse("gerenciarCurso")

class CursoUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'manager.change_curso'
    model = Curso
    fields = ['nome', 'descricao', 'coordenador']
    template_name = "manager/curso_form_update.html"

    def get_success_url(self):
        return reverse("gerenciarCurso")

class CursoDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'manager.delete_curso'
    model = Curso
    template_name = "manager/curso_confirm_delete.html"

    def get_success_url(self):
        return reverse("gerenciarCurso")

#GERENCIAMENTO DE ESTUDANTES
@login_required
@permission_required("users.view_estudanteprofile", raise_exception=True)
def gerenciarEstudante(request, pk):
    curso_id = pk
    curso = Curso.objects.get(id=curso_id)

    estudantes = []
    lista_estudanteprofile = EstudanteProfile.objects.all()

    for x in range(len(lista_estudanteprofile)-1, -1, -1):
        if(lista_estudanteprofile[x].curso.id == curso_id):
            estudantes.append(lista_estudanteprofile[x])
                   
    if(estudantes == []):
        estudantes = None
        messages.warning(request, f"Não há estudantes")

    context = {
        'estudantes': estudantes,
        'curso': curso
    }
    
    return render(request, 'manager/gerenciar-estudante.html', context)


@login_required
@permission_required("users.view_estudanteprofile", raise_exception=True)
def filtrarEstudante(request):

    if request.user.tipo == "Coordenador":
        cursos = Curso.objects.filter(coordenador = request.user.coordenador_profile.id)
    else:
        cursos = Curso.objects.all()

    if(cursos == [] or not cursos):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/filtrar-estudante.html', context)


class EstudanteDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'users.view_estudanteprofile'
    template_name = "manager/estudante_detail.html"

    def get(self, request, *args, **kwargs):
        estudante_id = self.kwargs['pk']

        estudante = EstudanteProfile.objects.get(id=estudante_id)
        disciplinas = Estudante_disciplina.objects.filter(estudante = estudante_id)

        context = {
            'object': estudante,
            'disciplinas': disciplinas,
        }
    
        return render(request, self.template_name, context)

class EstudanteDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'users.delete_estudanteprofile'
    model = EstudanteProfile
    template_name = "manager/estudante_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        estudanteprofile_id = self.kwargs['pk']

        lista_estudanteprofile = EstudanteProfile.objects.all()

        for x in range(len(lista_estudanteprofile)-1, -1, -1):
            if(lista_estudanteprofile[x].id == estudanteprofile_id):
                user_id = lista_estudanteprofile[x].user.id
                curso_id = lista_estudanteprofile[x].curso.id

        user = User.objects.filter(id=user_id)
        user.delete()

        return HttpResponseRedirect(reverse('gerenciarEstudante', kwargs={'pk': curso_id}))


class EstudanteUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'users.change_estudanteprofile'
    template_name = "manager/estudante_form_update.html"

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
                                                    'disciplina_form': EstudanteDisciplinaForm(prefix='DF')
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
        disciplina_form = EstudanteDisciplinaForm(request.POST, prefix='DF')


        email = user_form['email'].value()
        check_instance_email = User.objects.filter(email=email, id=user_id).exists()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True and check_instance_email == False):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)


        matricula = profile_form['matricula'].value()
        check_instance_matricula = EstudanteProfile.objects.filter(matricula=matricula, estudante=estudanteprofile_id).exists()
        check_matricula = EstudanteProfile.objects.filter(matricula=matricula).exists()

        if(check_matricula == True and check_instance_matricula == False):
            messages.warning(request, f"O número de matrícula inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)


        if(disciplina_form['disciplina'].value() != []):
            # Check form validation
            if user_form.is_valid() and profile_form.is_valid() and disciplina_form.is_valid():
                user_form.save()
                profile_form.save()

                Estudante_disciplina.objects.filter(estudante=estudanteprofile).delete()

                disciplinas = disciplina_form.cleaned_data.get('disciplina')
                for x in range(0, len(disciplinas), 1):
                    disciplina = Disciplina.objects.get(id=disciplinas[x])
                    estudante_disciplina = Estudante_disciplina(estudante=estudanteprofile, disciplina=disciplina)
                    estudante_disciplina.save()

            return HttpResponseRedirect(reverse('gerenciarEstudante', kwargs={'pk': estudanteprofile.curso.id}))
        else:
            return render(request, self.template_name, {
                                                        'user_form': UserForm(instance=user, prefix='UF'),
                                                        'profile_form': EstudanteProfileForm(instance=estudanteprofile, prefix='PF'),
                                                        'disciplina_form': EstudanteDisciplinaForm(prefix='DF'),
                                                        'mensagem': "Por favor, escolha ao menos uma disciplina",
                                                        'tag': "alert alert-warning"
                                                        }
                                                    )
            

class EstudanteCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'users.add_estudanteprofile'
    template_name = "manager/estudante_form_create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
                                                    'user_form': UserForm(prefix='UF'),
                                                    'profile_form': EstudanteProfileForm(prefix='PF'),
                                                    'disciplina_form': EstudanteDisciplinaForm(prefix='DF')
                                                    }
                                                )

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = EstudanteProfileForm(request.POST, prefix='PF')
        disciplina_form = EstudanteDisciplinaForm(request.POST, prefix='DF')

        email = user_form['email'].value()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)

        matricula = profile_form['matricula'].value()
        check_matricula = EstudanteProfile.objects.filter(matricula=matricula).exists()

        if(check_matricula == True):
            messages.warning(request, f"O número de matrícula inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)

        if(disciplina_form['disciplina'].value() != []):
            # Check form validation
            if user_form.is_valid() and profile_form.is_valid() and disciplina_form.is_valid():
                user = user_form.save(commit=False)
                user.tipo = "Estudante"
                user.save()

                user.estudante_profile.matricula = profile_form.cleaned_data.get('matricula')
                user.estudante_profile.curso = disciplina_form.cleaned_data.get('curso')
                user.estudante_profile.save()
                permission = Permission.objects.get(codename='add_presenca')
                user.user_permissions.add(permission)

                estudante = user.estudante_profile
                disciplinas = disciplina_form.cleaned_data.get('disciplina')
                
                for x in range(0, len(disciplinas), 1):
                    disciplina = Disciplina.objects.get(id=disciplinas[x])
                    disciplina_estudante = Estudante_disciplina(estudante=estudante, disciplina=disciplina)
                    disciplina_estudante.save()

                return HttpResponseRedirect(reverse('gerenciarEstudante', kwargs={'pk': user.estudante_profile.curso.id}))
        else:
            return render(request, self.template_name, {
                                                        'user_form': UserForm(prefix='UF'),
                                                        'profile_form': EstudanteProfileForm(prefix='PF'),
                                                        'disciplina_form': EstudanteDisciplinaForm(prefix='DF'),
                                                        'mensagem': "Por favor, escolha ao menos uma disciplina",
                                                        'tag': "alert alert-warning"
                                                        }
                                                    )        


def load_disciplinas_estudante(request):
    curso_id = request.GET.get('curso')
    if(curso_id == ''):
        disciplinas = Disciplina.objects.none()
    else:
        disciplinas = Disciplina.objects.filter(curso_id=curso_id)
    return render(request, 'manager/disciplina_checkbox.html', {'disciplinas': disciplinas})


#GERENCIAMENTO DE PROFESSORES
@login_required
@permission_required("users.view_professorprofile", raise_exception=True)
def gerenciarProfessor(request, curso_id):
    curso_id = curso_id
    curso = Curso.objects.get(id=curso_id)

    professores = []
    lista_professor_curso = Professor_curso.objects.all()

    for x in range(len(lista_professor_curso)-1, -1, -1):
        if(lista_professor_curso[x].curso.id == curso_id):
            professores.append(lista_professor_curso[x].professor)
                   
    if(professores == []):
        professores = None
        messages.warning(request, f"Não há professores")

    context = {
        'professores': professores,
        'curso': curso
    }
    
    return render(request, 'manager/gerenciar-professor.html', context)


@login_required
@permission_required("users.view_professorprofile", raise_exception=True)
def filtrarProfessor(request):
    
    if request.user.tipo == "Coordenador":
        cursos = Curso.objects.filter(coordenador = request.user.coordenador_profile.id)
    else:
        cursos = Curso.objects.all()

    if(cursos == [] or not cursos):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/filtrar-professor.html', context)

class ProfessorDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'users.view_professorprofile'
    template_name = "manager/professor_detail.html"

    def get(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        professorprofile_id = self.kwargs['professor_id']

        professorprofile = ProfessorProfile.objects.get(id=professorprofile_id)
        cursos = Professor_curso.objects.filter(professor=professorprofile_id)
        disciplinas = Disciplina.objects.filter(professor=professorprofile_id)

        context = {
            'object': professorprofile,
            'curso_id': curso_id,
            'cursos': cursos,
            'disciplinas': disciplinas,
        }
    
        return render(request, self.template_name, context)


class ProfessorDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'users.delete_professorprofile'
    template_name = "manager/professor_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        professorprofile_id = self.kwargs['professor_id']

        professorprofile = ProfessorProfile.objects.get(id=professorprofile_id)

        context = {
            'object': professorprofile,
            'curso_id': curso_id,
        }
    
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        professorprofile_id = self.kwargs['professor_id']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.filter(id=user_id)
        user.delete()

        return HttpResponseRedirect(reverse('gerenciarProfessor', kwargs={'curso_id': curso_id}))


class ProfessorUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'users.change_professorprofile'
    template_name = "manager/professor_form_update.html"

    def get(self, request, *args, **kwargs):
        professorprofile_id = self.kwargs['professor_id']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.get(id=user_id)

        return render(request, self.template_name, {
                                                    'user_form': UserForm(instance=user, prefix='UF'),
                                                    'curso_form': ProfessorCursoForm(prefix="CF"),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        professorprofile_id = self.kwargs['professor_id']

        lista_professorprofile = ProfessorProfile.objects.all()

        for x in range(len(lista_professorprofile)-1, -1, -1):
            if(lista_professorprofile[x].id == professorprofile_id):
                user_id = lista_professorprofile[x].user.id

        user = User.objects.get(id=user_id)
        professorprofile = ProfessorProfile.objects.get(id=professorprofile_id)

        user_form = UserForm(request.POST, instance=user, prefix='UF')
        curso_form = ProfessorCursoForm(request.POST, prefix='CF')

        email = user_form['email'].value()
        check_instance_email = User.objects.filter(email=email, id=user_id).exists()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True and check_instance_email == False):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)

        if(curso_form['curso'].value() != []):
            print("batata")
            # Check form validation
            if user_form.is_valid() and curso_form.is_valid():
                user_form.save()

                Professor_curso.objects.filter(professor=professorprofile).delete()

                cursos = curso_form.cleaned_data.get('curso')

                for x in range(0, len(cursos), 1):
                    curso = Curso.objects.get(id=cursos[x])
                    professor_curso = Professor_curso(professor=professorprofile, curso=curso)
                    professor_curso.save()

                return HttpResponseRedirect(reverse('gerenciarProfessor', kwargs={'curso_id': curso_id}))
        else:
            return render(request, self.template_name, {
                                                        'user_form': UserForm(instance=user, prefix='UF'),
                                                        'curso_form': ProfessorCursoForm(prefix="CF"),
                                                        'mensagem': "Por favor, escolha ao menos um curso",
                                                        'tag': "alert alert-warning"
                                                        }
                                                    )


class ProfessorCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'users.add_professorprofile'
    template_name = "manager/professor_form_create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
                                                    'user_form': UserForm(prefix='UF'),
                                                    'curso_form': ProfessorCursoForm(prefix="CF"),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']

        user_form = UserForm(request.POST, prefix='UF')
        curso_form = ProfessorCursoForm(request.POST, prefix='CF')

        email = user_form['email'].value()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)


        if(curso_form['curso'].value() != []):
            # Check form validation
            if user_form.is_valid() and curso_form.is_valid():
                user = user_form.save(commit=False)
                user.tipo = "Professor"
                user.save()

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
        else:
            return render(request, self.template_name, {
                                                        'user_form': UserForm(prefix='UF'),
                                                        'curso_form': ProfessorCursoForm(prefix="CF"),
                                                        'mensagem': "Por favor, escolha ao menos um curso",
                                                        'tag': "alert alert-warning"
                                                        }
                                                    )
        return HttpResponseRedirect(reverse('gerenciarProfessor', kwargs={'curso_id': curso_id}))


#GERENCIAMENTO DE COORDENADORES
@login_required
@permission_required("users.view_coordenadorprofile", raise_exception=True)
def gerenciarCoordenador(request, curso_id):
    curso_id = curso_id
    curso = Curso.objects.get(id=curso_id)

    coordenadores = []
    lista_cursos = Curso.objects.all()

    for x in range(len(lista_cursos)-1, -1, -1):
        if(lista_cursos[x].id == curso_id and lista_cursos[x].coordenador != None):
            coordenadores.append(lista_cursos[x].coordenador)
                   
    if(coordenadores == []):
        coordenadores = None
        messages.warning(request, f"Não há coordenadores")

    print(coordenadores)

    context = {
        'coordenadores': coordenadores,
        'curso': curso
    }
    
    return render(request, 'manager/gerenciar-coordenador.html', context)


@login_required
@permission_required("users.view_coordenadorprofile", raise_exception=True)
def filtrarCoordenador(request):
    cursos = Curso.objects.all()

    if(cursos == []):
        cursos = None
        messages.warning(request, f"Não há cursos")

    context = {
        'cursos': cursos,
    }
    
    return render(request, 'manager/filtrar-coordenador.html', context)

class CoordenadorDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'users.view_coordenadorprofile'
    template_name = "manager/coordenador_detail.html"

    def get(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        coordenadorprofile_id = self.kwargs['coordenador_id']

        coordenadorprofile = CoordenadorProfile.objects.get(id=coordenadorprofile_id)

        context = {
            'object': coordenadorprofile,
            'curso_id': curso_id,
        }
    
        return render(request, self.template_name, context)

class CoordenadorDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'users.delete_coordenadorprofile'
    template_name = "manager/coordenador_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        coordenadorprofile_id = self.kwargs['coordenador_id']

        coordenadorprofile = CoordenadorProfile.objects.get(id=coordenadorprofile_id)

        context = {
            'object': coordenadorprofile,
            'curso_id': curso_id,
        }
    
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        coordenadorprofile_id = self.kwargs['coordenador_id']

        lista_coordenadorprofile = CoordenadorProfile.objects.all()

        for x in range(len(lista_coordenadorprofile)-1, -1, -1):
            if(lista_coordenadorprofile[x].id == coordenadorprofile_id):
                user_id = lista_coordenadorprofile[x].user.id

        user = User.objects.filter(id=user_id)
        user.delete()

        return HttpResponseRedirect(reverse('gerenciarCoordenador', kwargs={'curso_id': curso_id}))


class CoordenadorCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'users.add_coordenadorprofile'
    template_name = "manager/coordenador_form_create.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
                                                    'user_form': UserForm(prefix='UF'),
                                                    }
                                                )

    def post(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']

        user_form = UserForm(request.POST, prefix='UF')

        email = user_form['email'].value()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)

        # Check form validation
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo = "Coordenador"
            user.save()

            user.coordenador_profile.save()
            permission = Permission.objects.get(codename='view_disciplina')
            permission2 = Permission.objects.get(codename='view_aula')
            permission3 = Permission.objects.get(codename='view_estudanteprofile')
            permission4 = Permission.objects.get(codename='view_professorprofile')
            permission5 = Permission.objects.get(codename='view_presenca')
            user.user_permissions.add(permission, permission2, permission3, permission4, permission5)

        return HttpResponseRedirect(reverse('gerenciarCoordenador', kwargs={'curso_id': curso_id}))


class CoordenadorUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'users.change_coordenadorprofile'
    template_name = "manager/coordenador_form_update.html"

    def get(self, request, *args, **kwargs):
        coordenadorprofile_id = self.kwargs['coordenador_id']

        lista_coordenadorprofile = CoordenadorProfile.objects.all()

        for x in range(len(lista_coordenadorprofile)-1, -1, -1):
            if(lista_coordenadorprofile[x].id == coordenadorprofile_id):
                user_id = lista_coordenadorprofile[x].user.id

        user = User.objects.get(id=user_id)

        return render(request, self.template_name, {
                                                    'user_form': UserForm(instance=user, prefix='UF'),
                                                    }
                                                )

        
    def post(self, request, *args, **kwargs):
        curso_id = self.kwargs['curso_id']
        coordenadorprofile_id = self.kwargs['coordenador_id']

        lista_coordenadorprofile = CoordenadorProfile.objects.all()

        for x in range(len(lista_coordenadorprofile)-1, -1, -1):
            if(lista_coordenadorprofile[x].id == coordenadorprofile_id):
                user_id = lista_coordenadorprofile[x].user.id

        user = User.objects.get(id=user_id)
        coordenadorprofile = CoordenadorProfile.objects.get(id=coordenadorprofile_id)

        user_form = UserForm(request.POST, instance=user, prefix='UF')

        email = user_form['email'].value()
        check_instance_email = User.objects.filter(email=email, id=user_id).exists()
        check_email = User.objects.filter(email=email).exists()

        if(check_email == True and check_instance_email == False):
            messages.warning(request, f"O e-mail inserido já existe no sistema")
            return HttpResponseRedirect(self.request.path_info)

        # Check form validation
        if user_form.is_valid():
            user_form.save()

        return HttpResponseRedirect(reverse('gerenciarCoordenador', kwargs={'curso_id': curso_id}))
