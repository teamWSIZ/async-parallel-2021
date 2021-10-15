from aiohttp import web

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome')
async def hello(request):
    return web.json_response({'comment': 'Welcome!'})


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=4000)
