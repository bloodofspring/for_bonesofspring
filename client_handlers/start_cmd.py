from client_handlers.base import *


class StartCmd(BaseHandler):
    FILTER = command("start")

    async def func(self):
        pass
