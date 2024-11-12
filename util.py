from datetime import datetime, timedelta

from colorama import Fore

from database.models import Notifications, SendTime

weekdays = {
    0: "в понедельник",
    1: "во вторник",
    2: "в среду",
    3: "в четверг",
    4: "в пятницу",
    5: "в субботу",
    6: "в воскресенье",
}


def clear_unused_time_points(user):
    unused = filter(lambda t: t.updated_at <= datetime.now() - timedelta(days=1), user.created_tp)
    for tp in unused:
        SendTime.delete_by_id(tp.id)



def color_log(text: str, colors: str | list[str], head_c: str = Fore.LIGHTWHITE_EX, separator: str = " ") -> None:
    now = datetime.now()

    if not isinstance(colors, list):
        print(head_c + f"[{now}]: >> " + colors + text)

    parts = text.split(separator)
    res = ""
    for w, c in zip(parts, colors):
        res += c + w + " "

    if len(parts) > len(colors):
        res += colors[-1] + res[len(colors) - 1:]

    print(head_c + f"[{now}]: >> " + res)


def render_notification(notification: Notifications) -> str:
    send_at: SendTime = notification.send_at[0]

    if send_at.consider_date:
        t = f"{send_at.send_date} {send_at.send_time}".capitalize()
    elif 0 <= send_at.weekday <= 6:
        t = f"{weekdays[send_at.weekday]}, {send_at.send_time}".capitalize()
    else:
        t = f"каждый день, в {send_at.send_time}".capitalize()

    if send_at.delete_after_execution:
        t += " (Удалится после отправки)"

    return (
        "Текст напоминания:"
        "\n{}"
        "\n\nВремя отправки: {}"
        "\nЧат для отправки: {}".format(notification.text, t, notification.chat_to_send[0].tg_id)
    )
