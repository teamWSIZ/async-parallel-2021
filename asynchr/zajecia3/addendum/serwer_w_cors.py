from asyncio import sleep

import aiohttp_cors
from aiohttp import web

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


async def blah():
    await sleep(1.3)


@routes.get('/')
async def hello(request):
    await blah()
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome/{id}')
async def hello(request):
    print('from get')
    return web.json_response({'comment': 'Welcome!'})


@routes.put('/welcome/{id}')
async def hellx(request):
    print('from put')
    return web.json_response({'comment': 'Welcome!'})


@routes.get('/square')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x ** 2
    return web.json_response({'result': xx})


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


async def starter():
    await sleep(0.2)
    print('app is starting..')

if __name__ == '__main__':
    web.run_app(starter(), port=4001)
