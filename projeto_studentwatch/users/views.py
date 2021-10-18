from django.shortcuts import redirect, render
from .forms import CursoForm, ProfessorProfileForm, EstudanteProfileForm, UserForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

@login_required
def estudante_profile_view(request):
    if request.method == 'POST':	
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = EstudanteProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_estudante = True
            user.save()

            user.estudante_profile.matricula = profile_form.cleaned_data.get('matricula')
            user.estudante_profile.curso = profile_form.cleaned_data.get('curso')
            user.estudante_profile.save()  

            nome = user_form.cleaned_data.get('username')
            messages.success(request, f"Estudante '{nome}' cadastrado")
            user_form = UserForm(request.POST, prefix='UF')
            profile_form = EstudanteProfileForm(request.POST, prefix='PF')
    else:
        user_form = UserForm(prefix='UF')
        profile_form = EstudanteProfileForm(prefix='PF')
		
    return render(request, 'users/cadastrar-estudante.html',{
			'user_form': user_form,
			'profile_form': profile_form,
	})

def auto_estudante_profile_view(request):
    if request.method == 'POST':	
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = EstudanteProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_estudante = True
            user.save()

            user.estudante_profile.matricula = profile_form.cleaned_data.get('matricula')
            user.estudante_profile.curso = profile_form.cleaned_data.get('curso')
            user.estudante_profile.save()  

            nome = user_form.cleaned_data.get('username')
            messages.success(request, f"Sua conta foi criada! Agora você pode acessar o sistema")
            user_form = UserForm(request.POST, prefix='UF')
            profile_form = EstudanteProfileForm(request.POST, prefix='PF')
            return redirect('login')
    else:
        user_form = UserForm(prefix='UF')
        profile_form = EstudanteProfileForm(prefix='PF')
		
    return render(request, 'users/autocadastro-estudante.html',{
			'user_form': user_form,
			'profile_form': profile_form,
	})

@login_required
def professor_profile_view(request):
    if request.method == 'POST':	
        user_form = UserForm(request.POST, prefix='UF')
        profile_form = ProfessorProfileForm(request.POST, prefix='PF')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_estudante = False
            user.save()

            user.professor_profile.campoextra = profile_form.cleaned_data.get('campoextra')
            user.professor_profile.save()  

            nome = user_form.cleaned_data.get('username')
            messages.success(request, f"Professor '{nome}' cadastrado")
            user_form = UserForm(request.POST, prefix='UF')
            profile_form = ProfessorProfileForm(request.POST, prefix='PF')
    else:
        user_form = UserForm(prefix='UF')
        profile_form = ProfessorProfileForm(prefix='PF')
		
    return render(request, 'users/cadastrar-professor.html',{
			'user_form': user_form,
			'profile_form': profile_form,
	})

@login_required
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


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'