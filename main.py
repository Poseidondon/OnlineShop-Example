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


def change_url_args(url, arg, value, mode='change'):
    if mode == 'change':
        if '?' in url:
            args = list(filter(lambda x: arg not in x, url.split('?')[1].split('&')))
            return '?' + '&'.join(sorted(args + [arg + '=' + value]))
        return '?' + arg + '=' + value
    elif mode == 'change_list':
        if '?' in url:
            args = list(filter(lambda x: arg not in x, request.url.split('?')[1].split('&')))
            return '?' + '&'.join(sorted(args + [arg + '=' + i for i in value]))
        return '?' + '&'.join(sorted([arg + '=' + i for i in value]))


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
    return redirect(request.url_root)


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
@login_required
def profile():
    session = db_session.create_session()
    return render_template('base.html', title='BNS | Личный кабинет')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    session = db_session.create_session()
    products = session.query(Product).all()
    tags = session.query(Tag).all()
    filter_args = request.args.getlist('tags-filter')

    if request.method == 'POST':
        tag_filter = request.form.getlist('tags-filter')
        return redirect(change_url_args(request.url, 'tags-filter', tag_filter, mode='change_list'))

    if request.args.get('order'):
        order = request.args.get('order')
    else:
        order = 0

    return render_template('shop.html', title='BNS | Магазин', products=products, order=order,
                           change_url_args=change_url_args, tags=tags, filter=filter_args)


@app.route('/shop/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.access_level < 1:
        abort(403)

    session = db_session.create_session()
    form = AddProductForum()
    if form.validate_on_submit():
        if session.query(Product).filter(Product.name == form.name.data).first():
            return render_template('add_product.html', title='BNS | Добавить продукт',
                                   form=form, tags=session.query(Tag),
                                   message="Товар с таким названием уже есть")
        product = Product(name=form.name.data,
                          description=form.description.data,
                          image=form.image.data.read(),
                          price=form.price.data,
                          amount=form.amount.data)
        for tag in request.form.getlist('tags'):
            if session.query(Tag).filter(Tag.name == tag).first():
                new_tag = session.query(Tag).filter(Tag.name == tag).first()
            else:
                new_tag = Tag(name=tag)
                session.add(new_tag)
            product.tags.append(new_tag)
        session.add(product)
        session.commit()
        return redirect('/shop')
    return render_template('add_product.html', title='BNS | Добавить продукт', form=form, tags=session.query(Tag))


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
    for user in session.query(Product):
        pprint(user.tags)

    app.run()


if __name__ == '__main__':
    main()
