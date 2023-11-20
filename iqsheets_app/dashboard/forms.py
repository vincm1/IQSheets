""" Forms for DB """
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

class FormelForm(FlaskForm):
    """ Form for Formel Generator """
    excel_google = RadioField('Die Formel ist für...?', validators=[DataRequired()], choices=["Excel", "Google Sheets"])
    formula_explain = RadioField('Formel oder Erklärung', validators=[DataRequired()], choices=["Erstellen", "Erklären"], render_kw={'class': 'form-select-input'})
    prompt = TextAreaField('Beschreiben Sie die Formel, die Sie erstellen möchten. Versuchen Sie, so detailliert wie möglich zu sein.', validators=[DataRequired(), Length(min=10, max=400)], render_kw={"style": "min-height: 10rem;"})
    submit = SubmitField('Formel generieren')
    
class SkriptForm(FlaskForm):
    """ Form for Skript Generator """
    vba_app = RadioField('Das Skript ist für...?', validators=[DataRequired()], 
                        choices=["Excel - VBA", "GSheets - Apps"])
    formula_explain = RadioField('Code oder Erklärung', validators=[DataRequired()], 
                                 choices=["Erstellen", "Erklären"], 
                                 render_kw={'class': 'form-select-input'})
    prompt = TextAreaField('Beschreibe das Skript, das du erstellen möchtest möglichst detailliert.',
                           validators=[DataRequired(), Length(min=10, max=400)],
                           render_kw={"style": "min-height: 10rem;",
                                      "placeholder":"z.B.: Erstelle mir ein Skript das alle Zellen < 100 EUR rot färbt."})
    submit = SubmitField('Formel generieren')

class SqlForm(FlaskForm):
    """ Form for Sql Generator """
    formula_explain = RadioField('Query erstellen oder Query erklären?...', validators=[DataRequired()], choices=["Erstellen", "Erklären"], render_kw={'class': 'form-select-input'})
    prompt = TextAreaField('Beschreibe die Query, die du erstellen möchtest so detailliert wie möglich.',
                           validators=[DataRequired(), Length(min=10, max=400)], 
                           render_kw={"style": "min-height: 10rem;",
                                      "placeholder": "z.B. Schreibe eine Query die alle Nutzer über 18J abfragt."})
    submit = SubmitField('Formel generieren')

class RegExForm(FlaskForm):
    """ Form for RegEx Generator """
    formula_explain = RadioField('RegEx erstellen oder Query erklären?...', validators=[DataRequired()], 
                                choices=["Erstellen", "Erklären"], render_kw={'class': 'form-select-input'})
    prompt = TextAreaField('Beschreibe die RegEx, die du erstellen möchtest möglichst detailliert.',
                            validators=[DataRequired(), Length(min=10, max=400)], 
                            render_kw={"style": "min-height: 10rem;",
                                       "placeholder": "z.B. Erstelle eine RegEx die prüft ob Sonderzeichen sowie Groß- und Kleinschreibung"})
    submit = SubmitField('Formel generieren')
    
class FeedbackForm(FlaskForm):
    """ Form for Formel Feedback by User """
    provider = HiddenField()
    favorite_type = HiddenField()
    method = HiddenField()
    command = HiddenField()
    prompt  = HiddenField()
    submit = SubmitField('Favoriten') 
