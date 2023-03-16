import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Picture(SqlAlchemyBase, UserMixin):
    __tablename__ = 'pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer)
    picture = sqlalchemy.Column(sqlalchemy.Binary)
