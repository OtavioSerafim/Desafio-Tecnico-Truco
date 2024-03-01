from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def inicio_jogo(request):
    
    if 'deck_id' in request.session:
        request.session.pop('deck_id')
        
    request.session['tentos_bot'] = 0
    request.session['tentos_player'] = 0
    
    return render(request, 'jogo/base.html')

@login_required
def resultado(request):
    
    if request.session['tentos_player'] >= 12:
        request.session['tentos_player'] = 0
        request.session['tentos_bot'] = 0
        user = request.user
        user.vitorias +=1
        user.save()
        
        return render(request, 'jogo/vitoria.html')

    if request.session['tentos_bot'] >=12:
        request.session['tentos_player'] = 0
        request.session['tentos_bot'] = 0
        return render(request, 'jogo/derrota.html')
    
    else:
        return redirect('Jogo-inicio')