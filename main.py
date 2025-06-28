"""
main.py — Entry point for the Kiyanka image resizer CLI tool.
"""

from PIL import Image  # Image module is used internally by logic, kept here for clarity
import logging

from models import *  # data classes and constants
from cli import *     # CLI class for user interaction

# Configure logging format and level
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Launch the CLI loop
    KiyankaCLI().cmdloop()
