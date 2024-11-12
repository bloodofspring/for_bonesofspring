from peewee import ForeignKeyField

from database.models import Users, SendTime
from database.models.base import BaseModel


class CreatedTimePoints(BaseModel):
    user = ForeignKeyField(Users, backref="created_tp")
    time_point = ForeignKeyField(SendTime)
