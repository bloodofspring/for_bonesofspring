from datetime import datetime

from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

from client_handlers.base import *
from database.models import SendTime
from util import render_notification, clear_unused_time_points


class StartCmd(BaseHandler):
    FILTER = command("start")

    @property
    def nearest_times(self):
        now = datetime.now()
        nearest = SendTime.select().where(
            ((SendTime.consider_date & SendTime.send_date == now.date()) |
             (SendTime.weekday.between(0, 6) & SendTime.weekday == now.weekday())) &
            (SendTime.send_time >= now.time())
        ).order_by(SendTime.send_time)

        return nearest

    @property
    def nearest_missions(self):
        nearest = self.nearest_times
        min_ = min(map(lambda t: t.send_time, nearest))
        same_min_operations = tuple(filter(lambda t: t.send_time == min_, nearest))

        return map(lambda t: t.oper[0], same_min_operations)

    @property
    def nearest_mission_for_current_user(self):
        nearest = self.nearest_times
        user = self.db_user
        clear_unused_time_points(user=user)

        a = map(lambda t: t.oper[0], nearest)
        b = filter(lambda o: o.created_by == user, a)
        c = min(b, key=lambda o: o.send_at.send_time)

        return c

    async def func(self):
        keyboard = ReplyKeyboardMarkup([
            [KeyboardButton("Добавить напоминание"), KeyboardButton("Мои напоминания")],
        ])
        await self.request.reply(
            render_notification(self.nearest_mission_for_current_user),
            reply_markup=keyboard
        )
