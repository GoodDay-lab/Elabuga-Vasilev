from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, DateField
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


class LoginForm2(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Job(FlaskForm):
    job = StringField("Название работы")
    work_size = StringField("Объём часов")
    collaborators = StringField("ID работников")
    start_date = DateField("Дата начала")
    end_date = DateField("Дата окончания")
    submit = SubmitField('Отправить')
