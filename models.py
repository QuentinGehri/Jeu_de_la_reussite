from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 'login' est le nom de la route de connexion de votre application


class Joueur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(20), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(80), nullable=False)
    meilleur_score = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Joueur.query.get(int(user_id))


@app.route('/update_score/<int:user_id>/<int:new_score>')
def update_score(user_id, new_score):
    # Rechercher l'utilisateur dans la base de données
    user = Joueur.query.get(user_id)
    if user:
        # Mettre à jour la colonne du meilleur score
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

