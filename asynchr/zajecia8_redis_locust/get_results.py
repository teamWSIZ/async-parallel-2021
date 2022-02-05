from dataclasses import asdict
from random import choice, randint

import requests

from utils.profile import ts

st = ts()
res = requests.get('http://localhost:4001/results?mintime=2:10:00&maxtime=2:15:00')
en = ts()
print(f'czas wykonania {en-st:.3f}s')
# print(res.json())