from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

LISTE_SUIT = ['H', 'S', 'D', 'C']
LISTE_VALUE = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6']


def init_deck():
    # deck_url = 'https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    cartes = ''
    for suit in LISTE_SUIT:
        for value in LISTE_VALUE:
            cartes += str(value) + str(suit)
            # Ajouter une virgule si ce n'est pas la dernière combinaison
            if not (suit == LISTE_SUIT[-1] and value == LISTE_VALUE[-1]):
                cartes += ','
    print(cartes)
    print(len(cartes))
    deck_url = f'https://www.deckofcardsapi.com/api/deck/new/shuffle/?cards={cartes}'
    response = requests.get(deck_url)
    if response.status_code == 200:
        # Charger les données JSON
        deck_data = response.json()
        return deck_data
    return None


def tirer_une_carte(id_deck):
    tirage_url = f'https://www.deckofcardsapi.com/api/deck/{id_deck}/draw/?count=36'
    response = requests.get(tirage_url)
    if response.status_code == 200:
        # Charger les données JSON
        carte_data = response.json()
        return carte_data
    return None


@app.route('/')
def index():
    # Appeler la fonction pour initialiser le deck et récupérer les données
    deck_data = init_deck()

    # Vérifier si les données du deck ont été récupérées avec succès
    if deck_data:
        # Appeler la fonction pour tirer une carte du deck spécifié
        carte = tirer_une_carte(deck_data['deck_id'])

        # Vérifier si les données de la carte ont été récupérées avec succès
        if carte:
            return render_template('index.html', carte_data=carte, liste_valeur=LISTE_VALUE)
        else:
            return "Erreur lors du tirage de la carte."
    else:
        return "Erreur lors de la récupération des données du deck."


if __name__ == '__main__':
    app.run(debug=True)
