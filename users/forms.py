from io import TextIOBase, UnsupportedOperation
from django import forms
from django.forms import ModelForm, TextInput, Textarea, EmailInput, Select, PasswordInput
from .models import Curso, Disciplina, ProfessorProfile, EstudanteProfile, Professor_curso
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    required_css_class = 'required'
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px;',
                'placeholder': 'Digite o nome'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Digite o e-mail'
            }),
            'password1': PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Digite a senha'
            }),
            'password2': PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Digite a senha novamente'
            })
        }
        labels = {
            'username': 'Nome',
            'email': 'E-mail',
            'password1': 'Senha',
            'password2': 'Confirmação da Senha'
        }

class EstudanteProfileForm(forms.ModelForm):
    class Meta:
        model = EstudanteProfile
        fields = ('matricula', 'curso',)
        widgets = {
            'matricula': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px;',
                'placeholder': 'Digite o Nº de matrícula'
            }),
            'curso': Select(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px;',
                'choices': Curso,
            })
        }
        labels = {
            'matricula': 'Matrícula'
        }
        
class ProfessorProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessorProfile
        fields = ('campoextra',)
        widgets = {
            'campoextra': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px;',
                'placeholder': 'Digite o campo extra do professor'
            })
        }
        labels = {
            'campoextra': 'Campo Extra'
        }


class CursoForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Curso
        fields = '__all__'   
        widgets = {
            'nome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 500px;',
                'placeholder': 'Digite o nome do curso'
                }),
            'descricao': Textarea(attrs={
                'class': "form-control", 
                'style': 'max-width: 500px;',
                'placeholder': 'Digite uma breve descrição do curso'
                })
        }
        labels = {
            'descricao': 'Descrição'
        }

class EscolherCursoForm(forms.Form): 

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EscolherCursoForm, self).__init__(*args, **kwargs) 

        lista_profiles = ProfessorProfile.objects.all()
        for x in range(0, len(lista_profiles), 1):
            if(lista_profiles[x].user == self.user):
                profile_id = lista_profiles[x].id

        cursos = Professor_curso.objects.filter(professor = profile_id)

    #cursos = Curso.objects.all()
        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos, widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 500px;'}))




class LoginForm(AuthenticationForm):
    required_css_class = 'required'
    username = forms.CharField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'max-width: 500px;', 'placeholder': 'Digite o e-mail'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'max-width: 500px;', 'placeholder': 'Digite a senha'}))
