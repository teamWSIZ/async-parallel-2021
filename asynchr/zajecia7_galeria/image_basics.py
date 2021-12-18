
from PIL import Image, ImageOps
from PIL.Image import BICUBIC
import io

# pip install Pillow

image = Image.open('sample.png')
print(image.size)  # (800, 701)
image = image.crop((0, 0, 600, 600))
# image = image.resize((100, 100), resample=BICUBIC)
# image = image.resize((100, 100), resample=BICUBIC)
image = ImageOps.scale(image, 0.3, resample=BICUBIC)

# zapis obrazka PIL.Image do tablicy bajtów, czyli "bytes"
image_bytes = io.BytesIO()
image.save(image_bytes, format='PNG')
bytes = image_bytes.getvalue()

# odczyt obrazka PIL.Image z tablicy bajtów, czyli "bytes"
image2 = Image.open(io.BytesIO(bytes))
image2.show()



image.save('sample_th.jpg')
image.show()