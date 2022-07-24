from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.util import find_menu
from loader import dp, bot
from datetime import datetime

from utils.db_api.user_commands import add_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=find_menu)
    user = message.from_user
    kwargs = dict(user_id=user.id, username=user.username, name=user.full_name, date_of_registration=datetime.now())
    referral = message.get_args()
    if referral:
        kwargs['referral'] = int(referral)
    await add_user(**kwargs)
