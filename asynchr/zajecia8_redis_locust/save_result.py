from dataclasses import asdict
from random import choice, randint
import requests
from asynchr.zajecia8_redis_locust.model import HKRunner

r = HKRunner(randint(0,10000), choice(['Kenya', 'Ethiopia', 'Japan']), 2 * 3600 + randint(500, 2000))

res = requests.put('http://localhost:4001/results', json=asdict(r))

print(res.json())