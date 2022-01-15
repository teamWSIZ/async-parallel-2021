from dataclasses import asdict
from random import choice, randint

import requests

res = requests.get('http://localhost:4001/results')
print(res.json())