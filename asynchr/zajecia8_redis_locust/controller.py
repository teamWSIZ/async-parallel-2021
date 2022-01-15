from asyncio import sleep
import aiohttp_cors
from aiohttp import web

from asynchr.zajecia8_redis_locust.db_service import DbService
from asynchr.zajecia8_redis_locust.model import HKRunner, get_time_from_str

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query} ; /users/117
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


@routes.get('/results')
async def get_runners(req):
    # w parametrach URL powinny przyjść `mintime` i `maxtime` w formacie `H:MM:SS`
    # czyli np. http://localhost:4001/results?mintime=2:00:01&maxtime=2:20:00
    mintime = req.rel_url.query.get('mintime', '0:00:00')
    maxtime = req.rel_url.query.get('maxtime', '9:00:00')
    mintime = get_time_from_str(mintime)
    maxtime = get_time_from_str(maxtime)

    results = await db().get_results_for_times(mintime, maxtime)
    re = [r.__dict__ for r in results]
    return web.json_response(re)


@routes.put('/results')
async def save_runners(req):
    """
    Enpoint do zapisywania wyników maratończyków; dane (w postaci pól potrzebnych do klasy HKRunner)
    powinny zostać wysłane w request-body.
    """
    # print(await req.text())
    hkr_dict = await req.json()
    res = HKRunner(**hkr_dict)
    print(f'saving the result: {res}')
    await db().save_runners_result(res)
    return web.json_response({'comment': 'OK'})


#  setup generous CORS:
app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

app.router.add_routes(routes)

print(app.router.routes())

for route in list(app.router.routes()):
    # print(f'adding {route}')
    cors.add(route)


def db() -> DbService:
    # helper/alias
    return app['db']


async def starter():
    """
    Starter / app factory, czyli miejsce gdzie można inicjalizować asynchronicze konstrukty.

    :return:
    """
    print('app is starting..')
    app['db'] = DbService()
    await db().initialize()
    return app


if __name__ == '__main__':
    web.run_app(starter(), port=4001)
