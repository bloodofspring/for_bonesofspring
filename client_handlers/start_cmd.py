from client_handlers.base import *
from datetime import datetime, time

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
        max_ = max(map(lambda t: t.send_time, nearest))
        same_max_operations = tuple(filter(lambda t: t.send_time == max_, nearest))

        return map(lambda t: t.oper[0], same_max_operations)

    async def func(self):
        await self.request.answer("Бот запущен!\nБлижайшая операция: {}")
