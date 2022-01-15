from asyncio import sleep

import aiohttp_cors
import aiosqlite
from aiohttp import web
from aiohttp.abc import BaseRequest

from asynchr.zajecia7_galeria.db_access import DbService
from asynchr.zajecia7_galeria.helpers import pil_image_from_picture, file_2_picture
from asynchr.zajecia7_galeria.model import Picture

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


@routes.get('/')
async def hello(request):
    return web.json_response({'comment': 'OK'})


"""
todo: 
- serwis bazy danych (a nie funkcje)                            [OK]
- odpowiednio RETURNING przy tworzeniu instancji                [OK]
- endpointy do ściągania thumbnaili obrazków
- ew. konwersja na thumbnaili na bas64 image... 
...
- logika userów - tworzenie, modyfikacja, hasła
- logowanie usera ... → token (potrzebny do update obrazków)
...
- tag-i obrazków, oraz endpointy do nadawania tagów obrazkom...
...
- frontend systemu...
"""


@routes.get('/pictures/{id}/full')
async def serve_file(req):
    print('get image of given pictureid')
    iid = int(req.match_info['id'])
    pic = await db().fetch_picture(iid)
    image = pil_image_from_picture(pic, full_image=True)
    image.save('_' + pic.filename)
    return web.FileResponse('_' + pic.filename)

@routes.get('/pictures')
async def serve_file(req):
    print('fetch all picture thumbnails')
    images = await db().fetch_thumbnails_all_pictures()
    for pic in images:
        serialize_picture_meta(pic)

    return web.json_response([pic.__dict__ for pic in images])



def serialize_picture_meta(pic: Picture):
    pic.created = str(pic.created)
    pic.data = ''


@routes.post('/upload')
async def accept_file(req: BaseRequest):
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    print('file upload request hit...')
    reader = await req.multipart()

    # field = await reader.next()
    # name = await field.read(decode=True)

    field = await reader.next()  # field.name =='file'
    filename = field.filename
    print(f'upload filename:{filename}')
    path = 'images/' + filename
    with open(path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            f.write(chunk)
    pic = file_2_picture(filename, 'images/')
    pic = await db().insert_picture(pic)
    pic.data = ''
    serialize_picture_meta(pic)
    return web.json_response(pic.__dict__)


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
    app['db'] = DbService('pic_db.db')
    return app


if __name__ == '__main__':
    web.run_app(starter(), port=4001)
