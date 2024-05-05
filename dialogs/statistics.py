from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.callbacks import Call


router = Router()


@router.callback_query(Call("channels_stats"))
async def get_channels_stats(callback: CallbackQuery):
    pass
