from datetime import datetime

from colorama import Fore

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
