import os

from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from models.services import get_channels_list
from services.statistics.scrap_channel_info import scrap_channel_list, create_client_session
from services.statistics.excel_writing import create_excel_table
from filters.callbacks import Call

router = Router()


class Statistics(StatesGroup):
    code = State()


@router.callback_query(Call("channels_stats"))
async def get_channels_stats(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    phone_hash = await create_client_session()

    await callback.message.answer("Введите код из СМС:")
    await state.update_data({"hash": phone_hash})
    return await state.set_state(Statistics.code)


@router.message(StateFilter(Statistics.code))
async def get_phone_code(message: Message, state: FSMContext):
    phone_hash = (await state.get_data())["hash"]
    channels_list = await get_channels_list()
    client_answer = await create_client_session(message.text, phone_hash)
    data = await scrap_channel_list(client_answer, channels_list)
    create_excel_table(data)
    await message.answer_document(FSInputFile("example.xlsx"))
    await state.clear()
