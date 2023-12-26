from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
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


class FormGameOver(FlaskForm):
    points = HiddenField('Points')
    csrf_token = HiddenField()
    submit_hidden = SubmitField('Recommencer', render_kw={'style': 'display:none;'})

    def to_js(self):
        return {
            'points': self.points.data,
            'csrf_token': self.csrf_token.data,
            'submit_label': self.submit_hidden.label.text,
            # Add more fields as needed
        }
