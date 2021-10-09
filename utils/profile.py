from datetime import datetime


def ts():
    return datetime.now().timestamp()


def clock():
    return datetime.now().strftime('%H:%M:%S.%f')[:]


def log(what):
    print(f'[{clock()}]: {what}')