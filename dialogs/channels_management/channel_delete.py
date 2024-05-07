from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from filters.callbacks import Call
from markups.markups import end_markup
from models.services import remove_channel

router = Router()


class ChannelDelDialog(StatesGroup):
    channel_id = State()


@router.callback_query(Call("channels_delete"))
async def delete_channel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelDelDialog.channel_id)
    await callback.message.answer("Укажите ID телеграм канала для удаления")
    await callback.message.delete_reply_markup()


@router.message(StateFilter(ChannelDelDialog.channel_id))
async def get_channel_id(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
    except ValueError:
        return await message.answer("ID указан некорректно, повторите ввод")

    await state.clear()
    if await remove_channel(channel_id):
        return await message.answer("Канал успешно удалён", reply_markup=end_markup)
    await message.answer("Канал с таким ID не найден", reply_markup=end_markup)
