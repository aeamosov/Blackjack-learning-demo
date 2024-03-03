from flask import Flask, render_template, request
import random
import requests
import json

app = Flask(__name__)

# List to store drawn cards
hand = []
def create_deck():
	deck_id = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
	return deck_id

def draw_card(deck_id):
	card = json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)
	return card
	
@app.route('/')
def index():
	return render_template('index.html', hand=hand)

@app.route('/game')
def new_game():
	deck_id = create_deck()
	global hand 
	hand = []	
	return render_template('game.html', deck_id=deck_id, hand=hand)
	
@app.route('/game/<deck_id>/draw')
def draw(deck_id):
	card = draw_card(deck_id)['cards'][0]	
	# Append the drawn card_image to the hand
	hand.append(card)
	return render_template('game.html', deck_id=deck_id, hand=hand)

#Конфиг запуска	
if __name__=='__main__':
	app.run(port=8000,debug=True)