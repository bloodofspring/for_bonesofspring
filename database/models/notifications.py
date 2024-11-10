from peewee import CharField, BooleanField, IntegerField, ForeignKeyField, DateField, TimeField

from database.models.base import BaseModel


class SendTime(BaseModel):
    send_date = DateField()
    send_time = TimeField()
    consider_date = BooleanField()
    weekday = IntegerField()  # pass -1 if week day is unimportant
    delete_after_execution = BooleanField()


class ChatToSend(BaseModel):
    tg_id = IntegerField()


class Notifications(BaseModel):
    text = CharField()
    send_time = ForeignKeyField(SendTime, backref="oper")
    chat_to_send = ForeignKeyField(ChatToSend, backref="oper")
