from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

increase_reputation_callback = CallbackData('increase_reputation', 'companion_id')
add_favorite_callback = CallbackData('add_favorite', 'companion_id')


async def get_companion_menu(companion_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔝 +1 к репутации", callback_data=increase_reputation_callback.new(companion_id))
            ],
            [
                InlineKeyboardButton(text="⭐ Добавить в Избранное", callback_data=add_favorite_callback.new(companion_id))
            ]
        ]
    )
