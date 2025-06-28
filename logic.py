"""
logic.py — Core logic for processing images using user-defined parameters.
"""

from PIL import Image
from PIL.Image import Image as PILImage
from functions import *
from models import ResizeInput


def process_image(new_input: ResizeInput) -> str:
    """
    Perform full image processing pipeline:
    resize the image and save the result.

    Args:
        new_input (ResizeInput): All parameters required for resizing and saving.

    Returns:
        str: Path to the saved output image.
    """
    export_image: PILImage = resize_image(new_input)
    save_image(export_image)
    return export_image.filename
