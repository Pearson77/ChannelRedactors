import os

from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    def __init__(self):
        load_dotenv()

    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_PASS = os.getenv('DB_PASS')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DB_URL = F""
