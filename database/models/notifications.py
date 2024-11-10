from peewee import CharField, DateTimeField, BooleanField, IntegerField, ForeignKeyField

from database.models.base import BaseModel


class SendTime(BaseModel):
    send_at = DateTimeField()
    consider_date = BooleanField()
    consider_week_day = BooleanField()


class ChatToSend(BaseModel):
    tg_id = IntegerField()

class Notifications(BaseModel):
    text = CharField()
    send_time = ForeignKeyField(SendTime)
    chat_to_send = ForeignKeyField(ChatToSend)
