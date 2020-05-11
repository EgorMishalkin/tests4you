import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase



class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    long_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    add = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    questions = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    final_grade = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)






