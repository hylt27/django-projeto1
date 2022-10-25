from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', context={'name': 'Henrique'})


# Create your views here.
