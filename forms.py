from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from models import db, Joueur


class FormulaireInscription(FlaskForm):
    pseudo = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Pseudo"})
    mot_de_passe = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("S'inscrire")

    def validate_pseudo(self, pseudo):
        pseudo_existant = Joueur.query.filter_by(pseudo=pseudo.data).first()
        if pseudo_existant:
            raise ValidationError("Le pseudo est déjà pris. Choisissez en un autre.")


class FormulaireConnexion(FlaskForm):
    pseudo = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Pseudo"})
    mot_de_passe = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("Se connecter")
