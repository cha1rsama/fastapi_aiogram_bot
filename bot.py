from config import TELEGRAM_BOT_TOKEN
from keyboards import ikb, lang, ru_ikb, uz_ikb
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.helper import HelperMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor

HELP_COMMAND = """
/start - Start the bot
/help - Commands list
"""
storage = MemoryStorage()
bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)


class User(StatesGroup):
    mode = HelperMode.snake_case
    start = State()
    lang_us = State()
    lang_uz = State()
    lang_ru = State()
    chat_id = State()


@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message):
    user = message['chat']['first_name']
    await message.delete()
    await message.answer_photo(photo='https://oneapp.ly/images/oa.png',
                               caption=f"👋🏻Hi <b>{user}!</b>\n🔹Welcome to OneApply bot!🔹"
                                       "\n\n<em>Please select a language</em>",
                               reply_markup=lang, parse_mode='HTML')
    chat_id = message['chat']['id']
    await message.answer(chat_id)



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))
async def login_handler(callback: types.CallbackQuery) -> None:
    if callback.data == 'btn_us':
        await callback.message.edit_media(media=InputMediaPhoto(media="https://oneapp.ly/_next/static/media"
                                                                      "/howWorksEmp1.726b8e51.png"))
        await callback.message.edit_caption('Thank you for choosing 🇺🇸\n'
                                            'Let me help you, you can post your vacancy from here 🧾\n'
                                            'Just click on the button below🔽\n\n'
                                            '🤔If you want more info about my features, click on Instructions')
        await callback.message.edit_reply_markup(ikb)

    if callback.data == 'btn_ru':
        await callback.message.edit_media(media=InputMediaPhoto(media="https://oneapp.ly/_next/static/media"
                                                                      "/howWorksEmp1.726b8e51.png"))
        await callback.message.edit_caption('Спасибо за выбор 🇷🇺\n'
                                            'Позвольте мне вам помочь, тут вы можете разместить свою вакансию 🧾\n'
                                            'Вам нужно будет всего лишь нажать на кнопку под описанием🔽\n\n'
                                            '🤔Если же хотите ознакомиться с полной инструкцией нажмите на Инструкции')
        await callback.message.edit_reply_markup(ru_ikb)

    if callback.data == 'btn_uz':
        await callback.message.edit_media(media=InputMediaPhoto(media="https://oneapp.ly/_next/static/media"
                                                                      "/howWorksEmp1.726b8e51.png"))
        await callback.message.edit_caption('Tanlaganiz uchun rahmat 🇺🇿\n'
                                            'Sizga yordam beraman, shu yerda o\'z Vakansiyangizni joylashingiz '
                                            'mumkin🧾\n'
                                            'Siz faqatgina pastdagi tugmasini bosishiz kerak🔽\n\n'
                                            '🤔Agar esa butunlay koʻrsatma bilan tanishmoqchi boʻlsangiz Koʻrsatma '
                                            'tugmasini bosing')
        await callback.message.edit_reply_markup(uz_ikb)

    if callback.data == 'btn_back':
        await start_command(callback.message)


        
@dp.message_handler(content_types='text')
async def any_text_command(message: types.Message):
    await help_command(message)


@dp.message_handler(commands=['cancel'])
async def help_command(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
    await message.delete()
