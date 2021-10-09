import asyncio
import time
from asyncio import sleep

from utils.profile import log, ts


async def job(n):
    log(f'starting job {n}')
    await sleep(1)
    if n == 500:
        log('long sleep')
        time.sleep(0.4)
    # log(f'ending job {n}')


async def event_loop_watchdog():
    """
        Funkcja którą wykorzystamy do kontroli nad prędkością wykonania event-loopa.
    W przypadku, gdy "nic się nie dzieje" funkcja powinna raportować "1000 RPM";
    Jakiekolwiek nie-async blokady będzie w niej widać...

        Ta funkcja nigdy się nie kończy -- jest odpowiednikiem serwisu który
    cały czas działa i cośtam sobie sprawdza/wykonuje np. periodycznie.
    """
    log('starting event loop watchdog')
    counter = 0
    st = ts()
    while True:
        counter += 1
        await sleep(0.001)
        if counter == 200:
            en = ts()
            rps = 200 / (en - st)
            log(f'loop speed: {rps:.0f} RPS ################')
            st = en
            counter = 0




async def main():
    log('starting main')
    # await job(1)
    asyncio.create_task(event_loop_watchdog())
    await sleep(1)

    tasks = []
    for i in range(10 ** 4):
        # await sleep(0.001)
        tasks.append(asyncio.create_task(job(i)))
    await asyncio.gather(*tasks)
    log('finishing main')
    await sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
