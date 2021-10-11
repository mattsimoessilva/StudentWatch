from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.forms.widgets import EmailInput, PasswordInput
from .models import Curso, Professor


class CursoForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Curso
        fields = '__all__'   
        widgets = {
            'nome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Digite o nome do curso'
                }),
            'descricao': Textarea(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Digite uma breve descrição do curso'
                })
        }
        labels = {
            'descricao': 'Descrição'
        }

class ProfessorForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Professor
        fields = '__all__'   
        widgets = {
            'nome': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Digite o nome do professor'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Digite o e-mail do professor'
                }),
            'senha': PasswordInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Digite a senha do professor'
                })
        }
        labels = {
            'email': 'E-mail'
        }