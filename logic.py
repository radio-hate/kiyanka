from PIL import Image
from PIL.Image import Image as PILImage
from functions import *


def process_image (new_input : ResizeInput) -> str: 
    export_image: PILImage = resize_image (new_input)
    save_image (export_image)
    return export_image.filename