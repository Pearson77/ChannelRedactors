import os

from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    def __init__(self):
        load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
