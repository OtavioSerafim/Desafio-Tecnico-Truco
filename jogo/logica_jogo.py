import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        
        # print('Pontos do jogador:', request.session['pontos_player'])
        # print('Pontos do bot:', request.session['pontos_bot'])
        # print('Tentos do bot:', request.session['tentos_bot'])
        # print('Tentos do jogador:', request.session['tentos_player'])
        # print('valor rodada:', request.session['valor_rodada'])

    
        return JsonResponse({'bot_card_code': carta_poderosa, 'pontos_player': pontos_player, 'pontos_bot': pontos_bot, 'tentos_player': request.session['tentos_player'], 'tentos_bot': request.session['tentos_bot']})
    else:
        return HttpResponse('Erro ao mover carta do bot', status=400)



#FUNÇÃO DA COMPRA DE CARTAS
def comprar_cartas(deck_id, pile_name):
    # Compra 3 cartas
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=3')
    response_json = response.json()

    # Extrai os códigos das cartas compradas
    cartas_compradas = [carta['code'] for carta in response_json['cards']]

    # Adiciona as cartas à pilha especificada
    response_pile = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/add/?cards={','.join(cartas_compradas)}')

    return response_pile

#PODER DAS CARTAS
def valor_carta(carta):
    valores = {
        '4C': 14,
        '7H': 13,
        'AS': 12,
        '7D': 11,
        '3H': 10, '3C': 10, '3D': 10, '3S': 10,
        '2H': 9, '2C': 9, '2D': 9, '2S': 9,
        'AH': 8, 'AC': 8, 'AD': 8,
        'KH': 7, 'KC': 7, 'KD': 7, 'KS': 7,
        'JH': 6, 'JC': 6, 'JD': 6, 'JS': 6,
        'QH': 5, 'QC': 5, 'QD': 5, 'QS': 5,
        '7C': 4, '7S': 4,
        '6H': 3, '6C': 3, '6D': 3, '6S': 3,
        '5H': 2, '5C': 2, '5D': 2, '5S': 2,
        '4H': 1, '4D': 1, '4S': 1
    }
    return valores.get(carta, 0)

#FUNÇÃO PARA DEFINIR A CARTA MAIS PODEROSA
def carta_mais_poderosa(cartas_bot):
    return max(cartas_bot, key=valor_carta)

def descartar_cartas(deck_id):
    # Obtenha as cartas no campo1 e campo2
    response_campo1 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo1/list/')
    response_campo2 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo2/list/')

    if response_campo1.status_code == 200 and response_campo2.status_code == 200:
        carta_campo1 = response_campo1.json()['piles']['campo1']['cards'][0]['code']
        carta_campo2 = response_campo2.json()['piles']['campo2']['cards'][0]['code']

        # Mova as cartas para a pilha de descarte
        response_descarte1 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/descarte/add/?cards={carta_campo1}')
        response_descarte2 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/descarte/add/?cards={carta_campo2}')

        if response_descarte1.status_code == 200 and response_descarte2.status_code == 200:
            return True
        else:
            return HttpResponse('Erro ao mover cartas para a pilha de descarte', status=400)
    else:
        return HttpResponse('Erro ao buscar cartas', status=400)
    
#FUNÇÃO PARA COMPARAR AS CARTAS E ATRIBUIR PONTOS
def comparar_cartas_e_atribuir_pontos(request, deck_id):
    # Obtenha as cartas no campo1 e campo2
    response_campo1 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo1/list/')
    response_campo2 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/campo2/list/')

    if response_campo1.status_code == 200 and response_campo2.status_code == 200:
        carta_campo1 = response_campo1.json()['piles']['campo1']['cards'][0]['code']
        carta_campo2 = response_campo2.json()['piles']['campo2']['cards'][0]['code']

        # Compare o valor das cartas
        if valor_carta(carta_campo1) > valor_carta(carta_campo2):
            # Incrementa pontos_player
            request.session['pontos_player'] += 1
        elif valor_carta(carta_campo1) < valor_carta(carta_campo2):
            # Incrementa pontos_bot
            request.session['pontos_bot'] += 1
        else:
            # Se as cartas tiverem o mesmo valor, incrementa pontos para ambos os jogadores
            request.session['pontos_player'] += 1
            request.session['pontos_bot'] += 1

        # Descarte as cartas
        descartar_cartas(deck_id)

        # Verifica se algum jogador atingiu 2 pontos
        if request.session['pontos_bot'] == 2 and request.session['pontos_player'] == 2:

            devolver_cartas_ao_baralho(deck_id)
            

        elif request.session['pontos_player'] == 2:
            request.session['tentos_player'] += request.session['valor_rodada']

            devolver_cartas_ao_baralho(deck_id)

        elif request.session['pontos_bot'] == 2:
            request.session['tentos_bot'] += request.session['valor_rodada']

            devolver_cartas_ao_baralho(deck_id)
            

        # Retorna os pontos atualizados
        return request.session['pontos_player'], request.session['pontos_bot']
    else:
        return HttpResponse('Erro ao buscar cartas', status=400)


def devolver_cartas_ao_baralho(deck_id):
    # Lista de todas as pilhas
    pilhas = ['descarte', 'player1', 'player2']

    for pilha in pilhas:
        # Obtem o número de cartas na pilha
        response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pilha}/list/')
        if response.status_code != 200:
            return HttpResponse('Erro ao buscar cartas da pilha', status=400)
        count = response.json()['piles'][pilha]['remaining']

        # Move todas as cartas da pilha de volta para o baralho
        response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pilha}/draw/?count={count}')
        if response.status_code != 200:
            return HttpResponse('Erro ao devolver cartas ao baralho', status=400)

    # Embaralha o baralho
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/')
    if response.status_code != 200:
        return HttpResponse('Erro ao embaralhar o baralho', status=400)
    
        # Compra cartas para o jogador e o bot
    comprar_cartas(deck_id, 'player1')
    comprar_cartas(deck_id, 'player2')
    
    return HttpResponse('Cartas devolvidas ao baralho e baralho embaralhado com sucesso', status=200)

@csrf_exempt
def pedido_truco(request):
    
    deck_id = request.POST.get('deck_id')
    # Obtenha as cartas do bot
    response_bot = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/list/')
    cartas_bot = [carta['code'] for carta in response_bot.json()['piles']['player2']['cards']]

    # Determine a carta mais poderosa que o bot tem
    carta_poderosa = carta_mais_poderosa(cartas_bot)
    
    # Verifica se o valor da carta mais poderosa é maior que 10
    if valor_carta(carta_poderosa) > 10:
        request.session['valor_rodada'] = 4
        return JsonResponse({'pontos_player': request.session['pontos_player']})

    else:
        request.session['pontos_player'] = 2
        request.session['tentos_player'] +=2
        response_descarte1 = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/descarte/add/?cards={carta_poderosa}')
        devolver_cartas_ao_baralho(deck_id)
        return JsonResponse({'pontos_player': request.session['pontos_player']})
