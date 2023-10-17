""" Forms for DB """
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

class DashboardForm(FlaskForm):
    excel_google = RadioField('Die Formel/Erklärung ist für...?', validators=[DataRequired()], choices=["Excel", "Google Sheets"], render_kw={'class': 'form-check-input'})
    info_prompt = RadioField('Was möchtest du generieren?', validators=[DataRequired()], choices=["Formel", "VBA"], render_kw={'class': 'form-check-input'})
    formula_explain = RadioField('Formel oder Erklärung', validators=[DataRequired()], choices=["Erstellen", "Erklären"], render_kw={'class': 'form-check-input'})
    prompt = TextAreaField('Welches Problem versuchen Sie zu lösen oder welche Formel wollen Sie verstehen? Versuchen Sie, so genau wie möglich zu sein.', validators=[DataRequired(), Length(min=10, max=400)], render_kw={"style": "min-height: 10rem;"})
    submit = SubmitField('Formel generieren')  
class FeedbackForm(FlaskForm):
    provider = HiddenField()
    favorite_type = HiddenField()
    method = HiddenField()
    command = HiddenField()
    prompt  = HiddenField()
    submit = SubmitField('Favoriten')  
