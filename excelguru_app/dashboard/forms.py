from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
class DashboardForm(FlaskForm):
    info_prompt = SelectField('Was möchtest du generieren?', validators=[DataRequired()], choices=["Formel", "VBA"], render_kw={'class': 'btn-group-toggle', 'data-toggle': 'buttons'})
    prompt = TextAreaField('Funktion die Zelle A1 mit Zelle B1 summiert z.B.', validators=[DataRequired(), Length(max=400)], render_kw={"style": "min-height: 10rem;"})
    submit = SubmitField('Formel')  