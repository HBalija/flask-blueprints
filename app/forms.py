from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length, Optional
from wtforms.widgets import TextArea


class NameForm(FlaskForm):
    name = StringField(
        'Add user name:', validators=[Required(), Length(1, 16)])
    description = StringField(
        'Short description', widget=TextArea(),
        validators=[Optional(), Length(max=200)])
    submit = SubmitField('Submit')
