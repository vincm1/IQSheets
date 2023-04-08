''' Landing Page forms '''
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class NewsletterForm(FlaskForm):
    email = StringField('Email Adresse', validators=[DataRequired(), Email()])
    submit = SubmitField()
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Adresse', validators=[DataRequired(), Email()])
    betreff = StringField('Dein Anliegen / Feeback', validators=[DataRequired()])
    text = TextAreaField('Was möchtest du uns mitteilen.', validators=[DataRequired()])
    submit = SubmitField('Abschicken')