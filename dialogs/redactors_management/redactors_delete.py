from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.filters import Call

router = Router()


@router.callback_query(Call("redactors_delete"))
async def delete_redactor(callback: CallbackQuery):
    pass
