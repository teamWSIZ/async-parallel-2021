from asyncio import sleep

import aiohttp_cors
import aiosqlite
from aiohttp import web
from aiohttp.abc import BaseRequest

from asynchr.zajecia7_galeria.db_access import fetch_picture, pil_image_from_picture

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
- serwis bazy danych (a nie funkcje)
- odpowiednio RETURNING przy tworzeniu instancji
- endpointy do ściągania thumbnaili obrazków
- ew. konwersja na thumbnaili na bas64 image... 
- logowanie usera ... → token (potrzebny do update obrazków)
- zmiana hasła usera
...
- tag-i obrazków, oraz endpointy do nadawania tagów obrazkom...
...
- frontend systemu...
"""

@routes.get('/pictures/{id}')
async def serve_file(req):
    print('get image of given pictureid')
    async with aiosqlite.connect('pic_db.db') as db:
        id = int(req.match_info.get('id', '0'))
        pic = (await fetch_picture(db, id))
        image = await pil_image_from_picture(pic, full_image=True)
        image.save('_' + pic.filename)
    return web.FileResponse('_' + pic.filename)


@routes.post('/upload')
async def accept_file(req: BaseRequest):
    # https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
    print('file upload request hit...')
    reader = await req.multipart()

    # field = await reader.next()
    # name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'file'
    print(f'read field object: {field}')
    filename = field.filename
    # Cannot rely on Content-Length if transfer is chunked.
    print(f'filename:{filename}')
    filename = 'images/' + filename
    size = 0
    with open(filename, 'wb') as f:
        file_as_bytes = b''
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            print(type(chunk))
            if not chunk:
                break
            size += len(chunk)
            file_as_bytes += chunk
            # f.write(chunk)
        f.write(file_as_bytes)

    return web.json_response({'name': filename, 'size': size})


@routes.get('/serve')
async def serve_file____(req: BaseRequest):
    return web.FileResponse('out.png')


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
    """
    Starter / app factory, czyli miejsce gdzie można inicjalizować asynchronicze konstrukty.

    :return:
    """
    print('app is starting..')
    return app


if __name__ == '__main__':
    web.run_app(starter(), port=4001)
