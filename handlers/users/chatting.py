from datetime import datetime
from pprint import pprint

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import MediaGroup

from loader import dp, bot
from utils.db_api.models import Message, Media


@dp.message_handler(content_types=["text"], state="chatting")
async def receive_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = int(data['companion'])

    await bot.send_message(companion, message.text)
    await Message.create(from_user_id=message.from_user, to_user_id=companion, send_time=datetime.now(),
                         text=message.text)


@dp.message_handler(content_types=["photo", "video", "document", "audio", "voice"], state="chatting")
async def receive_media(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = data['companion']

    if message.content_type == 'photo':
        media = await bot.get_file(message.photo.pop().file_id)
    else:
        media = await bot.get_file(message.__dict__['_values'][message.content_type].file_id)
    downloaded_file = await bot.download_file(media.file_path)

    sent_message = await Message.create(from_user_id=message.from_user, to_user_id=companion,
                                        send_time=datetime.now().replace(microsecond=0))
    await Media.create(msg_id=sent_message.id, file_name=media.file_path, file_information=media.as_json(),
                       file_type=message.content_type, caption=message.caption, file=downloaded_file.read())

    send_method = dict(Bot.__dict__)[f'send_{message.content_type}']
    kwargs = {'chat_id': companion, message.content_type: media.file_id, 'caption': message.caption}
    await send_method(bot, **kwargs)


@dp.message_handler(content_types=["contact"], state="chatting")
async def receive_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = data['companion']

    contact = message.contact
    sent_message = await Message.create(from_user=message.from_user, to_user=companion,
                                        send_time=datetime.now().replace(microsecond=0))
    await Media.create(msg_id=sent_message.id, file_information=contact.as_json(),
                       file_type="contact", caption=message.caption)
    await bot.send_contact(chat_id=companion, phone_number=contact.phone_number, first_name=contact.first_name)


@dp.message_handler(content_types=["location"], state="chatting")
async def receive_location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = data['companion']

    location = message.location
    sent_message = await Message.create(from_user=message.from_user, to_user=companion,
                                        send_time=datetime.now().replace(microsecond=0))
    await Media.create(msg_id=sent_message.id, file_information=location.as_json(),
                       file_type="location", caption=message.caption)
    await bot.send_location(companion, latitude=location.latitude, longitude=location.longitude)


@dp.message_handler(content_types=["sticker"], state="chatting")
async def receive_sticker(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = data['companion']

    sticker = message.sticker
    await bot.send_sticker(companion, sticker.file_id)


@dp.message_handler(content_types=["animation"], state="chatting")
async def receive_animation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    companion = data['companion']

    animation = message.animation
    await bot.send_animation(companion, animation.file_id)
