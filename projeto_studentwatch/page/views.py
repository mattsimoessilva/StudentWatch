from django.shortcuts import render
from .models import Professor


def home(request):
    context = {
        'professores': Professor.objects.all()
    }
    return render(request, 'page/home.html', context)


def about(request):
    return render(request, 'page/about.html', {'title': 'About'})
