from peewee import IntegerField, ForeignKeyField

from database.models.base import BaseModel


class User(BaseModel):
    tg_id = IntegerField()


class ChatToSend(BaseModel):
    tg_id = IntegerField()
    user = ForeignKeyField(User, backref="chats")
