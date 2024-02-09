from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import generate_csrf
from forms import FormulaireInscription, FormulaireConnexion, FormGameOver
from models import db, Joueur, update_score, fetch_info_joueur, historique_points, fetch_best_score
from PIL import Image, ImageDraw
from io import BytesIO
import random
import requests

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
    # db.drop_all()
    db.create_all()

LISTE_SUIT = ['H', 'S', 'D', 'C']
LISTE_VALUE = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6']
URL_DOS_CARTE = "https://www.deckofcardsapi.com/static/img/back.png"
LISTE_SYMBOLE = ["./static/images/coeur.png", "./static/images/pique.png", "./static/images/carreau.png",
                 "./static/images/trefle.png"]


def generate_profile_picture():
    # Create a blank image
    image = Image.new("RGBA", (226, 314), (255, 255, 255, 0))  # RGBA format with a transparent background
    draw = ImageDraw.Draw(image)

    deck_data = init_deck()
    id_deck = deck_data['deck_id']
    carte_data = tirer_les_cartes(id_deck, 1)

    if carte_data is not None:
        card_path = carte_data['cards'][0]['image']
        response = requests.get(card_path)

        if response.status_code == 200:
            # Open the card image
            card = Image.open(BytesIO(response.content))
            card = card.resize((135, 190))  # Adjust the size of the card as needed

            # Randomly choose a color
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)  # RGBA format

            # Draw a circular background
            draw.ellipse([(0, 0), (226, 314)], fill=color)

            # Calculate the position to center the card on the circular background
            card_position = ((226 - card.width) // 2, (314 - card.height) // 2)

            # Paste the resized card image onto the circular background
            image.paste(card, card_position, mask=card)

            # Save the image to a BytesIO object
            image_data = BytesIO()
            image.save(image_data, format='PNG')

            # Return the image data as bytes
            return image_data.getvalue()

    raise ValueError("API n'a pas ramené de carte")


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


def tirer_les_cartes(id_deck, nb_cartes=36):
    tirage_url = f'https://www.deckofcardsapi.com/api/deck/{id_deck}/draw/?count={nb_cartes}'
    response = requests.get(tirage_url)
    if response.status_code == 200:
        carte_data = response.json()
        return carte_data
    return None


@app.route('/jeu', methods=['GET', 'POST'])
@login_required
def jeu():
    form = FormGameOver()
    form.csrf_token.data = generate_csrf()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id
            update_score(user_id, form.points.data)
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
            if current_user.is_authenticated:
                info_joueur = fetch_info_joueur(current_user.id)
                historique_point = historique_points(current_user.id)
                meilleur_score = fetch_best_score(current_user.id)
                return render_template('jeu.html', carte_data=cartes, liste_valeur=LISTE_VALUE, dos_carte=URL_DOS_CARTE,
                                       liste=LISTE_SYMBOLE, liste_pos_correct=liste, form=form, info_joueur=info_joueur,
                                       historique_point=historique_point, meilleur_score=meilleur_score)
        else:
            return "Erreur lors du tirage de la carte."
    else:
        return "Erreur lors de la récupération des données du deck."


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = FormulaireInscription()
    if form.validate_on_submit():
        photo_profil = generate_profile_picture()
        print("Type de photo_profil:", type(photo_profil))
        mdp_crypte = bcrypt.generate_password_hash(form.mot_de_passe.data)
        nouveau_joueur = Joueur(pseudo=form.pseudo.data, mot_de_passe=mdp_crypte, meilleur_score=0,
                                photo_profil=photo_profil)
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
