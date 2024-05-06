import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class DateMessage(BaseFilter):
    async def __call__(self, message: Message):
        return re.match(r"^\d{2}.\d{2}.\d{4}$", message.text)


class TimeMessage(BaseFilter):
    async def __call__(self, message: Message):
        pattern = r"^(\d{2}:\d{2}) - (\d{2}:\d{2})$"
        match = re.match(pattern, message.text)

        if match:
            return {"start": match.group(1), "end": match.group(2)}
        return False
