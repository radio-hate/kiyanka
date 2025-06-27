#main.py
from PIL import Image
import logging
from logic import process_image  
from models import *
from cli import *

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    KiyankaCLI().cmdloop()


