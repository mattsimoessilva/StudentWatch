from django import forms
from .models import Curso
from users.models import CoordenadorProfile
from django.forms import ModelForm, TextInput, Textarea, EmailInput, Select, PasswordInput

class FiltrarDisciplinaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FiltrarDisciplinaForm, self).__init__(*args, **kwargs) 

        cursos = Curso.objects.all()

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos)


class FiltrarAulaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FiltrarAulaForm, self).__init__(*args, **kwargs) 

        cursos = Curso.objects.all()

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos)


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