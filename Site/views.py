import requests
from django.shortcuts import render
from django.contrib.auth import get_user_model


def inicio(request):    
    return render(request, 'Site/base.html')

def home(request):
    return render(request, 'Site/home.html')

def regras(request):
    return render(request, 'Site/regras.html')

def leaderboards(request):
    User = get_user_model()
    users = User.objects.all().order_by('-vitorias')  # Ordena os usuários pelo número de vitórias
    return render(request, 'Site/leaderboards.html', {'users': users})