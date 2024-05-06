import os

from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from telethon import TelegramClient
from telethon.tl.types.auth import SentCode

from models.services import get_channels_list
from services.statistics.scrap_channel_info import scrap_channel_list, create_client_session
from services.statistics.excel_writing import create_excel_table
from filters.callbacks import Call
from config import Config

config = Config()
router = Router()


class Statistics(StatesGroup):
    code = State()


@router.callback_query(Call("channels_stats"))
async def get_channels_stats(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    client = TelegramClient('session_name', config.API_ID, config.API_HASH)
    await client.connect()
    phone_hash = (await client.send_code_request(config.PHONE)).phone_code_hash

    await callback.message.answer("Введите код из СМС:")
    await state.update_data({"client": client, "hash": phone_hash})
    return await state.set_state(Statistics.code)


@router.message(StateFilter(Statistics.code))
async def get_phone_code(message: Message, state: FSMContext):
    data = await state.get_data()
    client = data.get("client")
    phone_hash = data.get("hash")

    client.sign_in(config.PHONE, message.text, phone_code_hash=phone_hash)

    channels_list = await get_channels_list()
    data = await scrap_channel_list(client, channels_list)
    create_excel_table(data)
    await message.answer_document(FSInputFile("example.xlsx"))
    await state.clear()
    os.remove("example.xlsx")
    os.remove("session_name.session")
