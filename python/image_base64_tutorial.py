import base64
from io import BytesIO
import PIL.Image

# if running in WSL
# sudo apt install imagemagick

with open("image.base64", "rb") as image_file:
    encoded_string = base64.b64decode(image_file.read())

    img = PIL.Image.open(BytesIO(encoded_string))
    img.show()