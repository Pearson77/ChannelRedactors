from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.callbacks import Call

router = Router()


@router.callback_query(Call("channels_delete"))
async def delete_channel(callback: CallbackQuery):
    pass
