"""
functions.py — Low-level image manipulation functions: resize and save.
"""

from PIL import Image, ImageOps
from PIL.Image import Image as PILImage
import os, logging
import models
from models import * 

logger = logging.getLogger(__name__)


def resize_image ( new_input : ResizeInput) -> bool | PILImage:
    """
    Resize an image using the specified parameters.

    Modes:
        - 'thumbnail': in-place resize (mutates original)
        - 'contain': scales down to fit inside box
        - 'cover': scales up and crops to fill box
        - 'fit': like cover but with alignment
        - 'pad': adds padding to fit box (forces .png)

    Args:
        new_input (ResizeInput): dataclass with all resize settings

    Returns:
        PILImage: result image with `.filename` set
        bool: False if any error occurred
    """
    src_path: str = new_input.src_path
    out_size: tuple[int, int] = new_input.out_size
    resize_mode: str = new_input.resize_mode
    save_extension: str = new_input.save_extension
    resample_mode: int = new_input.resample_mode
    pad_color: tuple[int,...] = new_input.pad_color

    resize_modes: tuple[str, ...] = models.RESIZE_MODES
    if resize_mode not in resize_modes:
        raise ValueError(f"Invalid resize_mode: {resize_mode}")
    
    try:
        with Image.open(src_path) as src_image:
            logger.info(f'Imported image: {src_image.format}, {src_image.size}, {src_image.mode}')
            base_name: str = os.path.splitext(src_path)[0]
            ext: str = save_extension

            # Resize logic per mode
            if resize_mode == 'thumbnail':
                export_image = src_image.copy()
                export_image.thumbnail(out_size, resample_mode)
            elif resize_mode == 'contain':
                export_image = ImageOps.contain(src_image, out_size, method=resample_mode)
            elif resize_mode == 'cover':
                export_image = ImageOps.cover(src_image, out_size, method=resample_mode)
            elif resize_mode == 'fit':
                export_image = ImageOps.fit(src_image, out_size, method=resample_mode)
            else:  # pad
                if src_image.mode != "RGBA":
                    src_image = src_image.convert("RGBA")
                export_image = ImageOps.pad(src_image, out_size,color=pad_color, method=resample_mode)
                ext = '.png'
                logger.info('Extension overridden to .png for transparent pad mode')

            # Attach filename to image
            export_image.filename = base_name + f'_{export_image.size[0]}x{export_image.size[1]}' + ext
            return export_image

    except (OSError, ValueError) as ext:
        logger.info(f"Cannot resize: {src_path}, reason: {ext}")
        return False  


def save_image(export_image: PILImage) -> str | bool:
    """
    Save a processed image to disk using its `.filename` field.

    Args:
        export_image (PILImage): PIL object with .filename set

    Returns:
        str: path where saved
        bool: False if error or no filename
    """
    if not isinstance(export_image.filename, str) or not export_image.filename:
        return False
    try:
        export_image.save(export_image.filename)
        logger.info(f'File saved to: {export_image.filename}')
    except (OSError, ValueError) as error:
        logger.error(f'File NOT saved to: {export_image.filename}, reason {error}')
        return False
    return export_image.filename
