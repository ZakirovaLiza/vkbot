import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Bday(SqlAlchemyBase):
    __tablename__ = 'bdays'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=False, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    day = sqlalchemy.Column(sqlalchemy.Integer)
    month = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer)
