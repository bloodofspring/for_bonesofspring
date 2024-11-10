from pyrogram.filters import create, command, regex
from pyrogram.handlers import MessageHandler
from pyrogram import Client


__all__ = ["BaseHandler", "Client", "command", "regex", "create"]


class BaseHandler:
    """Базовый обработчик-исполнитель"""
    __name__ = ""
    HANDLER = MessageHandler
    FILTER = create(lambda _, __, ___: False)

    async def func(self):
        raise NotImplementedError

    def set_init_vals(self, **data):
        for k in data:
            setattr(self, k, data[k])

    async def __call__(self, client: Client, request):
        self.set_init_vals(client=client, request=request)

        try:
            await self.func()
        except Exception as e:
            setattr(self, "execution_error", e)

    @property
    def de_pyrogram_handler(self):
        return self.HANDLER(self, self.FILTER)
