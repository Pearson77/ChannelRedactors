import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from filters.messages import DateMessage
from markups.markups import schedule_markup
from filters.callbacks import Call

router = Router()


class Dialog(StatesGroup):
    user_id = State()
    channels = State()
    schedule_type = State()
    schedule_time = State()
    start_date = State()


@router.callback_query(Call("channels_add"))
async def add_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите Telegram ID пользователя")
    await callback.message.delete()
    await state.set_state()


@router.message(StateFilter(Dialog.user_id))
async def get_user_id(message: Message, state: FSMContext):
    try:
        await state.update_data({"user_id": int(message.text)})
        await message.answer("Укажите ID канала для редактора")
        await state.set_state(Dialog.channels)
    except ValueError:
        await message.answer("Некорректно указан Telegram ID, введите повторно")


@router.message(StateFilter(Dialog.channels))
async def get_username(message: Message, state: FSMContext):
    try:
        await state.update_data({"channel_id": int(message.text)})
        await message.answer("Выберите тип рабочей недели:", reply_markup=schedule_markup)
        await state.set_state(Dialog.schedule_type)
    except ValueError:
        await message.answer("Некорректно указан Telegram ID, введите повторно")


@router.callback_query(StateFilter(Dialog.schedule_type))
async def get_schedule_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"schedule_type": callback.data})
    if callback.data == "2&2":
        await callback.message.answer("Выберите дату старта графика:")
        return await state.set_state(Dialog.start_date)
    await callback.message.answer("Выберите промежуток времени работы")
    await state.set_state(Dialog.schedule_time)


@router.message(StateFilter(Dialog.start_date), DateMessage())
async def get_start_date(message: Message, state: FSMContext):
    day, month, year = map(int, message.text.split("."))
    date = datetime.date(year, month, day)
    await state.update_data({"start_date": date})


@router.message(StateFilter(Dialog.schedule_time))
async def get_schedule_time(message: Message, state: FSMContext):
    pass
