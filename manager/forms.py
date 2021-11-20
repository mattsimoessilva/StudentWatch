from django import forms
from .models import Curso
from users.models import CoordenadorProfile
from django.forms import ModelForm, TextInput, Textarea, EmailInput, Select, PasswordInput

class FiltrarDisciplinaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FiltrarDisciplinaForm, self).__init__(*args, **kwargs) 

        lista_profiles = CoordenadorProfile.objects.all()
        for x in range(0, len(lista_profiles), 1):
            if(lista_profiles[x].user == self.user):
                profile_id = lista_profiles[x].id

        #cursos = Coordenador_curso.objects.filter(coordenador = profile_id)
        cursos = Curso.objects.all()

        self.fields['curso'] = forms.ModelChoiceField(label="Curso", queryset=cursos, widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 500px;'}))


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