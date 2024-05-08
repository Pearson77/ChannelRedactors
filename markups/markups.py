from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


__start_buttons = [
    [InlineKeyboardButton(text="Статистика каналов", callback_data="channels_stats")],
    [InlineKeyboardButton(text="Управление редакторами", callback_data="redactors_management")],
    [InlineKeyboardButton(text="Управление каналами", callback_data="channels_management")],
]
start_markup = InlineKeyboardMarkup(inline_keyboard=__start_buttons)


__redactors_management_buttons = [
    [InlineKeyboardButton(text="Назначить редактора", callback_data="redactors_add")],
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


__schedule_buttons = [
    [InlineKeyboardButton(text="По будням", callback_data="5&2")],
    [InlineKeyboardButton(text="По выходным", callback_data="2")],
    [InlineKeyboardButton(text="2 через 2", callback_data="2&2")],
]
schedule_markup = InlineKeyboardMarkup(inline_keyboard=__schedule_buttons)


__edit_buttons = [
    [InlineKeyboardButton(text="Редактировать каналы", callback_data="channels_edit")],
    [InlineKeyboardButton(text="Редактировать график", callback_data="schedule_edit")],
    [InlineKeyboardButton(text="В главное меню", callback_data="back_to_home")],
]
edit_markup = InlineKeyboardMarkup(inline_keyboard=__edit_buttons)


__end_button = [
    [InlineKeyboardButton(text="В главное меню", callback_data="back_to_home")],
]
end_markup = InlineKeyboardMarkup(inline_keyboard=__end_button)
