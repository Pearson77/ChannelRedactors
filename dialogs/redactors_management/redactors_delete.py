from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command


router = Router()


@router.message()
async def on_message(message: Message):
    pass
