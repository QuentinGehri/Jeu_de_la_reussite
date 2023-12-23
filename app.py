from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import FormulaireInscription, FormulaireConnexion
from models import db, Joueur
import requests
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdd.db'
app.config['SECRET_KEY'] = 'sixtrefle'
db.init_app(app)
bcrypt = Bcrypt(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "connexion"


@login_manager.user_loader
def load_user(id_joueur):
    return Joueur.query.get(int(id_joueur))


with app.app_context():
    db.create_all()

LISTE_SUIT = ['H', 'S', 'D', 'C']
LISTE_VALUE = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6']
URL_DOS_CARTE = "https://www.deckofcardsapi.com/static/img/back.png"
LISTE_SYMBOLE = ["./static/images/coeur.png", "./static/images/pique.png", "./static/images/carreau.png",
                 "./static/images/trefle.png"]


def init_deck():
    cartes = ''
    for suit in LISTE_SUIT:
        for value in LISTE_VALUE:
            cartes += str(value) + str(suit)
            if not (suit == LISTE_SUIT[-1] and value == LISTE_VALUE[-1]):
                cartes += ','
    deck_url = f'https://www.deckofcardsapi.com/api/deck/new/shuffle/?cards={cartes}'
    response = requests.get(deck_url)
    if response.status_code == 200:
        deck_data = response.json()
        return deck_data
    return None


def tirer_les_cartes(id_deck):
    tirage_url = f'https://www.deckofcardsapi.com/api/deck/{id_deck}/draw/?count=36'
    response = requests.get(tirage_url)
    if response.status_code == 200:
        carte_data = response.json()
        return carte_data
    return None


@app.route('/jeu')
@login_required
def jeu():
    deck_data = init_deck()
    if deck_data:
        cartes = tirer_les_cartes(deck_data['deck_id'])
        if cartes:
            # tableau_position_correct = np.empty((4, 9), dtype=object)
            liste = []
            for s in range(len(LISTE_SUIT)):
                for v in range(len(LISTE_VALUE)):
                    # tableau_position_correct[s][v] = value + LISTE_SUIT[s]
                    liste.append(LISTE_VALUE[v] + LISTE_SUIT[s])
            print(liste)
            return render_template('jeu.html', carte_data=cartes, liste_valeur=LISTE_VALUE, dos_carte=URL_DOS_CARTE,
                                   liste=LISTE_SYMBOLE, liste_pos_correct=liste)
        else:
            return "Erreur lors du tirage de la carte."
    else:
        return "Erreur lors de la récupération des données du deck."


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = FormulaireInscription()
    if form.validate_on_submit():
        mdp_crypte = bcrypt.generate_password_hash(form.mot_de_passe.data)
        nouveau_joueur = Joueur(pseudo=form.pseudo.data, mot_de_passe=mdp_crypte, meilleur_score=0)
        db.session.add(nouveau_joueur)
        db.session.commit()
        login_user(nouveau_joueur)
        return redirect(url_for('jeu'))
    return render_template('register.html', form=form)


@app.route('/deconnexion', methods=['GET', 'POST'])
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))


@app.route('/', methods=['GET', 'POST'])
def connexion():
    form = FormulaireConnexion()
    if form.validate_on_submit():
        joueur_connecte = Joueur.query.filter_by(pseudo=form.pseudo.data).first()
        if joueur_connecte:
            if bcrypt.check_password_hash(joueur_connecte.mot_de_passe, form.mot_de_passe.data):
                login_user(joueur_connecte)
                return redirect(url_for('jeu'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
