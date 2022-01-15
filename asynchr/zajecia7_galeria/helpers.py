import base64
import datetime
import io
from typing import Tuple

from PIL import Image

from asynchr.zajecia7_galeria.model import Picture


def get_thumbnail(image: Image) -> Image:
    image = image.crop((0, 0, 320, 200))
    # image = ImageOps.scale(image, 0.3, resample=BICUBIC)
    return image


def row_2_picture(row: Tuple, with_data=True) -> Picture:
    if with_data:
        p = Picture(*row)
    else:
        p = Picture(row[0], None, *row[1:])
    p.created = datetime.datetime.fromtimestamp(p.created)
    return p


def file_2_picture(filename: str, path='') -> Picture:
    image = Image.open(path + filename)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    bytes = image_bytes.getvalue()  # sposób na "wyrwanie" danych obrazka w postaci bytes (format PNG)

    thumb = get_thumbnail(image)
    thumb_bytes = io.BytesIO()
    thumb.save(thumb_bytes, format='PNG')
    thb = (base64.b64encode(thumb_bytes.getvalue())).decode('UTF-8')

    # todo: by thumbnail wyświetlić w html-u trzeba dodać prefix 'data:image/png;base64,'
    return Picture(-1, data=bytes, data_thumbnail=thb, filename=filename, description='',
                   creator_userid=-1, created=datetime.datetime.now())


def pil_image_from_picture(picture: Picture, full_image=True) -> Image:
    """
    :return: Image który można skonstruować na podstawie danych w instancji Picture
    """
    if full_image:
        image = Image.open(io.BytesIO(picture.data))
    else:
        image = Image.open(io.BytesIO(picture.data_thumbnail))
    return image
