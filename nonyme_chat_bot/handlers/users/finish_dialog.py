from keyboards.default.util import find_menu

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.companion_menu import get_companion_menu
from keyboards.inline.favorites import get_conversation_request_menu
from loader import dp, bot


@dp.message_handler(Text("Закончить диалог"), state=("chatting", None))
async def finish(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await state.get_state() is None:
        await message.answer("Диалог окончен", reply_markup=find_menu)
    else:
        data = await state.get_data()
        companion = data['companion']
        companion_state = dp.current_state(chat=companion, user=companion)

        await bot.send_message(user_id, "Диалог окончен", reply_markup=find_menu)
        await bot.send_message(companion, "Собеседник завершил диалог", reply_markup=find_menu)

        await bot.send_message(user_id, "Последнее слово:", reply_markup=await get_companion_menu(companion))
        await bot.send_message(companion, "Последнее слово:", reply_markup=await get_companion_menu(user_id))

        await check_conversation_request(user_id)
        await check_conversation_request(companion)

        await state.reset_state()
        await companion_state.reset_state()


async def check_conversation_request(user_id):
    data = await dp.current_state(chat=user_id, user=user_id).get_data()
    if 'conversation_request' in data:
        request_user_state = dp.current_state(chat=data['conversation_request'], user=data['conversation_request'])
        request_user_data = await request_user_state.get_data()
        if await request_user_state.get_state() == 'wait_for_favorite' and request_user_data['favorite_user_id'] == user_id:
            await bot.send_message(user_id, "У вас был запрос на беседу!",
                                   reply_markup=await get_conversation_request_menu(data['conversation_request']))
