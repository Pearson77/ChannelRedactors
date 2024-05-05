import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class DateMessage(BaseFilter):
    def __call__(self, message: Message):
        return re.match(r"\d{2}.\d{2}.\d{4}", message.text)
