from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
### File Upload Form for admin page ###
class TemplatesForm(FlaskForm):
    template = FileField('Template', validators=[DataRequired()])
    submit = SubmitField('Hochladen')    
    