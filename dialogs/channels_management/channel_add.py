import aiogram
from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from config import Config
from filters.callbacks import Call
from markups.markups import end_markup
from models.services import add_channel

router = Router()
config = Config()
bot = Bot(config.BOT_TOKEN)


class ChannelAddDialog(StatesGroup):
    channel_id = State()


@router.callback_query(Call("channels_add"))
async def add_channel_(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelAddDialog.channel_id)
    await callback.message.answer("Укажите ID телеграм канала для добавления")
    await callback.message.delete_reply_markup()


@router.message(StateFilter(ChannelAddDialog.channel_id))
async def get_channel_id(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
    except ValueError:
        return await message.answer("ID указан некорректно, повторите ввод")

    await state.clear()

    try:
        admins_info = await bot.get_chat_administrators(channel_id)
        bot_id = (await bot.get_me()).id
    except aiogram.exceptions.TelegramBadRequest:
        return await message.answer("Я не являюсь администратором указанного канала", reply_markup=end_markup)

    admin_obj = None
    for admin in admins_info:
        if admin.user.id == bot_id:
            admin_obj = admin
            break

    if not admin_obj:
        return await message.answer("Я не являюсь администратором указанного канала", reply_markup=end_markup)
    if not admin_obj.can_promote_members:
        return await message.answer("Я не могу назначать администраторов канала", reply_markup=end_markup)
    if not await add_channel(channel_id):
        return await message.answer("Этот канал уже зарегистрирован!", reply_markup=end_markup)
    await message.answer("Канал успешно добавлен!", reply_markup=end_markup)
