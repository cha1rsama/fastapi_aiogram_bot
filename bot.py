
from keyboards import lang, ru_btn
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import add_user, get_token, database
from handler import applicants_list, applicants_get, vacancies, next_page, storage, prev_page, text, main_page
import pymongo.errors
import os

HELP_COMMAND = """
/start - Start the bot
/help - Commands list
"""
token = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    token_get = await get_token(message.chat.id)
    try:
        await message.delete()
    except(Exception,):
        pass
    try:
        token = token_get['token']
        await main_page(token, message)
    except (Exception,):
        user = message.chat.first_name
        await message.answer_photo(photo="https://i.ibb.co/xLz57JW/set.png",
                                   caption=f"👋🏻Добро пожаловать <b>{user}!</b>\n\nЯ помогу вам разместить вакансию "
                                           f"прямо из телеграма "
                                           "\nУпрощаем ваш найм с OneApp!"
                                           "\nНичего лишнего, только результат"
                                           "\n\n<em>Выберите язык</em>",
                                   reply_markup=lang, parse_mode='HTML')
        try:
            await add_user(chat_id=message.chat.id, username=message.from_user.username,
                           lang_code=message.from_user.language_code)
        except pymongo.errors.DuplicateKeyError:
            pass


@dp.callback_query_handler(text_startswith='btn')
async def login_handler(callback: types.CallbackQuery):
    if callback.data == 'btn_c':
        await callback.message.delete()
    if callback.data == 'btn_v':
        await bot.send_chat_action(callback.message.chat.id, action='typing')
        await vacancies(callback=callback)
    if callback.data == "btn_b":
        await callback.message.delete()
        await vacancies(callback=callback)


@dp.callback_query_handler(text='ru')
async def lang_select(callback: types.CallbackQuery):
    await ru_btn(callback=callback)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('$'))
async def applicant_handler(callback: types.CallbackQuery):
    await applicants_list(applicants=await applicants_get(callback=callback, slug=callback.data), callback=callback)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('next'))
async def next_page_handler(callback: types.CallbackQuery):
    await next_page(callback=callback)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('prev'))
async def prev_page_handler(callback: types.CallbackQuery):
    await prev_page(callback=callback)


@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    data = message.web_app_data
    print(data)
    await message.answer(data)
    token = data.data.strip("\"")
    if token == 'applicant':
        await message.answer('You cant')
    # await main_page(token, message)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
    await message.delete()
