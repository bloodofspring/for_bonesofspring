from client_handlers.base import *
from datetime import datetime

from database.models import SendTime


class StartCmd(BaseHandler):
    FILTER = command("start")

    @property
    def nearest_missions(self):
        now = datetime.now()

        nearest = SendTime.select().where(
            ((SendTime.consider_date & SendTime.send_date == now.date()) |
            (SendTime.weekday.between(0, 6) & SendTime.weekday == now.weekday())) &
            (SendTime.send_time >= now.time())
        ).order_by(SendTime.send_time)

        return nearest[:]

    async def func(self):
        pass
