from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, TextAreaField, SubmitField, DateField, SelectMultipleField
from wtforms.validators import DataRequired
### File Upload Form for admin page ###

category_choices = ["Business", "Produktivität", "Projektmanagement", "Zeitmanagement"]
class TemplatesForm(FlaskForm):
    template_name = FileField('Template', validators=[DataRequired()])
    template_category = SelectField('Kategorie', choices=category_choices, validators=[DataRequired()])
    template_description = TextAreaField('Beschreibung', validators=[DataRequired()])
    submit = SubmitField('Hochladen')    


class PromptForm(FlaskForm):
    start_date = DateField('start', validators=[DataRequired()])
    end_date = DateField('end', validators=[DataRequired()])
    submit = SubmitField('Pick dates')    

class FineTuneForm(FlaskForm):
    prompt = SelectMultipleField(validators=[DataRequired()])
    submit = SubmitField('Finetune')