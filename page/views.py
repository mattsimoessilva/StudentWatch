from django.shortcuts import render, redirect


def home(request):
    if (request.user.is_authenticated and request.user.tipo == "Estudante"):
        return redirect('registrarPresenca')
    elif(request.user.is_authenticated and request.user.tipo == "Professor"):
        return redirect('escolherCurso')
    else:
        return render(request, 'page/home.html')


def about(request):
    return render(request, 'page/about.html', {'title': 'About'})
