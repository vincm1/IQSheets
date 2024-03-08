""" User forms """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp, Optional
from iqsheets_app.models import User

#### Check: Email bereits vorhanden. ####
def check_email(self, field):
    """ check if email aready registered """
    if User.query.filter_by(email=field.data).first():
        raise ValidationError(f'Email bereits registriert!')
class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired(), check_email])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"), 
                            EqualTo('confirm_pw', message="Passwörter stimmen nicht überein!"),
                            Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", message="Passwort muss Sonderzeichen, Groß-Kleinschreibung.")])
    confirm_pw = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Registrieren')
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember = BooleanField(default="checked", description="Lorem")
    submit = SubmitField('Login')
    
class EditUserForm(FlaskForm):
    firstname = StringField('Vorname', validators=[Optional()], )
    lastname = StringField('Nachname', validators=[ Optional()])
    job_description = StringField('Berufsbezeichnung', validators=[Optional()])
    submit = SubmitField('Speichern')
    
class EditUserEmailForm(FlaskForm):
    new_email = EmailField('Email', validators=[Email(), check_email])
    new_email_confirm = EmailField('Email', validators=[Email(), EqualTo('new_email', message="E-mail Adressen stimmen nicht überein!")])
    submit = SubmitField('Speichern')
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Altes Passwort', validators=[DataRequired()])
    password = PasswordField('Neues Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"),
                            Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", 
                                   message="Passwort muss Sonderzeichen & Groß-Kleinschreibung enthalten."),
                            EqualTo('confirm_pw', message='Passwörter stimmen nicht überein!.')])
    confirm_pw = PasswordField('Neues Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Passwort speichern')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Keine valide Emailadresse!")])
    submit = SubmitField('Passwort zurücksetzen')
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"),
                                                           Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", 
                                                                message="Passwort muss Sonderzeichen, Groß-Kleinschreibung enthalten.")])
    confirm_pw = PasswordField('Wiederholen', validators=[DataRequired(), EqualTo('password', message="Passwörter stimmen nicht überein!")])
    submit = SubmitField('Passwort bestätigen')
