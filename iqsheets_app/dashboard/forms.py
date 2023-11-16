""" Forms for DB """
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

class DashboardForm(FlaskForm):
    excel_google = RadioField('Die Formel/Erklärung ist für...?', validators=[DataRequired()], choices=["Excel", "Google Sheets"], render_kw={'class': 'form-select-input'})
    formula_explain = RadioField('Formel oder Erklärung', validators=[DataRequired()], choices=["Erstellen", "Erklären"], render_kw={'class': 'form-select-input'})
    prompt = TextAreaField('Beschreiben Sie die Formel, die Sie erstellen möchten. Versuchen Sie, so detailliert wie möglich zu sein.', validators=[DataRequired(), Length(min=10, max=400)], render_kw={"style": "min-height: 10rem;"})
    submit = SubmitField('Formel generieren')  
class FeedbackForm(FlaskForm):
    provider = HiddenField()
    favorite_type = HiddenField()
    method = HiddenField()
    command = HiddenField()
    prompt  = HiddenField()
    submit = SubmitField('Favoriten')  
