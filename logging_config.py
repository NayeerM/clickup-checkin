import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create a file handler with a date in the filename
now = datetime.now()
filename = f'app_{now.strftime("%Y-%m-%d")}.log'
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)