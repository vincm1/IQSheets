from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
class DashboardForm(FlaskForm):
    excel_google = info_prompt = SelectField('Was möchtest du generieren?', validators=[DataRequired()], choices=["Excel", "Google Sheets"], render_kw={'class': 'btn-group-toggle', 'data-toggle': 'buttons'})
    info_prompt = SelectField('Was möchtest du generieren?', validators=[DataRequired()], choices=["Formel", "VBA"], render_kw={'class': 'btn-group-toggle', 'data-toggle': 'buttons'})
    formula_explain = SelectField('Formel oder Erklärung', validators=[DataRequired()], choices=["Erstellen", "Erklären"], render_kw={'class': 'btn-group-toggle', 'data-toggle': 'buttons'})
    prompt = TextAreaField('Funktion die Zelle A1 mit Zelle B1 summiert z.B.', validators=[DataRequired(), Length(max=400)], render_kw={"style": "min-height: 10rem;"})
    submit = SubmitField('Formel')  
class FavoritesForm(FlaskForm):
    favorite_method = HiddenField()
    favorite_type = HiddenField()
    command = HiddenField()
    prompt = HiddenField()
    submit = SubmitField()  