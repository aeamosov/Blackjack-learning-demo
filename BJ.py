from flask import Flask, render_template, request
import random
import requests
import json

app = Flask(__name__)
#стоимости карт (упрощенно)
card_values={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'JACK':10,'QUEEN':10,'KING':10,'ACE':11}
hand = []
dealer_hand = []
#Создание колоды
def create_deck():
	deck_id = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	return deck_id
#Вытягивание карты
def draw_card(deck_id):
	card = json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)
	return card
#отображение стартовой страницы	
@app.route('/')
def index():
	return render_template('index.html')

#вытягивание карты игроком
@app.route('/game/<deck_id>/draw')
def draw(deck_id):
	card = draw_card(deck_id)['cards'][0]	
	hand.append(card)
	hand_value = sum(card_values[x['value']] for x in hand)
	dealer_hand_value = sum(card_values[x['value']] for x in dealer_hand)
	return render_template('game.html', deck_id=deck_id, hand=hand, hand_value=hand_value, dealer_hand=dealer_hand, dealer_hand_value=dealer_hand_value)
	
#Страница новой игры
@app.route('/game')
def new_game():
	deck_id = create_deck()
	global hand 
	hand = []
	global dealer_hand 
	dealer_hand = []
	#первая карта игрока вытягивается сразу
	draw(deck_id)
	hand_value = sum(card_values[x['value']] for x in hand)
	#вытягивание дилером
	for i in range (0,2):
		dealer_card = draw_card(deck_id)['cards'][0]	
		dealer_hand.append(dealer_card)
	dealer_hand_value = sum(card_values[x['value']] for x in dealer_hand)
	return render_template('game.html', deck_id=deck_id, hand=hand, hand_value=hand_value, dealer_hand=dealer_hand, dealer_hand_value=dealer_hand_value)

#Конфиг запуска	
if __name__=='__main__':
	app.run(port=8000,debug=True)