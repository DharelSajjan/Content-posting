import os
import logging 
from logging.handlers import RotatingFileHandler

LOG_FILE = "app.log"
LOG_LEVEL = logging.INFO

# Ensure the log folder exists.
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Define a rotating file handler
handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=1)

# Set the logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Get the root logger and set its level and handler
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)
root_logger.addHandler(handler)

def get_logger(name):
    return logging.getLogger(name)