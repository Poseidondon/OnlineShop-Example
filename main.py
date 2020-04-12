from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.__all_models import *
from data.forms import *

from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return redirect('/shop')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='BNS | Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='BNS | Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='BNS | Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='BNS | Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='BNS | Регистрация', form=form)


@app.route('/profile')
def profile():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Личный кабинет')


@app.route('/shop')
def shop():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Магазин')


@app.route('/configurator')
def configurator():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Конфигуратор')


@app.route('/configurations')
def configurations():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Сборки')


@app.route('/cart')
def cart():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Корзина')


def main():
    db_session.global_init("db/shop.sqlite")

    session = db_session.create_session()
    for user in session.query(User):
        pprint(user.__dict__)

    app.run()


if __name__ == '__main__':
    main()
