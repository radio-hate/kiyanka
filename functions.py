#import
from PIL import Image, ImageOps
from PIL.Image import Image as PILImage
import os, logging
from models import * 

logger = logging.getLogger(__name__)

def resize_image ( new_input : ResizeInput) -> bool | PILImage:
    src_path: str = new_input.src_path
    out_size: tuple[int, int] = new_input.out_size
    resize_mode: str = new_input.resize_mode
    save_extension: str = new_input.save_extension
    resample_mode: int = new_input.resample_mode
    pad_color: tuple[int,...] = new_input.pad_color

    """
    Resize an image using the specified mode and return the processed image object.

    Loads an image from disk, resizes it using one of the supported modes
    ('thumbnail', 'contain', 'cover', 'fit', 'pad'), and returns a Pillow image object.
    For 'pad', transparency is applied and the output format is forced to PNG.

    Args:
        src_path (str): Path to the input image file.
        out_size (tuple[int, int], optional): Target size (width, height). Defaults to (1920, 1920).
        resize_mode (str, optional): Resize mode. Defaults to 'cover'.
        save_extension (str, optional): Output file extension. Ignored if mode is 'pad'. Defaults to '.jpg'.
        resample_mode (int, optional): Resampling filter. Defaults to Image.Resampling.BILINEAR

    Returns:
        PILImage: Resized image object with `.filename` set, or
        bool: False if an error occurred.
    """

    # Validate allowed resize modes
    resize_modes: tuple[str, ...] = ('thumbnail', 'contain', 'cover', 'fit', 'pad')
    if resize_mode not in resize_modes:
        raise ValueError(f"Invalid resize_mode: {resize_mode}")
    
    try:
        # Open input image
        with Image.open(src_path) as src_image:
            logger.info(f'Imported image: {src_image.format}, {src_image.size}, {src_image.mode}')

            # Build base output filename
            base_name: str = os.path.splitext(src_path)[0]
            ext: str = save_extension

            # Resize based on selected mode
            if resize_mode == 'thumbnail':
                export_image = PILImage.thumbnail(src_image, out_size, method=resample_mode)
            elif resize_mode == 'contain':
                export_image = ImageOps.contain(src_image, out_size, method=resample_mode)
            elif resize_mode == 'cover':
                export_image = ImageOps.cover(src_image, out_size, method=resample_mode)
            elif resize_mode == 'fit':
                export_image = ImageOps.fit(src_image, out_size, method=resample_mode)
            else:  # 'pad' mode with transparency
                if src_image.mode != "RGBA":
                    src_image = src_image.convert("RGBA")  # ensure alpha channel
                export_image = ImageOps.pad(src_image, out_size,color=pad_color, method=resample_mode)
                ext = '.png'
                logger.info('Extension overridden to .png for transparent pad mode')

            # Attach final filename to image
            export_image.filename = base_name + f'_{export_image.size[0]}x{export_image.size[1]}' + ext
            return export_image

    # Catch and log file I/O or format issues
    except (OSError, ValueError) as ext:
        logger.info(f"Cannot resize: {src_path}, reason: {ext}")
        return False  


def save_image(export_image: PILImage) -> str | bool:
    """
    Save a Pillow image to disk using its `.filename` attribute.

    Attempts to write the image to the path stored in `export_image.filename`.
    Logs success or failure.

    Args:
        export_image (PILImage): A Pillow image object with `.filename` set.

    Returns:
        str: Path where the image was saved, or
        bool: False if saving failed or filename is invalid.
    """
    # Ensure image has a valid filename
    if not isinstance(export_image.filename, str) or not export_image.filename:
        return False
    try:
        # Attempt to save image
        export_image.save(export_image.filename)
        logger.info(f'File saved to: {export_image.filename}')
    except (OSError, ValueError) as error:
        logger.error(f'File NOT saved to: {export_image.filename}, reason {error}')
        return False
    return export_image.filename
