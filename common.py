import datetime


def now_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def now_time():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]


def log_line(path: str, line: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

