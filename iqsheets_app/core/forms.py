''' Landing Page forms '''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NewsletterForm(FlaskForm):
    email = StringField('Email Adresse', validators=[DataRequired(), Email()])
    submit = SubmitField()

class BetaTestForm(FlaskForm):
    email = StringField('Email Adresse', validators=[DataRequired(), Email()])
    submit = SubmitField()