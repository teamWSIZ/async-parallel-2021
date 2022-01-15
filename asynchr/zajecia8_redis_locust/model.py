from dataclasses import dataclass


@dataclass
class HKRunner:
    race_no: int
    country: str
    time: int


def get_time_from_str(time_str: str):
    # time_str ~ H:MM:SS
    data = time_str.split(':')
    seconds = int(data[0]) * 3600 + int(data[1]) * 60 + int(data[2])
    return seconds
