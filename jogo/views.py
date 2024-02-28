from django.shortcuts import render

def inicio_jogo(request):    
    return render(request, 'jogo/base.html')
