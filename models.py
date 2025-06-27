from PIL import Image,ImageDraw,ImageOps
from PIL.Image import Image as PILImage
from dataclasses import dataclass
import cmd

RESIZE_MODES: tuple[str, ...] = ('thumbnail', 'contain', 'cover', 'fit', 'pad')

@dataclass
class ResizeInput:
    src_path: str = ''
    out_size: tuple[int, int] = (1920, 1920)
    resize_mode: str = RESIZE_MODES[2]
    save_extension: str = '.jpg'
    resample_mode: int = Image.Resampling.BICUBIC
    pad_color: tuple[int,...] = (0,0,0,0)

