"""
cli.py — Command-line interface for the Kiyanka image resizing tool.
"""

import logging
import cmd
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
A small tool to resize image for your needs.
Type "help" to see available commands.'''

    def do_resize(self, import_parameters: str):
        """
        Resize Image: path width,height resize_mode extension

        Example:
            >> resize C:/img.png 768,768 2 .webp

        resize modes:
            0 thumbnail()
            1 contain()
            2 cover()
            3 fit()
            4 pad()
        """
        if not import_parameters.strip():
            print(
'''
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
        try:
            parts = import_parameters.split()
            w = int(parts[1].split(',')[0])
            h = int(parts[1].split(',')[1])
            new_input = ResizeInput(
                src_path = parts[0],
                out_size = (w, h),
                resize_mode = RESIZE_MODES[int(parts[2])],
                save_extension = parts[3],
                pad_color = (0, 0, 0, 0)
            )
            process_image(new_input)
        except Exception as e:
            print("Error:", e)

    def do_quit(self, line: str):
        """
        Exit the CLI.
        """
        return True
