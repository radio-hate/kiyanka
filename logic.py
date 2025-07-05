"""
logic.py — Core logic for processing images using user-defined parameters.
"""

from PIL import Image
from PIL.Image import Image as PILImage
from functions import *
from models import ResizeInput


def resize_and_save(new_input: ResizeInput) -> str:
    """
    Resizes an image based on input parameters and saves the result.

    Args:
        new_input (ResizeInput): Configuration for resizing, including:
            - src_path: path to the input image
            - out_size: (width, height) tuple
            - resize_mode: one of the supported modes
            - save_extension: desired output format
            - resample_mode: PIL resampling method
            - pad_color: color for padding, if applicable

    Returns:
        str: Path to the saved output image.
    """
    # Perform resizing using logic layer
    export_image: PILImage = resize_image(new_input)

    # Save the processed image to disk
    save_image(export_image)

    # Return path where image was saved
    return export_image.filename


def rembg_and_save(new_input: RembgInput) -> str:
    """
    Removes background from an image and saves the result.

    Args:
        new_input (RembgInput): Input data for background removal.

    Returns:
        str: Path to the saved output image.
    """
    # Run background removal and get processed image
    export_image: PILImage = rembg_processing(new_input)

    # Save image to disk using attached .filename
    save_image(export_image)

    # Return path where image was saved
    return export_image.filename
