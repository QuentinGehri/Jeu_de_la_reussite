from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdd.db'
app.config['SECRET_KEY'] = 'sixtrefle'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(id_joueur):
    return joueur.query.get(int(id_joueur))

class joueur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(20), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(80), nullable=False)


class FormulaireInscription(FlaskForm):
    pseudo = StringField(validators=[InputRequired(), Length(min=4, max=20)]
                         , render_kw={"placeholder": "Pseudo"})
    mot_de_passe = PasswordField(validators=[InputRequired(), Length(min=4, max=20)]
                               , render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("S'inscrire")

    def valider_pseudo(self, pseudo):
        pseudo_existant = joueur.query.filter_by(pseudo=pseudo.data).first()
        if pseudo_existant:
            raise ValidationError("Le pseudo est déjà pris. Choisissez en un autre.")

class FormulaireConnexion(FlaskForm):
    pseudo = StringField(validators=[InputRequired(), Length(min=4, max=20)]
                         , render_kw={"placeholder": "Pseudo"})
    mot_de_passe = PasswordField(validators=[InputRequired(), Length(min=4, max=20)]
                               , render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("Se connecter")

LISTE_SUIT = ['H', 'S', 'D', 'C']
LISTE_VALUE = ['A', 'K', 'Q', 'J', '0', '9', '8', '7', '6']

def create_app():
    with app.app_context():
        # Import the model inside the app context
        from your_module import joueur
        db.create_all()


def init_deck():
    # deck_url = 'https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
    cartes = ''
    for suit in LISTE_SUIT:
        for value in LISTE_VALUE:
            cartes += str(value) + str(suit)
            # Ajouter une virgule si ce n'est pas la dernière combinaison
            if not (suit == LISTE_SUIT[-1] and value == LISTE_VALUE[-1]):
                cartes += ','
    deck_url = f'https://www.deckofcardsapi.com/api/deck/new/shuffle/?cards={cartes}'
    response = requests.get(deck_url)
    if response.status_code == 200:
        # Charger les données JSON
        deck_data = response.json()
        return deck_data
    return None


def tirer_les_cartes(id_deck):
    tirage_url = f'https://www.deckofcardsapi.com/api/deck/{id_deck}/draw/?count=36'
    response = requests.get(tirage_url)
    if response.status_code == 200:
        # Charger les données JSON
        carte_data = response.json()
        return carte_data
    return None


@app.route('/jeu')
@login_required
def jeu():
    # Appeler la fonction pour initialiser le deck et récupérer les données
    deck_data = init_deck()

    # Vérifier si les données du deck ont été récupérées avec succès
    if deck_data:
        # Appeler la fonction pour tirer les cartes du deck spécifiée
        cartes = tirer_les_cartes(deck_data['deck_id'])

        # Vérifier si les données de la carte ont été récupérées avec succès
        if cartes:
            return render_template('jeu.html', carte_data=cartes, liste_valeur=LISTE_VALUE)
        else:
            return "Erreur lors du tirage de la carte."
    else:
        return "Erreur lors de la récupération des données du deck."


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = FormulaireInscription()
    if form.validate_on_submit():
        mdp_crypte = bcrypt.generate_password_hash(form.mot_de_passe.data)
        nouveau_joueur = joueur(pseudo=form.pseudo.data, mot_de_passe=mdp_crypte)
        db.session.add(nouveau_joueur)
        db.session.commit()
        return redirect(url_for('connexion'))
    return render_template('register.html', form=form)

@app.route('/deconnexion', methods=['GET', 'POST'])
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))

@app.route('/', methods=['GET', 'POST'])
def connexion():
    form = FormulaireConnexion()
    if form.validate_on_submit():
        joueur_connecte = joueur.query.filter_by(pseudo=form.pseudo.data).first()
        if joueur_connecte:
            if bcrypt.check_password_hash(joueur_connecte.mot_de_passe, form.mot_de_passe.data):
                login_user(joueur_connecte)
                return redirect(url_for('jeu'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
