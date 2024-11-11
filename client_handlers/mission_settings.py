from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from client_handlers.base import *
from database.models import Notifications
from util import render_notification


class MissionsList(BaseHandler):
    FILTER = regex("Мои напоминания") | create(lambda _, __, q: q and q.data and q.data == "notifications_main")

    @property
    def keyboard(self):  # , page: int
        user = self.db_user
        all_n = Notifications.select().where(Notifications.created_by == user)
        keyboard = [[
            InlineKeyboardButton(
                n.text[:30] + ("..." if len(n.text) > 30 else ""),
                callback_data=f"at_mission {n.id}"
            )
        ] for _, n in enumerate(all_n, start=1)]

        return keyboard

    async def func(self):
        await self.request.reply(
            "",
            reply_markup=self.keyboard
        )


class Mission(BaseHandler):
    FILTER = create(lambda _, __, q: q and q.data and q.data.startswith("at_mission"))

    async def func(self):
        _, id_ = self.request.data.split()
        id_ = int(id_)

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Удалить напоминание", callback_data=f"rm_mission {id_}"),
            InlineKeyboardButton("К напоминаниям", callback_data="notifications_main"),
        ]])

        await self.request.message.reply(
            render_notification(Notifications.get_by_id(id_)),
            reply_markup=keyboard,
        )


class AddMission(BaseHandler):
    FILTER = regex("Добавить напоминание")

    async def func(self):
        pass


class RmMission(BaseHandler):
    FILTER = create(lambda _, __, q: q and q.data and q.data.startswith("rm_mission"))

    async def func(self):
        _, id_ = self.request.data.split()
        id_ = int(id_)

        Notifications.delete_by_id(id_)

        await self.request.message.reply(
            "Напоминание удалено!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("К напоминаниям", callback_data="notifications_main")
            ]])
        )
