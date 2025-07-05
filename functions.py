"""
functions.py — Low-level image manipulation functions: resize, remove background and save.
"""

from PIL import Image, ImageOps
from PIL.Image import Image as PILImage
from rembg import remove
import os, logging, io
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
        - 'pad': adds padding to fit box (forces .png if alpha < 255)

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
            extention: str = save_extension

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
                if src_image.mode != "RGBA" and pad_color [3] < 255:
                    src_image = src_image.convert("RGBA")
                    extention: str = '.png'
                    logger.info('Extension overridden to .png for transparent pad mode')
                export_image = ImageOps.pad(src_image, out_size,color=pad_color, method=resample_mode)

            # Attach filename to image
            export_image.filename = base_name + f'_{export_image.size[0]}x{export_image.size[1]}'+ f'_{resize_mode}' + extention
            return export_image

    except (OSError, ValueError) as ext:
        logger.info(f"Cannot resize: {src_path}, reason: {ext}")
        return False  

def rembg_processing(new_input: RembgInput) -> bool | PILImage:
    """
    Removes background from an input image using rembg.

    Args:
        new_input (RembgInput): Dataclass containing:
            - src_path: path to source image file.
            - calculation_device: 'cpu' or 'cuda' (currently unused).

    Returns:
        PILImage: Image object with transparent background if successful.
        bool: False if operation failed.
    """
    _src_path: str = new_input.src_path
    _calculation_device: str = new_input.calculation_device  # Reserved for future device control
    base_name, extention = os.path.splitext(_src_path)

    try:
        # Read input image as binary
        with open(_src_path, 'rb') as image_with_bg:
            src_image: bytes = image_with_bg.read()

            # Run background removal
            image_without_bg: bytes = remove(src_image)

            # Decode result from bytes to PIL Image
            export_image: PILImage = Image.open(io.BytesIO(image_without_bg))

            # Ensure image has alpha channel for transparency
            if export_image.mode != "RGBA":
                export_image = export_image.convert("RGBA")
                extention = '.png'
                logger.info('Extension overridden to .png for transparent background')

            # Set output filename
            export_image.filename = base_name + '_no_bg' + extention
            return export_image

    except (OSError, ValueError) as ext:
        logger.info(f"Cannot remove bg: {_src_path}, reason: {ext}")
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
