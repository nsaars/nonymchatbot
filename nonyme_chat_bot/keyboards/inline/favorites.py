from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.db_commands import get_user_favorites
from utils.db_api.user_commands import get_user_by_id

favorite_callback = CallbackData("favorite", "id")
conversation_request_callback = CallbackData("conversation_request", "cancel", "id")


async def get_favorites_menu(user):
    favorites_keyboard = InlineKeyboardMarkup()

    favorites = await get_user_favorites(user)
    for i, fav in enumerate(favorites, 1):
        favorite = await get_user_by_id(fav.favorite_id)
        favorites_keyboard.insert(
            InlineKeyboardButton(text=f"Аноним {i}", callback_data=favorite_callback.new(id=favorite.user_id)))
    if favorites_keyboard['inline_keyboard']:
        return favorites_keyboard
    return False


async def get_conversation_request_menu(from_user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏁 Начать беседу",
                                     callback_data=conversation_request_callback.new(cancel=0, id=from_user_id))
            ],
            [
                InlineKeyboardButton(text="🚫 Отклонить запрос",
                                     callback_data=conversation_request_callback.new(cancel=1, id=from_user_id))
            ]
        ]
    )
