from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp
from excelguru_app.models import User

#### Checks: Nutzername & Email bereits vorhanden. ####
def check_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError(f'Nutzername bereits registriert!')
        
def check_email(self, field):
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
    username = StringField('Username', validators=[DataRequired(), check_username])
    email = EmailField('Email', validators=[Email(), DataRequired(), check_email])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, message="Mindestens 8 Zeichen!"), 
                            EqualTo('confirm_pw', message="Passwörter stimmen nicht überein!"),
                            Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", message="Passwort muss Sonderzeichen, Groß-Kleinschreibung.")])
    confirm_pw = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Speichern')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Neues Passwort')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[DataRequired(), Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])", 
                            message="Passwort muss Sonderzeichen, Groß-Kleinschreibung.")])
    confirm_pw = PasswordField('Wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Passwort bestätigen')

class DashboardForm(FlaskForm):
    info_prompt = SelectField('Was möchtest du generieren?', choices=["Formel", "VBA"], render_kw={'class': 'btn-group-toggle', 'data-toggle': 'buttons'})
    prompt = TextAreaField('Funktion die Zelle A1 mit Zelle B1 summiert z.B.', validators=[DataRequired(), Length(max=400)])
    submit = SubmitField('Formel')  