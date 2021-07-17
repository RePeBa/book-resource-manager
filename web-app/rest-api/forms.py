from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=40)])

    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=60)])

    submit = SubmitField('Save')


