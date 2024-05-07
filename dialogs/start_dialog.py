import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from markups.markups import start_markup, channels_markup, redactors_markup
from filters.callbacks import Call

router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await message.reply("Выберите действие...", reply_markup=start_markup)


@router.callback_query(Call("redactors_management"))
async def redactors_management_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=redactors_markup)


@router.callback_query(Call("channels_management"))
async def channels_management_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=channels_markup)


@router.callback_query(Call("back_to_home"))
async def go_home(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text="Выберите действие...")
    except aiogram.exceptions.TelegramBadRequest:
        pass
    await callback.message.edit_reply_markup(reply_markup=start_markup)
    await state.clear()
