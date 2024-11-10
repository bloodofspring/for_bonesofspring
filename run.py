"""Run this file to start instances"""
from instances import client
from client_handlers import active_handlers
from database.create import create_tables


def add_handlers() -> None:
    for handler in active_handlers:
        client.add_handler(handler().de_pyrogram_handler)


def run_bot() -> None:
    add_handlers()
    create_tables()
    print("Клиент запущен!")
    client.run()


if __name__ == "__main__":
    run_bot()
