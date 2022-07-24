from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.companion_menu import increase_reputation_callback, add_favorite_callback
from loader import dp
from utils.db_api.db_commands import add_user_favorite
from utils.db_api.user_commands import get_user_by_user_id, increase_reputation


@dp.callback_query_handler(increase_reputation_callback.filter(), state='*')
async def change_reputation(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    companion = await get_user_by_user_id(callback_data['companion_id'])
    await increase_reputation(companion)
    await callback.message.delete_reply_markup()
    if await state.get_state() is None:
        await callback.message.answer("Репутация вашего собеседника была повышена :)")


@dp.callback_query_handler(add_favorite_callback.filter(), state='*')
async def add_favorite(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user = await get_user_by_user_id(callback.from_user.id)
    companion = await get_user_by_user_id(callback_data['companion_id'])
    favorite = await add_user_favorite(user, companion)
    if await state.get_state() is None:
        if favorite:
            await callback.message.answer("Собеседник добавлен в ⭐ Избранное")
        else:
            await callback.message.answer("Собеседник уже у вас в ⭐ Избранное")
    await callback.message.delete_reply_markup()
