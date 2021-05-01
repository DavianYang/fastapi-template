from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
from app.domain.user import User

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(60), nullable=False),
    Column('email', String(255), nullable=False),
    Column('photo', String(255), nullable=True),
    Column('password', String(255), nullable=False),
    Column('password_changed', String(255), nullable=False)
)

def start_mappers():
    user_mapper = mapper(User, users)