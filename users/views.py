from django.shortcuts import redirect, render
from .forms import ProfessorProfileForm, EstudanteProfileForm, UserForm, LoginForm, FiltrarPresencaForm2
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from .models import EstudanteProfile
from manager.models import Presenca, Turno, Aula, Curso, Disciplina, Professor_curso, Estudante_disciplina
import datetime
import calendar


@login_required
@permission_required("users.add_estudanteprofile", raise_exception=True)
def estudante_profile_view(request):
    if request.method == 'POST':	
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = EstudanteProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo = "Estudante"
            user.save()

            user.estudante_profile.matricula = profile_form.cleaned_data.get('matricula')
            user.estudante_profile.curso = profile_form.cleaned_data.get('curso')
            user.estudante_profile.save()  
            permission = Permission.objects.get(codename='add_presenca')
            user.user_permissions.add(permission)

            return HttpResponseRedirect(reverse('gerenciarEstudante', kwargs={'pk': user.estudante_profile.curso.id}))
    else:
        user_form = UserForm(prefix='UF')
        profile_form = EstudanteProfileForm(prefix='PF')
		
    return render(request, 'users/cadastrar-estudante.html',{
			'user_form': user_form,
			'profile_form': profile_form,
	})


@login_required
@permission_required("users.add_professorprofile", raise_exception=True)
def professor_profile_view(request):
    if request.method == 'POST':	
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = ProfessorProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.tipo = "Professor"
            user.save()

            user.professor_profile.campoextra = profile_form.cleaned_data.get('campoextra')
            user.professor_profile.save()
            permission = Permission.objects.get(codename='view_presenca')
            permission2 = Permission.objects.get(codename='view_aula')
            user.user_permissions.add(permission, permission2)

            messages.success(request, f"Professor cadastrado")
            user_form = UserForm(prefix='UF')
            profile_form = ProfessorProfileForm(prefix='PF')
    else:
        user_form = UserForm(prefix='UF')
        profile_form = ProfessorProfileForm(prefix='PF')
		
    return render(request, 'users/cadastrar-professor.html',{
			'user_form': user_form,
			'profile_form': profile_form,
	})


@login_required
@permission_required("manager.add_presenca", raise_exception=True)
def registrarPresenca(request):
    usuario = request.user
    data = datetime.datetime.now().date()
    hora = datetime.datetime.now().time()
    dia_semana = calendar.day_name[data.weekday()]
    curso = None
    turno = None
    aula = None
    presenca_anterior = 0
    presenca_registrada = False

    lista_turnos = Turno.objects.all()
    for x in range(0, len(lista_turnos), 1):
        if(hora > lista_turnos[x].inicio and hora < lista_turnos[x].fim):
            turno = lista_turnos[x]

    lista_profiles = EstudanteProfile.objects.all()
    for x in range(0, len(lista_profiles), 1):
        if(lista_profiles[x].user == usuario):
            profile = lista_profiles[x]

    

    lista_aulas = Aula.objects.all()
    for x in range(0, len(lista_aulas), 1):

        if(lista_aulas[x].disciplina.curso == profile.curso and lista_aulas[x].turno == turno and lista_aulas[x].dia_semana.nome == dia_semana):
            aula = lista_aulas[x]
            curso = lista_aulas[x].disciplina.curso
            disciplina = Estudante_disciplina.objects.filter(estudante=usuario.estudante_profile.id, disciplina=aula.disciplina.id)

    lista_presencas = Presenca.objects.all()
    for x in range(0, len(lista_presencas), 1):
        if(lista_presencas[x].aula.turno == turno and lista_presencas[x].estudante.user == usuario and lista_presencas[x].data == data):
            presenca_anterior += 1

    if request.method == 'POST':

        if(turno != None and aula != None and presenca_anterior == 0):
            reg = Presenca(estudante=profile, data=data, aula=aula)
            reg.save()
            messages.success(request, f"Presença registrada")
            presenca_registrada = True

    print(disciplina)
    
    if(curso == None or aula == None or turno == None or not disciplina):
        disciplina = None
        messages.warning(request, f"Desculpe, não há nenhuma aula no momento")

    if(presenca_anterior != 0):
        messages.warning(request, f"Você já registrou presença na aula atual")


    context = {
            'curso': curso,
            'aula': aula,
            'turno': turno,
            'presenca_anterior': presenca_anterior,
            'presenca_registrada': presenca_registrada,
            'disciplina': disciplina
    }
    return render(request, 'users/registrar-presenca.html', context)


@login_required
@permission_required("manager.view_presenca", raise_exception=True)
def visualizarPresenca(request):
    if request.method=='POST':
        form = FiltrarPresencaForm2(request.POST, user = request.user)
        print(form.errors)
        if form.is_valid():
            dados = form.cleaned_data
            disciplina = dados.get('disciplina')
            curso = dados.get('curso')
            data = dados.get('data')
            turno = dados.get('turno')
            usuario = request.user



            presencas = []
            lista_presencas = Presenca.objects.all()

            for x in range(len(lista_presencas)-1, -1, -1):
                if(lista_presencas[x].aula.disciplina.professor.user == usuario and lista_presencas[x].aula.disciplina == disciplina  and lista_presencas[x].data == data and lista_presencas[x].aula.turno == turno):
                    presencas.append(lista_presencas[x])
                   
            if(presencas == []):
                presencas = None
                messages.warning(request, f"Não há registros de presença")

            context = {
                'presencas': presencas,
                'curso': curso,
                'disciplina': disciplina,
                'data': data,
                'turno': turno
            }
    else:
        return redirect('filtrarPresenca')
    
    return render(request, 'users/visualizar-presenca.html', context)

def load_disciplinas(request):
    professor_curso_id = request.GET.get('curso')
    if(professor_curso_id == ''):
        disciplinas = Disciplina.objects.none()
    else:
        curso_id = Professor_curso.objects.get(id=professor_curso_id).curso.id
        disciplinas = Disciplina.objects.filter(curso_id=curso_id, professor=request.user.professor_profile.id)
    return render(request, 'users/disciplina_dropdown.html', {'disciplinas': disciplinas})

def load_turnos(request):
    disciplina_id = request.GET.get('disciplina')
    curso_id = request.GET.get('curso_id')
    if(disciplina_id == '' or curso_id == ''):
        turnos = Turno.objects.none()
    else:
        turnos = Turno.objects.all()

    return render(request, 'users/turno_dropdown.html', {'turnos': turnos})

@login_required
@permission_required("manager.view_presenca", raise_exception=True)
def filtrarPresenca(request):
    form = FiltrarPresencaForm2(user=request.user)
    return render(request, 'users/filtrar-presenca.html', {'form': form})

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

def error_403_view(request, exception):
    return render(request, 'users/403.html')