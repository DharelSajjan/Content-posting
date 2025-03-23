from os import getenv

from dotenv import find_dotenv, load_dotenv

# load environment variables
load_dotenv(find_dotenv())

STAGE = getenv("STAGE", "test")
