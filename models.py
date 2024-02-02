from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy import LargeBinary
import base64

db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 'login' est le nom de la route de connexion de votre application


class Joueur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(20), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(80), nullable=False)
    meilleur_score = db.Column(db.Integer, nullable=False)
    photo_profil = db.Column(db.LargeBinary)
    scores = db.relationship('ScoreJoueur', backref='joueur', lazy=True)


class ScoreJoueur(db.Model, UserMixin):
    id_score = db.Column(db.Integer, primary_key=True)
    id_joueur = db.Column(db.Integer, db.ForeignKey('joueur.id'), nullable=False)
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)


class Score(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    score_joueurs = db.relationship('ScoreJoueur', backref='score', lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return Joueur.query.get(int(user_id))


@app.route('/fetch_info_joueur/<int:player_id>', methods=['GET'])
def fetch_info_joueur(player_id):
    player = Joueur.query.filter_by(id=player_id).first()
    if player:
        player_info = {
            'pseudo': player.pseudo,
            'meilleur_score': player.meilleur_score,
            'photo_profil': base64.b64encode(player.photo_profil).decode('utf-8'),
        }
        return player_info
    else:
        return "Utilisateur non trouvé"


@app.route('/historique_points/<int:user_id>', methods=['GET'])
def historique_points(user_id):
    # Rechercher l'utilisateur dans la base de données
    user = Joueur.query.get(user_id)
    if user:
        # Récupérer l'historique des points du joueur
        scores_joueur = ScoreJoueur.query.filter_by(id_joueur=user_id).all()
        # Retrieve only the last 5 entries
        last_5_entries = [{'score': score.score.score} for score in scores_joueur[-5:]][::-1]
        return jsonify({'historique': last_5_entries})
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404


def get_best_score(user_id):
    user = Joueur.query.get(user_id)
    if user:
        return jsonify({'best_score': user.meilleur_score})
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404


@app.route('/best_score/<int:user_id>', methods=['GET'])
def fetch_best_score(user_id):
    return get_best_score(user_id)


@app.route('/update_score/<int:user_id>/<int:new_score>')
def update_score(user_id, new_score):
    # Rechercher l'utilisateur dans la base de données
    user = Joueur.query.get(user_id)
    if user:
        # Mettre à jour la colonne du meilleur score
        score = Score.query.filter_by(score=new_score).first()
        if not score:
            # Si le score n'existe pas, le créer
            score = Score(score=new_score)
            db.session.add(score)
            db.session.commit()
        # Vérifier si le lien entre le joueur et le score existe dans la table ScoreJoueur
        link_exists = ScoreJoueur.query.filter_by(id_joueur=user_id, score_id=score.id).first()
        if not link_exists:
            # Si le lien n'existe pas, le créer
            score_joueur = ScoreJoueur(id_joueur=user_id, score_id=score.id)
            db.session.add(score_joueur)
            db.session.commit()
        meilleur_score = user.meilleur_score
        if int(meilleur_score) < int(new_score):
            user.meilleur_score = new_score
            # Commit des modifications dans la base de données
            db.session.commit()
            return f"Le meilleur score de {user.pseudo} a été mis à jour : {user.meilleur_score}"
        else :
            return f"Le score est moins bien qu'avant"
    else:
        return "Utilisateur non trouvé"

