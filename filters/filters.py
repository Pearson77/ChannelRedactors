from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class Call(BaseFilter):
    def __init__(self, slug: str):
        self.slug = slug

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.slug
