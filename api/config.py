import logging
from os import getenv

from dotenv import load_dotenv

load_dotenv()

config = {"minecraft_dir": getenv("MINECRAFT_DIR")}
