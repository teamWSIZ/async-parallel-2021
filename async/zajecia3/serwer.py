from asyncio import sleep

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


@routes.get('/welcome')
async def hello(request):
    return web.json_response({'comment': 'Welcome!'})


@routes.get('/square')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x**2
    return web.json_response({'result': xx})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=4000)
