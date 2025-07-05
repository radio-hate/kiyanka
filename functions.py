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
                if ((src_image.mode != "RGBA" and
                    pad_color [3] < 255) or
                    extention.lower() in ('.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
                    ):
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
    Removes the background from an image using the rembg library.
    Supports both standard (hard edge) and alpha matting (soft edge) modes.

    Args:
        new_input (RembgInput): Input parameters including:
            - src_path (str): Path to source image.
            - session: Optional model session object.
            - alpha_matting (bool): Whether to use soft edge masking.
            - alpha_matting_*: Various thresholds and settings for matting.
            - background_color (tuple | None): Replace transparency with solid color.
            - force_return_bytes (bool): Always return bytes (not used here).

    Returns:
        PILImage: Processed image with transparent or solid background.
        bool: False if operation failed.
    """
    _src_path: str = new_input.src_path
    _calculation_device: str = new_input.calculation_device  # currently unused
    _session = new_input.session
    _alpha_matting = new_input.alpha_matting
    _alpha_matting_foreground_threshold = new_input.alpha_matting_foreground_threshold
    _alpha_matting_background_threshold = new_input.alpha_matting_background_threshold
    _alpha_matting_erode_structure_size = new_input.alpha_matting_erode_structure_size
    _alpha_matting_base_size = new_input.alpha_matting_base_size
    _background_color = new_input.background_color
    _force_return_bytes = new_input.force_return_bytes

    base_name, extention = os.path.splitext(_src_path)

    try:
        # Read input image in binary mode
        with open(_src_path, 'rb') as image_with_bg:
            _src_image: bytes = image_with_bg.read()

            # Perform background removal
            image_without_bg: bytes = remove(
                data=_src_image,
                session=_session,
                alpha_matting=_alpha_matting,
                alpha_matting_foreground_threshold=_alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=_alpha_matting_background_threshold,
                alpha_matting_erode_structure_size=_alpha_matting_erode_structure_size,
                alpha_matting_base_size=_alpha_matting_base_size,
                background_color=_background_color,
                force_return_bytes=False  # always returns PIL.Image in this context
            )

            # Load result from bytes into a PIL Image
            export_image: PILImage = Image.open(io.BytesIO(image_without_bg))

            # Ensure RGBA mode for transparency
            if (export_image.mode != "RGBA" or 
                extention.lower() in ('.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
                ):
                export_image = export_image.convert("RGBA")
                extention: str = '.png'
                logger.info('Extension overridden to .png for transparent background')

            # Attach output filename
            alpha_matting_mode_suffix:str = 'soft' if _alpha_matting else 'hard'
            export_image.filename = base_name + '_no_bg_'+ alpha_matting_mode_suffix + extention
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
