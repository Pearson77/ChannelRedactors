from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.filters import Call

router = Router()


@router.callback_query(Call("channels_add"))
async def add_channel(callback: CallbackQuery):
    pass
