import requests
from django.http import HttpResponse
from django.shortcuts import render


def inicio(request):    
    return render(request, 'Site/base.html')

def home(request):
    return render(request, 'Site/home.html')

def regras(request):
    return render(request, 'Site/regras.html')
