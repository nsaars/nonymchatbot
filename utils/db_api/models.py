from aiogram.types import location
from sqlalchemy import sql, Column, Sequence, String, Integer, ForeignKey, DateTime, Text, JSON, BigInteger, \
    Binary, Boolean
from utils.db_api.database import db


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(BigInteger, Sequence("users_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(31))
    name = Column(String(31))
    reputation = Column(Integer, default=0)
    referral = Column(BigInteger, nullable=True)
    date_of_registration = Column(DateTime)

    grade = Column(Integer, nullable=True)
    gender = Column(Boolean, nullable=True)

    def __repr__(self):
        return f"""
            User: {self.id} - https://t.me/{self.username}
        """


class Message(db.Model):
    __tablename__ = "messages"
    query: sql.Select

    id = Column(BigInteger, Sequence("messages_id_seq"), primary_key=True)
    text = Column(Text, nullable=True)
    send_time = Column(DateTime)
    from_user_id = Column(BigInteger, ForeignKey("users", "id"))
    to_user_id = Column(BigInteger, ForeignKey("users", "id"))

    def __repr__(self):
        return f"""
            Message: {self.id} - {self.text}
        """


class Media(db.Model):
    __tablename__ = "medias"
    query: sql.Select

    id = Column(BigInteger, Sequence("medias_id_seq"), primary_key=True)
    caption = Column(Text, nullable=True)
    file_name = Column(String(63))
    file_information = Column(JSON)
    file_type = Column(String(15))
    file = Column(Binary)
    msg_id = Column(BigInteger, ForeignKey("messages", "id"))

    def __repr__(self):
        return f"""
            Media: {self.id} - {self.file_type}
        """


class Favorite(db.Model):
    __tablename__ = "favorites"
    query: sql.select

    id = Column(BigInteger, Sequence("favorites_id_seq"), primary_key=True)
    favorite_id = Column(BigInteger, ForeignKey("users", "id"))
    user_id = Column(BigInteger, ForeignKey("users", "id"))

    def __repr__(self):
        return f"""
            One of favorites of {self.user_id} is {self.favorite_id}
        """


class News(db.Model):
    __tablename__ = "news"
    query: sql.Select

    id = Column(BigInteger, Sequence("medias_id_seq"), primary_key=True)
    text = Column(Text)
    date = Column(DateTime)
