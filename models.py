"""
models.py — Data structures and constants for image operations.
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
    Input container for background removal using the rembg library.

    Attributes:
        src_path (str): Path to the input image file.
        calculation_device (str): Device type for processing ('cpu', 'cuda').
        session (any): Optional model session object (e.g. from new_session()).
        alpha_matting (bool): Enables alpha matting for smoother edge blending.
        alpha_matting_foreground_threshold (int): Pixel intensity threshold to consider as definite foreground.
        alpha_matting_background_threshold (int): Pixel intensity threshold to consider as definite background.
        alpha_matting_erode_structure_size (int): Size of the erosion structure applied in matting.
        alpha_matting_base_size (int): Base resolution for alpha matting.
        background_color (tuple | None): Solid background color (e.g. (255,255,255)) instead of transparency.
        force_return_bytes (bool): If True, return raw bytes instead of a PIL.Image object.
    """
    src_path: str = ''
    calculation_device: str = ''
    session: any = None
    alpha_matting: bool = True
    alpha_matting_foreground_threshold: int = 240
    alpha_matting_background_threshold: int = 10
    alpha_matting_erode_structure_size: int = 10
    alpha_matting_base_size: int = 1000
    background_color: tuple = None
    force_return_bytes: bool = False

