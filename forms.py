from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    surname = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    motivation = TextAreaField('Мотивация')
    # sex = RadioField('Пол', validators=[DataRequired()])
    submit = SubmitField('Войти')
