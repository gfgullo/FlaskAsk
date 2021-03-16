from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, length


class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=100)])
    body = StringField("Write your question", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Publish')


class AnswerForm(FlaskForm):
    body = StringField("Write your answer", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Publish')
