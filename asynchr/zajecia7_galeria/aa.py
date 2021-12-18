import io

from PIL import Image

img = Image.open('sample.png')
image_bytes = io.BytesIO()
img.save(image_bytes, format='PNG')
bytes = image_bytes.getvalue()
print(bytes)
img.show()