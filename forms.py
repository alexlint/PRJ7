from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    search = StringField(' ',validators=[DataRequired( )])
    submit = SubmitField(u'go!')

