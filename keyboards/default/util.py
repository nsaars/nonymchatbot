from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

find_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔎 Начать поиск")], [KeyboardButton(text="⭐ Избранное")]],
                                resize_keyboard=True)
end_finding_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Прекратить поиск")]], resize_keyboard=True)
finish_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Закончить диалог")]], resize_keyboard=True)
cancel_request_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить запрос")]], resize_keyboard=True)

yes_no_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]], resize_keyboard=True)
cancel_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить")]], resize_keyboard=True)