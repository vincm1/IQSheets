""" User forms """
from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FileField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp, Optional
from iqsheets_app.models import User

#### Checks: Nutzername & Email bereits vorhanden. ####
def check_username(self, field):
    """ check if username already registered """
    if User.query.filter_by(username=field.data).first():
        raise ValidationError(f'Nutzername bereits registriert!')
        
def check_email(self, field):
    """ check if email aready registered """
    if User.query.filter_by(email=field.data).first():
        raise ValidationError(f'Email bereits registriert!')
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), check_username])
    email = EmailField('Email', validators=[Email(), DataRequired(), check_email])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"), 
                            EqualTo('confirm_pw', message="Passwörter stimmen nicht überein!"),
                            Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", message="Passwort muss Sonderzeichen, Groß-Kleinschreibung.")])
    confirm_pw = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Registrieren')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[ Optional(), check_username])
    email = EmailField('Email', validators=[Email(), Optional(), check_email])
    job_description = StringField('Berufsbezeichnung', validators=[Optional()])
    profile_picture = FileField('Profilbild', render_kw={'accept': 'image/*', 'class': 'd-none'}, id='file-input')
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_picture.label = Markup('<i class="bx bx-camera"></i>')
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Altes Passwort', validators=[DataRequired()])
    password = PasswordField('Neues Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"),
                            Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", 
                                   message="Passwort muss Sonderzeichen & Groß-Kleinschreibung enthalten.")])
    confirm_pw = PasswordField('Neues Passwort bestätigen', validators=[DataRequired(),
                                EqualTo('password', message='Passwörter stimmen nicht überein!.')])
    submit = SubmitField('Passwort speichern')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Keine valide Emailadresse!")])
    submit = SubmitField('Weiter')
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"),
                                                           Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", 
                                                                message="Passwort muss Sonderzeichen, Groß-Kleinschreibung enthalten.")])
    confirm_pw = PasswordField('Wiederholen', validators=[DataRequired(), EqualTo('password', message="Passwörter stimmen nicht überein!")])
    submit = SubmitField('Passwort bestätigen')
