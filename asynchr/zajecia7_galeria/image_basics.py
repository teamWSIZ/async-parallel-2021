from PIL import Image, ImageOps
from PIL.Image import BICUBIC

image = Image.open('sample.png')
print(image.size)  # (800, 701)
image = image.crop((0, 0, 600, 600))
# image = image.resize((100, 100), resample=BICUBIC)
# image = image.resize((100, 100), resample=BICUBIC)
image = ImageOps.scale(image, 0.3, resample=BICUBIC)
image.save('sample_th.jpg')
image.show()