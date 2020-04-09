from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.__all_models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return redirect('/shop')


@app.route('/shop')
def shop():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Магазин')


@app.route('/shop/test')
def shop_test():
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

    ses = db_session.create_session()

    app.run()


if __name__ == '__main__':
    main()
