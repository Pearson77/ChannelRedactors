from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from filters.callbacks import Call
from models.services import delete_user

router = Router()


class DeleteDialog(StatesGroup):
    user_id = State()


@router.callback_query(Call("redactors_delete"))
async def delete_redactor(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ID пользователя для удаления:")
    await callback.message.delete_reply_markup()
    await state.set_state(DeleteDialog.user_id)


@router.message(StateFilter(DeleteDialog.user_id))
async def get_redactor_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        return await message.answer("Некорректно указан ID пользователя, введите повторно")

    await state.clear()
    if await delete_user(user_id):
        return await message.answer("Редактор успешно удалён")
    await message.answer("Редактор с таким ID не найден!")
