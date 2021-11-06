import asyncio
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple

import asyncpg
from asyncache import cached
from cachetools import TTLCache

from utils.profile import log

DB_HOST = '10.10.0.33'
DB_DB = 'student'
DB_USER = 'student'
DB_PASS = 'wsiz#1234'


def dicts(rows):
    """
    Convert DB-rows to dictionaries.
    Note: use only for DB-rows, not for collections of objects.
    :param rows:
    :return:
    """
    return [dict(r) for r in rows]


@dataclass
class Person:
    # przykład klasy danych odpowiadającej tabeli na bazie
    id: int
    name: str


async def create_pool():
    log(f'creating pool for db:{DB_HOST}:5432, db={DB_DB}')

    pool = await asyncpg.create_pool(host=DB_HOST, port=5432, database=DB_DB, user=DB_USER,
                                     password=DB_PASS)
    log(f'pool created')
    return pool


class DbService:
    pool: asyncpg.pool.Pool

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    # DISTRICTS

    @cached(TTLCache(10, ttl=600))
    async def get_all_persons(self) -> List[Person]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('select * from s1.person')
        return [Person(**d) for d in dicts(rows)]

    async def update_person(self, person: Person):
        p = person  # alias

        async with self.pool.acquire() as c:
            res = await c.fetch('''
                            UPDATE s1.person
                            SET name=$2
                            WHERE id = $1
                            RETURNING *''', p.id, p.name)
            d = dict(res[0])
            return Person(**d)

    async def create_person(self, person: Person) -> Person:
        p = person
        async with self.pool.acquire() as c:
            res = await c.fetch('''
                        INSERT INTO s1.person(name) 
                        VALUES ($1) RETURNING *''',
                                p.name)
            d = dict(res[0])
            return Person(**d)


async def run_it():
    pool = await create_pool()
    db = DbService(pool)
    print(await db.get_all_persons())
    print(await db.create_person(Person(0,'xiaoli')))
    p = Person(3, 'xiaoli3')
    print(await db.update_person(p))
    log('--')


if __name__ == '__main__':
    asyncio.run(run_it())
