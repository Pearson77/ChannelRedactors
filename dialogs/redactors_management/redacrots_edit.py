from aiogram import Router
from aiogram.types import Message, CallbackQuery

from filters.filters import Call

router = Router()


@router.callback_query(Call("redactors_edit"))
async def edit_redactor(callback: CallbackQuery):
    pass
