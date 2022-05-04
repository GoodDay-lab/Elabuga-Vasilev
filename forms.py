from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    surname = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    motivation = TextAreaField('Мотивация')
    # sex = RadioField('Пол', validators=[DataRequired()])
    submit = SubmitField('Заргаться')


class Authorization(FlaskForm):
    austronaut_id = StringField("ID астронавта", validators=[DataRequired()])
    austronaut_passw = PasswordField("Пароль астронавта", validators=[DataRequired()])
    capitain_id = StringField("ID капитана", validators=[DataRequired()])
    capitain_passw = PasswordField("Пароль капитана", validators=[DataRequired()])
    submit = SubmitField("Доступ")


class UploadForm(FlaskForm):
    file = FileField("Прикрепите файл", validators=[DataRequired()])
    submit = SubmitField("Отправить")
