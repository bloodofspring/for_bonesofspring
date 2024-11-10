"""Run this file to start instances"""
from colorama import Fore

from instances import client
from database.create import create_tables
from util import color_log


def run_bot() -> None:
    create_tables()
    color_log("Клиент запущен", colors=Fore.LIGHTYELLOW_EX, head_c=Fore.LIGHTWHITE_EX)
    client.run()


if __name__ == "__main__":
    run_bot()
