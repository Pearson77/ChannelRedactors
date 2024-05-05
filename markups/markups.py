from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


__start_buttons = [
    [InlineKeyboardButton(text="Статистика каналов", callback_data="channels_stats")],
    [InlineKeyboardButton(text="Управление редакторами", callback_data="redactors_management")],
    [InlineKeyboardButton(text="Управление каналами", callback_data="channels_management")],
    [InlineKeyboardButton(text="В главное меню", callback_data="back_to_home")],
]
start_markup = InlineKeyboardMarkup(inline_keyboard=__start_buttons)


__redactors_management_buttons = [
    [InlineKeyboardButton(text="Назначить редактора", callback_data="redactors_add")],
    [InlineKeyboardButton(text="Изменить редактора", callback_data="redactors_edit")],
    [InlineKeyboardButton(text="Удалить редактора", callback_data="redactors_delete")],
    [InlineKeyboardButton(text="В главное меню", callback_data="back_to_home")],
]
redactors_markup = InlineKeyboardMarkup(inline_keyboard=__redactors_management_buttons)


__channels_management_buttons = [
    [InlineKeyboardButton(text="Добавить канал", callback_data="channels_add")],
    [InlineKeyboardButton(text="Удалить канал", callback_data="channels_delete")],
    [InlineKeyboardButton(text="В главное меню", callback_data="back_to_home")],
]
channels_markup = InlineKeyboardMarkup(inline_keyboard=__channels_management_buttons)