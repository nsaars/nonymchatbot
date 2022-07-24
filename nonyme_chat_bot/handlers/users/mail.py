import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked

from data.config import ADMINS
from keyboards.default.util import yes_no_menu, find_menu, cancel_menu
from loader import dp, bot
from utils.db_api.user_commands import get_users


async def mail(text, not_mailed=None):
    if not_mailed is None:
        not_mailed = await get_users()

    for user in not_mailed:
        user_state = dp.current_state(chat=user.user_id, user=user.user_id)
        if await user_state.get_state() is None:
            try:
                await bot.send_message(user.user_id, text)
            except BotBlocked:
                print(f"User {user.username if user.username else user.user_id} blocked the bot!")
            not_mailed.remove(user)
    if not_mailed:
        await asyncio.sleep(10)
        await mail(text, not_mailed)


@dp.message_handler(Command('mail'))
async def send_mail(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Пришлите текст рассылки", reply_markup=cancel_menu)
        await state.set_state("adding_mail")


@dp.message_handler(content_types=["text"], state="adding_mail")
async def add_mail_text(message: types.Message, state: FSMContext):
    if message.text == "Отменить":
        await message.answer("Ничего рассылать не будем :D", reply_markup=find_menu)
        await state.reset_state()
    else:
        mail_text = message.text
        await message.answer(f"Рассылка будет выглядить так:")
        await message.answer(mail_text)
        await message.answer("Сохранить текст?", reply_markup=yes_no_menu)
        await state.update_data({"mail_text": mail_text})
        await state.set_state("saving_mail")


@dp.message_handler(content_types=["text"], state="saving_mail")
async def send_mail(message: types.Message, state: FSMContext):
    if message.text == "Да":
        data = await state.get_data()
        mail_text = data['mail_text']
        await message.answer("Рассылка началась!", reply_markup=find_menu)
        await state.reset_state()
        await mail(mail_text)
    elif message.text == "Нет":
        await message.answer("Пришлите текст заново :)", reply_markup=cancel_menu)
        await state.set_state("adding_mail")
    else:
        await message.answer("Нет такого варианта ответа :(")
