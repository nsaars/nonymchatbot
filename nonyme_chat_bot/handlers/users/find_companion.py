from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default.util import find_menu, end_finding_menu
from loader import dp, bot
from utils.db_api.user_commands import get_users
from keyboards.default import util


@dp.message_handler(Text("🔎 Начать поиск"))
async def find_companion(message: types.Message, state: FSMContext):
    for user in await get_users():  # todo: create is_searching column in users
        companion_state = dp.current_state(chat=user.user_id, user=user.user_id)

        if await companion_state.get_state() == "wait_for_companion":
            companion = companion_state.user

            await state.set_state("chatting")
            await companion_state.set_state("chatting")

            await state.update_data({'companion': companion})
            await companion_state.update_data({'companion': message.from_user.id})

            await bot.send_message(message.from_user.id, "Собеседник нашёлся, напишите сообщение!",
                                   reply_markup=util.finish_menu)
            await bot.send_message(companion, "Собеседник нашёлся, напишите сообщение!",
                                   reply_markup=util.finish_menu)
            break
    else:
        await state.set_state("wait_for_companion")
        await message.answer(text="Идёт поиск...", reply_markup=end_finding_menu)


@dp.message_handler(Text("Прекратить поиск"), state=("wait_for_companion", None))
async def stop_searching(message: types.Message, state: FSMContext):
    await message.answer(text="Поиск прекращён", reply_markup=find_menu)
    await state.reset_state()
