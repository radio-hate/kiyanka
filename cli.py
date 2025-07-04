"""
cli.py — Command-line interface for the Kiyanka image resizing tool.
"""

import logging
import cmd
import re
from logic import process_image  
from models import ResizeInput, RESIZE_MODES

logger = logging.getLogger(__name__)


class KiyankaCLI(cmd.Cmd):
    """
    Interactive CLI tool for image resizing.

    Commands:
        - resize <path> <WxH> <mode_id> <ext>
        - quit
    """
    prompt = '>> '
    intro = '''Welcome to Kiyanka.
A small tool to resize images for your needs.
---------------------------------------------
Available commands: resize, help, quit.
---------------------------------------------
Format of resize command: path width,height resize_mode extension
Example:
    >> resize C:/img.png 768,768 2 .jpg
                    resize modes:
                                 0 thumbnail()
                                 1 contain()
                                 2 cover()
                                 3 fit()
                                 4 pad()'''

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
            color_input = input('''Enter pad color as R,G,B,A (e.g. 0,0,0,255): >> ''')
            try:
                r, g, b, alpha = map(int, color_input.split(','))
                user_pad_color = (r, g, b, alpha)  
            except ValueError:
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

            process_image(new_input)

        except Exception as e:
            print("Error:", e)

    def do_quit(self, line: str):
        """
        Exit the CLI.
        """
        return True
