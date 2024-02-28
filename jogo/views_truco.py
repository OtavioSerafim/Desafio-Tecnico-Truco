import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .logica_jogo import comprar_cartas, carta_mais_poderosa, comparar_cartas_e_atribuir_pontos


tentos_bot = 0
tentos_player = 0
pontos_player = 0
pontos_bot = 0
valor_rodada = 2


# VIEW DO JOGO
def jogo(request):
    
     # Inicializa as variáveis na sessão
    request.session['tentos_bot'] = 0
    request.session['tentos_player'] = 0
    request.session['pontos_player'] = 0
    request.session['pontos_bot'] = 0
    request.session['valor_rodada'] = 2

    
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
    
    
@csrf_exempt
def move_card(request):
    card_code = request.POST.get('card_code')
    deck_id = request.POST.get('deck_id')

    # Move a carta para a pilha "campo1"
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo1/add/?cards={card_code}')

    if response.status_code == 200:
        # Obtenha as cartas do bot
        response_bot = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/list/')
        cartas_bot = [carta['code'] for carta in response_bot.json()['piles']['player2']['cards']]

        # Determine a carta mais poderosa que o bot tem
        carta_poderosa = carta_mais_poderosa(cartas_bot)

        # Mova a carta mais poderosa para a pilha "campo2"
        response_bot_move = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo2/add/?cards={carta_poderosa}')
        
    if response_bot_move.status_code == 200:
        
        # Chama a função para comparar as cartas e atribuir pontos
        pontos_player, pontos_bot = comparar_cartas_e_atribuir_pontos(request, deck_id)
        
        print('Pontos do jogador:', request.session['pontos_player'])
        print('Pontos do bot:', request.session['pontos_bot'])
        print('Tentos do bot:', request.session['tentos_bot'])
        print('Tentos do jogador:', request.session['tentos_player'])

    
        return JsonResponse({'bot_card_code': carta_poderosa, 'pontos_player': pontos_player, 'pontos_bot': pontos_bot, })
    else:
        return HttpResponse('Erro ao mover carta do bot', status=400)
