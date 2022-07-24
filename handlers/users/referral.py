from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot


@dp.message_handler(Command('referral'))
async def referral(message: types.Message):
    bot_info = await bot.get_me()
    await message.answer(f"Твоя реферальная ссылка http://t.me/{bot_info['username']}?start={message.from_user.id}")
