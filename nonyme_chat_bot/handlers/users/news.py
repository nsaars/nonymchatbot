from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from keyboards.default.util import yes_no_menu, find_menu, cancel_menu
from loader import dp
from utils.db_api import db_commands


@dp.message_handler(Command('news'))
async def send_news(message: types.Message):
    news = await db_commands.get_last_news()
    if news:
        await message.answer(news.text)
    else:
        await message.answer("В боте пока нет никаких новостей")

    await message.answer("Есть предложения по поводу бота? Пиши в диррект https://t.me/nsaars 😉")


@dp.message_handler(Command('add_news'))
async def add_news(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Пришлите текст новости, которую пользователи будут видеть, используя команду /news",
                             reply_markup=cancel_menu)
        await state.set_state("adding_news")


@dp.message_handler(content_types=["text"], state="adding_news")
async def add_news_text(message: types.Message, state: FSMContext):
    if message.text == "Отменить":
        await message.answer("Походу новостей нет :D", reply_markup=find_menu)
        await state.reset_state()
    else:
        news_text = message.text
        await message.answer(f"Информация будет выглядить так:")
        await message.answer(news_text)
        await message.answer("Сохранить новость?", reply_markup=yes_no_menu)
        await state.update_data({"news_text": news_text})
        await state.set_state("saving_news")


@dp.message_handler(content_types=["text"], state="saving_news")
async def save_news(message: types.Message, state: FSMContext):
    if message.text == "Да":
        data = await state.get_data()
        news = data['news_text']
        await db_commands.add_news(text=news, date=datetime.now())
        await message.answer("Новость была успешно добавлена!", reply_markup=find_menu)
        await state.reset_state()
    elif message.text == "Нет":
        await message.answer("Пришлите текст заново :)", reply_markup=cancel_menu)
        await state.set_state("adding_news")
    else:
        await message.answer("Нет такого варианта ответа :(")
