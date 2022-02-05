import time
from dataclasses import asdict, dataclass
from random import randint, choice

from locust import HttpUser, task, between, FastHttpUser


@dataclass
class HKRunner:
    race_no: int
    country: str
    time: int


class QuickstartUser(FastHttpUser):
    wait_time = between(0.1, 0.2)

    @task(30)
    def hello_world(self):
        self.client.get('/')

    # @task(5)
    # def get_khresults(self):
    #     mintime_mm = 1
    #     maxtime_mm = mintime_mm + randint(0,20)
    #     # self.client.get(f'/results?mintime=2:{mintime_mm}:00&maxtime=2:{maxtime_mm}:00')
    #     self.client.get(f'/results')
    #
    # @task(1)
    # def put_khresults(self):
    #     r = HKRunner(randint(0, 10000), choice(['Kenya', 'Ethiopia', 'Japan']), 2 * 3600 + randint(500, 2000))
    #     self.client.put('/results', json=asdict(r))

    def on_start(self):
        print('starting')
