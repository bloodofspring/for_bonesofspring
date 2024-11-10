"""Run this file to start instances"""
from instances import client
from database.create import create_tables


def run_bot() -> None:
    create_tables()
    print("Клиент запущен!")
    client.run()


if __name__ == "__main__":
    run_bot()
