from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default.util import find_menu, cancel_request_menu
from keyboards.inline.favorites import get_favorites_menu, favorite_callback, get_conversation_request_menu, \
    conversation_request_callback
from loader import dp, bot
from utils.db_api.user_commands import get_user_by_user_id
from keyboards.default import util


@dp.message_handler(Text("⭐ Избранное"))
async def get_favorites(message: types.Message):
    user = await get_user_by_user_id(message.from_user.id)
    menu = await get_favorites_menu(user)
    if menu:
        await message.answer(text="Ваши избранные ⭐", reply_markup=menu)
    else:
        await message.answer(text="У вас пока что нет избранных собеседников 🤔")


@dp.callback_query_handler(favorite_callback.filter(), state='*')
async def send_conversation_request(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    user_state = dp.current_state(chat=user_id, user=user_id)
    favorite_user_id = callback_data['id']
    favorite_user_state = dp.current_state(chat=favorite_user_id, user=favorite_user_id)

    if await user_state.get_state() == "chatting":
        await callback.message.answer("Чтоб отправить запрос, закончи диалог!")
    elif await user_state.get_state() in ["wait_for_favorite", "wait_for_companion"]:
        await callback.message.answer("Чтоб отправить запрос, отмени ожидание собеседника!")
    else:
        await user_state.set_state("wait_for_favorite")
        await bot.send_message(user_id, "Запрос на беседу отправлен!", reply_markup=cancel_request_menu)

        message = await bot.send_message(favorite_user_id, "Вам запрос на беседу!",
                                         reply_markup=await get_conversation_request_menu(user_id))
        await user_state.update_data({'favorite_user_id': int(favorite_user_id), 'message_id': message.message_id})
        await favorite_user_state.update_data({'conversation_request': user_id})


@dp.message_handler(Text("Отменить запрос"), state=("wait_for_favorite", None))
async def cancel_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    favorite_user_id = data['favorite_user_id']
    message_id = data['message_id']
    await bot.delete_message(chat_id=favorite_user_id, message_id=message_id)
    await state.reset_state()
    await message.answer(text="Запрос отменён", reply_markup=find_menu)


@dp.callback_query_handler(conversation_request_callback.filter(), state='*')
async def answer_conversation_request(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    requesting_user_id = callback_data['id']
    requesting_user_state = dp.current_state(chat=requesting_user_id, user=requesting_user_id)

    if int(callback_data['cancel']):
        await requesting_user_state.reset_state()
        await callback.message.delete_reply_markup()
        await bot.send_message(requesting_user_id, "Запрос отклонён", reply_markup=find_menu)
    else:
        if await state.get_state() == "chatting":
            await callback.message.answer("Чтоб принять запрос, закончи диалог!")

        elif await state.get_state() in ["wait_for_favorite", "wait_for_companion"]:
            await callback.message.answer("Чтоб принять запрос, отмени ожидание собеседника!")

        else:
            await callback.message.delete_reply_markup()

            await state.set_state("chatting")
            await requesting_user_state.set_state("chatting")

            await state.update_data({'companion': requesting_user_id})
            await requesting_user_state.update_data({'companion': callback.from_user.id})

            await bot.send_message(callback.from_user.id, "Вы приняли запрос, напишите сообщение!",
                                   reply_markup=util.finish_menu)
            await bot.send_message(requesting_user_id, "Собеседник принял запрос, напишите сообщение!",
                                   reply_markup=util.finish_menu)
