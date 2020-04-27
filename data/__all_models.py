import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    purchase_history = sqlalchemy.Column(sqlalchemy.String, default='')
    cart = sqlalchemy.Column(sqlalchemy.String, default='')
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # access_level: 0 - user, 1 - admin, 2 - owner
    access_level = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    purchase_amount = sqlalchemy.Column(sqlalchemy.PickleType, default=0)

    tags = orm.relation("Tag",
                        secondary="products_to_tags",
                        backref="products")


class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    association_table = sqlalchemy.Table('products_to_tags', SqlAlchemyBase.metadata,
                                         sqlalchemy.Column('products', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('products.id')),
                                         sqlalchemy.Column('tags', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('tags.id'))
                                         )
