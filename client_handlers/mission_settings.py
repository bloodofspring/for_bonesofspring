from datetime import datetime

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


class GetDateTimeAndChat(BaseHandler):
    FILTER = create(lambda _, __, q: q & q.data & q.data.startswith("CHANGE"))

    def __init__(self):
        super().__init__()
        self.datetime = datetime(
            year=0, month=0, day=0,
            hour=0, minute=0, second=0,
        )
        self.reg_weekday = False
        self.reg_date = False
        self.del_after_exec = False

    @property
    def date_keyboard(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("<<", callback_data="change date day -1"),
                InlineKeyboardButton("День: {}".format(self.datetime.day), callback_data=""),
                InlineKeyboardButton(">>", callback_data="change date day +1")
            ],
            [
                InlineKeyboardButton("<<", callback_data="date month -1"),
                InlineKeyboardButton("Месяц: {}".format(self.datetime.month), callback_data=""),
                InlineKeyboardButton(">>", callback_data="change date month +1")
            ],
            [
                InlineKeyboardButton("<<", callback_data="date year -1"),
                InlineKeyboardButton("Год: {}".format(self.datetime.year), callback_data="", ),
                InlineKeyboardButton(">>", callback_data="change date year -1")
            ],
            [InlineKeyboardButton(
                "Не учитывать дату" if self.reg_date else "Учитывать дату", callback_data="change_consider_date"
            )],
            [
                InlineKeyboardButton("<<", callback_data="change hour -1"),
                InlineKeyboardButton("Час: {}".format(self.datetime.hour), callback_data=""),
                InlineKeyboardButton(">>", callback_data="change hour +1")
            ],
            [
                InlineKeyboardButton("<<", callback_data="change minute -1"),
                InlineKeyboardButton("минута: {}".format(self.datetime.minute), callback_data=""),
                InlineKeyboardButton(">>", callback_data="change minute +1")
            ],
            [
                InlineKeyboardButton("<<", callback_data="change second -1"),
                InlineKeyboardButton("Секунда: {}".format(self.datetime.second), callback_data=""),
                InlineKeyboardButton(">>", callback_data="change second +1")
            ],
            [InlineKeyboardButton(
                "Не учитывать день недели" if self.reg_weekday else "Учитывать день недели",
                callback_data="change_reg_weekday"
            )],
            [InlineKeyboardButton(
                "Не удалять после исполнения" if self.del_after_exec else "Удалить после исполнения",
                callback_data="change_del_after_exec"
            )],
            [InlineKeyboardButton("Готово", callback_data="change submit")],
        ])

        return keyboard

    def set_values(self):  # call data format! "CHANGE-YYYY-MM-DD-HH-MM-SS-1-0-1" (reg_weekday, reg_date, del_after_exec)
        self.datetime = datetime(*map(int, self.request.data.split("-")[1:7]))
        self.reg_weekday = bool(self.request.data.split("-")[7])
        self.reg_date = bool(self.request.data.split("-")[8])
        self.del_after_exec = bool(self.request.data.split("-")[9])

    async def func(self):
        self.set_values()


class AddMission(BaseHandler):
    FILTER = regex("Добавить напоминание")

    async def get_chat(self):
        pass

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
