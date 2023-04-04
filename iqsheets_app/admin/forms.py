from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
### File Upload Form for admin page ###

category_choices = ["Business", "Produktivität", "Projektmanagement", "Zeitmanagement"]
class TemplatesForm(FlaskForm):
    template_name = FileField('Template', validators=[DataRequired()])
    template_category = SelectField('Kategorie', choices=category_choices, validators=[DataRequired()])
    template_description = TextAreaField('Beschreibung', validators=[DataRequired()])
    submit = SubmitField('Hochladen')    
    