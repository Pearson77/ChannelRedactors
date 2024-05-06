# from aiogram import Bot, Dispatcher
#
#
# async def main():
#     dp = Dispatcher()
#     bot = Bot(token="6709428815:AAGSpOrmE5_pSw-s-tjI8Z88V97V9IL1_kQ")
#     await bot.delete_webhook(True)
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     main()
#
#
#
#
#
#

from aiogram import Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from filters.callbacks import Call

router = Router()


class DialogEdit(StatesGroup):
    user_id = State()
    channel = State()
    schedule_type = State()
    start_date = State()
    schedule_time = State()


@router.callback_query(Call("redactors_edit"))
async def edit_redactor(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите Telegram ID пользователя для редактирования")
    await callback.message.delete_reply_markup()
    '''Todo: Проверка id пользователя (если есть пользователь с таким id, то дальше, иначе ТАКОГО ПОЛЬЗОВАТЕЛЯ НЕТ)'''
    await state.set_state(DialogEdit.user_id)


@router.message(StateFilter(DialogEdit.user_id))
async def get_user_id(message: Message, state: FSMContext):
    try:
        await state.update_data({"user_id": int(message.text)})
        '''Todo: , [InlineKeyboardButton(text="Отмена", callback_data="cancel")] Нужно для возможности отмены действия'''
        await message.answer("Что вы хотите отредактировать?", reply_markup=InlineKeyboardMarkup(row_width=2,
                                                                                                 inline_keyboard=[
                                                                                                     [InlineKeyboardButton(
                                                                                                         text="Редактировать каналы",
                                                                                                         callback_data="edit_channels")],
                                                                                                     [InlineKeyboardButton(
                                                                                                         text="Редактировать график",
                                                                                                         callback_data="edit_schedule")]]))
    except ValueError:
        await message.answer("Некорректно указан Telegram ID, введите повторно")


@router.callback_query(Call("edit_channels"))
async def edit_channels(callback: CallbackQuery, state: FSMContext):
    """Todo: Сделать вывод каналов пользователя клавиатурой в формате Удалить CHANNEL
    user_data = await state.get_data()
    user_id = user_data.get("user_id")
    channels = [1, 2, 3]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"remove_channel_{channel}")
    keyboard.add(InlineKeyboardButton(text="Добавить каналы", callback_data="add_channels")
    await callback.message.answer("Выберите каналы для редактирования:",
                                   reply_markup=channels_edit_markup(channels))"""
    await callback.message.answer("Введите ID канала для редактирования")
    await callback.message.delete_reply_markup()
    await state.set_state(DialogEdit.channel)


@router.message(StateFilter(DialogEdit.channel))
async def get_channel_id(message: Message, state: FSMContext):
    try:
        channel_id = int(message.text)
        await state.update_data({"channel_id": channel_id})
        await message.answer("ID отредактирован")
    except ValueError:
        await message.answer("Некорректный ID канала, введите повторно")


@router.callback_query(Call("edit_schedule"), )
async def edit_schedule(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите тип рабочей недели:",
                                  reply_markup=InlineKeyboardMarkup(row_width=3,
                                                                    inline_keyboard=[
                                                                        [InlineKeyboardButton(
                                                                            text="Будние",
                                                                            callback_data="edit_weekdays")],
                                                                        [InlineKeyboardButton(
                                                                            text="Выходные",
                                                                            callback_data="edit_weekend")],
                                                                        [InlineKeyboardButton(
                                                                            text="2 через 2",
                                                                            callback_data="edit_2&2")]]))
    await callback.message.delete_reply_markup()
    await state.set_state(DialogEdit.schedule_type)


@router.callback_query(StateFilter(DialogEdit.schedule_type))
async def get_schedule_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"schedule_type": callback.data})
    await callback.message.delete_reply_markup()
    if callback.data == "2&2":
        await callback.message.answer("Выберите дату старта графика:")
        return await state.set_state(DialogEdit.start_date)
    await callback.message.answer("Выберите промежуток времени работы")
    await state.set_state(DialogEdit.schedule_time)
