from django import forms
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from .models import Curso, Disciplina, Professor_curso, Aula
from users.models import CoordenadorProfile
from django.forms import ModelForm, TextInput, Textarea, EmailInput, Select, PasswordInput


class EscolherCursoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = self.user = kwargs.pop('user', None)
        super(EscolherCursoForm, self).__init__(*args, **kwargs) 

        if user.is_staff:
            cursos = Curso.objects.all()
        elif user.tipo == "Coordenador":
            cursos = Curso.objects.filter(coordenador = CoordenadorProfile.objects.get(user=user))

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos)


class ProfessorCursoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfessorCursoForm, self).__init__(*args, **kwargs) 

        lista_cursos = []
        cursos = Curso.objects.all()

        for x in range(0, len(cursos), 1):
            lista_cursos.append([cursos[x].id, cursos[x].nome])
        
        self.fields['curso'] = forms.MultipleChoiceField(label="Curso(s)", choices=lista_cursos, widget=CheckboxSelectMultiple())

class EstudanteDisciplinaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EstudanteDisciplinaForm, self).__init__(*args, **kwargs) 

        cursos = Curso.objects.all()
        lista_teste = []

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos, widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 500px;'}))
        
        self.fields['disciplina'] = forms.MultipleChoiceField(label="Disciplina(s)", choices=lista_teste, widget=CheckboxSelectMultiple())

        if 'DF-curso' in self.data:
            try:
                lista_disciplinas = []
                disciplinas = Disciplina.objects.all()

                for x in range(0, len(disciplinas), 1):
                        lista_disciplinas.append([disciplinas[x].id, disciplinas[x].nome])

                self.fields['disciplina'] = forms.MultipleChoiceField(label="Disciplina(s)", choices=lista_disciplinas, widget=CheckboxSelectMultiple())
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        