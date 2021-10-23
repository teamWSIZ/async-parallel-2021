import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from time import sleep


def job(n):
    print(f'entered {n}')
    sleep(10)
    print(f'leaving {n}')
    return n


with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for i in range(10):
        futures.append(executor.submit(job, i))
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
