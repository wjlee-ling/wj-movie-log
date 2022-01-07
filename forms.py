from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    # to-do: add 'date'
    user_name = StringField(label='작성자', default='구경꾼', validators=[DataRequired()])
    #user_email = StringField(label='이메일', validators=[Email()])
    comment = TextAreaField(label='댓글', validators=[DataRequired()])
    submit = SubmitField(label='submit')
    