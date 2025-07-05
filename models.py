"""
models.py — Data structures and constants for image resizing operations.
"""

from PIL import Image, ImageDraw, ImageOps
from PIL.Image import Image as PILImage  # Type alias for static type checking
from dataclasses import dataclass

# Supported resize modes for the CLI and logic layer
RESIZE_MODES: tuple[str, ...] = ('thumbnail', 'contain', 'cover', 'fit', 'pad')


@dataclass
class ResizeInput:
    """
    Container for all user-defined and default parameters
    needed to perform an image resize operation.

    Attributes:
        src_path (str): Path to the source image file.
        out_size (tuple[int, int]): Target output dimensions (width, height).
        resize_mode (str): Strategy for resizing. Must be one of RESIZE_MODES.
        save_extension (str): Output file format, e.g., '.jpg', '.png'.
        resample_mode (int): PIL resampling method (e.g. BICUBIC, LANCZOS).
        pad_color (tuple[int,...]): Color used for padding when applicable (RGBA or RGB).
    """
    src_path: str = ''
    out_size: tuple[int, int] = (1920, 1920)
    resize_mode: str = RESIZE_MODES[2]  # default to 'cover'
    save_extension: str = '.jpg'
    resample_mode: int = Image.Resampling.BICUBIC
    pad_color: tuple[int, ...] = (0, 0, 0, 0)

@dataclass
class RembgInput:
    """
    Container for background removal input parameters.

    Attributes:
        src_path (str): Path to the input image file.
        calculation_device (str): Desired compute backend (e.g., 'cpu', 'cuda').
                                  Currently not used but reserved for future support.
    """
    src_path: str = ''
    calculation_device: str = ''
