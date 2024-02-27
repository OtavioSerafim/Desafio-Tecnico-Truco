import requests
from django.http import HttpResponse
from django.shortcuts import render

def ordem(request):
    response = requests.get('https://deckofcardsapi.com/api/deck/new/draw/?count=52')
    deck_id = response.json()['deck_id']
    manilhas = ['4C','7H','AS','7D']

    for manilha in manilhas:
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/manilhas/add/?cards={manilha}')

    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/manilhas/list/')
    
    if response.status_code == 200:
        cards = response.json()['piles']['manilhas']['cards']
        return render(request, 'Site/ordem.html', {'cards': cards})
    else:
        return HttpResponse('Erro ao listar cartas da pilha', status=400)
    
    
def ordem_2(request):
    response = requests.get('https://deckofcardsapi.com/api/deck/new/?cards=3H,2H,AH,KH,JH,QH,7S,6H,5H,4H')
    deck_id = response.json()['deck_id']
    remaining = response.json()['remaining']
    
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={remaining}')
    response_json = response.json()
    
    if response.status_code == 200:
        cards = response_json['cards']
        return render(request, 'Site/ordem_2.html', {'cards': cards})
    else:
        return HttpResponse('Erro ao buscar cartas', status=400)
    