from flask import Flask, render_template, request
import random
import requests
import json

app = Flask(__name__)

# List to store drawn cards
drawn_cards = []
def create_deck():
    deck_id = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
    return deck_id

def draw_card(deck_id):
    card = json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck_id+'/draw/?count=1').text)
    return card
	
@app.route('/')
def index():
    return render_template('index.html', drawn_cards=drawn_cards)

@app.route('/draw')
def draw():
    deck_id = create_deck()
    card = draw_card(deck_id)['cards'][0]
    card_image = card['image']
    
    # Append the drawn card to the list
    drawn_cards.append(card_image)
    
    return render_template('index.html', card_image=card_image, drawn_cards=drawn_cards)

#Конфиг запуска	
if __name__=='__main__':
	app.run(port=8000,debug=True)