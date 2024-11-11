from client_handlers.base import *


class MissionsList(BaseHandler):
    FILTER = regex("Мои напоминания")

    async def func(self):
        pass


class AddMission(BaseHandler):
    FILTER = regex("Добавить напоминание")

    async def func(self):
        pass


class RmMission(BaseHandler):
    FILTER = create(lambda _, __, q: q and q.data and q.data.startswith("rm_mission"))

    async def func(self):
        pass
