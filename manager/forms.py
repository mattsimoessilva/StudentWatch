from django import forms
from .models import Curso
from users.models import CoordenadorProfile
from django.forms import ModelForm, TextInput, Textarea, EmailInput, Select, PasswordInput


class EscolherCursoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EscolherCursoForm, self).__init__(*args, **kwargs) 

        cursos = Curso.objects.all()

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos)

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'   
        widgets = {
            'nome': TextInput(attrs={
                'placeholder': 'Digite o nome do curso'
                }),
            'descricao': Textarea(attrs={
                'placeholder': 'Digite uma breve descrição do curso'
                })
        }
        labels = {
            'descricao': 'Descrição'
        }