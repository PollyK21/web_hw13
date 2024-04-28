from sqlalchemy import Column, Integer, String, func, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        UniqueConstraint('id', 'user_id', name='unique_tag_user'),
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="tags")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
