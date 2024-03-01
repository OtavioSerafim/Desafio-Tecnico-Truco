import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .logica_jogo import comprar_cartas, carta_mais_poderosa, comparar_cartas_e_atribuir_pontos, pedido_truco, move_card



# VIEW DO JOGO
def jogo(request):
    
    # Inicializa as variáveis na sessão
    if request.session['tentos_player'] != 0 or request.session['tentos_bot'] != 0:
        request.session['pontos_player'] = 0
        request.session['pontos_bot'] = 0
        request.session['valor_rodada'] = 2
    
    else:
        request.session['tentos_bot'] = 0
        request.session['tentos_player'] = 0
        request.session['pontos_player'] = 0
        request.session['pontos_bot'] = 0
        request.session['valor_rodada'] = 2

    # Verifica se já existe um deck_id na sessão
    if 'deck_id' in request.session:
        deck_id = request.session['deck_id']
    else:
        # Gera um novo baralho e armazena o deck_id na sessão
        baralho_truco=['4C','7H','AS','7D',
                       '3H','3C','3D','3S',
                       '2H','2C','2D','2S',
                       'AH','AC','AD',
                       'KH','KC','KD','KS',
                       'JH','JC','JD','JS',
                       'QH','QC','QD','QS',
                       '7C','7S',
                       '6H','6C','6D','6S',
                       '5H','5C','5D','5S',
                       '4H','4D','4S']
        
        response = requests.get(f'https://deckofcardsapi.com/api/deck/new/shuffle/?cards={','.join(baralho_truco)}')
        deck_id = response.json()['deck_id']
        request.session['deck_id'] = deck_id  # Armazena o deck_id na sessão
        # Compra cartas e adiciona à pilha "player1"
        comprar_cartas(deck_id, 'player1')

        # Compra cartas e adiciona à pilha "player2"
        comprar_cartas(deck_id, 'player2')
        
        

    # Obtenha as cartas do bot
    response_bot = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/list/')
    cards_bot = [carta for carta in response_bot.json()['piles']['player2']['cards']]

    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/player1/list/')

    if response.status_code == 200:
        cards = response.json()['piles']['player1']['cards']
        return render(request, 'jogo/truco.html', {'cards': cards, 'cards_bot': cards_bot, 'deck_id': deck_id})
    else:
        return HttpResponse('Erro ao buscar cartas', status=400)
    
    
