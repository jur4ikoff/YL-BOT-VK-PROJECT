import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    bdate = sqlalchemy.Column(sqlalchemy.String)
    sex = sqlalchemy.Column(sqlalchemy.String)
    # email = sqlalchemy.Column(sqlalchemy.String,
    #                          index=True, unique=True, nullable=True)
    # age = sqlalchemy.Column(sqlalchemy.Integer,
    #                       index=True, nullable=True, unique=False)
    # position = sqlalchemy.Column(sqlalchemy.String,
    #                             index=True, nullable=True)
    # speciality = sqlalchemy.Column(sqlalchemy.String,
    #                               index=True, nullable=True)
    # address = sqlalchemy.Column(sqlalchemy.String,
    #                            index=True, nullable=True)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # news = orm.relation("News", back_populates='user')
