from asyncio import sleep

import aiohttp_cors
from aiohttp import web

from asynchr.zajecia5_db.db_service import create_pool, DbService, Person

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


@routes.get('/persons')
async def get_persons(request):
    persons = await db.get_all_persons()
    return web.json_response([p.__dict__ for p in persons])


@routes.get('/insert')
async def insert(request):
    name = request.rel_url.query['name']
    new_person = await db.create_person(Person(-1, name))
    return web.json_response(new_person.__dict__)


@routes.get('/update')
async def update(request):
    id = int(request.rel_url.query['id'])
    name = request.rel_url.query['name']
    updated_person = await db.update_person(Person(id, name))
    return web.json_response(updated_person.__dict__)


@routes.get('/delete')
async def delete(request):
    id = int(request.rel_url.query['id'])
    await db.delete_person(id)
    return web.json_response({'result': 'OK'})


###################
# Obiekty dostępne dla wszystkich metod

db: DbService


async def starter():
    global db
    """
    Starter / app factory, czyli miejsce gdzie można inicjalizować asynchronicze konstrukty.
    :return:
    """
    # tworzenie serwisu dostępu do bazy danych
    db = DbService()
    await db.initalize()
    print('app is starting..')
    return app


app = web.Application()
app.add_routes(routes)
web.run_app(starter(), port=4000)
