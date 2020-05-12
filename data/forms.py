from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])

    surname = StringField('*Фамилия')
    name = StringField('*Имя')
    address = StringField('*Адрес')

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('*Описание')
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'gif'],
                                                             'Выберите изображение')])
    price = IntegerField('Цена (₽)', validators=[DataRequired()])
    amount = IntegerField('*Кол-во на складе', default=0)
    submit = SubmitField('Сохранить')


class ChangeBalance(FlaskForm):
    amount = IntegerField('Количество (₽)', validators=[DataRequired()])
    submit = SubmitField('Добавить')
