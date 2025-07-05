"""
cli.py — Command-line interface for the Kiyanka image resizing tool.
"""

import logging
import cmd
import re
from logic import resize_and_save, rembg_and_save  
from models import ResizeInput, RembgInput, RESIZE_MODES

logger = logging.getLogger(__name__)


class KiyankaCLI(cmd.Cmd):
    """
    Interactive CLI tool for:
     -image resizing
     -removing background

    Commands:
        - resize <path> <WxH> <mode_id> <ext>
        - rembg <path>
        - quit
    """
    prompt = '>> '
    intro = '''Welcome to Kiyanka 0.1.0
A small tool for:
  - image resizing
  - background removal
---------------------------------------------
Available commands: resize, rembg, help, quit.
---------------------------------------------

- Format of the resize command:
  path width,height resize_mode extension

  Example:
    >> resize C:/img.png 768,768 2 .jpg

  Resize modes:
    0 thumbnail()  - shrink to fit inside, keeps aspect ratio
    1 contain()    - fit inside box, may leave empty space
    2 cover()      - fill box, image may be cropped
    3 fit()        - like cover(), but with centering
    4 pad()        - fit inside and pad remaining space

- Format of the rembg command:
  path [soft|hard]   # optional edge mode (default: soft)

  Example:
    >> rembg C:/img.png soft
    '''
    def do_resize(self, import_parameters: str):
        """
        Resize an image using user-provided CLI arguments.

        Arguments format:
            <path> <width,height> <resize_mode_id> <file_extension>

        If resize mode 4 (pad) is selected, the user will be prompted to enter
        the padding color in RGBA format.

        Example:
            >> resize C:/img.png 768,768 4 .png

        resize modes:
            0 thumbnail()
            1 contain()
            2 cover()
            3 fit()
            4 pad()
        """
        user_pad_color: tuple[int, int, int, int] = (0, 0, 0, 255)  # Default pad color

        if not import_parameters.strip():
            print(
'''
Please provide the arguments
Example:
---------------------------------------------
>> resize C:/img.png 768,768 2 .webp
---------------------------------------------
               resize modes: 0 thumbnail()
                             1 contain()
                             2 cover()
                             3 fit()
                             4 pad()'''
                )
            return
        
        parts: list[str] = re.split(r'\s*(?:,|\s)\s*',import_parameters)

        # Prompt for custom pad color if resize mode is pad
        if RESIZE_MODES[int(parts[3])] == 'pad':
            color_input:str = input('''Enter pad color as R,G,B,A in range 0-255 (e.g. 0,0,0,255 is Black): >> ''')
            components:list[str] = re.split(r'\s*(?:,|\s)\s*',color_input)
            if (
                len(components) == 4
                and all(c.strip().isdigit() for c in components)
                and all(0 <= int(c) <= 255 for c in components)
            ):
                user_pad_color = tuple(map(int, components)) #(r, g, b, alpha)
            else:
                print("Invalid color format. Using default black.")
                user_pad_color = (0, 0, 0, 255)      
        try:
            _src_path: str = parts[0] 
            _width: str = int(parts[1]) 
            _height: str = int(parts[2]) 
            _resize_mode: str = RESIZE_MODES[int(parts[3])] 
            _save_extension: str = parts[4] 
          
            new_input = ResizeInput(
                src_path = _src_path,
                out_size = (_width,_height),
                resize_mode = _resize_mode,
                save_extension = _save_extension,
                pad_color = user_pad_color
            )

            resize_and_save(new_input)

        except Exception as e:
            logger.error(f"Resize failed: {e}")

    def do_rembg(self, import_parameters: str):
        """
        CLI command to remove background from an image.

        Expected input format:
            <path_to_image> <edge_mode>

        - <edge_mode> must be either 'hard' or 'soft'
        - 'soft' enables alpha matting for smoother edges (default)

        Example:
            >> rembg C:/images/photo.jpg soft
            >> rembg C:/images/photo.jpg hard

        Args:
            import_parameters (str): Raw user input string containing image path
                                    and optional edge mode.
        """
        EDGE_SOFT:str = 'soft'
        EDGE_HARD:str = 'hard'
        try:
            # Split input by spaces and/or commas
            parts: list[str] = re.split(r'\s*(?:,|\s)\s*', import_parameters)

            # Validate presence of input
            if not parts or not parts[0]:
                print("No input path provided.")
                return

            _src_path: str = parts[0]
            if len(parts) > 1 and parts[1].lower() == EDGE_HARD:
                _alpha_matting: bool = False
            elif len(parts) > 1 and parts[1].lower() == EDGE_SOFT:
                _alpha_matting: bool = True
            else:
                print("Unknown edge mode, defaulting to 'hard'")
                _alpha_matting: bool = False
            
            # Pack arguments into dataclass
            new_input = RembgInput(
                src_path=_src_path,
                alpha_matting= _alpha_matting,
                calculation_device='CPU',  # Placeholder for future GPU support
            )

            # Run removal and save result
            output_path = rembg_and_save(new_input)
            print(f"Saved: {output_path}")

        except Exception as e:
            logger.error(f"Rembg failed: {e}")

    def do_quit(self, line: str):
        """
        Exit the CLI.
        """
        return True
