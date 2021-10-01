from django.shortcuts import render

presence = [
    {
        'student': 'Matheus da Silva',
        'date': '30/09/2021',
        'time': '11:24'
    },
        {
        'student': 'Guilherme Carvalho',
        'date': '20/09/2021',
        'time': '18:30'
    }
]


def home(request):
    context = {
        'presence': presence
    }
    return render(request, 'page/home.html', context)


def about(request):
    return render(request, 'page/about.html', {'title': 'About'})
